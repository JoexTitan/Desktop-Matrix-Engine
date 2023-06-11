import os
import webbrowser
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QKeySequence, QPalette, QColor, QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QTreeWidget, \
    QTreeWidgetItem, QHeaderView, QStyleFactory, QShortcut, QApplication
from FileSearchWorker import FileSearchWorker

class FileSearcher(QMainWindow):
    def __init__(self):
        super().__init__()

        # Setting window properties
        self.setWindowTitle("File Search")
        self.setFixedSize(800, 400)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Setting the application style
        QApplication.setStyle(QStyleFactory.create("Fusion"))
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#282c34"))
        palette.setColor(QPalette.WindowText, QColor("#abb2bf"))
        palette.setColor(QPalette.Base, QColor("#282c34"))
        palette.setColor(QPalette.AlternateBase, QColor("#3e4451"))
        palette.setColor(QPalette.ToolTipBase, QColor("#282c34"))
        palette.setColor(QPalette.ToolTipText, QColor("#abb2bf"))
        palette.setColor(QPalette.Text, QColor("#abb2bf"))
        palette.setColor(QPalette.Button, QColor("#3e4451"))
        palette.setColor(QPalette.ButtonText, QColor("#abb2bf"))
        palette.setColor(QPalette.Highlight, QColor("#528bff"))
        palette.setColor(QPalette.HighlightedText, QColor("#f8f8f2"))
        QApplication.setPalette(palette)

        # Create widgets
        self.central_widget = QWidget(self)
        self.layout = QVBoxLayout(self.central_widget)
        self.search_box = QLineEdit(self)
        self.results_tree = QTreeWidget(self)
        self.results_tree.setHeaderHidden(True)
        self.results_tree.setColumnCount(2)
        self.results_tree.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Set widget properties
        self.search_box.setPlaceholderText("Type to search...")
        self.search_box.setStyleSheet("QLineEdit { border: 1px solid gray; border-radius: 5px; padding: 5px; }")
        self.search_box.setFont(QFont("Segoe UI", 12))
        self.results_tree.setStyleSheet("QTreeView::item { height: 25px; }")
        self.results_tree.setFont(QFont("Segoe UI", 10))

        # Build layout
        self.layout.addWidget(self.search_box)
        self.layout.addWidget(self.results_tree)
        self.setCentralWidget(self.central_widget)

        # Initialize search worker
        self.search_worker = None

        # Connect signals and slots
        self.search_box.textChanged.connect(self.start_search)
        self.search_box.returnPressed.connect(self.open_selected_file)
        self.results_tree.itemActivated.connect(self.open_selected_file)

    def start_search(self, query):
        if self.search_worker:
            self.search_worker.quit()

        self.results_tree.clear()

        if query:
            self.search_worker = FileSearchWorker(query)
            self.search_worker.search_result.connect(self.add_search_result)
            self.search_worker.start()

    def add_search_result(self, file_path):
        file_name = os.path.basename(file_path)
        directory_name = os.path.dirname(file_path)
        result_item = QTreeWidgetItem([file_name, directory_name])
        result_item.setToolTip(0, file_path)
        self.results_tree.addTopLevelItem(result_item)

    def open_selected_file(self):
        selected_items = self.results_tree.selectedItems()
        if selected_items:
            file_path = selected_items[0].toolTip(0)
            if os.path.isfile(file_path):
                webbrowser.open(file_path)

        self.close()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
