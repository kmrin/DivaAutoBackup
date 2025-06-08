import os
import sys
import vdf
import time
import shutil 
import psutil
import zipfile
import platform
import subprocess

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Callable, Any

from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtGui import QIcon

from .gui import SplashScreen, UserConfirmation, FirstTimeExperienceDialog, show_error, show_trace
from .log import logger
from .conf import conf, write_config
from .helpers import get_base_path

IS_WIN = platform.system() == "Windows"


def handle_errors(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            show_trace(f"An error occurred in {func.__name__}: {str(e)}", e)
            raise
    return wrapper


class Paths(BaseModel):
    std: str
    dml: str
    eden: str


class DivaAutoBackup:
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.paths: Optional[Paths] = None
        
        icon_path = os.path.join(get_base_path(), "assets", "logo.png")
        if os.path.exists(icon_path):
            logger.debug("ICON FOUND")
            self.app.setWindowIcon(QIcon(icon_path))
        
        self.splash = SplashScreen()
        
        home_dir = os.path.expanduser("~")
        default_backup_path = os.path.join(home_dir, "DivaAutoBackup")
        
        conf.backup_path = default_backup_path
        
        write_config(conf)
    
    @handle_errors
    def check_steam(self) -> None:
        self.show_splash_message("Checking presence of Steam")
        
        if IS_WIN:
            steam_exe = os.path.join(conf.steam_path, "steam.exe")
            
            if os.path.isfile(steam_exe) and os.access(steam_exe, os.X_OK):
                self.show_splash_message("Steam found")
            else:
                show_error("Steam couldn't be found on the configured path")
        
        else:
            if shutil.which("steam") is not None:
                self.show_splash_message("Steam found")
            else:
                show_error("Steam couldn't be found, make sure it is installed and callable from PATH")
    
    @handle_errors
    def get_steam_libraries(self) -> list[str]:
        libs = []
        steam_paths = [os.path.expanduser(path) for path in conf.linux_steam_library_paths]
        
        for steam_root in steam_paths:
            self.show_splash_message(f"Looking for Steam libraries in {steam_root}")
            
            vdf_path = os.path.join(steam_root, "steamapps", "libraryfolders.vdf")
            
            if os.path.exists(vdf_path):
                with open(vdf_path, "r", encoding="utf-8") as f:
                    data = vdf.load(f)
                    
                    for k, v in data["libraryfolders"].items():
                        if k.isdigit():
                            libs.append(v["path"])
        
        self.show_splash_message(f"Found {len(libs)} Steam libraries")
        
        return libs
    
    @handle_errors
    def get_proton_prefix(self) -> str:
        for lib in self.get_steam_libraries():
            self.show_splash_message(f"Looking for Proton prefix in {lib}")
            
            compat_path = os.path.join(lib, "steamapps", "compatdata", str(conf.app_id), "pfx")
            
            if os.path.exists(compat_path):
                self.show_splash_message(f"Found Proton prefix in {compat_path}")
                return compat_path
        
        show_error("No Proton prefix found, make sure you have opened the game at least once in Steam")
        sys.exit(1)
    
    @handle_errors
    def get_paths(self) -> Paths:
        paths: dict[str, str] = {}
        
        if IS_WIN:
            paths["std"] = os.path.join(os.path.expanduser("~"), conf.appdata_std_path)
            paths["dml"] = os.path.join(os.path.expanduser("~"), conf.appdata_dml_path)
            paths["eden"] = os.path.join(os.path.expanduser("~"), conf.appdata_edn_path)
            
        else:
            proton_prefix = self.get_proton_prefix()
            
            paths["std"] = os.path.join(proton_prefix, "drive_c", "users", "steamuser", conf.appdata_std_path)
            paths["dml"] = os.path.join(proton_prefix, "drive_c", "users", "steamuser", conf.appdata_dml_path)
            paths["eden"] = os.path.join(proton_prefix, "drive_c", "users", "steamuser", conf.appdata_edn_path)
        
        return Paths(**paths)
    
    @handle_errors
    def launch_game(self) -> int:
        self.show_splash_message("Launching Diva")
        
        if IS_WIN:
            steam_path = os.path.join(conf.steam_path, "steam.exe")
            subprocess.Popen([steam_path, "-applaunch", str(conf.app_id)])
        
        else:
            subprocess.Popen(["steam", "-applaunch", str(conf.app_id)])
                
        for attempt in range(15):
            time.sleep(1.5)
            
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    if proc.info["name"] == conf.exec_name:
                        game_pid = proc.info["pid"]
                        self.show_splash_message(f"Diva has started with PID {game_pid}")
                        
                        return game_pid
                
                except (
                        psutil.NoSuchProcess,
                        psutil.AccessDenied,
                        psutil.ZombieProcess,
                ):
                    continue
                
            self.show_splash_message(f"Waiting for Diva to start... ({attempt + 1}/15)")
        
        show_error("Couldn't find Diva process, did it crash?")
        sys.exit(1)
    
    @handle_errors
    def monitor_process(self, pid: int) -> None:
        logger.info(f"Monitoring Diva with PID {pid}")
        
        while True:
            running = False
            
            for proc in psutil.process_iter(["pid", "name"]):
                try:
                    if proc.info["pid"] == pid:
                        running = True
                        break
                
                except (
                        psutil.NoSuchProcess,
                        psutil.AccessDenied,
                        psutil.ZombieProcess,
                ):
                    continue
            
            if not running:
                logger.warning(f"Diva has exited")
                break
            
            time.sleep(1)
    
    @handle_errors
    def do_backup(self) -> None:
        if self.paths is None:
            show_error("Failed to fetch paths, object is None.")
            sys.exit(1)
        
        logger.info("Backing up")
        
        timestamp = (
            datetime.now().strftime("%Y-%B-%d_%H%M")
            if IS_WIN else
            datetime.now().strftime("%Y.%m.%d_%H:%M")
        )
        
        if conf.eden_project and not os.path.exists(self.paths.eden):
            show_error("EDEN Project save location not found but is enabled in the config")
            sys.exit(1)
        
        logger.info(f"Ensuring backup directory exists: {conf.backup_path}")
        os.makedirs(conf.backup_path, exist_ok=True)
        
        dml_not_found = not conf.eden_project and not os.path.exists(self.paths.dml)
        
        if dml_not_found:
            logger.warning("DML save location not found, defaulting to standard.")
            
            if not os.path.exists(self.paths.std):
                show_error("Standard save location not found.")
                sys.exit(1)
        
        save_folder = self.paths.eden if conf.eden_project else self.paths.std if dml_not_found else self.paths.dml
        backup_path = os.path.join(conf.backup_path, f"Diva-{timestamp}.zip")
        
        logger.info(f"Backing up to {backup_path}")
        
        with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(save_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, save_folder)
                    
                    zipf.write(file_path, arcname)
        
        logger.info(f"Backup complete! Saved to {backup_path}")
    
    def show_splash_message(self, message: str) -> None:
        logger.info(f"Splash message: {message}")
        
        self.splash.show_message(message)
        self.app.processEvents()
    
    def close_splash(self) -> None:
        self.splash.close()
    
    def close_app(self) -> None:
        app = QApplication.instance()
        if app:
            app.quit()
        
        sys.exit(0)
    
    def run(self) -> int:
        logger.info("Starting Diva Auto Backup...")
        
        if conf.first_time_experience:
            fte_dialog = FirstTimeExperienceDialog()
            if fte_dialog.exec() != QDialog.DialogCode.Accepted:
                logger.info("User cancelled first time setup")
                self.close_app()
                return 0

        self.splash.show()
        self.app.processEvents()
        
        self.paths = self.get_paths()
        
        if self.paths is None:
            show_error("Failed to fetch paths, object is None.")
        
        self.check_steam()
        
        pid = self.launch_game()
        
        self.close_splash()
        self.monitor_process(pid)
        
        dialog = UserConfirmation()
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.do_backup()
        else:
            logger.info("User declined backup")
        
        self.close_app()
        
        return self.app.exec()