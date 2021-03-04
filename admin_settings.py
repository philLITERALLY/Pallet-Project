'''This module handles the various admin controlled settings'''

BOARD_WIDTH = 0
BOARD_LENGTH = 1200
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
    global BOARD_LENGTH
    BOARD_LENGTH = value

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