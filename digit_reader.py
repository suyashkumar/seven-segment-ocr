"""
digit_reader.py
Module to extract and read seven-segment display digits from an
ROI in an image.
@author: Suyash Kumar <suyashkumar2003@gmail.com>
"""
import cv2
import os
import time
import warnings
# Read Environment Vars
dev = int(os.environ['DEV'])
demo = int(os.environ['DEMO'])
if (not dev):
    warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt

# Number Mapping:
mapping = {
    "0101000": 1,
    "0110111": 2,
    "0101111": 3,
    "1101010": 4,
    "1001111": 5,
    "1011111": 6,
    "1011011": 6,
    "0101100": 7,
    "1101100": 7,
    "1111111": 8,
    "1101110": 9,
    "1101111": 9,
    "1111101": 0
}

def cropImage(image, roi):
    #print roi
    clone = image.copy()
    retImg = clone[roi[0][1]:roi[1][1], roi[0][0]:roi[1][0]]
    return retImg

def line_profile(image, profType, loc):
    height, width = image.shape[:2]
    if (profType == "h"):
        return image[int(round(height*loc)):int(round(height*loc))+1, 0:width]
    elif(profType == "v"):
        return image[0:height, int(round(0.5*width)):int(round(0.5*width)+1)]

def getProcessStringHoriz(arr):
    firstHalf = check_high(arr[0:int(round(len(arr)/2))])
    lastHalf  = check_high(arr[int(round(len(arr)/2)):len(arr)])
    return str(firstHalf)+str(lastHalf)

def getProcessStringVert(arr):
    firstQuarter = check_high(arr[0:int(round(len(arr)/4))])
    middleHalf   = check_high(arr[int(round(1*len(arr)/4)):int(round(3*len(arr)/4))])
    lastQuarter  = check_high(arr[int(3*round(len(arr)/4)):len(arr)])
    return str(firstQuarter)+str(middleHalf)+str(lastQuarter)


def check_high(arraySlice, N=8, threshold=100):
    arraySlice = arraySlice[5:]
    numInRow = 0
    maxInRow = 0
    for x in arraySlice:
        if (x>=threshold):
            numInRow = numInRow + 1
        else:
            if numInRow > maxInRow:
                maxInRow = numInRow
            numInRow = 0
    if (maxInRow > N or numInRow >N):
        return 1
    else:
        return 0


"""
Returns digit given a cropped grayscale image of the 7 segments.
In the image 0 is signal and 255 is background
"""
def resolve_digit(croppedImage):
    #L1Coord = [(round(height*.25),round(height*.25)+1), (0,width)]
    L1 = line_profile(croppedImage, "h", 0.25)
    L2 = line_profile(croppedImage, "h", 0.75)
    L3 = line_profile(croppedImage, "v", 0.5)
    L1Arr = [int(x) for x in L1[0]]
    L2Arr = [int(x) for x in L2[0]]
    L3Arr = [int(x) for x in L3]

    #cv2.imshow("orig",croppedImage)
    processString = getProcessStringHoriz(L1Arr)+getProcessStringHoriz(L2Arr)+getProcessStringVert(L3Arr)
    digit = mapping.get(processString)
    if (digit is None):
        print "Digit not recognized: " + processString
        cv2.imshow("orig", croppedImage)
        digit = input("What digit is this? Enter here: ")
        cv2.waitKey(0)
    #cv2.waitKey(0)
    if (dev):
        print processString
        print mapping[processString]
        # Show images and line profiles:
        cv2.imshow("L1", L1)
        cv2.imshow("L2", L2)
        cv2.imshow("L3",L3)
        cv2.imshow("orig",croppedImage)

        plt.figure(1)
        plt.subplot(311)
        plt.plot(L1Arr)
        plt.title("L1")
        plt.subplot(312)
        plt.plot(L2Arr)
        plt.title("L2")
        plt.subplot(313)
        plt.plot(L3Arr)
        plt.title("L3")
        plt.show()

        cv2.waitKey(0)
    return digit

def read_digits(image, roiPoints):
    digits = []
    for selection in xrange(0,len(roiPoints)/2):
        currentSel = image.copy()
        currentSel = cv2.cvtColor(currentSel, cv2.COLOR_BGR2GRAY) # Convert to grayscale
        currentSel = cropImage(currentSel, [roiPoints[selection*2], roiPoints[2*selection+1]])
        digit=resolve_digit(currentSel)
        digits.append(digit)
        if (demo):
            cv2.imshow("demo",currentSel)
            print digit
            cv2.waitKey(0)
    return digits
