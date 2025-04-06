from PyQt6.QtWidgets import QMessageBox, QDialog, QVBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit
from PyQt6.QtCore import Qt
from ui.dialogs.style_dialog import CustomDialog
class BookInfoChecker():
    def is_title_valid(self, title):
            """Checks if the title is valid."""
            if not title:
                return False, "Title is missing."
            if not isinstance(title, str):
                return False, "Title must be a string."
            if not title.strip():
                return False, "Title cannot be empty or only whitespace."
            if len(title) > 255:
                return False, "Title is too long (max 255 characters)."
            return True, ""

    def is_author_valid(self, author):
        """Checks if the author is valid."""
        if not author:
            return False, "Author is missing."
        if not isinstance(author, str):
            return False, "Author must be a string."
        if not author.strip():
            return False, "Author cannot be empty or only whitespace."
        if len(author) > 40:
            return False, "Author is too long (max 40 characters)."
        return True, ""

    def is_description_valid(self, description):
        """Checks if the description is valid."""
        if description is not None and not isinstance(description, str):
            return False, "Description must be a string."
        return True, ""

    def is_cover_link_valid(self, cover_link):
        """Checks if the cover link is valid."""
        if not cover_link:
            return True, ""  # Allow empty cover link
        if not isinstance(cover_link, str):
            return False, "Cover link must be a string."
        if not cover_link.lower().endswith((".png", ".jpg", ".jpeg")):
            return False, "Cover link must end with .png, .jpg, or .jpeg."
        return True, ""

    def is_epub_link_valid(self, epub_link):
        """Checks if the epub link is valid."""
        if not epub_link:
            return False, "Epub link is missing."
        if not isinstance(epub_link, str):
            return False, "Epub link must be a string."
        if not epub_link.lower().endswith(".epub"):
            return False, "Epub link must end with .epub."
        return True, ""
    def check_book_data(self, book_data:dict):
        """Validates all book data fields and returns a dictionary of errors."""
        errors = {}
        is_valid = True

        # Determine the fields to validate dynamically from the book_data keys
        fields_to_validate = list(book_data.keys())  # Get the keys from book_data

        validation_methods = [
            ('title', self.is_title_valid),
            ('author', self.is_author_valid),
            ('description', self.is_description_valid),
            ('cover_link', self.is_cover_link_valid),
            ('epub_link', self.is_epub_link_valid),
        ]

        for field_name, validation_method in validation_methods:
            if field_name in fields_to_validate:
                is_field_valid, message = validation_method(book_data.get(field_name))
                if not is_field_valid:
                    errors[field_name] = message
                    is_valid = False

        return is_valid, errors

class BookDialog(CustomDialog):
    def __init__(self, admin_db, parent=None):
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

        if is_valid:
            self.accept()
        else:
            error_message = "\n".join([f"{field}: {msg}" for field, msg in errors.items()])
            QMessageBox.warning(self, "Invalid Data", f"Please correct the following errors:\n{error_message}")