from PyQt6.QtWidgets import QLineEdit

class LineEditManager:
    """Manager class for handling QLineEdit operations."""
    
    def __init__(self, line_edit: QLineEdit):
        """Initialize with a QLineEdit widget.
        
        Args:
            line_edit: QLineEdit widget to manage
        """
        self.line_edit = line_edit

    def set_placeholder_text(self, text: str):
        """Set placeholder text for the line edit.
        
        Args:
            text: Text to display as placeholder
        """
        self.line_edit.setPlaceholderText(text)

    def toggle_echo_mode(self):
        """Toggle between password and normal echo mode."""
        if self.line_edit.echoMode() == QLineEdit.EchoMode.Password:
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.line_edit.setEchoMode(QLineEdit.EchoMode.Password)

    def set_password_mode(self, is_password: bool = True):
        """Set the echo mode for password input.
        
        Args:
            is_password: True for password mode, False for normal mode
        """
        mode = QLineEdit.EchoMode.Password if is_password else QLineEdit.EchoMode.Normal
        self.line_edit.setEchoMode(mode)