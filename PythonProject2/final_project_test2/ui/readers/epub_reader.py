from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtWebEngineWidgets import QWebEngineView
import zipfile
import bs4
from ui.dialogs.style_dialog import CustomDialog
class EpubReader(CustomDialog):
    def __init__(self, book_link, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Read Book")
        self.setGeometry(100, 100, 900, 600)

        self.epub_path = book_link
        self.chapter_index = 0

        # UI Elements
        self.read_area = QWebEngineView(self)
        self.next_btn = QPushButton("Next Chapter")
        self.prev_btn = QPushButton("Previous Chapter")

        self.next_btn.clicked.connect(self.next_chapter)
        self.prev_btn.clicked.connect(self.previous_chapter)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.read_area)
        layout.addWidget(self.next_btn)
        layout.addWidget(self.prev_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setLayout(layout)

        # Load chapters
        self.chapters = self.extract_chapters()
        self.load_chapter()

    def extract_chapters(self):
        chapters = []
        try:
            with zipfile.ZipFile(self.epub_path, "r") as epub_zip:
                text_files = sorted(
                    [f for f in epub_zip.namelist() if f.endswith(".xhtml") or f.endswith(".html")]
                )

                for text_file in text_files:
                    with epub_zip.open(text_file, "r") as file:
                        soup = bs4.BeautifulSoup(file.read(), "html.parser")
                        chapters.append(soup.prettify())

        except Exception as e:
            print(f"Error loading EPUB: {e}")
        return chapters

    def load_chapter(self):
        if 0 <= self.chapter_index < len(self.chapters):
            self.read_area.setHtml(self.chapters[self.chapter_index])

    def next_chapter(self):
        if self.chapter_index < len(self.chapters) - 1:
            self.chapter_index += 1
            self.load_chapter()

    def previous_chapter(self):
        if self.chapter_index > 0:
            self.chapter_index -= 1
            self.load_chapter()