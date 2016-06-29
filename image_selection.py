import cv2

refPts = []
doneSelecting = False
image=1
numSelected=0
def click_handler(event, x, y, flags, pram):
    global refPts, doneSelecting, image, numSelected
    if(event == cv2.EVENT_LBUTTONDOWN):
        if(len(refPts)==0):
            refPts = [(x,y)]
        else:
            refPts.append((x,y))
    elif (event == cv2.EVENT_LBUTTONUP):
        refPts.append((x,y))
        doneSelecting = True
        cv2.rectangle(image, refPts[numSelected*2], refPts[(numSelected*2)+1], (0,255,0), 2, lineType=8)
        cv2.imshow("image",image)
        numSelected = numSelected+1


def getSelectionsFromImage(img):
    global image, refPts, numSelected
    image = img
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
        for x in range(0, len(refPts)/2):
            print x
            roi = clone[refPts[0+(x*2)][1]:refPts[1+(x*2)][1], refPts[0+(2*x)][0]:refPts[1+(2*x)][0]]
            cv2.imshow("ROI"+str(x), roi)
    else:
        print "Even number "
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return refPts
