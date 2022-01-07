
import PySimpleGUI as sg

# my modules
import program_state    # Programs State
import admin_settings   # Admin settings
import handle_config    # Programs Configuration

def admin(event, window):
    window.find_element('-LIVE-MODE-').Update(button_color=sg.theme_button_color())
    window.find_element('-BARK-MODE-').Update(button_color=sg.theme_button_color())
    window.find_element('-POSITION-MODE-').Update(button_color=sg.theme_button_color())
    window.find_element('-CALIBRATE-LAYOUT-').Update(visible=False)
    window.find_element('-REJECT-LAYOUT-').Update(visible=False)
    window.find_element('-CAM-THRESH-LAYOUT-').Update(visible=False)
    window.find_element('-SIDE1-POSITION-LAYOUT-').Update(visible=False)
    window.find_element('-SIDE2-POSITION-LAYOUT-').Update(visible=False)
    window.find_element('-IO-LAYOUT-').Update(visible=False)
    window.find_element('-ADMIN-BOX1-TEXT-').Update('THRESH')
    window.find_element('-ADMIN-BOX1-TEXT-').Update(visible=True)
        
    # When the setup button is pressed
    if event == '-SETUP-':
        # stop run mode
        program_state.set_run_mode(False)

        # change to admin view
        window.find_element('-VIEW-LAYOUT-').Update(visible=False)
        window.find_element('-ADMIN-LAYOUT-').Update(visible=True)
        
        # default state to live mode
        program_state.set_live(True)

        # turn live button on
        window.find_element('-LIVE-MODE-').Update(button_color=('black', 'yellow'))
        window.find_element('-IO-LAYOUT-').Update(visible=True)
        window.find_element('-CALIBRATE-LAYOUT-').Update(visible=True)
        window.find_element('-REJECT-LAYOUT-').Update(visible=True)
        window.find_element('-ADMIN-BOX1-TEXT-').Update(visible=False)
        
    # When the cancel button is pressed
    if event == '-CANCEL-':
        window.find_element('-VIEW-LAYOUT-').Update(visible=True)
        window.find_element('-ADMIN-LAYOUT-').Update(visible=False)
        
        # make sure admin modes are off
        program_state.set_live(False)
        program_state.set_thresh(False)

    # When the shut down button is pressed
    if event == '-SHUT-DOWN-':
        program_state.stop_program()

    # When live mode button is pressed
    if event == '-LIVE-MODE-':
        program_state.set_live(True)     # turn on live view mode

        # turn live button on
        window.find_element('-LIVE-MODE-').Update(button_color=('black', 'yellow'))
        window.find_element('-IO-LAYOUT-').Update(visible=True)
        window.find_element('-CALIBRATE-LAYOUT-').Update(visible=True)
        window.find_element('-REJECT-LAYOUT-').Update(visible=True)
        window.find_element('-ADMIN-BOX1-TEXT-').Update(visible=False)

    # When bark thresh mode button is pressed
    if event == '-BARK-MODE-':
        program_state.set_thresh(True)       # turn on box thresh mode

        # turn thresh button on
        window.find_element('-BARK-MODE-').Update(button_color=('black', 'yellow'))
        window.find_element('-CAM-THRESH-LAYOUT-').Update(visible=True)
        window.find_element('-IO-LAYOUT-').Update(visible=True)

    # When position mode button is pressed
    if event == '-POSITION-MODE-':
        program_state.set_live(True)     # turn on live view mode

        # turn side 1 button on
        window.find_element('-POSITION-MODE-').Update(button_color=('black', 'yellow'))
        window.find_element('-SIDE1-POSITION-LAYOUT-').Update(visible=True)
        window.find_element('-SIDE2-POSITION-LAYOUT-').Update(visible=True)
        window.find_element('-IO-LAYOUT-').Update(visible=True)

def board(event, window):
    if event == '-WIDTH-70-': # 70
        handle_config.setValue('BOARD SETTINGS', 'BOARD_WIDTH', -52)
        window.find_element('-WIDTH-70-').Update(button_color=('black', 'yellow'))

        window.find_element('-WIDTH-96-').Update(button_color=sg.theme_button_color())
        window.find_element('-WIDTH-120-').Update(button_color=sg.theme_button_color())
    
    if event == '-WIDTH-96-':
        handle_config.setValue('BOARD SETTINGS', 'BOARD_WIDTH', 0)
        window.find_element('-WIDTH-96-').Update(button_color=('black', 'yellow'))
        
        window.find_element('-WIDTH-70-').Update(button_color=sg.theme_button_color())
        window.find_element('-WIDTH-120-').Update(button_color=sg.theme_button_color())
    
    if event == '-WIDTH-120-':
        handle_config.setValue('BOARD SETTINGS', 'BOARD_WIDTH', 47)
        window.find_element('-WIDTH-120-').Update(button_color=('black', 'yellow'))
        
        window.find_element('-WIDTH-70-').Update(button_color=sg.theme_button_color())
        window.find_element('-WIDTH-96-').Update(button_color=sg.theme_button_color())

    if event == '-LENGTH--':
        newLength = handle_config.BOARD_LENGTH - 10
        admin_settings.set_board_length(newLength)
        window.find_element('-BOARD-LENGTH-').update(str(newLength))

    if event == '-LENGTH+-':
        newLength = handle_config.BOARD_LENGTH + 10
        admin_settings.set_board_length(newLength)
        window.find_element('-BOARD-LENGTH-').update(str(newLength))

def thresh(event, window):
    if event == '-CAM-THRESH--':
        handle_config.setValue('THRESH SETTINGS', 'CAM_THRESH', handle_config.CAM_THRESH - 5)

    if event == '-CAM-THRESH+-':
        handle_config.setValue('THRESH SETTINGS', 'CAM_THRESH', handle_config.CAM_THRESH + 5)
    
    window.find_element('-CAM-THRESH-').update(str(handle_config.CAM_THRESH))

def position(event):
    if event == '-SIDE1-LEFT-':
        admin_settings.set_side1_box_lr(-5)

    if event == '-SIDE1-RIGHT-':
        admin_settings.set_side1_box_lr(5)

    if event == '-SIDE1-UP-':
        admin_settings.set_side1_box_ud(-5)

    if event == '-SIDE1-DOWN-':
        admin_settings.set_side1_box_ud(5)

    if event == '-SIDE2-LEFT-':
        admin_settings.set_side2_box_lr(-5)

    if event == '-SIDE2-RIGHT-':
        admin_settings.set_side2_box_lr(5)

    if event == '-SIDE2-UP-':
        admin_settings.set_side2_box_ud(-5)

    if event == '-SIDE2-DOWN-':
        admin_settings.set_side2_box_ud(5)