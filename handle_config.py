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

    # Rejection settings
    global EDGE_FLIP_LEVEL, EDGE_REJECT_LEVEL, MID_REJECT_LEVEL

    # Thresh settings
    global CAM1_THRESH, CAM2_THRESH

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

    # Get Rejection Settings
    EDGE_FLIP_LEVEL = config.getint('REJECT SETTINGS', 'EDGE_FLIP_LEVEL')
    EDGE_REJECT_LEVEL = config.getint('REJECT SETTINGS', 'EDGE_REJECT_LEVEL')
    MID_REJECT_LEVEL = config.getint('REJECT SETTINGS', 'MID_REJECT_LEVEL')

    # Get Thresh Settings
    CAM1_THRESH = config.getint('THRESH SETTINGS', 'CAM1_THRESH')
    CAM2_THRESH = config.getint('THRESH SETTINGS', 'CAM2_THRESH')

    # Get AIO Settings
    AIO_WAIT = config.getfloat('AIO', 'AIO_WAIT')