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

    # Setup Camera Settings
    global CAM_WIDTH, CAM_HEIGHT, CAM_EXPOSURE
    global FRAME_WIDTH, WAIT_GRAB, AFTER_GRAB

    # Board settings
    global BOARD_WIDTH, BOARD_LENGTH
    global CAM1_BOX_COUNT, CAM2_BOX_COUNT

    # Rejection settings
    global REJECT_LEVEL

    # Transform settings
    global CAM1_TRANS_LEFT, CAM1_TRANS_RIGHT, CAM2_TRANS_LEFT, CAM2_TRANS_RIGHT

    # Thresh settings
    global CAM1_THRESH, CAM2_THRESH

    # Box positioning
    global SIDE1_VERT, SIDE2_VERT

    # AIO Settings
    global AIO_WAIT

    # Load config file
    config = ConfigParser()
    config.read(my_path + '/config.ini')

    # Get Camera Settings
    CAM_WIDTH = config.getint('CAMERA', 'CAM_WIDTH')
    CAM_HEIGHT = config.getint('CAMERA', 'CAM_HEIGHT')
    CAM_EXPOSURE = config.getint('CAMERA', 'CAM_EXPOSURE')
    FRAME_WIDTH = config.getint('CAMERA', 'FRAME_WIDTH')
    WAIT_GRAB = config.getfloat('CAMERA', 'WAIT_GRAB')
    AFTER_GRAB = config.getfloat('CAMERA', 'AFTER_GRAB')

    # Get Board Settings
    BOARD_WIDTH = config.getint('BOARD SETTINGS', 'BOARD_WIDTH')
    BOARD_LENGTH = config.getint('BOARD SETTINGS', 'BOARD_LENGTH')
    CAM1_BOX_COUNT = config.getint('BOARD SETTINGS', 'CAM1_BOX_COUNT')
    CAM2_BOX_COUNT = config.getint('BOARD SETTINGS', 'CAM2_BOX_COUNT')

    # Get Rejection Settings
    REJECT_LEVEL = config.getint('REJECT SETTINGS', 'REJECT_LEVEL')

    # Get Transform Settings
    CAM1_TRANS_LEFT = config.getint('TRANSFORM SETTINGS', 'CAM1_TRANS_LEFT')
    CAM1_TRANS_RIGHT = config.getint('TRANSFORM SETTINGS', 'CAM1_TRANS_RIGHT')
    CAM2_TRANS_LEFT = config.getint('TRANSFORM SETTINGS', 'CAM2_TRANS_LEFT')
    CAM2_TRANS_RIGHT = config.getint('TRANSFORM SETTINGS', 'CAM2_TRANS_RIGHT')

    # Get Thresh Settings
    CAM1_THRESH = config.getint('THRESH SETTINGS', 'CAM1_THRESH')
    CAM2_THRESH = config.getint('THRESH SETTINGS', 'CAM2_THRESH')

    # Get box positioning
    SIDE1_VERT = config.getint('BOX POSITIONING', 'SIDE1_VERT')
    SIDE2_VERT = config.getint('BOX POSITIONING', 'SIDE2_VERT')

    # Get side 1 cam 1 box positions
    for box in range(16):                                                   # VARIABLE?!
        leftPos = 'SIDE1_CAM1_BOX' + str(box) + '_LEFT'
        rightPos = 'SIDE1_CAM1_BOX' + str(box) + '_RIGHT'
        globals()[leftPos] = config.getint('BOX POSITIONING', leftPos)
        globals()[rightPos] = config.getint('BOX POSITIONING', rightPos)

    # Get side 1 cam 2 box positions
    for box in range(17):                                                   # VARIABLE?!
        leftPos = 'SIDE1_CAM2_BOX' + str(box) + '_LEFT'
        rightPos = 'SIDE1_CAM2_BOX' + str(box) + '_RIGHT'
        globals()[leftPos] = config.getint('BOX POSITIONING', leftPos)
        globals()[rightPos] = config.getint('BOX POSITIONING', rightPos)

    # Get side 2 cam 1 box positions
    for box in range(16):                                                   # VARIABLE?!
        leftPos = 'SIDE2_CAM1_BOX' + str(box) + '_LEFT'
        rightPos = 'SIDE2_CAM1_BOX' + str(box) + '_RIGHT'
        globals()[leftPos] = config.getint('BOX POSITIONING', leftPos)
        globals()[rightPos] = config.getint('BOX POSITIONING', rightPos)

    # Get side 2 cam 2 box positions
    for box in range(17):                                                   # VARIABLE?!
        leftPos = 'SIDE2_CAM2_BOX' + str(box) + '_LEFT'
        rightPos = 'SIDE2_CAM2_BOX' + str(box) + '_RIGHT'
        globals()[leftPos] = config.getint('BOX POSITIONING', leftPos)
        globals()[rightPos] = config.getint('BOX POSITIONING', rightPos)

    # Get AIO Settings
    AIO_WAIT = config.getfloat('AIO', 'AIO_WAIT')