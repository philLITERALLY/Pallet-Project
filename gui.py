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
            frame1 = worker_thread.camera1.read()
            frame2 = worker_thread.camera2.read()

            text_input = values['-FILENAME-IN-']
            cv2.imwrite('images/stored/' + text_input + '_cam1.png', frame1)
            cv2.imwrite('images/stored/' + text_input + '_cam2.png', frame2)

        # When the camera button is pressed switch the cameras
        if event == '-CAMERA-':
            tempCam1 = worker_thread.camera1
            worker_thread.camera1 = worker_thread.camera2
            worker_thread.camera2 = tempCam1

        # admin events
        if event in ('-SETUP-', '-CANCEL-', '-SHUT-DOWN-', '-LIVE-MODE-', '-TRANSFORM-MODE-', '-BARK-MODE-'):
            handle_events.admin(event, window)

        # board events
        if event in ('-WIDTH-70-', '-WIDTH-96-', '-WIDTH-120-', '-LENGTH--', '-LENGTH+-'):
            handle_events.board(event, window)

        # transform events
        if event in ('-CAM1-TOP--', '-CAM1-TOP+-', '-CAM1-BOT--', '-CAM1-BOT+-', '-CAM2-TOP--', '-CAM2-TOP+-', '-CAM2-BOT--', '-CAM2-BOT+-'):
            handle_events.transform(event, window)

        # thresh events
        if event in ('-CAM1-THRESH--', '-CAM1-THRESH+-', '-CAM2-THRESH--', '-CAM2-THRESH+-'):
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

        # When the increase reject value is pressed
        if event == '-BORDERLINE+-':
            handle_config.setValue('REJECT SETTINGS', 'BORDERLINE_LEVEL', handle_config.BORDERLINE_LEVEL + 1)
            rejectStr = str(handle_config.BORDERLINE_LEVEL) + '%'
            window.find_element('-BORDERLINE-LEVEL-').update(rejectStr)
            
        # When the decrease reject value is pressed
        if event == '-BORDERLINE--':
            handle_config.setValue('REJECT SETTINGS', 'BORDERLINE_LEVEL', handle_config.BORDERLINE_LEVEL - 1)
            rejectStr = str(handle_config.BORDERLINE_LEVEL) + '%'
            window.find_element('-BORDERLINE-LEVEL-').update(rejectStr)

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

            side1White, _ = board_logic.main(worker_thread.camera1, worker_thread.camera2, 1, window, True)
            _, side2White = board_logic.main(worker_thread.camera1, worker_thread.camera2, 2, window, True)

            # Update variables
            handle_config.setValue('REJECT SETTINGS', 'SIDE1_PERC', side1White)
            handle_config.setValue('REJECT SETTINGS', 'SIDE2_PERC', side2White)

    # if user exits the window, then close the window and exit the GUI func
    window.close()