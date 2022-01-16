'''This module does handles the UI and UI events'''

from tkinter.constants import S
import PySimpleGUI as sg

# my modules
import program_state    # Programs State
import handle_events    # handles the UI button events
import handle_config    # module to handle config settings
import worker_thread    # main thread that handles workflow
import board_logic      # checks if board is pass or fail
import cv2

def main(window):

    while not program_state.STOP_PROGRAM:
        event, values = window.read()
        
        # When window is closed
        if event in (sg.WIN_CLOSED, 'Exit'):
            program_state.stop_program()
            break
        
        if event == '-GRAB-':
            frame = worker_thread.camera.read()
            text_input = values['-FILENAME-IN-']
            cv2.imwrite('images/stored/' + text_input + '.png', frame)

        # admin events
        if event in ('-SETUP-', '-CANCEL-', '-SHUT-DOWN-', '-LIVE-MODE-', '-BARK-MODE-', '-POSITION-MODE-'):
            handle_events.admin(event, window)

        # board position events
        if event in ('-SIDE1-LEFT-', '-SIDE1-RIGHT-', '-SIDE1-UP-', '-SIDE1-DOWN-', '-SIDE2-LEFT-', '-SIDE2-RIGHT-', '-SIDE2-UP-', '-SIDE2-DOWN-'):
            handle_events.position(event)

        # board events
        if event in ('-WIDTH-70-', '-WIDTH-96-', '-WIDTH-120-', '-LENGTH--', '-LENGTH+-'):
            handle_events.board(event, window)

        # thresh events
        if event in ('-CAM-THRESH--', '-CAM-THRESH+-'):
            handle_events.thresh(event, window)

        # When the reset button is pressed
        if event == '-RESET-':
            program_state.clear_results()

            window.find_element('-TOTAL-PASSED-').update(str(0))
            window.find_element('-TOTAL-INSPECTED-').update(str(0))

        # When the start button is pressed
        if event == '-START-':
            window.find_element('-START-').Update(button_color=('black', 'yellow'))
            program_state.set_run_mode(True)
            
        # When the start button is pressed
        if event == '-STOP-':
            window.find_element('-START-').Update(button_color=sg.theme_button_color())
            program_state.set_run_mode(False)

        # When the increase edge variance value is pressed
        if event == '-EDGE+-':
            handle_config.setValue('REJECT SETTINGS', 'EDGE_VARIANCE', handle_config.EDGE_VARIANCE + 1)
            edgeStr = str(handle_config.EDGE_VARIANCE) + '%'
            window.find_element('-EDGE-VARIANCE-LEVEL-').update(edgeStr)

        # When the decrease edge variance value is pressed
        if event == '-EDGE--':
            handle_config.setValue('REJECT SETTINGS', 'EDGE_VARIANCE', handle_config.EDGE_VARIANCE - 1)
            edgeStr = str(handle_config.EDGE_VARIANCE) + '%'
            window.find_element('-EDGE-VARIANCE-LEVEL-').update(edgeStr)

        # When the increase mid size value is pressed
        if event == '-MID-SIZE+-':
            handle_config.setValue('REJECT SETTINGS', 'MID_SIZE', handle_config.MID_SIZE + 1)
            midSizeStr = str(handle_config.MID_SIZE) + '%'
            window.find_element('-MID-SIZE-').update(midSizeStr)
            
        # When the decrease mid size value is pressed
        if event == '-MID-SIZE--':
            handle_config.setValue('REJECT SETTINGS', 'MID_SIZE', handle_config.MID_SIZE - 1)
            midSizeStr = str(handle_config.MID_SIZE) + '%'
            window.find_element('-MID-SIZE-').update(midSizeStr)

        # When the increase reject value is pressed
        if event == '-REJECT+-':
            handle_config.setValue('REJECT SETTINGS', 'REJECT_LEVEL', handle_config.REJECT_LEVEL + 1)
            rejectStr = str(handle_config.REJECT_LEVEL) + '%'
            window.find_element('-REJECT-LEVEL-').update(rejectStr)
            
        # When the decrease reject value is pressed
        if event == '-REJECT--':
            handle_config.setValue('REJECT SETTINGS', 'REJECT_LEVEL', handle_config.REJECT_LEVEL - 1)
            rejectStr = str(handle_config.REJECT_LEVEL) + '%'
            window.find_element('-REJECT-LEVEL-').update(rejectStr)

        # When fault is flagged
        if event == '-FAULT-':
            sg.Popup(                               # show popup
                'Fault',
                'Clamps not closed correctly',
                background_color='red',
                font=("Helvetica", 25),
                no_titlebar=True,
                keep_on_top=True
            )
            program_state.set_run_mode(False)       # stop running
            program_state.set_fault(False)          # stop fault

        # When calibrate button is pressed
        if event == '-CALIBRATE-':
            board_logic.calibrate(worker_thread.camera)

    # if user exits the window, then close the window and exit the GUI func
    window.close()