from configparser import ConfigParser
import ast
import os

my_path = os.path.abspath(os.path.dirname(__file__))

def getArray(config, section, variable):
    return ast.literal_eval(config.get(section, variable))

def setValue(section, variable, value):
    config.set(section, variable, str(value))              # Set new value
    with open(my_path + '/config.ini', 'w') as configfile: # Save new value
        config.write(configfile)    
    globals()[variable] = value                            # update global variable to new value

def init():
    # Config File
    global config

    # Setup Delay settings
    global START_DELAY, WAIT_GRAB, AFTER_GRAB, JAM_DELAY

    # Setup Camera Settings
    global CAM_WIDTH, CAM_HEIGHT, CAM_EXPOSURE
    global FRAME_WIDTH

    # Board settings
    global BOARD_WIDTH, BOARD_LENGTH
    global SIDE1_TOP, SIDE1_LEFT, SIDE1_HEIGHT, SIDE1_WIDTH
    global SIDE2_TOP, SIDE2_LEFT, SIDE2_HEIGHT, SIDE2_WIDTH

    # Rejection settings
    global REJECT_LEVEL, EDGE_VARIANCE, MID_SIZE
    global SIDE1_PERC, SIDE1A_PERC, SIDE1B_PERC, SIDE1C_PERC
    global SIDE2_PERC, SIDE2A_PERC, SIDE2B_PERC, SIDE2C_PERC

    # Thresh settings
    global CAM_THRESH

    # AIO Settings
    global AIO_WAIT

    # Load config file
    config = ConfigParser()
    config.read(my_path + '/config.ini')

    # Get Delay Settings
    START_DELAY = config.getfloat('DELAY', 'START_DELAY')
    WAIT_GRAB = config.getfloat('DELAY', 'WAIT_GRAB')
    AFTER_GRAB = config.getfloat('DELAY', 'AFTER_GRAB')
    JAM_DELAY = config.getfloat('DELAY', 'JAM_DELAY')

    # Get Camera Settings
    CAM_WIDTH = config.getint('CAMERA', 'CAM_WIDTH')
    CAM_HEIGHT = config.getint('CAMERA', 'CAM_HEIGHT')
    CAM_EXPOSURE = config.getint('CAMERA', 'CAM_EXPOSURE')
    FRAME_WIDTH = config.getint('CAMERA', 'FRAME_WIDTH')

    # Get Board Settings
    BOARD_WIDTH = config.getint('BOARD SETTINGS', 'BOARD_WIDTH')
    BOARD_LENGTH = config.getint('BOARD SETTINGS', 'BOARD_LENGTH')
    SIDE1_TOP = config.getint('BOARD SETTINGS', 'SIDE1_TOP')
    SIDE1_LEFT = config.getint('BOARD SETTINGS', 'SIDE1_LEFT')
    SIDE1_HEIGHT = config.getint('BOARD SETTINGS', 'SIDE1_HEIGHT')
    SIDE1_WIDTH = config.getint('BOARD SETTINGS', 'SIDE1_WIDTH')
    SIDE2_TOP = config.getint('BOARD SETTINGS', 'SIDE2_TOP')
    SIDE2_LEFT = config.getint('BOARD SETTINGS', 'SIDE2_LEFT')
    SIDE2_HEIGHT = config.getint('BOARD SETTINGS', 'SIDE2_HEIGHT')
    SIDE2_WIDTH = config.getint('BOARD SETTINGS', 'SIDE2_WIDTH')

    # Get Rejection Settings
    REJECT_LEVEL = config.getint('REJECT SETTINGS', 'REJECT_LEVEL')
    EDGE_VARIANCE = config.getint('REJECT SETTINGS', 'EDGE_VARIANCE')
    MID_SIZE = config.getint('REJECT SETTINGS', 'MID_SIZE')

    # Get Percentage Ratios
    SIDE1_PERC = config.getfloat('REJECT SETTINGS', 'SIDE1_PERC')
    SIDE1A_PERC = config.getfloat('REJECT SETTINGS', 'SIDE1A_PERC')
    SIDE1B_PERC = config.getfloat('REJECT SETTINGS', 'SIDE1B_PERC')
    SIDE1C_PERC = config.getfloat('REJECT SETTINGS', 'SIDE1C_PERC')
    SIDE2_PERC = config.getfloat('REJECT SETTINGS', 'SIDE2_PERC')
    SIDE2A_PERC = config.getfloat('REJECT SETTINGS', 'SIDE2A_PERC')
    SIDE2B_PERC = config.getfloat('REJECT SETTINGS', 'SIDE2B_PERC')
    SIDE2C_PERC = config.getfloat('REJECT SETTINGS', 'SIDE2C_PERC')

    # Get Thresh Settings
    CAM_THRESH = config.getint('THRESH SETTINGS', 'CAM_THRESH')

    # Get AIO Settings
    AIO_WAIT = config.getfloat('AIO', 'AIO_WAIT')