from misc import Misc
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog


class StartWindow(QWidget):
    def __init__(self, process_folder_event):
        super().__init__()

        self.process_folder_event = process_folder_event

        self.setWindowTitle(Misc.ProgName.value)

        self.setFixedSize(500, 350)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        select_btn = QPushButton("Select Folder To Upload")
        select_btn.clicked.connect(self._open_folder_picker)
        layout.addWidget(select_btn)

    def _open_folder_picker(self):
        self.process_folder_event(QFileDialog.getExistingDirectory())
