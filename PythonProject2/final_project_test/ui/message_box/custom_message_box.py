import sys
import os
from PyQt6.QtWidgets import QMessageBox, QLabel,QStyle
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

class CustomMessageBox(QMessageBox):
    def __init__(self, title, message, icon):
        super().__init__()

        # Get the absolute path to the image
        base_path = os.path.dirname(os.path.abspath(__file__))  # Get current script directory
        texture_path = os.path.join(base_path, "wood_texture.png").replace("\\", "/")  # Ensure cross-platform compatibility

        # Set MessageBox properties
        self.setWindowTitle(f"✦ {title} ✦")  # Aesthetic title
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
                background-color: #d2b48c;  /* Warm brown, wood-like feel */
                border: 2px solid #8b5a2b;  /* Dark brown border */
                font: bold 12pt "Arial";  /* Classic book-style font */
                color: black; /* Black text for readability */
                background-image: url('{texture_path}'); /* Dynamic path */
                background-position: center;
                background-repeat: no-repeat;
                background-size: 100% 100%; /* Ensure the background covers the entire box */
            }}
            QLabel {{
                qproperty-alignment: AlignCenter; /* Ensure text is centered */
            }}
            QMessageBox QLabel#qt_msgbox_label {{
                qproperty-alignment: AlignCenter; /* Center align message box text */
            }}
            QMessageBox QLabel#qt_msgbox_icon_label {{
                qproperty-alignment: AlignVCenter | AlignLeft; /* Move icon to middle-left */
                padding-left: 20px;
                min-width: 64px;
            }}
            QPushButton {{
                background-color: #8b5a2b;  /* Darker brown for contrast */
                border: 1px solid #5a3825;
                color: white;
                font: bold 11pt "Garamond";
                padding: 6px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #704214;  /* Darker shade on hover */
            }}
        """)

        # Set an icon (optional: change this to a library/book-themed icon)
        self.setWindowIcon(QIcon(os.path.join(base_path, "library_icon.png")))  
    
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
    def information(parent, title, message):
        """Custom Information Message Box"""
        msg_box = CustomMessageBox(title, message, QMessageBox.Icon.Information)
        return msg_box.exec()

    @staticmethod
    def warning(parent, title, message):
        """Custom Warning Message Box"""
        msg_box = CustomMessageBox(title, message, QMessageBox.Icon.Warning)
        return msg_box.exec()

    @staticmethod
    def critical(parent, title, message):
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
