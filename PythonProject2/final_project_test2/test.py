from encodings.hex_codec import hex_encode
import sys
import zipfile
import bs4
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtWebEngineWidgets import QWebEngineView
from httpx import head
from resources.config import BASE_DIR, BOOKS_DIR
from database.admin import AdminManager
from database.user import UserManager
from ui.dialogs.book_dialog import BookDialog
from database.config import DB_CONFIG
from utils.table.table import TableWidgetManager
from ui.readers.epub_reader import EpubReader
from ui.message_box.custom_message_box import CustomMessageBox



    # Add temporarily to test
# if __name__ == "__main__":
#     print(f"Project root: {BASE_DIR}")
#     print(f"Alert icon exists: {ALERT_ICON.exists()}")
#     print(f"Bell icon exists: {BELL_ICON.exists()}")
    
# app = QApplication.instance() or QApplication(sys.argv)
# admin = AdminManager(DB_CONFIG['CONNECTION_STRING_1'])
# admin.connect()
# window = QMainWindow()
# a = BookDialog(admin, parent= window)
# window.show()
# sys.exit(app.exec())



# user_manager = UserManager(DB_CONFIG['CONNECTION_STRING_1']) 
# user_manager.connect()
# headers, data = user_manager.get_book_rankings("borrow_count", "daily", "DESC")
# print(headers)
# print(data)

# table_manager = TableWidgetManager()
# new_headers, data = table_manager.swap_columns(headers, data)
# print(new_headers)
# print(data)

if __name__ == "__main__":
    
    # book_link = "Lord of the Mysteries.epub"
    # book_path = BOOKS_DIR / book_link
    # print(book_path)
    # app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    # reader = EpubReader(book_link=book_path)  # Replace with your EPUB file path
    # reader.show()
    # sys.exit(app.exec())
    
    # app = QApplication(sys.argv)
    # window = QWidget()

    # # Example Message
    # CustomMessageBox.information(window, "Library Notice", """The book has been successfully returned.
    #                              \n We glad your greate prefrenec on our books
    #                              \nejiwfkewofkewokfewkofokewkofewkofkowefkowe
    #                              \nfiewjfiewjfijewfkewkfewkofkweofkoewkofewokfwokfok""")
    # window.show()
    # sys.exit(app.exec())
        
    a = UserManager(DB_CONFIG['CONNECTION_STRING_2'])
    a.connect()
    b = AdminManager(DB_CONFIG['CONNECTION_STRING_2'])
    a.user_id = 1
    # result = a.is_book_borrowed(24)
    # result2 = a.able_to_borrow()
    # print(result)
    # print(result2)
    
    # title = b.get_book_title(24)
    # print(title)
    print(a.get_profile())
    print(b.is_admin_exists())
    
    
    


