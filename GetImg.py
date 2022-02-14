import cv2
import argparse
import sys
from utils.perf import get_meter

CV_WINDOW_NAME = 'Image'

def Get_args():
    '''
    Parses arguments from the command line
    '''
    parser = argparse.ArgumentParser(description = 'Get img file & display')
    parser.add_argument( '-i', '--input', 
                        type=str, default = None,
                        help = 'Input image. Default = None')
    return parser.parse_args()

def main():
    ARGS = Get_args()
    
    # Create display window
    cv2.namedWindow(CV_WINDOW_NAME)

    overall_meter = get_meter("background")

    # while (cam.isOpened()):
    frame = cv2.imread(ARGS.input)
    prop_val = cv2.getWindowProperty(CV_WINDOW_NAME, cv2.WND_PROP_ASPECT_RATIO)
    cv2.imshow(CV_WINDOW_NAME, frame)
    while(True):
        if (prop_val < 0.0):
            print('Window closed')
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('User press quit')
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    sys.exit(main())
