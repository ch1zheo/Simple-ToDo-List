import sys

from PyQt6.QtWidgets import QApplication

from main_window import MainWindow
from styles import DARK_STYLESHEET

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
