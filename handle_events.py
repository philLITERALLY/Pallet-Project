
import PySimpleGUI as sg

# my modules
import program_state    # Programs State
import admin_settings   # Admin settings
import handle_config    # Programs Configuration

def admin(event, window):
    window.FindElement('-TRANSFORM-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-BOXES-1-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-BOXES-2-MODE-').Update(button_color=sg.theme_button_color())
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
    window.FindElement('-SIDE1-BOXES-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE2-BOXES-LAYOUT-').Update(visible=False)
    window.FindElement('-ADMIN-BOX1-TEXT-').Update('CAM 1')
    window.FindElement('-ADMIN-BOX2-TEXT-').Update('CAM 2')
    
    # When the setup button is pressed
    if event == '-SETUP-':
        # change to admin view
        window.FindElement('-VIEW-LAYOUT-').Update(visible=False)
        window.FindElement('-ADMIN-LAYOUT-').Update(visible=True)
        
        # default state to transform mode
        program_state.set_transform(True)

        # turn transform button on
        window.FindElement('-TRANSFORM-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-TRANSFORM-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-TRANSFORM-LAYOUT-').Update(visible=True)
        
    # When the cancel button is pressed
    if event == '-CANCEL-':
        window.FindElement('-VIEW-LAYOUT-').Update(visible=True)
        window.FindElement('-ADMIN-LAYOUT-').Update(visible=False)
        
        # make sure admin modes are off
        program_state.set_thresh_boxes_1(False)
        program_state.set_thresh(False)
        program_state.set_thresh_boxes_2(False)
        program_state.set_transform(False)

    # When transform mode button is pressed
    if event == '-TRANSFORM-MODE-':
        program_state.set_transform(True)     # turn on transform view mode

        # turn transform button on
        window.FindElement('-TRANSFORM-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-TRANSFORM-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-TRANSFORM-LAYOUT-').Update(visible=True)

    # When bark thresh mode button is pressed
    if event == '-BARK-MODE-':
        program_state.set_thresh(True)       # turn on box thresh mode

        # turn thresh button on
        window.FindElement('-BARK-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-THRESH-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-THRESH-LAYOUT-').Update(visible=True)

    # When boxes mode button is pressed
    if event == '-BOXES-1-MODE-':
        program_state.set_thresh_boxes_1(True)  # turn on boxes mode

        # turn boxes button on
        window.FindElement('-BOXES-1-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-ADMIN-BOX1-TEXT-').Update('ALL BOXES')
        window.FindElement('-ADMIN-BOX2-TEXT-').Update('SELECT BOX')
        window.FindElement('-SIDE1-VERTICAL-LAYOUT-').Update(visible=True)
        window.FindElement('-SIDE1-BOX-SELECT-LAYOUT-').Update(visible=True)
        window.FindElement('-SIDE1-BOXES-LAYOUT-').Update(visible=True)
        window.FindElement('-BOX-POS-TEXT-').Update(visible=True)

    # When boxes 2 mode button is pressed
    if event == '-BOXES-2-MODE-':
        program_state.set_thresh_boxes_2(True)       # turn on line thresh mode

        # turn thresh button on
        window.FindElement('-BOXES-2-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-ADMIN-BOX1-TEXT-').Update('ALL BOXES')
        window.FindElement('-ADMIN-BOX2-TEXT-').Update('SELECT BOX')
        window.FindElement('-SIDE2-VERTICAL-LAYOUT-').Update(visible=True)
        window.FindElement('-SIDE2-BOX-SELECT-LAYOUT-').Update(visible=True)
        window.FindElement('-SIDE2-BOXES-LAYOUT-').Update(visible=True)
        window.FindElement('-BOX-POS-TEXT-').Update(visible=True)

def board(event, window):
    if event == '-WIDTH-70-': # 70
        admin_settings.set_board_width(-52)
        window.FindElement('-WIDTH-70-').Update(button_color=('black', 'yellow'))

        window.FindElement('-WIDTH-96-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-120-').Update(button_color=sg.theme_button_color())
    
    if event == '-WIDTH-96-':
        admin_settings.set_board_width(0) # 0 is neutral
        window.FindElement('-WIDTH-96-').Update(button_color=('black', 'yellow'))
        
        window.FindElement('-WIDTH-70-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-120-').Update(button_color=sg.theme_button_color())
    
    if event == '-WIDTH-120-':
        admin_settings.set_board_width(47)
        window.FindElement('-WIDTH-120-').Update(button_color=('black', 'yellow'))
        
        window.FindElement('-WIDTH-70-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-96-').Update(button_color=sg.theme_button_color())

    if event == '-LENGTH--':
        newLength = admin_settings.BOARD_LENGTH - 10
        admin_settings.set_board_length(newLength)
        window.FindElement('-BOARD-LENGTH-').update(str(newLength))

    if event == '-LENGTH+-':
        newLength = admin_settings.BOARD_LENGTH + 10
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

def boxes(event):
    if event == '-CAM1-LEFT-':
        admin_settings.set_cam1_box_lr(-5)

    if event == '-CAM1-RIGHT-':
        admin_settings.set_cam1_box_lr(5)

    if event == '-SIDE1-UP-':
        handle_config.setValue('BOX POSITIONING', 'SIDE1_VERT', handle_config.SIDE1_VERT - 5)

    if event == '-SIDE1-DOWN-':
        handle_config.setValue('BOX POSITIONING', 'SIDE1_VERT', handle_config.SIDE1_VERT + 5)

    if event == '-CAM2-LEFT-':
        admin_settings.set_cam2_box_lr(-5)

    if event == '-CAM2-RIGHT-':
        admin_settings.set_cam2_box_lr(5)

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