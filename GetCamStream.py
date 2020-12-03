import cv2
import argparse
import sys

CV_WINDOW_NAME = 'Camera'

def Get_args():
    '''
    Parses arguments from the command line
    '''
    parser = argparse.ArgumentParser(description = 'Get video from camera source')
    parser.add_argument( '--cam_width', metavar = 'cam resolution width',
                        type=int, default = 640,
                        help = 'Camera capture resolution width. default=640')
    parser.add_argument( '--cam_height', metavar = 'cam resolution height',
                        type=int, default = 480,
                        help = 'Camera capture resolution height. default=480')
    parser.add_argument( '-s', '--cam_source', metavar = 'Cam source v4linux or MIPI CSI',
                        type=str, default = '/dev/video0',
                        help = 'Camera source. Default = /dev/video0')
    parser.add_argument('-m', '--use-MIPI', 
                        dest='MIPI', action='store_true', default=False, 
                        help='Iput source is MIPI CSI. Default = False')
    parser.add_argument('-v', '--use-video', 
                        dest='video', action='store_true', default=False, 
                        help='Iput source is video. Default = False')
    return parser.parse_args()

def main():
    ARGS = Get_args()
    if ARGS.MIPI:
        print("Use MIPI CSI camera: {}\n".format(ARGS.MIPI))
        cam = cv2.VideoCapture(ARGS.cam_source, cv2.CAP_GSTREAMER)
    elif ARGS.video:
        print("Use video: {}\n".format(ARGS.video))
        cam = cv2.VideoCapture(ARGS.cam_source)
    else:
        print("Use v4l2 camera")
        cam = cv2.VideoCapture(ARGS.cam_source, cv2.CAP_V4L2)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, ARGS.cam_width)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, ARGS.cam_height)
    
    # Create display window
    cv2.namedWindow(CV_WINDOW_NAME)

    while (cam.isOpened()):
        ret_val, frame = cam.read()
        if (not ret_val):
            print("No image from camera, exiting...")
            break
        prop_val = cv2.getWindowProperty(CV_WINDOW_NAME, cv2.WND_PROP_ASPECT_RATIO)
        if (prop_val < 0.0):
            print('Window closed')
            break
        cv2.imshow(CV_WINDOW_NAME, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('User press quit')
            break
    else:
        print("Cannot get cam stream!")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    sys.exit(main())
