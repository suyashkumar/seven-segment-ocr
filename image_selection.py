"""
This module gives the user an image to specify selections
in and returns those selections
@author: Suyash Kumar <suyashkumar2003@gmail.com>
"""
import cv2
import sys

# Shared variable declarations
refPts = []
image=1
numSelected=0

"""
Called every time a click event is fired on the displayed
image. Is used to record ROI selections from the user, and
updates the image to place a bounding box highlighting the
ROIs
"""
def click_handler(event, x, y, flags, pram):
    global refPts, image, numSelected

    if(event == cv2.EVENT_LBUTTONDOWN):
        if(len(refPts)==0):
            refPts = [(x,y)]
        else:
            refPts.append((x,y))
    elif (event == cv2.EVENT_LBUTTONUP):
        refPts.append((x,y))
        cv2.rectangle(image, refPts[numSelected*2], refPts[(numSelected*2)+1], (0,255,0), 2, lineType=8)
        cv2.imshow("image",image)
        numSelected = numSelected+1


def getSelectionsFromImage(img):
    global image, refPts, numSelected
    image = img
    refPts = [] # Reinit refPts
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_handler)
    cv2.imshow("image",image)
    while True:
        #cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF
        if (key == ord("d")):
            break;
        if (key == ord("r")):
            refPts = refPts[:len(refPts)-2]
            numSelected = numSelected-1
            image = clone.copy()
    if ((len(refPts) % 2) == 0):
        print len(refPts)/2
        print refPts
        for selection in range(0, len(refPts)/2):
            roi = clone[refPts[0+(selection*2)][1]:refPts[1+(selection*2)][1], refPts[0+(2*selection)][0]:refPts[1+(2*selection)][0]]
            cv2.imshow("ROI"+str(selection), roi)
    else:
        sys.exit("Selection Capture didn't get an even number of bounding points.")

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return refPts
