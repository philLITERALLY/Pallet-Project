'''This module sets up the cameras'''

# External Libraries
import cv2
import queue
import threading
import time
import numpy as np

# My Modules
import info_logger

# bufferless VideoCapture
class VideoCapture:
  def __init__(self, camera):
    self.camera = camera
    self.cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
    self.cap.set(3, 3840)                # CAM WIDTH
    self.cap.set(4, 2160)                # CAM HEIGHT
    # self.cap.set(5, handle_config.CAM_FPS)
    time.sleep(5)
    self.cap.set(15, -3)                 # CAM EXPOSURE

    for x in range(10):                 # WARM UP CAM BY GRABBING 10 IMAGES...
        _, _ = self.cap.read()

    info_logger.camera_settings(camera, self.cap)

    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      _, _ = self.cap.read()

  def read(self):
    _, frame = self.cap.read()
    
    while np.sum(frame) == 0:
      _, frame = self.cap.read()

    return frame

  def release(self):
      self.cap.release()