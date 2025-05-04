import sys
from PyQt6.QtWidgets import QApplication
import qdarkstyle
from ui import TranscriptionApp

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = TranscriptionApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()