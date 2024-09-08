import sys

from PySide6.QtWidgets import QApplication

from gui.app import StoryApp


def main():
    app = QApplication(sys.argv)
    ex = StoryApp()
    ex.show()
    sys.exit(app.exec())
