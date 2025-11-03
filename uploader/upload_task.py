from PyQt6.QtCore import QObject, pyqtSignal
import time

class UploadTask(QObject):

    finished = pyqtSignal()
    upload_signal = pyqtSignal()
    #league_signal = pyqtSignal(Leagues)


    def __init__(self, uploads):
        super().__init__()

        self.uploads = uploads

    def run(self):

        for file in self.uploads.keys():
            for person in self.uploads[file]:
                self.upload_signal.emit()
                time.sleep(1)

        self.finished.emit()
