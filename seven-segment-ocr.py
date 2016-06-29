import argparse
import cv2
import image_selection
import digit_reader
video = cv2.VideoCapture('test.mov') # Open video
success,image = video.read() # Get first frame

refPts=image_selection.getSelectionsFromImage(image)
fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
video.release()
print refPts
digit_reader.read_digits(image,refPts)
