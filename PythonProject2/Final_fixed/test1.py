import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QColor, QPalette, QIcon

class CustomOSWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.oldPos = self.pos()
        self.isMaximized = False

    def initUI(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setupTitleBar()
        self.setupContent()

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.content_widget)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Custom OS Window")
        self.show()

    def setupTitleBar(self):
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(30)

        wood_color = QColor(210, 180, 140)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, wood_color)
        self.title_bar.setAutoFillBackground(True)
        self.title_bar.setPalette(palette)

        title_layout = QHBoxLayout(self.title_bar)
        title_label = QLabel("Custom OS Window")
        title_label.setStyleSheet("color: black;")

        minimize_button = QPushButton()
        minimize_button.setIcon(QIcon.fromTheme("window-minimize"))
        minimize_button.setStyleSheet("""
            QPushButton {
                min-width: 40px;
                min-height: 25px;
            }
        """)
        minimize_button.clicked.connect(self.showMinimized)

        maximize_button = QPushButton()
        maximize_button.setIcon(QIcon.fromTheme("window-maximize"))
        maximize_button.setStyleSheet("""
            QPushButton {
                min-width: 40px;
                min-height: 25px;
            }
        """)
        maximize_button.clicked.connect(self.toggleMaximize)

        close_button = QPushButton()
        close_button.setIcon(QIcon.fromTheme("window-close"))
        close_button.setStyleSheet("""
            QPushButton {
                min-width: 40px;
                min-height: 25px;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)
        close_button.clicked.connect(self.close)

        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(minimize_button)
        title_layout.addWidget(maximize_button)
        title_layout.addWidget(close_button)

        self.title_bar.mouseMoveEvent = self.moveWindow
        self.title_bar.mousePressEvent = self.getPos

    def setupContent(self):
        self.content_widget = QLabel("Content Area")
        self.content_widget.setStyleSheet("background-color: white;")

    def getPos(self, event):
        self.oldPos = event.globalPosition().toPoint()

    def moveWindow(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition().toPoint()

    def toggleMaximize(self):
        if self.isMaximized:
            self.showNormal()
            self.isMaximized = False
        else:
            self.showMaximized()
            self.isMaximized = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomOSWindow()
    sys.exit(app.exec())