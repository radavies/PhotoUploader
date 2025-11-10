from PyQt6.QtCore import QObject, pyqtSignal

class UploadTask(QObject):

    finished = pyqtSignal()
    upload_signal = pyqtSignal()

    def __init__(self, uploads, dropbox_helper, auth_code):
        super().__init__()

        self.uploads = uploads
        self.dropbox_helper = dropbox_helper
        self.auth_code = auth_code
        self.upload_status = False

    def run(self):

        auth_success = self.dropbox_helper.authorize(self.auth_code)

        if auth_success:

            self.upload_status = self.dropbox_helper.upload_files(self.uploads, self.upload_signal)

        self.finished.emit()


    def get_upload_status(self):
        return self.upload_status
