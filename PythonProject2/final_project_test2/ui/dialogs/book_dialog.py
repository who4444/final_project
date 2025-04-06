from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit
from PyQt6.QtCore import Qt
from ui.dialogs.style_dialog import CustomDialog
from utils.checker import BookInfoChecker
from database.admin import AdminManager

class BookDialog(CustomDialog):
    def __init__(self, admin_db : AdminManager, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Book")
        self.setGeometry(100, 100, 400, 300)
        self.admin_db = admin_db
        layout = QVBoxLayout()

        self.title_input = QLineEdit(self)

        self.genre_combo = QComboBox(self)
        genres = self.admin_db.get_genre()
        for genre_id, genre_name in genres:
            self.genre_combo.addItem(genre_name, genre_id)

        self.author_input = QLineEdit(self)
        self.description_input = QLineEdit(self)
        self.cover_link_input = QLineEdit(self)
        self.epub_link_input = QLineEdit(self)

        layout.addWidget(QLabel("Title:"))
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Genre:"))
        layout.addWidget(self.genre_combo)

        layout.addWidget(QLabel("Author:"))
        layout.addWidget(self.author_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_input)
        layout.addWidget(QLabel("Cover Link:"))
        layout.addWidget(self.cover_link_input)
        layout.addWidget(QLabel("Epub Link:"))
        layout.addWidget(self.epub_link_input)

        self.add_btn = QPushButton("Submit")
        self.add_btn.clicked.connect(self.on_add_clicked)  # Connect to custom handler
        layout.addWidget(self.add_btn)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)
    def load_data(self, title, genre_id, author, description, cover_link, epub_link):
        self.title_input.setText(title)
        self.genre_combo.setCurrentIndex(genre_id)
        self.author_input.setText(author)
        self.description_input.setText(description)
        self.cover_link_input.setText(cover_link)
        self.epub_link_input.setText(epub_link)
    def get_book_data(self):
        return {
            'title': self.title_input.text(),
            'genre': self.genre_combo.currentData(),
            'author': self.author_input.text(),
            'description': self.description_input.text(),
            'cover_link': self.cover_link_input.text(),
            'epub_link': self.epub_link_input.text(),
        }

    def on_add_clicked(self):
        book_data = self.get_book_data()
        checker = BookInfoChecker()
        
        is_valid, errors = checker.check_book_data(book_data)

        if not is_valid:
            error_message = "\n".join([f"{field}: {msg}" for field, msg in errors.items()])
            QMessageBox.warning(self, "Invalid Data", f"Please correct the following errors:\n{error_message}")
            return
            
        is_existed = self.admin_db.check_book_exists(book_data['title'])
        if is_existed:
            QMessageBox.warning(self, "Invalid name", f"The book name is existed")
            return
        self.accept()
