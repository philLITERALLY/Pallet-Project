'''This module handles the programs state'''

RUN_MODE = False
SETUP_PLANK = False
DROP_PLANK = True
FAULT = False
STOP_PROGRAM = False
SHOW_TRANSFORM = False
THRESH_MODE = False
THRESH_BOX_1_MODE = False
THRESH_BOX_2_MODE = False
BOX_MODIFY = 0
CAM1_BOX_MODIFY = None
CAM2_BOX_MODIFY = None
CLEAR_RESULTS = False
TOTAL_INSPECTED = 0
TOTAL_PASSED = 0
ROTATE_STATE = 0
SIDE_STATE = 1

def set_run_mode(value):
    global RUN_MODE
    RUN_MODE = value

def setup_plank(value):
    global SETUP_PLANK
    SETUP_PLANK = value

def drop_plank(value):
    global DROP_PLANK
    DROP_PLANK = value

def set_fault(value):
    global FAULT
    FAULT = value

def stop_program():
    global STOP_PROGRAM
    STOP_PROGRAM = True

def set_transform(value):
    global SHOW_TRANSFORM, THRESH_BOX_1_MODE, THRESH_MODE, THRESH_BOX_2_MODE
    SHOW_TRANSFORM = value

    # if turning on this mode then disable others
    if value:
        THRESH_BOX_1_MODE = False
        THRESH_BOX_2_MODE = False
        THRESH_MODE = False

def set_thresh(value):
    global SHOW_TRANSFORM, THRESH_BOX_1_MODE, THRESH_BOX_2_MODE, THRESH_MODE
    THRESH_MODE = value

    # if turning on this mode then disable others
    if value:
        SHOW_TRANSFORM = False
        THRESH_BOX_1_MODE = False
        THRESH_BOX_2_MODE = False

def set_thresh_boxes_1(value):
    global SHOW_TRANSFORM, THRESH_BOX_1_MODE, THRESH_BOX_2_MODE, THRESH_MODE, SIDE_STATE
    THRESH_BOX_1_MODE = value
    SIDE_STATE = 1

    admin_box_change(0)

    # if turning on this mode then disable others
    if value:
        SHOW_TRANSFORM = False
        THRESH_MODE = False
        THRESH_BOX_2_MODE = False

def set_thresh_boxes_2(value):
    global SHOW_TRANSFORM, THRESH_BOX_1_MODE, THRESH_BOX_2_MODE, THRESH_MODE, SIDE_STATE
    THRESH_BOX_2_MODE = value
    SIDE_STATE = 2
    
    admin_box_change(0)

    # if turning on this mode then disable others
    if value:
        SHOW_TRANSFORM = False
        THRESH_MODE = False
        THRESH_BOX_1_MODE = False

def clear_results():
    global TOTAL_INSPECTED, TOTAL_PASSED
    TOTAL_INSPECTED = 0
    TOTAL_PASSED = 0

def increase_total_inspected():
    global TOTAL_INSPECTED
    TOTAL_INSPECTED += 1

def increase_total_passed():
    global TOTAL_PASSED
    TOTAL_PASSED += 1

def toggle_rotate_state():
    global ROTATE_STATE
    
    if ROTATE_STATE == 1:
        ROTATE_STATE = 0
    else:
        ROTATE_STATE = 1

def admin_box_change(value):
    global BOX_MODIFY, CAM1_BOX_MODIFY, CAM2_BOX_MODIFY

    possible1Boxes = 15 # CHANGE TO BE Variable ?!
    possible2Boxes = 16 # CHANGE TO BE Variable ?!

    if value < 0 or value > possible1Boxes + possible2Boxes + 1:
        return

    BOX_MODIFY = value

    if value <= possible1Boxes:
        CAM1_BOX_MODIFY = value
        CAM2_BOX_MODIFY = None
    else:
        CAM1_BOX_MODIFY = None
        CAM2_BOX_MODIFY = value - possible1Boxes - 1