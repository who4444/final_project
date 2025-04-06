from PyQt6.QtWidgets import QVBoxLayout,QTableWidget
from ui.dialogs.style_dialog import CustomDialog
from utils.table.table import TableWidgetManager

class NotificationDialog(CustomDialog):
    def __init__(self, parent=None,data=None,headers=None):
        super().__init__(parent)
        self.data = data
        self.headers = headers
        self.setWindowTitle("Notifications")
        self.setFixedSize(650,400)

        layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_manager = TableWidgetManager()

        layout.addWidget(self.table_widget)

        self.setLayout(layout)
        

    def show_notifications(self):
        self.table_manager.load_data(self.table_widget,self.data,self.headers, table_type="notification")
        self.exec()