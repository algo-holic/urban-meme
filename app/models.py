import cv2


class Image:
    def __init__(self, filepath):
        self.image = cv2.imread(filepath)

    def result(self):
        return [{}, {}, {}]
