import os
from PyQt5.QtCore import QThread, pyqtSignal
from fuzzywuzzy import fuzz

class FileSearchWorker(QThread):
    search_result = pyqtSignal(str)

    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        self.search_directory(os.path.expanduser("~"))

    def search_directory(self, directory):
        # Adding Desktop as the first directory to search
        desktop_dir = os.path.join(directory, "Desktop")
        if os.path.isdir(desktop_dir):
            self.search_in_directory(desktop_dir)

        for root, dirs, files in os.walk(directory):
            # Ignoring the hidden directories - ignore dot files
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                if dir_name.lower() == "desktop":
                    continue
                self.search_in_directory(dir_path)

    def search_in_directory(self, directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                similarity = fuzz.ratio(self.query.lower(), file.lower())
                if similarity > 70:  # Adjusting the threshold/sensitivity as needed
                    file_path = os.path.join(root, file)
                    self.search_result.emit(file_path)
