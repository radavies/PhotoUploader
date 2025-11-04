import os, sys
from uploader.photo_uploader import PhotoUploader

def start():

    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle, the PyInstaller bootloader
        # extends the sys module by a flag frozen=True and sets the app
        # path into variable _MEIPASS'.
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    print(application_path)

    uploader = PhotoUploader(application_path)
    uploader.start_app()

if __name__ == '__main__':
    start()