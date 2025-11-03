from misc import Misc
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QProgressBar


class ProcessWindow(QWidget):
    def __init__(self, uploads, do_upload_event):
        super().__init__()

        self.do_upload_event = do_upload_event
        self.setWindowTitle(Misc.ProgName.value)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        total_uploads = self._get_uploads_required(uploads)

        title_label = QLabel("{} images processed. {} uploads required".format(len(uploads.keys()), total_uploads), objectName="headingLbl")
        layout.addWidget(title_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, total_uploads)
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.progress_bar)

        self.go_btn = QPushButton("Go")
        self.go_btn.clicked.connect(self._upload_button_pushed)
        layout.addWidget(self.go_btn)

    def _get_uploads_required(self, uploads):
        count = 0
        for file in uploads.keys():
            for person in uploads[file]:
                count += 1

        return count

    def _upload_button_pushed(self):
        self.go_btn.setDisabled(True)
        self.go_btn.setText("Uploading...")
        self.do_upload_event()

    def update_progress(self):
        self.progress_bar.setValue(self.progress_bar.value() + 1)