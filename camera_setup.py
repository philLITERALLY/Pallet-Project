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
      ret, frame = self.cap.read()
      if not ret:                   # capture frame error
        print('Image read error')
        break
      if np.sum(frame) == 0:        # frame empty for some reason
        continue
      if not self.q.empty():        # if queue is not empty clear it
        try:
          self.q.get_nowait()       # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    cam_path = 'another-' + str(self.camera) + '.jpg'
    img = cv2.imread(cam_path)
    return img
    # return self.q.get()

  def release(self):
      self.cap.release()