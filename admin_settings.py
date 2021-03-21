'''This module handles the various admin controlled settings'''

import image_handling # image handling

BOARD_WIDTH = 0
BOARD_LENGTH = 1200
CAM1_BOX_COUNT = 13
CAM2_BOX_COUNT = 14
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
    
    if value < 30 * 2:
        CAM1_BOX_COUNT = 1
    elif value < 80 * 2:
        CAM1_BOX_COUNT = 2
    elif value < 120 * 2:
        CAM1_BOX_COUNT = 3
    elif value < 170 * 2:
        CAM1_BOX_COUNT = 4
    elif value < 215 * 2:
        CAM1_BOX_COUNT = 5
    elif value < 305 * 2:
        CAM1_BOX_COUNT = 6
    elif value < 350 * 2:
        CAM1_BOX_COUNT = 7
    elif value < 395 * 2:
        CAM1_BOX_COUNT = 8
    elif value < 440 * 2:
        CAM1_BOX_COUNT = 9
    elif value < 490 * 2:
        CAM1_BOX_COUNT = 10
    elif value < 530 * 2:
        CAM1_BOX_COUNT = 11
    elif value < 580 * 2:
        CAM1_BOX_COUNT = 12
    elif value < 620 * 2:
        CAM1_BOX_COUNT = 13
    elif value < 670 * 2:
        CAM1_BOX_COUNT = 14
    elif value < 710 * 2:
        CAM1_BOX_COUNT = 15
    else:
        CAM1_BOX_COUNT = 16

    if value < 20 * 2:
        CAM2_BOX_COUNT = 1
    elif value < 65 * 2:
        CAM2_BOX_COUNT = 2
    elif value < 110 * 2:
        CAM2_BOX_COUNT = 3
    elif value < 155 * 2:
        CAM2_BOX_COUNT = 4
    elif value < 200 * 2:
        CAM2_BOX_COUNT = 5
    elif value < 245 * 2:
        CAM2_BOX_COUNT = 6
    elif value < 290 * 2:
        CAM2_BOX_COUNT = 7
    elif value < 338 * 2:
        CAM2_BOX_COUNT = 8
    elif value < 382 * 2:
        CAM2_BOX_COUNT = 9
    elif value < 430 * 2:
        CAM2_BOX_COUNT = 10
    elif value < 470 * 2:
        CAM2_BOX_COUNT = 11
    elif value < 520 * 2:
        CAM2_BOX_COUNT = 12
    elif value < 562 * 2:
        CAM2_BOX_COUNT = 13
    elif value < 610 * 2:
        CAM2_BOX_COUNT = 14
    elif value < 655 * 2: 
        CAM2_BOX_COUNT = 15
    elif value < 720 * 2: 
        CAM2_BOX_COUNT = 16
    else: 
        CAM2_BOX_COUNT = 17

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