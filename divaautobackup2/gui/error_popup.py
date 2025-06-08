import os
import sys
import traceback

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon, QPixmap

from PySide6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QTextEdit
)

from ..helpers import get_base_path
from ..log import logger


class ErrorPopup(QDialog):
    def __init__(self, parent=None, dont_close: bool = False):
        super().__init__(parent)
        self.setWindowTitle("Oops!")
        self.setModal(True)
        self.resize(500, 300)
        self.dont_close = dont_close
        icon_path = os.path.join(get_base_path(), "assets", "logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        error_layout = QHBoxLayout()
        
        self.error_image = QLabel()
        self.error_image.setFixedSize(32, 32)
        error_image_path = os.path.join(get_base_path(), "assets", "error.png")
        if os.path.exists(error_image_path):
            pixmap = QPixmap(error_image_path)
            scaled_pixmap = pixmap.scaled(
                32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.error_image.setPixmap(scaled_pixmap)
            self.error_image.setAlignment(Qt.AlignmentFlag.AlignTop)
        error_layout.addWidget(self.error_image)
        
        error_layout.addSpacing(10)
        
        self.error_label = QLabel()
        self.error_label.setWordWrap(True)
        font = QFont()
        font.setBold(True)
        self.error_label.setFont(font)
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        error_layout.addWidget(self.error_label)
        
        layout.addLayout(error_layout)
        
        self.traceback_area = QTextEdit()
        self.traceback_area.setReadOnly(True)
        self.traceback_area.setFont(QFont("Consolas", 9))
        self.traceback_area.hide()
        layout.addWidget(self.traceback_area)
        
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.ok_button = QPushButton("OK")
        if self.dont_close:
            self.ok_button.setText("Ok")
            self.ok_button.clicked.connect(self.close)
        else:
            self.ok_button.clicked.connect(self.close_application)
        self.ok_button.setDefault(True)
        button_layout.addWidget(self.ok_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def close_application(self):
        app = QApplication.instance()
        if app:
            app.quit()
        sys.exit(0)


def show_error(error_message: str, dont_close: bool = False):
    logger.error(error_message)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    popup = ErrorPopup(dont_close=dont_close)
    popup.error_label.setText(error_message)
    
    popup.adjustSize()
    popup.resize(500, popup.sizeHint().height())
    
    popup.exec()


def show_trace(error_message: str, exception: Exception):
    logger.error(error_message)
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    popup = ErrorPopup()
    popup.error_label.setText(error_message)
    
    popup.traceback_area.show()
    popup.resize(600, 450)
    
    tb_str = ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
    popup.traceback_area.setPlainText(tb_str)
    
    popup.exec()