import argparse
import cv2
import image_selection
import digit_reader

"""
Reads selected digits at intervals specified by samplePeriod from.
the video specified by videoPath. Returns a list containing lists
of numbers read at each period.
"""
def read_video_digits(videoPath, samplePeriod):
    video = cv2.VideoCapture(videoPath) # Open video
    success,image = video.read() # Get first frame
    selections=image_selection.getSelectionsFromImage(image)

    fps = video.get(cv2.cv.CV_CAP_PROP_FPS) # Get FPS
    frameInterval = int(round(fps * samplePeriod))
    totalFrames = video.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)

    digitMatrix = [] # Holds list of dgits from each sample

    for frameNumber in xrange(0,int(round(totalFrames/frameInterval))):
        video.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frameNumber*frameInterval) # Set frame to read next
        success,image = video.read() # Get frame
        digits = digit_reader.read_digits(image, selections) # Get digits
        digitMatrix.append(digits)

    video.release()
    return digitMatrix

def to_csv(digitsReadArray, outputFileName):
    with open(outputFileName,'w') as f:
        for sample in digitsReadArray:
            f.write(str(sample[0])+"."+str(sample[1])+str(sample[2]))
            f.write("\n")


if __name__=="__main__":
    # Set up argument parsing:
    parser = argparse.ArgumentParser()
    parser.add_argument('--video', help = "Input Video File")
    parser.add_argument('--output', help = "Output data file", default="out.csv")
    args = parser.parse_args()
    digitsReadArray = read_video_digits(args.video, 1)
    to_csv(digitsReadArray, args.output)
