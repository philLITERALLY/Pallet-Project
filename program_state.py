'''This module handles the programs state'''

RUN_MODE = False
SETUP_PLANK = False
DROP_PLANK = True
FAULT = False
STOP_PROGRAM = False
LIVE_MODE = False
SHOW_TRANSFORM = False
COLUMN_MODE = False
THRESH_MODE = False
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

def set_live(value):
    global LIVE_MODE, SHOW_TRANSFORM, COLUMN_MODE, THRESH_MODE
    LIVE_MODE = value

    # if turning on this mode then disable others
    if value:
        SHOW_TRANSFORM = False
        COLUMN_MODE = False
        THRESH_MODE = False

def set_transform(value):
    global LIVE_MODE, SHOW_TRANSFORM, COLUMN_MODE,  THRESH_MODE
    SHOW_TRANSFORM = value

    # if turning on this mode then disable others
    if value:
        LIVE_MODE = False
        COLUMN_MODE = False
        THRESH_MODE = False

def set_column(value):
    global LIVE_MODE, SHOW_TRANSFORM, COLUMN_MODE, THRESH_MODE
    COLUMN_MODE = value

    # if turning on this mode then disable others
    if value:
        LIVE_MODE = False
        SHOW_TRANSFORM = False
        THRESH_MODE = False

def set_thresh(value):
    global LIVE_MODE, SHOW_TRANSFORM, COLUMN_MODE, THRESH_MODE
    THRESH_MODE = value

    # if turning on this mode then disable others
    if value:
        LIVE_MODE = False
        SHOW_TRANSFORM = False
        COLUMN_MODE = False

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