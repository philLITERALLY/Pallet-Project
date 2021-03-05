'''This module handles the various admin controlled settings'''

import image_handling # image handling

BOARD_WIDTH = 0
BOARD_LENGTH = 1200
CAM1_BOX_COUNT = 12
CAM2_BOX_COUNT = 15
CAM1_TRANS_LEFT = 110
CAM2_TRANS_LEFT = 90
CAM1_TRANS_RIGHT = 105
CAM2_TRANS_RIGHT = 130
CAM1_BOX_POS_LR = 0
CAM2_BOX_POS_LR = 0
CAM1_BOX_POS_UD = 0
CAM2_BOX_POS_UD = 0
CAM1_THRESH = 0
CAM2_THRESH = 0
    
def set_board_width(value):
    global BOARD_WIDTH
    BOARD_WIDTH = value
    
def set_board_length(value):
    global BOARD_LENGTH, CAM1_BOX_COUNT, CAM2_BOX_COUNT
    BOARD_LENGTH = value
    
    pixelValueCam1 = value * (1533 / 1200) # using ratio of plank to pixel find value for cam 1
    pixelValueCam2 = value * (1848 / 1200) # using ratio of plank to pixel find value for cam 2

    if pixelValueCam1 < 200:
        CAM1_BOX_COUNT = 1
    elif pixelValueCam1 < 327:
        CAM1_BOX_COUNT = 2
    elif pixelValueCam1 < 454:
        CAM1_BOX_COUNT = 3
    elif pixelValueCam1 < 580:
        CAM1_BOX_COUNT = 4
    elif pixelValueCam1 < 710:
        CAM1_BOX_COUNT = 5
    elif pixelValueCam1 < 847:
        CAM1_BOX_COUNT = 6
    elif pixelValueCam1 < 974:
        CAM1_BOX_COUNT = 7
    elif pixelValueCam1 < 1105:
        CAM1_BOX_COUNT = 8
    elif pixelValueCam1 < 1232:
        CAM1_BOX_COUNT = 9
    elif pixelValueCam1 < 1360:
        CAM1_BOX_COUNT = 10
    elif pixelValueCam1 < 1492:
        CAM1_BOX_COUNT = 11
    elif pixelValueCam1 < 1543: # ??
        CAM1_BOX_COUNT = 12
    else:
        CAM1_BOX_COUNT = len(image_handling.cam1BoxThresh())

    if pixelValueCam2 < 158:
        CAM2_BOX_COUNT = 1
    elif pixelValueCam2 < 282:
        CAM2_BOX_COUNT = 2
    elif pixelValueCam2 < 408:
        CAM2_BOX_COUNT = 3
    elif pixelValueCam2 < 537:
        CAM2_BOX_COUNT = 4
    elif pixelValueCam2 < 662:
        CAM2_BOX_COUNT = 5
    elif pixelValueCam2 < 797:
        CAM2_BOX_COUNT = 6
    elif pixelValueCam2 < 929:
        CAM2_BOX_COUNT = 7
    elif pixelValueCam2 < 1058:
        CAM2_BOX_COUNT = 8
    elif pixelValueCam2 < 1190:
        CAM2_BOX_COUNT = 9
    elif pixelValueCam2 < 1320:
        CAM2_BOX_COUNT = 10
    elif pixelValueCam2 < 1451:
        CAM2_BOX_COUNT = 11
    elif pixelValueCam2 < 1580:
        CAM2_BOX_COUNT = 12
    elif pixelValueCam2 < 1709:
        CAM2_BOX_COUNT = 13
    elif pixelValueCam2 < 1838:
        CAM2_BOX_COUNT = 14
    elif pixelValueCam2 < 1920: # ??
        CAM2_BOX_COUNT = 15
    else:
        CAM2_BOX_COUNT = len(image_handling.cam2BoxThresh())

def set_cam1_trans_left(value):
    global CAM1_TRANS_LEFT
    CAM1_TRANS_LEFT += value

def set_cam2_trans_left(value):
    global CAM2_TRANS_LEFT
    CAM2_TRANS_LEFT += value

def set_cam1_trans_right(value):
    global CAM1_TRANS_RIGHT
    CAM1_TRANS_RIGHT += value

def set_cam2_trans_right(value):
    global CAM2_TRANS_RIGHT
    CAM2_TRANS_RIGHT += value

def set_cam1_box_lr(value):
    global CAM1_BOX_POS_LR
    CAM1_BOX_POS_LR += value

def set_cam2_box_lr(value):
    global CAM2_BOX_POS_LR
    CAM2_BOX_POS_LR += value

def set_cam1_box_ud(value):
    global CAM1_BOX_POS_UD
    CAM1_BOX_POS_UD += value

def set_cam2_box_ud(value):
    global CAM2_BOX_POS_UD
    CAM2_BOX_POS_UD += value

def set_cam1_thresh(value):
    global CAM1_THRESH
    CAM1_THRESH += value

def set_cam2_thresh(value):
    global CAM2_THRESH
    CAM2_THRESH += value