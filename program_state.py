'''This module handles the programs state'''

global RUN_MODE, STOP_PROGRAM, ADMIN_USER
global CALIBRATE_MODE, THRESH_MODE, REQUEST_CALIBRATE
global CLEAR_RESULTS

RUN_MODE = False
STOP_PROGRAM = False
ADMIN_USER = False
CALIBRATE_MODE = False
THRESH_MODE = False
REQUEST_CALIBRATE = 0
CLEAR_RESULTS = False

def set_admin_user(value):
    global ADMIN_USER
    ADMIN_USER = value

def set_calibrate_mode(value):
    global CALIBRATE_MODE
    CALIBRATE_MODE = value

def set_thresh(value):
    global THRESH_MODE
    THRESH_MODE = value

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