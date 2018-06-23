# seven-segment-ocr
A program and set of Python modules to parse digits from videos of seven segment displays. This program does not operate on a trained model--rather, it takes a universal approach by taking three line profiles to efficiently and effectively determine which digit is shown.
## Usage

Simply supply a path to a video of a seven segment display and an interval to sample the digits at and an output file will be generated (by default out.csv) with the recognized digits at each sample interval. Before proceeding, the program first presents the first frame of the video and you must click and drag rectangular selections around the digits in the video and then press "d" when done or "r" to redraw rectangles. The program will then go though and recognize and parse the digits at each interval.

```bash
python seven_segment_ocr.py --video VIDEO_PATH --output OUTPUT_DATA_FILE --period SAMPLE_PERIOD
```

This will bring up the first frame of the video where you can draw rectangles around the digits you want to parse throughout the video. When you're done selecting as many digits as you'd like, press "d" and then enter. To redraw rectangles press "r" instead of "d". 

## Modules

* `image_selection.py`: Functions to present the user an image and returns retangular ROIs the user selects (specifically `getSelectionsFromImage(img)`)
* `digit_reader.py`: Functions to parse all the seven segment display digits (specified by retangular ROIs) and return the recognized igits (see `read_digits(image, roiPoints)`). 
* `seven_segment_ocr.py`: The main entry point for the program is here. Given a video path and a sample interval (in seconds), it gets ROIs from the user and parses digits out of the video at every sample interval. 
