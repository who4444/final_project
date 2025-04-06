from PyQt6.QtWidgets import (QApplication, QDialog, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox, QWidget)
from PyQt6.QtCore import Qt
from ui.dialogs.style_dialog import CustomDialog

class AdminSignUpDialog(CustomDialog):
    def __init__(self, parent=None):
        
        super().__init__(parent)
        self.setWindowTitle("Admin Sign Up")
        self.setModal(True)

        self.layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_edit = QLineEdit()
        self.password_label = QLabel("Password:")
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        self.signup_button = QPushButton("Sign Up")
        self.signup_button.clicked.connect(self.signup)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_edit)
        self.layout.addWidget(self.password_label)
        self.layout.addWidget(self.password_edit)
        self.layout.addWidget(self.confirm_password_label)
        self.layout.addWidget(self.confirm_password_edit)
        self.layout.addWidget(self.signup_button)

        self.setLayout(self.layout)
        self.signup_info = None #added to store signup info.

    def signup(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        # Store the signup info.
        self.signup_info = {"username": username, "password": password} #store data.

        QMessageBox.information(self, "Success", "Admin sign up successful.")
        self.accept()

    def get_signup_info(self): #new method to return the signup info.
        return self.signup_info

