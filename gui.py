'''This module does handles the UI and UI events'''

from tkinter.constants import S
import PySimpleGUI as sg

# my modules
import program_state    # Programs State
import handle_events    # handles the UI button events
import handle_config    # module to handle config settings
import worker_thread    # main thread that handles workflow
import aio              # handles the aio
import cv2

def main(window):
    singleState = False

    while not program_state.STOP_PROGRAM:
        event, values = window.read()
        
        # When window is closed
        if event in (sg.WIN_CLOSED, 'Exit'):
            program_state.stop_program()
            break
        
        side = 1
        if 'SIDE2' in event:
            side = 2

        if event == '-GRAB-':
            cam1 = worker_thread.camera1.read()
            cam2 = worker_thread.camera2.read()

            text_input = values['-FILENAME-IN-']
            cv2.imwrite('images/stored/' + text_input + '_cam1.jpg', cam1)
            cv2.imwrite('images/stored/' + text_input + '_cam2.jpg', cam2)

        # When the camera button is pressed switch the cameras
        if event == '-CAMERA-':
            tempCam1 = worker_thread.camera1
            worker_thread.camera1 = worker_thread.camera2
            worker_thread.camera2 = tempCam1

        # When the single button is pressed perform actions
        if event == '-SINGLE-':
            
            # PAUL NOTES            
            # 1st press - Out0 on,wait for IN0&1,Out1 on wait 50ms Out2 on wait for IN3 grab images.
            if not singleState:
                program_state.setup_plank(True)
                singleState = not singleState

            # 2th press - Out2 off wait IN2,Out 0 & 1 off.
            else:
                program_state.drop_plank(True)
                singleState = not singleState

        # When the rotate button is pressed perform actions
        if event == '-ROTATE-':
            program_state.toggle_rotate_state()                               # change rotate state
            aio.setOutput(4, program_state.ROTATE_STATE, window)              # send new rotate state

        # admin events
        if event in ('-SETUP-', '-CANCEL-', '-LIVE-MODE-', '-TRANSFORM-MODE-', '-COLUMN-MODE-', '-BARK-MODE-'):
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
        if event == '-EDGE-REJECT+-':
            handle_config.setValue('REJECT SETTINGS', 'EDGE_REJECT_LEVEL', handle_config.EDGE_REJECT_LEVEL + 1)
            rejectStr = str(handle_config.EDGE_REJECT_LEVEL) + '%'
            window.find_element('-EDGE-REJECT-LEVEL-').update(rejectStr)
            
        # When the decrease reject value is pressed
        if event == '-EDGE-REJECT--':
            handle_config.setValue('REJECT SETTINGS', 'EDGE_REJECT_LEVEL', handle_config.EDGE_REJECT_LEVEL - 1)
            rejectStr = str(handle_config.EDGE_REJECT_LEVEL) + '%'
            window.find_element('-EDGE-REJECT-LEVEL-').update(rejectStr)

        # When the increase reject value is pressed
        if event == '-MID-REJECT+-':
            handle_config.setValue('REJECT SETTINGS', 'MID_REJECT_LEVEL', handle_config.MID_REJECT_LEVEL + 1)
            rejectStr = str(handle_config.MID_REJECT_LEVEL) + '%'
            window.find_element('-MID-REJECT-LEVEL-').update(rejectStr)
            
        # When the decrease reject value is pressed
        if event == '-MID-REJECT--':
            handle_config.setValue('REJECT SETTINGS', 'MID_REJECT_LEVEL', handle_config.MID_REJECT_LEVEL - 1)
            rejectStr = str(handle_config.MID_REJECT_LEVEL) + '%'
            window.find_element('-MID-REJECT-LEVEL-').update(rejectStr)

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

    # if user exits the window, then close the window and exit the GUI func
    window.close()