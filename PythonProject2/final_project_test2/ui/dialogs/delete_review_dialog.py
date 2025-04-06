from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from ui.dialogs.style_dialog import CustomDialog  
class DeleteReview(CustomDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Review")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()

        self.label = QLabel("Select a reason for deletion:")
        layout.addWidget(self.label)

        # ComboBox with deletion reasons
        self.reason_box = QComboBox()
        self.reason_box.addItems([
            "Inappropriate content",
            "Spam or advertising",
            "Hate speech",
            "False information"])
        layout.addWidget(self.reason_box)
        self.delete_button = QPushButton("Delete")
        self.cancel_button = QPushButton("Cancel")

        self.delete_button.clicked.connect(self.accept)  # Proceed with deletion
        self.cancel_button.clicked.connect(self.reject)  # Cancel

        layout.addWidget(self.delete_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def get_selected_reason(self):
        return self.reason_box.currentText()
    