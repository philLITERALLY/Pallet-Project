'''This module handles the various admin controlled settings'''

import handle_config    # Programs Configuration
    
def set_board_length(value):

    handle_config.setValue('BOARD SETTINGS', 'BOARD_LENGTH', value)
    
    if value < 30 * 2:
        CAM1_BOX_COUNT = 1
    elif value < 80 * 2:
        CAM1_BOX_COUNT = 2
    elif value < 120 * 2:
        CAM1_BOX_COUNT = 3
    elif value < 170 * 2:
        CAM1_BOX_COUNT = 4
    elif value < 215 * 2:
        CAM1_BOX_COUNT = 5
    elif value < 305 * 2:
        CAM1_BOX_COUNT = 6
    elif value < 350 * 2:
        CAM1_BOX_COUNT = 7
    elif value < 395 * 2:
        CAM1_BOX_COUNT = 8
    elif value < 440 * 2:
        CAM1_BOX_COUNT = 9
    elif value < 490 * 2:
        CAM1_BOX_COUNT = 10
    elif value < 530 * 2:
        CAM1_BOX_COUNT = 11
    elif value < 580 * 2:
        CAM1_BOX_COUNT = 12
    elif value < 620 * 2:
        CAM1_BOX_COUNT = 13
    elif value < 670 * 2:
        CAM1_BOX_COUNT = 14
    elif value < 710 * 2:
        CAM1_BOX_COUNT = 15
    else:
        CAM1_BOX_COUNT = 16

    if value < 20 * 2:
        CAM2_BOX_COUNT = 1
    elif value < 65 * 2:
        CAM2_BOX_COUNT = 2
    elif value < 110 * 2:
        CAM2_BOX_COUNT = 3
    elif value < 155 * 2:
        CAM2_BOX_COUNT = 4
    elif value < 200 * 2:
        CAM2_BOX_COUNT = 5
    elif value < 245 * 2:
        CAM2_BOX_COUNT = 6
    elif value < 290 * 2:
        CAM2_BOX_COUNT = 7
    elif value < 338 * 2:
        CAM2_BOX_COUNT = 8
    elif value < 382 * 2:
        CAM2_BOX_COUNT = 9
    elif value < 430 * 2:
        CAM2_BOX_COUNT = 10
    elif value < 470 * 2:
        CAM2_BOX_COUNT = 11
    elif value < 520 * 2:
        CAM2_BOX_COUNT = 12
    elif value < 562 * 2:
        CAM2_BOX_COUNT = 13
    elif value < 610 * 2:
        CAM2_BOX_COUNT = 14
    elif value < 655 * 2: 
        CAM2_BOX_COUNT = 15
    elif value < 720 * 2: 
        CAM2_BOX_COUNT = 16
    else: 
        CAM2_BOX_COUNT = 17

    handle_config.setValue('BOARD SETTINGS', 'CAM1_BOX_COUNT', CAM1_BOX_COUNT)
    handle_config.setValue('BOARD SETTINGS', 'CAM2_BOX_COUNT', CAM2_BOX_COUNT)