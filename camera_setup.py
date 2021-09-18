'''This module sets up the cameras'''

# External Libraries
import cv2
import queue
import threading
import time
import numpy as np
from datetime import datetime

# My Modules
import info_logger
import handle_config

# bufferless VideoCapture
class VideoCapture:
  def __init__(self, camera):
    self.needImg = False
    self.camera = camera
    print('Start Cam: ', self.camera, datetime.now().time())
    self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)
    
    self.cap.set(3, handle_config.CAM_WIDTH)                # CAM WIDTH
    self.cap.set(4, handle_config.CAM_HEIGHT)               # CAM HEIGHT
    # self.cap.set(5, handle_config.CAM_FPS)
    time.sleep(5)
    self.cap.set(15, handle_config.CAM_EXPOSURE)                 # CAM EXPOSURE


    for x in range(10):                 # WARM UP CAM BY GRABBING 10 IMAGES...
      _, self.frame = self.cap.read()

    info_logger.camera_settings(self.camera, self.cap)

    self.run = True
    self.t = threading.Thread(target=self._reader)
    self.t.daemon = True
    self.t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while self.run:
      ret, frame = self.cap.read()
      if not ret:                   # capture frame error
        print('RET error: ', self.camera, datetime.now().time())

        print('Releasing Camera...')
        self.cap.release()
        print('Setting up Camera...')
        self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)

        self.cap.set(3, handle_config.CAM_WIDTH)                # CAM WIDTH
        self.cap.set(4, handle_config.CAM_HEIGHT)               # CAM HEIGHT
        # self.cap.set(5, handle_config.CAM_FPS)
        time.sleep(5)
        self.cap.set(15, handle_config.CAM_EXPOSURE)                 # CAM EXPOSURE

        for x in range(10):                 # WARM UP CAM BY GRABBING 10 IMAGES...
          _, self.frame = self.cap.read()

        info_logger.camera_settings(self.camera, self.cap)
        print('Camera Reset...?')

        continue
      if np.sum(frame) == 0:        # frame empty for some reason
        print('Empty Frame error: ', self.camera, datetime.now().time())

        print('Releasing Camera...')
        self.cap.release()
        print('Setting up Camera...')
        self.cap = cv2.VideoCapture(self.camera, cv2.CAP_DSHOW)

        self.cap.set(3, handle_config.CAM_WIDTH)                # CAM WIDTH
        self.cap.set(4, handle_config.CAM_HEIGHT)               # CAM HEIGHT
        # self.cap.set(5, handle_config.CAM_FPS)
        time.sleep(5)
        self.cap.set(15, handle_config.CAM_EXPOSURE)                 # CAM EXPOSURE

        for x in range(10):                 # WARM UP CAM BY GRABBING 10 IMAGES...
          _, self.frame = self.cap.read()

        info_logger.camera_settings(self.camera, self.cap)
        print('Camera Reset...?')

        continue

      dim = (3840, 2160)
      resized = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
      self.frame = resized
      self.needImg = False

  def read(self):
    self.needImg = True 

    while self.needImg and self.run:
      continue

    return self.frame

  def release(self):
    self.run = False
    self.t.join()
    self.cap.release()

class StaticImage:
    def __init__(self, camera):
      self.camera = camera
      self.number = 0

    def read(self):
      if self.camera == 0:
        if self.number == 0:
          self.image = cv2.imread("images/workflow test/cam1/b1.png")
          self.number = 1
        elif self.number == 1:
          self.image = cv2.imread("images/workflow test/cam1/b2.png")
          self.number = 2
        elif self.number == 2:
          self.image = cv2.imread("images/workflow test/cam1/b3.png")
          self.number = 3
        else:
          self.image = cv2.imread("images/workflow test/cam1/b4.png")
          self.number = 0
      else:
        if self.number == 0:
          self.image = cv2.imread("images/workflow test/cam2/b1.png")
          self.number = 1
        elif self.number == 1:
          self.image = cv2.imread("images/workflow test/cam2/b2.png")
          self.number = 2
        elif self.number == 2:
          self.image = cv2.imread("images/workflow test/cam2/b3.png")
          self.number = 3
        else:
          self.image = cv2.imread("images/workflow test/cam2/b4.png")
          self.number = 0

      return self.image

    def release(self):
      self.image = None