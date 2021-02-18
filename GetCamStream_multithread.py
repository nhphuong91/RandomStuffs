import cv2
import argparse
import sys
from threading import Thread
from utils.perf import get_meter

CV_WINDOW_NAME = 'Camera'

class WebcamVideoStream:
    def __init__(self, name="WebcamVideoStream", ARGS=()):
        # initialize the video camera stream and read the first frame
        # from the stream
        if ARGS.MIPI:
            print("Use MIPI CSI camera: {}\n".format(ARGS.MIPI))
            self.stream = cv2.VideoCapture(ARGS.cam_source, cv2.CAP_GSTREAMER)
        elif ARGS.video:
            print("Use video: {}\n".format(ARGS.video))
            self.stream = cv2.VideoCapture(ARGS.cam_source)
        else:
            print("Use v4l2 camera")
            self.stream = cv2.VideoCapture(ARGS.cam_source, cv2.CAP_V4L2)
            self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, ARGS.cam_width)
            self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, ARGS.cam_height)

        (self.grabbed, self.frame) = self.stream.read()

        # initialize the thread name
        self.name = name

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        self.t = Thread(target=self.update, name=self.name)
        self.t.daemon = True
        self.t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while self.stream.isOpened():
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                break
            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()
        else:
            #  Something wrong with video source
            print("Cannot get video stream!")
        # Release video source
        self.stream.release()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
        self.t.join()
        
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
    args = Get_args()
    cam = WebcamVideoStream(ARGS=args)
    cam.start()

    overall_meter = get_meter("background")

    # Create display window
    cv2.namedWindow(CV_WINDOW_NAME)

    while True:
        overall_meter.begin()
        frame = cam.read()
        overall_meter.end()
        cv2.putText(frame, "(Overall Speed) {:.1f} FPS".format(overall_meter.smooth_speed()), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (38,0,255), 1, cv2.LINE_AA)
        prop_val = cv2.getWindowProperty(CV_WINDOW_NAME, cv2.WND_PROP_ASPECT_RATIO)
        if (prop_val < 0.0):
            print('Window closed')
            break
        cv2.imshow(CV_WINDOW_NAME, frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print('User press quit')
            break
    cam.stop()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    sys.exit(main())
