import os
import platform

from PySide6.QtGui import QIcon

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QCheckBox, QPushButton, QFileDialog
)

from ..conf import conf, write_config
from ..helpers import get_base_path
from .error_popup import show_error


class FirstTimeExperienceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Diva Auto Backup - First Time Setup")
        self.setModal(True)
        self.setFixedSize(500, 220)
        
        icon_path = os.path.join(get_base_path(), "assets", "logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        steam_layout = QVBoxLayout()
        steam_label = QLabel("Choose your Steam path if you have it installed on a non-standard location:")
        steam_layout.addWidget(steam_label)
        
        steam_input_layout = QHBoxLayout()
        
        self.steam_path_input = QLineEdit()
        self.steam_path_input.setPlaceholderText(conf.steam_path)
        self.steam_path_input.setText(conf.steam_path)
        
        if platform.system() == "Linux":
            self.steam_path_input.setReadOnly(True)
        
        steam_input_layout.addWidget(self.steam_path_input)
        
        self.browse_button = QPushButton("Browse...")
        self.browse_button.setMaximumWidth(80)
        self.browse_button.clicked.connect(self.browse_steam_path)
        if platform.system() == "Linux":
            self.browse_button.setEnabled(False)
        steam_input_layout.addWidget(self.browse_button)
        
        steam_layout.addLayout(steam_input_layout)
        
        if platform.system() == "Linux":
            linux_note = QLabel("Steam path is automatically detected on Linux")
            linux_note.setStyleSheet("font-style: italic; color: gray; font-size: 11px;")
            steam_layout.addWidget(linux_note)
        
        layout.addLayout(steam_layout)
        
        backup_layout = QVBoxLayout()
        backup_label = QLabel("Choose where to store your backups:")
        backup_layout.addWidget(backup_label)
        
        backup_input_layout = QHBoxLayout()
        
        self.backup_path_input = QLineEdit()
        self.backup_path_input.setPlaceholderText(conf.backup_path)
        self.backup_path_input.setText(conf.backup_path)
        backup_input_layout.addWidget(self.backup_path_input)
        
        self.backup_browse_button = QPushButton("Browse...")
        self.backup_browse_button.setMaximumWidth(80)
        self.backup_browse_button.clicked.connect(self.browse_backup_path)
        backup_input_layout.addWidget(self.backup_browse_button)
        
        backup_layout.addLayout(backup_input_layout)
        layout.addLayout(backup_layout)
        
        self.eden_checkbox = QCheckBox("I use the Eden Project")
        self.eden_checkbox.setChecked(conf.eden_project)
        layout.addWidget(self.eden_checkbox)
        
        layout.addStretch()
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.save_button = QPushButton("Save")
        self.save_button.setDefault(True)
        self.save_button.setMinimumWidth(100)
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def browse_steam_path(self):
        current_path = self.steam_path_input.text().strip() or conf.steam_path
        start_dir = current_path if os.path.exists(current_path) else os.path.expanduser("~")
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Steam Installation Folder",
            start_dir,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder:
            if not os.path.exists(os.path.join(folder, "steam.exe")):
                show_error("Steam executable not found in the selected Steam folder", dont_close=True)
                return
            
            self.steam_path_input.setText(folder)
    
    def browse_backup_path(self):
        current_path = self.backup_path_input.text().strip() or conf.backup_path
        start_dir = current_path if os.path.exists(current_path) else os.path.expanduser("~")
        
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Backup Folder",
            start_dir,
            QFileDialog.Option.ShowDirsOnly
        )
        
        if folder:
            if not os.access(folder, os.W_OK):
                show_error(
                    "DivaAutoBackup doesn't have write permissions to the selected backup folder",
                    dont_close=True
                )
                return
            
            self.backup_path_input.setText(folder)
    
    def save_settings(self):
        steam_path = self.steam_path_input.text().strip() or conf.steam_path
        backup_path = self.backup_path_input.text().strip() or conf.backup_path
        
        conf.steam_path = steam_path.replace("\\", "/")
        conf.backup_path = backup_path.replace("\\", "/")
        conf.eden_project = self.eden_checkbox.isChecked()
        conf.first_time_experience = False
        
        write_config(conf)
        
        self.accept()
