'''This module handles the programs state'''

global RUN_MODE, STOP_PROGRAM, ADMIN_USER
global CALIBRATE_MODE, THRESH_MODE, THRESH_BOX_MODE
global REQUEST_CALIBRATE
global CLEAR_RESULTS

RUN_MODE = False
STOP_PROGRAM = False
ADMIN_USER = False
CALIBRATE_MODE = False
SHOW_TRANSFORM = False
THRESH_MODE = False
THRESH_BOX_MODE = False
REQUEST_CALIBRATE = 0
CLEAR_RESULTS = False

def set_admin_user(value):
    global ADMIN_USER
    ADMIN_USER = value

def set_calibrate_mode(value):
    global CALIBRATE_MODE
    CALIBRATE_MODE = value

def set_transform(value):
    global SHOW_TRANSFORM, THRESH_BOX_MODE, THRESH_MODE
    SHOW_TRANSFORM = value

    # if turning on this mode then disable others
    if value:
        THRESH_BOX_MODE = False
        THRESH_MODE = False

def set_thresh_boxes(value):
    global SHOW_TRANSFORM, THRESH_BOX_MODE, THRESH_MODE
    THRESH_BOX_MODE = value

    # if turning on this mode then disable others
    if value:
        SHOW_TRANSFORM = False
        THRESH_MODE = False

def set_thresh(value):
    global SHOW_TRANSFORM, THRESH_BOX_MODE, THRESH_MODE
    THRESH_MODE = value

    # if turning on this mode then disable others
    if value:
        SHOW_TRANSFORM = False
        THRESH_BOX_MODE = False

def request_calibration(value):
    global REQUEST_CALIBRATE
    REQUEST_CALIBRATE = value

def set_run_mode(value):
    global RUN_MODE
    RUN_MODE = value

def stop_program():
    global STOP_PROGRAM
    STOP_PROGRAM = True

def clear_results():
    global CLEAR_RESULTS
    CLEAR_RESULTS = True

def results_cleared():
    global CLEAR_RESULTS
    CLEAR_RESULTS = False



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