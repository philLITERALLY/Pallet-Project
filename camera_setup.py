'''This module sets up the cameras'''

# External Libraries
import cv2      # OpenCV
import time     # time

# My Modules
import info_logger

def main(camera):
    '''Initialise and apply camera settings'''
    capture = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
    capture.set(3, 3840)                # CAM WIDTH
    capture.set(4, 2160)                # CAM HEIGHT
    # capture.set(5, handle_config.CAM_FPS)
    # time.sleep(5)
    # capture.set(15, handle_config.CAM_EXPOSURE)

    info_logger.camera_settings(camera, capture)

    return capture