
import PySimpleGUI as sg

# my modules
import program_state

def admin(event, window):
    window.FindElement('-TRANSFORM-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-BOXES-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-THRESH-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-CAM1-TRANSFORM-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM1-BOXES-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM1-THRESH-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM2-TRANSFORM-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM2-BOXES-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM2-THRESH-LAYOUT-').Update(visible=False)
    
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
        program_state.set_thresh_boxes(False)
        program_state.set_thresh(False)
        program_state.set_transform(False)

    # When transform mode button is pressed
    if event == '-TRANSFORM-MODE-':
        program_state.set_transform(True)     # turn on transform view mode

        # turn transform button on
        window.FindElement('-TRANSFORM-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-TRANSFORM-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-TRANSFORM-LAYOUT-').Update(visible=True)

    # When boxes mode button is pressed
    if event == '-BOXES-MODE-':
        program_state.set_thresh_boxes(True)  # turn on boxes mode

        # turn boxes button on
        window.FindElement('-BOXES-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-BOXES-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-BOXES-LAYOUT-').Update(visible=True)

    # When thresh mode button is pressed
    if event == '-THRESH-MODE-':          
        program_state.set_thresh(True)       # turn on thresh mode

        # turn thresh button on
        window.FindElement('-THRESH-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-THRESH-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-THRESH-LAYOUT-').Update(visible=True)

def board(event, window):
    if event == '-WIDTH-X-':
        program_state.set_board_width(30)
        window.FindElement('-WIDTH-X-').Update(button_color=('black', 'yellow'))

        window.FindElement('-WIDTH-96-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-120-').Update(button_color=sg.theme_button_color())
    
    if event == '-WIDTH-96-':
        program_state.set_board_width(0) # 0 is neutral
        window.FindElement('-WIDTH-96-').Update(button_color=('black', 'yellow'))
        
        window.FindElement('-WIDTH-X-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-120-').Update(button_color=sg.theme_button_color())
    
    if event == '-WIDTH-120-':
        program_state.set_board_width(47)
        window.FindElement('-WIDTH-120-').Update(button_color=('black', 'yellow'))
        
        window.FindElement('-WIDTH-X-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-96-').Update(button_color=sg.theme_button_color())

    if event == '-LENGTH--':
        newLength = program_state.BOARD_LENGTH - 10
        program_state.set_board_length(newLength)
        window['-BOARD-LENGTH-'].update(str(newLength))

    if event == '-LENGTH+-':
        newLength = program_state.BOARD_LENGTH + 10
        program_state.set_board_length(newLength)
        window['-BOARD-LENGTH-'].update(str(newLength))

def transform(event, window):
    if event == '-CAM1-TOP--':
        program_state.set_cam1_trans_right(2)

    if event == '-CAM1-TOP+-':
        program_state.set_cam1_trans_right(-2)

    if event == '-CAM1-BOT--':
        program_state.set_cam1_trans_left(-2)

    if event == '-CAM1-BOT+-':
        program_state.set_cam1_trans_left(2)

    if event == '-CAM2-TOP--':
        program_state.set_cam2_trans_left(2)

    if event == '-CAM2-TOP+-':
        program_state.set_cam2_trans_left(-2)

    if event == '-CAM2-BOT--':
        program_state.set_cam2_trans_right(-2)

    if event == '-CAM2-BOT+-':
        program_state.set_cam2_trans_right(2)

    window['-CAM1-TOP-'].update(str(program_state.CAM1_TRANS_RIGHT))
    window['-CAM1-BOT-'].update(str(program_state.CAM1_TRANS_LEFT))
    window['-CAM2-TOP-'].update(str(program_state.CAM2_TRANS_LEFT))
    window['-CAM2-BOT-'].update(str(program_state.CAM2_TRANS_RIGHT))

def boxes(event):
    if event == '-CAM1-LEFT-':
        program_state.set_cam1_box_lr(-5)

    if event == '-CAM1-RIGHT-':
        program_state.set_cam1_box_lr(5)

    if event == '-CAM1-UP-':
        program_state.set_cam1_box_ud(-5)

    if event == '-CAM1-DOWN-':
        program_state.set_cam1_box_ud(5)

    if event == '-CAM2-LEFT-':
        program_state.set_cam2_box_lr(-5)

    if event == '-CAM2-RIGHT-':
        program_state.set_cam2_box_lr(5)

    if event == '-CAM2-UP-':
        program_state.set_cam2_box_ud(-5)

    if event == '-CAM2-DOWN-':
        program_state.set_cam2_box_ud(5)

def thresh(event, window):
    if event == '-CAM1-THRESH--':
        program_state.set_cam1_thresh(-5)

    if event == '-CAM1-THRESH+-':
        program_state.set_cam1_thresh(5)

    if event == '-CAM2-THRESH--':
        program_state.set_cam2_thresh(-5)

    if event == '-CAM2-THRESH+-':
        program_state.set_cam2_thresh(5)
    
    window['-CAM1-THRESH-'].update(str(program_state.CAM1_THRESH))
    window['-CAM2-THRESH-'].update(str(program_state.CAM2_THRESH))











