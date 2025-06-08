#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess


def build(windowed: bool = False) -> None:
    mode = "windowed" if windowed else "console"
    
    print(f"Building with {mode} mode")
    
    for path in ["build", "dist"]:
        if os.path.exists(path):
            shutil.rmtree(path)
    
    icon_path = "divaautobackup/assets/logo.ico"
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "DivaAutoBackup.spec"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        
        print("Build successful")
        print("Copying external files")
        
        shutil.copy2("config.yml", "dist/config.yml")
        
        log_path = "dist/dab2.log"
        if not os.path.exists(log_path):
            with open(log_path, "w") as f:
                f.write("")
        
        print("Build complete! Dist folder ready for distribution")
    
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        sys.exit(1)
    

if __name__ == "__main__":
    build(windowed=False)
