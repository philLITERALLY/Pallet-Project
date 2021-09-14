from threading import Thread
import cv2
import CountsPerSec

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True

    def threadVideoGet(source=0):
        """
        Dedicated thread for grabbing video frames with VideoGet object.
        Main thread shows video frames.
        """

        video_getter = VideoGet(source).start()
        cps = CountsPerSec().start()

        while True:
            if (cv2.waitKey(1) == ord("q")) or video_getter.stopped:
                video_getter.stop()
                break

            frame = video_getter.frame
            frame = putIterationsPerSec(frame, cps.countsPerSec())
            cv2.imshow("Video", frame)
            cps.increment()