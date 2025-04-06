from better_profanity import profanity
from PyQt6.QtWidgets import (
    QLineEdit,
    QAbstractItemView,
    QTableWidgetItem,
    QTableWidget,
    QHeaderView
)
from PyQt6.QtCore import Qt
def toggle_echo_mode(line_edit: QLineEdit):
    if line_edit.echoMode() == QLineEdit.EchoMode.Password:
        line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
    else:
        line_edit.setEchoMode(QLineEdit.EchoMode.Password)
profanity.load_censor_words()

def moderate_reviews(review):
    return profanity.contains_profanity(review)