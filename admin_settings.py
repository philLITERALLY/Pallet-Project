'''This module handles the various admin controlled settings'''

import handle_config    # Programs Configuration
    
def set_board_length(value):
    handle_config.setValue('BOARD SETTINGS', 'BOARD_LENGTH', value)