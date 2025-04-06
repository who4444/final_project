import sys
import os
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from resources.config import IMAGES_DIR

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Get base path for assets
        texture_path = os.path.join(IMAGES_DIR, "Background.png").replace("\\", "/")

        self.setStyleSheet(f"""
            QDialog {{
                background-color: #e6ccb2;  /* Light brown parchment feel */
                font: 14pt "Arial Black";  /* Classic book-style font */
                color: rgb(74, 59, 49); /* Darker text for readability */
                background-image: url('{texture_path}'); /* Dynamic path */
                background-position: center;
                background-repeat: no-repeat;
                background-size: cover; /* Ensure the background covers the entire box */
                padding: 20px; /* Add space around content */
            }}
            QLabel {{
                qproperty-alignment: AlignCenter;
                font-size: 14pt;
                color: #F7F7F7;  /* Darker brown for readability */
            }}
            QPushButton {{
                background-color: #a97155;  /* Rich warm brown button */
                border: 2px solid #6b4226;
                color: white;
                font: bold 12pt "Garamond";
                padding: 8px;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background-color: #704214;  /* Darker wood tone on hover */
            }}
        """)
    

# Example Usage:
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)

    dialog = CustomDialog()
    dialog.setWindowTitle("This is the test dialog")
    # Layout
    layout = QVBoxLayout(dialog)

    # Message Label
    dialog.label = QLabel(dialog)
    dialog.label.setText("This is the test dialog")
    layout.addWidget(dialog.label)

    # Buttons
    dialog.ok_button = QPushButton("OK")
    dialog.ok_button.clicked.connect(dialog.accept)
    layout.addWidget(dialog.ok_button)

    dialog.setLayout(layout)

    dialog.exec()

