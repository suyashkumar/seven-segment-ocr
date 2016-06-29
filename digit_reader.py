import cv2

class DigitReader:
    def __init__(self, croppedImage):
        self.croppedImage = croppedImage
    def printIt(self):
        print self.croppedImage
