from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QLabel
from PyQt6.QtCore import Qt
from .style_dialog import CustomDialog

class UserProfileDialog(CustomDialog):
    """Dialog for displaying user profile information."""
    
    def __init__(self, column_names: list, row_data: list, parent=None):
        """Initialize user profile dialog.
        
        Args:
            column_names: List of column names
            row_data: List of values for each column
            parent: Parent widget
        """
        super().__init__(parent)
        self.setWindowTitle("User Information")
        self._setup_layout(column_names, row_data)
        self.adjustSize()

    def _setup_layout(self, column_names: list, row_data: list):
        """Set up the dialog layout with user data."""
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        for col_index, col_name in enumerate(column_names):
            value = row_data[col_index]
            label = QLabel(str(value))
            label.setWordWrap(True)
            label.setAlignment(Qt.AlignmentFlag.AlignRight)
            form_layout.addRow(col_name, label)

        layout.addLayout(form_layout)