from PyQt6.QtCore import QObject, pyqtSignal
import time

class UploadTask(QObject):

    finished = pyqtSignal()
    upload_signal = pyqtSignal()

    def __init__(self, uploads, dropbox_helper, auth_code, upload_message_event):
        super().__init__()

        self.uploads = uploads
        self.dropbox_helper = dropbox_helper
        self.auth_code = auth_code
        self.upload_message_event = upload_message_event
        self.upload_status = False

    def run(self):


        auth_success = self.dropbox_helper.authorize(self.auth_code)

        if auth_success:

            self.upload_status = True

            for file in self.uploads.keys():
                for person in self.uploads[file]:
                    upload_result = self.dropbox_helper.upload_file(file)
                    self.upload_message_event(upload_result['message'])

                    if not upload_result['status']:
                        self.upload_status = False

                    self.upload_signal.emit()

        self.finished.emit()


    def get_upload_status(self):
        return self.upload_status
