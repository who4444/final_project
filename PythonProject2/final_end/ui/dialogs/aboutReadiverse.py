from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from ui.dialogs.style_dialog import CustomDialog


class AboutAppDialog(CustomDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About Readiverse")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # App Name & Version
        app_name = QLabel("<b>Readiverse</b>")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version = QLabel("Version 1.0.0")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Description
        description = QLabel("<i>A library management system for book lovers.</i>")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Features
        features = QLabel(
            "📚 Manage book inventory\n"
            "⭐ Rate and review books\n"
            "📈 View daily, weekly, and monthly rankings\n"
            "⏳ Track borrow history and penalties\n"
            "🛠 Admin tools for review moderation"
        )
        features.setAlignment(Qt.AlignmentFlag.AlignCenter)

        copyright_label = QLabel("© 2025 Readiverse Team. All rights reserved.")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add widgets to layout
        layout.addWidget(app_name)
        layout.addWidget(version)
        layout.addWidget(description)
        layout.addWidget(features)
        layout.addWidget(copyright_label)

        self.setLayout(layout)
