import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QMouseEvent
from PySide6.QtWidgets import QSplashScreen

from ..log import logger
from ..helpers import get_base_path


class SplashScreen(QSplashScreen):
    def __init__(self) -> None:
        image_path = os.path.join(get_base_path(), "assets", "splash.png")
        logger.debug(f"Splash image path: {image_path}")
        pixmap = QPixmap(image_path)
        
        # super().__init__(pixmap, f=Qt.WindowType.WindowStaysOnTopHint)
        super().__init__(pixmap)
        
        self.setFixedSize(pixmap.width(), pixmap.height())
        
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.width(),
                self.height(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.setPixmap(scaled_pixmap)
        
        self.current_message = ""
        logger.debug(f"Splash screen initialized with size: {self.width()}x{self.height()}")
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        event.ignore()

    def drawContents(self, painter: QPainter) -> None:
        if self.current_message:
            painter.setPen(Qt.GlobalColor.white)
            
            font = painter.font()
            font.setPointSize(14)
            font.setBold(True)
            
            painter.setFont(font)
            
            text_width = painter.fontMetrics().horizontalAdvance(self.current_message)
            
            x = (self.width() - text_width) / 2
            y = self.height() - 30
            
            painter.drawText(int(x), int(y), self.current_message)
    
    def show_message(self, message: str) -> None:
        self.current_message = message
        logger.debug(f"Splash message: {message}")
        self.repaint()