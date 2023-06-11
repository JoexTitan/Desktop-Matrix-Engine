import sys
from PyQt5.QtWidgets import QApplication
from FileSearcher import FileSearcher

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the main window UI
    window = FileSearcher()
    window.show()

    sys.exit(app.exec_())
