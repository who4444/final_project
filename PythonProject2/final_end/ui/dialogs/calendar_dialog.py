from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCalendarWidget, QPushButton, QMessageBox
from PyQt6.QtCore import QDate
from ui.dialogs.style_dialog import CustomDialog
class CalendarDialog(CustomDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Return Date")
        self.setGeometry(300, 300, 400, 300)

        # --- Layout & Calendar ---
        layout = QVBoxLayout()
        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)

        # --- Confirm Button ---
        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.validate_and_accept)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def validate_and_accept(self):
        """Validates that the selected date is in the future before accepting."""
        selected_date = self.calendar.selectedDate()
        today = QDate.currentDate()
        if selected_date < today:
            QMessageBox.warning(self, "Date Error", "Return date must be in the future.")
        else:
            self.accept()  # Only accept if date is valid

    def get_selected_date(self):
        """Returns the selected date as a string (YYYY-MM-DD)."""
        return self.calendar.selectedDate().toString("yyyy-MM-dd")
    
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow
    app = QApplication(sys.argv)
    dialog = CalendarDialog()
    dialog.exec()
    window = QMainWindow()
    window.show()
    sys.exit(app.exec())
