from iptcinfo3 import IPTCInfo

class PhotoUploader:

    def __init__(self):
        _uploads = []


    def start_uploads(self, input_folder):
        self._test_reading()
        return


    def _test_reading(self):
        info = IPTCInfo('images/Motherwell_CupSemi_Press_30Oct25_012.jpg')

        people = info['headline'].decode("utf-8").split(',')

        for person in people:
            print(person.strip())

        return