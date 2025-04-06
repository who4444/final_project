from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtCore import Qt
# UI configuration
UI_CONFIG = {
    "WINDOW_TITLE": "Library Management System",
    "WINDOW_SIZE": (900, 600),
    "STYLES": {
        "MAIN_COLOR": "rgb(239, 230, 221)",
        "BUTTON_COLOR": "rgb(74, 120, 86)",
        "TEXT_COLOR": "rgb(74, 59, 49)"
    }
}
class MainWindowControl(QMainWindow):
    """Base window controller that handles window-level configurations."""
    
    def __init__(self, ui_controller):
        """
        Initialize window with a UI controller class.
        
        Args:
            ui_controller_class: Class that implements the UI logic
        """
        super().__init__()
        # Initialize window properties
        self.initialize_window()
        self.ui_controller = ui_controller
        # Create UI controller
        self.ui_controller.setupUi(self)

    def initialize_window(self):
        """Configure base window properties from config."""
        # Set window title
        self.setWindowTitle(UI_CONFIG["WINDOW_TITLE"])
        
        # Set window size
        width, height = UI_CONFIG["WINDOW_SIZE"]
        self.setFixedSize(width, height)
        
        # Set window flags
        self.setWindowFlags(
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.WindowCloseButtonHint |
            Qt.WindowType.WindowMinimizeButtonHint
        )

    def closeEvent(self, event):
        """Delegate close event to UI controller if it exists."""
        if hasattr(self.ui_controller, 'closeEvent'):
            self.ui_controller.closeEvent(event)
        else:
            super().closeEvent(event)
