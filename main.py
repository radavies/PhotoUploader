from uploader.photo_uploader import PhotoUploader

def start():
    uploader = PhotoUploader()
    uploader.start_app()

if __name__ == '__main__':
    start()