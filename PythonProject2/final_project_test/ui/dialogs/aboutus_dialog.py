import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QHBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class AboutUsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Us")
        self.setFixedSize(500, 350)  # Adjusted height for better spacing

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # App Info
        app_info = QLabel("<b>Readiverse</b><br><i>A passionate final project.</i>")
        app_info.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center text
        layout.addWidget(app_info)

        # Team Section
        team_layout = QHBoxLayout()
        team_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align center

        members = [
            ("Quoc Khiem", "Lead Developer", "Khiem.png"),
            ("Tan Phuc", "UI Designer", "Phuc.png"),
            ("Tuan Dat", "Database Engineer", "Dat.png"),
        ]

        # Get script directory
        for name, role, img in members:
            member_widget = QWidget()
            member_layout = QVBoxLayout()
            member_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            image_dir = "C:/Users/kelaien/Documents/Python Scripts/final_project/PythonProject2/final_project_test/resources/images"

            # Create the full path to the image
            img_path = os.path.join(image_dir, img)

            # Load and resize image
            pixmap = QPixmap(img_path)
            image_label = QLabel()
            if pixmap.isNull():
                image_label.setText("(Image Not Found)")
                print(f"Failed to load image: {img_path}")
            else:
                pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                       Qt.TransformationMode.SmoothTransformation)
                image_label.setPixmap(pixmap)

            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Name and Role
            name_label = QLabel(f"<b>{name}</b><br>{role}")
            name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Add widgets
            member_layout.addWidget(image_label)
            member_layout.addWidget(name_label)

            member_widget.setLayout(member_layout)
            team_layout.addWidget(member_widget)

        layout.addLayout(team_layout)

        acknowledgment = QLabel("<i>We appreciate your support throughout the course.</i>")
        layout.addWidget(acknowledgment)
        acknowledgment.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
