
import PySimpleGUI as sg

# my modules
import program_state    # Programs State
import admin_settings   # Admin settings
import handle_config    # Programs Configuration

def updateBoxDetailsText(window, side):
    # Figure out what CAM and BOX we're on
    cam = 1
    box = program_state.CAM1_BOX_MODIFY
    if program_state.CAM2_BOX_MODIFY != None:
        cam = 2
        box = program_state.CAM2_BOX_MODIFY

    # Get boxes details
    leftPos = getattr(handle_config, 'SIDE' + str(side) + '_CAM' + str(cam) + '_BOX' + str(box) + '_LEFT')
    rightPos = getattr(handle_config, 'SIDE' + str(side) + '_CAM' + str(cam) + '_BOX' + str(box) + '_RIGHT')

    # Update text for what width of box we're modifying
    window.FindElement('-SIDE' + str(side) + '-BOX-WIDTH-').Update(str(rightPos - leftPos))

    # Update text for what start position of box we're modifying
    window.FindElement('-SIDE' + str(side) + '-BOX-POS-').Update(str(leftPos))

def admin(event, window):
    window.FindElement('-LIVE-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-TRANSFORM-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-BARK-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-CAM1-TRANSFORM-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM2-TRANSFORM-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM1-THRESH-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM2-THRESH-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE1-VERTICAL-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE2-VERTICAL-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE1-BOX-SELECT-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE2-BOX-SELECT-LAYOUT-').Update(visible=False)
    window.FindElement('-BOX-POS-TEXT-').Update(visible=False)
    window.FindElement('-IO-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE1-BOXES-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE2-BOXES-LAYOUT-').Update(visible=False)
    window.FindElement('-ADMIN-BOX1-TEXT-').Update('CAM 1')
    window.FindElement('-ADMIN-BOX2-TEXT-').Update('CAM 2')
        
    # When the setup button is pressed
    if event == '-SETUP-':
        # change to admin view
        window.FindElement('-VIEW-LAYOUT-').Update(visible=False)
        window.FindElement('-ADMIN-LAYOUT-').Update(visible=True)
        
        # default state to live mode
        program_state.set_live(True)

        # turn transform button on
        window.FindElement('-LIVE-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-TRANSFORM-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-TRANSFORM-LAYOUT-').Update(visible=True)
        window.FindElement('-IO-LAYOUT-').Update(visible=True)
        
    # When the cancel button is pressed
    if event == '-CANCEL-':
        window.FindElement('-VIEW-LAYOUT-').Update(visible=True)
        window.FindElement('-ADMIN-LAYOUT-').Update(visible=False)
        
        # make sure admin modes are off
        program_state.set_live(False)
        program_state.set_thresh(False)
        program_state.set_transform(False)

    # When live mode button is pressed
    if event == '-LIVE-MODE-':
        program_state.set_live(True)     # turn on live view mode

        # turn live button on
        window.FindElement('-LIVE-MODE-').Update(button_color=('black', 'yellow'))

    # When transform mode button is pressed
    if event == '-TRANSFORM-MODE-':
        program_state.set_transform(True)     # turn on transform view mode

        # turn transform button on
        window.FindElement('-TRANSFORM-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-TRANSFORM-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-TRANSFORM-LAYOUT-').Update(visible=True)
        window.FindElement('-IO-LAYOUT-').Update(visible=True)

    # When bark thresh mode button is pressed
    if event == '-BARK-MODE-':
        program_state.set_thresh(True)       # turn on box thresh mode

        # turn thresh button on
        window.FindElement('-BARK-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-THRESH-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-THRESH-LAYOUT-').Update(visible=True)
        window.FindElement('-IO-LAYOUT-').Update(visible=True)

def board(event, window):
    if event == '-WIDTH-70-': # 70
        handle_config.setValue('BOARD SETTINGS', 'BOARD_WIDTH', -52)
        window.FindElement('-WIDTH-70-').Update(button_color=('black', 'yellow'))

        window.FindElement('-WIDTH-96-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-120-').Update(button_color=sg.theme_button_color())
    
    if event == '-WIDTH-96-':
        handle_config.setValue('BOARD SETTINGS', 'BOARD_WIDTH', 0)
        window.FindElement('-WIDTH-96-').Update(button_color=('black', 'yellow'))
        
        window.FindElement('-WIDTH-70-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-120-').Update(button_color=sg.theme_button_color())
    
    if event == '-WIDTH-120-':
        handle_config.setValue('BOARD SETTINGS', 'BOARD_WIDTH', 47)
        window.FindElement('-WIDTH-120-').Update(button_color=('black', 'yellow'))
        
        window.FindElement('-WIDTH-70-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-96-').Update(button_color=sg.theme_button_color())

    if event == '-LENGTH--':
        newLength = handle_config.BOARD_LENGTH - 10
        admin_settings.set_board_length(newLength)
        window.FindElement('-BOARD-LENGTH-').update(str(newLength))

    if event == '-LENGTH+-':
        newLength = handle_config.BOARD_LENGTH + 10
        admin_settings.set_board_length(newLength)
        window.FindElement('-BOARD-LENGTH-').update(str(newLength))

def transform(event, window):
    if event == '-CAM1-TOP--':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM1_TRANS_RIGHT', handle_config.CAM1_TRANS_RIGHT + 2)

    if event == '-CAM1-TOP+-':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM1_TRANS_RIGHT', handle_config.CAM1_TRANS_RIGHT - 2)

    if event == '-CAM1-BOT--':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM1_TRANS_LEFT', handle_config.CAM1_TRANS_LEFT - 2)

    if event == '-CAM1-BOT+-':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM1_TRANS_LEFT', handle_config.CAM1_TRANS_LEFT + 2)

    if event == '-CAM2-TOP--':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM2_TRANS_LEFT', handle_config.CAM2_TRANS_LEFT + 2)

    if event == '-CAM2-TOP+-':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM2_TRANS_LEFT', handle_config.CAM2_TRANS_LEFT - 2)

    if event == '-CAM2-BOT--':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM2_TRANS_RIGHT', handle_config.CAM2_TRANS_RIGHT - 2)

    if event == '-CAM2-BOT+-':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM2_TRANS_RIGHT', handle_config.CAM2_TRANS_RIGHT + 2)

    window.FindElement('-CAM1-TOP-').update(str(handle_config.CAM1_TRANS_RIGHT))
    window.FindElement('-CAM1-BOT-').update(str(handle_config.CAM1_TRANS_LEFT))
    window.FindElement('-CAM2-TOP-').update(str(handle_config.CAM2_TRANS_LEFT))
    window.FindElement('-CAM2-BOT-').update(str(handle_config.CAM2_TRANS_RIGHT))

def thresh(event, window):
    if event == '-CAM1-THRESH--':
        handle_config.setValue('THRESH SETTINGS', 'CAM1_THRESH', handle_config.CAM1_THRESH - 5)

    if event == '-CAM1-THRESH+-':
        handle_config.setValue('THRESH SETTINGS', 'CAM1_THRESH', handle_config.CAM1_THRESH + 5)

    if event == '-CAM2-THRESH--':
        handle_config.setValue('THRESH SETTINGS', 'CAM2_THRESH', handle_config.CAM2_THRESH - 5)

    if event == '-CAM2-THRESH+-':
        handle_config.setValue('THRESH SETTINGS', 'CAM2_THRESH', handle_config.CAM2_THRESH + 5)
    
    window.FindElement('-CAM1-THRESH-').update(str(handle_config.CAM1_THRESH))
    window.FindElement('-CAM2-THRESH-').update(str(handle_config.CAM2_THRESH))