import pathlib
import sys
import time
from pathlib import Path

from PyQt6 import QtCore

from misc import Misc
from iptcinfo3 import IPTCInfo
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from interface.start_window import StartWindow
from interface.process_window import ProcessWindow
from uploader.upload_task import UploadTask
from uploader.dropbox_helper import DropboxHelper

class PhotoUploader:

    def __init__(self, application_path):
        self.uploads = {}
        self.app_window = None
        self.process_window = None
        self.upload_thread = None
        self.upload_task = None
        self.data_folder_path = pathlib.Path('{}/{}'.format(application_path, Misc.DataFolderPath.value)).absolute()

        self.dropbox_helper = DropboxHelper(self.data_folder_path)


    def start_app(self):
        app = QApplication(sys.argv)
        app.setApplicationName(Misc.ProgName.value)

        icon_file = self.data_folder_path / Misc.IconFileName.value
        app.setWindowIcon(QIcon(str(pathlib.Path(icon_file).absolute())))

        css_file = self.data_folder_path / Misc.CSSFileName.value

        app.setStyleSheet(open(pathlib.Path(css_file).absolute()).read())
        self.app_window = StartWindow(self.process_folder_event)
        self.app_window.show()

        sys.exit(app.exec())

    def process_folder_event(self, folder):
        self.app_window.close()

        files = pathlib.Path(folder).iterdir()

        for file in files:
            if file.suffix.lower() == ".jpg" or file.suffix.lower() == ".jpeg":
                self.read_metadata(file)

        self.process_window = ProcessWindow(self.uploads, self.do_upload, self.dropbox_helper)
        self.process_window.show()

    def read_metadata(self, file):
        info = IPTCInfo(file)

        people = info['headline'].decode("utf-8").split(',')

        for person in people:
            if file in self.uploads.keys():
                self.uploads[file].append(person.strip())
            else:
                self.uploads[file] = [person]

    def do_upload(self, auth_code):

        self.upload_thread = QtCore.QThread()

        self.upload_task = UploadTask(self.uploads, self.dropbox_helper, auth_code, self.update_upload_message)
        self.upload_task.moveToThread(self.upload_thread)

        self.upload_thread.started.connect(self.upload_task.run)
        self.upload_task.finished.connect(self.upload_thread.quit)
        self.upload_thread.finished.connect(self.after_upload)

        self.upload_task.upload_signal.connect(self.update_progress)

        self.upload_thread.start()

    def update_progress(self):
        self.process_window.update_progress()

    def update_upload_message(self, message):
        self.process_window.update_upload_message(message)

    def after_upload(self):
        if self.upload_task.get_upload_status():
            time.sleep(5)
            self.process_window.close()
        else:
            self.process_window.display_upload_error()
