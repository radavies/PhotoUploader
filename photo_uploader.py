import sys
from pathlib import Path
from misc import Misc
from iptcinfo3 import IPTCInfo
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from interface.app_window import AppWindow

class PhotoUploader:

    def __init__(self):
        self._uploads = []

    def start_app(self):
        app = QApplication(sys.argv)
        app.setApplicationName(Misc.ProgName.value)

        folder = Path(Misc.DataFolderPath.value)
        icon_file = folder / Misc.IconFileName.value
        app.setWindowIcon(QIcon(str(icon_file)))

        css_file = folder / Misc.CSSFileName.value
        app.setStyleSheet(open(css_file).read())

        window = AppWindow()
        window.show()

        sys.exit(app.exec())

    def start_uploads(self, input_folder):
        self._test_reading()
        return


    def _test_reading(self):
        info = IPTCInfo('images/Motherwell_CupSemi_Press_30Oct25_012.jpg')

        people = info['headline'].decode("utf-8").split(',')

        for person in people:
            print(person.strip())

        return