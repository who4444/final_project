from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from ui.dialogs.style_dialog import CustomDialog
from ui.message_box.custom_message_box import CustomMessageBox
from database.admin import AdminManager

class AddGenreDialog(CustomDialog):
    def __init__(self,  admin_manager :AdminManager,parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Genre")
        self.setGeometry(100, 100, 300, 150)
        self.admin_manager = admin_manager

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.genre_input = QLineEdit()
        self.genre_input.setPlaceholderText("Enter new genre")
        layout.addWidget(self.genre_input)

        add_button = QPushButton("Add Genre")
        add_button.clicked.connect(self.add_genre)
        layout.addWidget(add_button)

        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        layout.addWidget(cancel_button)

    def add_genre(self):
        genre_name = self.genre_input.text()
        if not genre_name:
            CustomMessageBox.warning(self, "Blank Genre", "please enter a genre name")
            return
        
        if self.admin_manager.is_genre_exists(genre_name):
            CustomMessageBox.warning(self, "Duplicate Genre", "genre name already exists")
            return
        self.accept()
    def get_genre_name(self):
        return self.genre_input.text()