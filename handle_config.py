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
    global BORDERLINE_LEVEL, REJECT_LEVEL
    global SIDE1_PERC, SIDE2_PERC

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
    BORDERLINE_LEVEL = config.getint('REJECT SETTINGS', 'BORDERLINE_LEVEL')
    REJECT_LEVEL = config.getint('REJECT SETTINGS', 'REJECT_LEVEL')
    SIDE1_PERC = config.getfloat('REJECT SETTINGS', 'SIDE1_PERC')
    SIDE2_PERC = config.getfloat('REJECT SETTINGS', 'SIDE2_PERC')

    # Get Thresh Settings
    CAM_THRESH = config.getint('THRESH SETTINGS', 'CAM_THRESH')

    # Get AIO Settings
    AIO_WAIT = config.getfloat('AIO', 'AIO_WAIT')