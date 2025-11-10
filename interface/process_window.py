from misc import Misc
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QProgressBar, QLineEdit, QTextEdit
import pyperclip


class ProcessWindow(QWidget):
    def __init__(self, uploads, do_upload_event, dropbox_helper):
        super().__init__()

        self.do_upload_event = do_upload_event
        self.setWindowTitle(Misc.ProgName.value)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        total_uploads = self._get_uploads_required(uploads)

        title_label = QLabel("{} images processed. {} uploads required".format(len(uploads.keys()), total_uploads), objectName="headingLbl")
        self.layout.addWidget(title_label)

        self.dropbox_url = dropbox_helper.get_auth_url()

        if self.dropbox_url is not None:
            path_label = QLabel("Files will uploaded to '{}' on Dropbox.".format(Misc.DropboxUploadPath.value))
            self.layout.addWidget(path_label)

            copy_button = QPushButton("Click to copy URL to clipboard, then paste into browser to get auth code.")
            copy_button.clicked.connect(self._copy_button_pushed)
            self.layout.addWidget(copy_button)

            auth_text_label = QLabel("Paste auth code here:")
            self.layout.addWidget(auth_text_label)

            self.auth_text = QLineEdit()
            self.layout.addWidget(self.auth_text)

            self.go_btn = QPushButton("Go")
            self.go_btn.clicked.connect(self._upload_button_pushed)
            self.layout.addWidget(self.go_btn)

            self.progress_bar = QProgressBar()
            self.progress_bar.setRange(0, total_uploads)
            self.progress_bar.setValue(0)
            self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(self.progress_bar)

        else:
            issue_label = QLabel("Dropbox Creds Issue.", objectName="errorLbl")
            self.layout.addWidget(issue_label)


    @staticmethod
    def _get_uploads_required(uploads):
        count = 0
        for file in uploads.keys():
            for person in uploads[file]:
                count += 1

        return count

    def _upload_button_pushed(self):
        if self.auth_text.text().strip() != "":
            self.go_btn.setDisabled(True)
            self.go_btn.setText("Uploading...")
            self.do_upload_event(self.auth_text.text().strip())

    def _copy_button_pushed(self):
        pyperclip.copy(self.dropbox_url)

    def update_progress(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)

    def display_upload_error(self):
        issue_label = QLabel("Dropbox Upload Error.", objectName="errorLbl")
        self.layout.addWidget(issue_label)