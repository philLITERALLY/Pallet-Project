'''This module handles the programs state'''

RUN_MODE = False
FAULT = False
STOP_PROGRAM = False
LIVE_MODE = False
SHOW_TRANSFORM = False
THRESH_MODE = False
CLEAR_RESULTS = False
TOTAL_INSPECTED = 0
TOTAL_PASSED = 0

def set_run_mode(value):
    global RUN_MODE
    RUN_MODE = value

def set_fault(value):
    global FAULT
    FAULT = value

def stop_program():
    global STOP_PROGRAM
    STOP_PROGRAM = True

def set_live(value):
    global LIVE_MODE, SHOW_TRANSFORM, THRESH_MODE
    LIVE_MODE = value

    # if turning on this mode then disable others
    if value:
        SHOW_TRANSFORM = False
        THRESH_MODE = False

def set_transform(value):
    global LIVE_MODE, SHOW_TRANSFORM, THRESH_MODE
    SHOW_TRANSFORM = value

    # if turning on this mode then disable others
    if value:
        LIVE_MODE = False
        THRESH_MODE = False

def set_thresh(value):
    global LIVE_MODE, SHOW_TRANSFORM, THRESH_MODE
    THRESH_MODE = value

    # if turning on this mode then disable others
    if value:
        LIVE_MODE = False
        SHOW_TRANSFORM = False

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