'''This module handles the programs state'''

RUN_MODE = False
FAULT = False
STOP_PROGRAM = False
SHOW_TRANSFORM = False
THRESH_MODE = False
THRESH_BOX_MODE = False
CLEAR_RESULTS = False
REJECT_LIMIT = 10
TOTAL_INSPECTED = 0
TOTAL_PASSED = 0
ROTATE_STATE = 0

def set_run_mode(value):
    global RUN_MODE
    RUN_MODE = value

def set_fault(value):
    global FAULT
    FAULT = value

def stop_program():
    global STOP_PROGRAM
    STOP_PROGRAM = True

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

def clear_results():
    global TOTAL_INSPECTED, TOTAL_PASSED
    TOTAL_INSPECTED = 0
    TOTAL_PASSED = 0

def set_reject_limit(value):
    global REJECT_LIMIT
    REJECT_LIMIT = value

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