import sys
import os
from PyQt6.QtWidgets import QMessageBox, QLabel,QStyle
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from resources.config import IMAGES_DIR, ICONS_DIR
class CustomMessageBox(QMessageBox):
    def __init__(self, title, message, icon):
        super().__init__()

        # Get the absolute path to the image
        texture_path = os.path.join(IMAGES_DIR, "Background.png").replace("\\", "/")  # Ensure
        # cross-platform compatibility
        # Set MessageBox properties
        self.setWindowTitle(f" {title} ")  # Aesthetic title
        self.setText(message)
        self.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        # Set and align icon properly
        icon_pixmap = self.iconPixmapFromEnum(icon)
        if icon_pixmap:
            self.setIconPixmap(icon_pixmap)
        else:
            self.setIcon(icon)

        # Apply Vintage Style with Wood Floor Background
        self.setStyleSheet(f"""
            QMessageBox {{
                background-color: #d2b48c;
                font: 16pt "Arial Black";  /* Classic book-style font */
                color: #26242d;
                background-image: url('{texture_path}'); /* Dynamic path */
                background-position: center;
                background-repeat: no-repeat;
                background-size: 100% 100%; /* Ensure the background covers the entire box */
            }}
            QLabel {{
                font: 16pt "Arial Black";  
                color: #26242d;
            }}
            QPushButton {{
                background-color: rgb(43, 40, 50);
                color: rgb(244, 209, 174);
                border-radius: 5px;
                font: 87 15pt "Arial Black";
                padding: 10px
            }}
            QPushButton:hover {{
                background-color:rgb(64, 61, 70);
            }}
            QPushButton:pressed {{
                background-color: rgb(38, 36, 45);
            }}
        """)

        # Set an icon (optional: change this to a library/book-themed icon)
        self.setWindowIcon(QIcon(os.path.join(ICONS_DIR, "library_icon.png")))  
    
    def iconPixmapFromEnum(self, icon_enum):
        """Convert QMessageBox.Icon to QPixmap for proper alignment"""
        icon_map = {
            QMessageBox.Icon.Information: QStyle.StandardPixmap.SP_MessageBoxInformation,
            QMessageBox.Icon.Warning: QStyle.StandardPixmap.SP_MessageBoxWarning,
            QMessageBox.Icon.Critical: QStyle.StandardPixmap.SP_MessageBoxCritical,
            QMessageBox.Icon.Question: QStyle.StandardPixmap.SP_MessageBoxQuestion,
        }

        standard_icon = icon_map.get(icon_enum, None)
        if standard_icon is not None:
            return self.style().standardIcon(standard_icon).pixmap(45, 45)

        return None

    @staticmethod
    def information(parent, title, message, buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel, default_button=QMessageBox.StandardButton.Cancel):
        """Custom Information Message Box"""
        msg_box = CustomMessageBox(title, message, QMessageBox.Icon.Information)
        return msg_box.exec()

    @staticmethod
    def warning(parent, title, message, buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel, default_button=QMessageBox.StandardButton.Cancel):
        """Custom Warning Message Box"""
        msg_box = CustomMessageBox(title, message, QMessageBox.Icon.Warning)
        return msg_box.exec()

    @staticmethod
    def critical(parent, title, message, buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel, default_button=QMessageBox.StandardButton.Cancel):
        """Custom Critical Error Message Box"""
        msg_box = CustomMessageBox(title, message, QMessageBox.Icon.Critical)
        return msg_box.exec()

    @staticmethod
    def question(parent, title, message, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, default_button=QMessageBox.StandardButton.No):
        """Custom Question Message Box with configurable buttons"""
        msg_box = CustomMessageBox(title, message, QMessageBox.Icon.Question)
        msg_box.setStandardButtons(buttons)
        msg_box.setDefaultButton(default_button)
        return msg_box.exec()
