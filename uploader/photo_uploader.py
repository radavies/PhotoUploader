import pathlib
import sys
from pathlib import Path
from misc import Misc
from iptcinfo3 import IPTCInfo
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from interface.app_window import AppWindow

class PhotoUploader:

    def __init__(self):
        self.uploads = {}
        self.app_window = None

    def start_app(self):
        app = QApplication(sys.argv)
        app.setApplicationName(Misc.ProgName.value)

        folder = Path(Misc.DataFolderPath.value)
        icon_file = folder / Misc.IconFileName.value
        app.setWindowIcon(QIcon(str(icon_file)))

        css_file = folder / Misc.CSSFileName.value
        app.setStyleSheet(open(css_file).read())

        self.app_window = AppWindow(self.process_folder_event)
        self.app_window.show()

        sys.exit(app.exec())

    def process_folder_event(self, folder):
        self.app_window.close()

        files = pathlib.Path(folder).iterdir()

        for file in files:
            if file.suffix.lower() == ".jpg" or file.suffix.lower() == ".jpeg":
                self.read_metadata(file)

        print("done")

    def read_metadata(self, file):
        info = IPTCInfo(file)

        people = info['headline'].decode("utf-8").split(',')

        for person in people:
            if file in self.uploads.keys():
                self.uploads[file].append(person)
            else:
                self.uploads[file] = [person]