'''This module handles the various admin controlled settings'''

import handle_config    # Programs Configuration
    
def set_board_length(value):
    handle_config.setValue('BOARD SETTINGS', 'BOARD_LENGTH', value)

def set_side1_box_lr(value):
    handle_config.setValue('BOARD SETTINGS', 'SIDE1_LEFT', handle_config.SIDE1_LEFT + value)

def set_side1_box_ud(value):
    handle_config.setValue('BOARD SETTINGS', 'SIDE1_TOP', handle_config.SIDE1_TOP + value)

def set_side2_box_lr(value):
    handle_config.setValue('BOARD SETTINGS', 'SIDE2_LEFT', handle_config.SIDE2_LEFT + value)

def set_side2_box_ud(value):
    handle_config.setValue('BOARD SETTINGS', 'SIDE2_TOP', handle_config.SIDE2_TOP + value)