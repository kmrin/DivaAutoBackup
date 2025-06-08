import random

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt

MESSAGES = [
    "Sweet gameplay! Would you like to backup your progress?",
    "You've gone so far, would you like to backup your progress?",
    "Hi there! Would you like to backup your progress?",
    "Hey fellow Diver, Vocaloider? Is that weird? Anyway, would you like to backup your progress?",
    "Would you like to backup your progress?",
]


class UserConfirmation(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        
        self.setWindowTitle("Backup confirmation")
        self.selected_message = random.choice(MESSAGES)
        self.init_ui()
    
    def init_ui(self) -> None:
        layout = QVBoxLayout()
        
        self.label = QLabel(self.selected_message)
        self.label.setWordWrap(True)
        
        font = QFont()
        font.setBold(True)
        
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        layout.addWidget(self.label)
        
        buttons_layout = QHBoxLayout()
    
        self.yes_button = QPushButton("Yes please!")
        self.yes_button.clicked.connect(self.yes_clicked)
        self.yes_button.setMinimumWidth(80)
        buttons_layout.addWidget(self.yes_button)
        
        self.no_button = QPushButton("No, thanks")
        self.no_button.clicked.connect(self.no_clicked)
        self.no_button.setMinimumWidth(80)
        buttons_layout.addWidget(self.no_button)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        
        self.setModal(True)
        self.resize(500, self.sizeHint().height())
    
    def yes_clicked(self) -> None:
        self.accept()
    
    def no_clicked(self) -> None:
        self.reject()