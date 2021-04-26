'''This module does handles the UI and UI events'''

from tkinter.constants import S
import PySimpleGUI as sg
import concurrent.futures

# my modules
import program_state    # Programs State
import handle_events    # handles the UI button events
import handle_config    # module to handle config settings
import worker_thread    # main thread that handles workflow
import aio              # handles the aio

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
                window.FindElement('-SINGLE-').Update('IN PROGRESS', button_color=('black', 'red'))
                
                # setup_ok = worker_thread.setup_for_image(window) # get set up to take image
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    threadTest = executor.submit(worker_thread.setup_for_image, window)
                    setup_ok = threadTest.result()
                    print(setup_ok)

                if not setup_ok:
                    continue

                singleState = not singleState
                window.FindElement('-SINGLE-').Update('SINGLE', button_color=('black', 'yellow'))

            # 2th press - Out2 off wait IN2,Out 0 & 1 off.
            else:
                window.FindElement('-SINGLE-').Update(button_color=sg.theme_button_color())
                worker_thread.drop_plank(window)
                aio.setOutput(0, 0, window)                                       # turn board stop off
                singleState = not singleState

        # When the rotate button is pressed perform actions
        if event == '-ROTATE-':
            program_state.toggle_rotate_state()                               # change rotate state
            aio.setOutput(3, program_state.ROTATE_STATE, window)              # send new rotate state

        # admin events
        if event in ('-SETUP-', '-CANCEL-', '-TRANSFORM-MODE-', '-BOXES-1-MODE-', '-BOXES-2-MODE-', '-BARK-MODE-'):
            handle_events.admin(event, window)

        # board events
        if event in ('-WIDTH-70-', '-WIDTH-96-', '-WIDTH-120-', '-LENGTH--', '-LENGTH+-'):
            handle_events.board(event, window)

        # transform events
        if event in ('-CAM1-TOP--', '-CAM1-TOP+-', '-CAM1-BOT--', '-CAM1-BOT+-', '-CAM2-TOP--', '-CAM2-TOP+-', '-CAM2-BOT--', '-CAM2-BOT+-'):
            handle_events.transform(event, window)
            
        # box position events
        if event in ('-SIDE1-LEFT-', '-SIDE1-RIGHT-', '-SIDE1-UP-', '-SIDE1-DOWN-', '-SIDE2-LEFT-', '-SIDE2-RIGHT-', '-SIDE2-UP-', '-SIDE2-DOWN-'):
            handle_events.boxes(event, window)

        # thresh events
        if event in ('-CAM1-THRESH--', '-CAM1-THRESH+-', '-CAM2-THRESH--', '-CAM2-THRESH+-'):
            handle_events.thresh(event, window)

        # changing individual box
        if event in ('-SIDE1-BOX--', '-SIDE1-BOX+-', '-SIDE2-BOX--', '-SIDE2-BOX+-'):
            value = 1
            if '--' in event: 
                value = -1

            handle_events.boxChange(event, window, side, value)

        # modifying an individual box
        if 'BOX-WIDTH' in event or 'BOX-POS' in event:
            value = 2
            if '--' in event: 
                value = -2

            handle_events.modifyBox(event, window, side, value)

        # When the reset button is pressed
        if event == '-RESET-':
            program_state.clear_results()

            window.FindElement('-TOTAL-PASSED-').update(str(0))
            window.FindElement('-TOTAL-INSPECTED-').update(str(0))

        # When the start button is pressed
        if event == '-START-':
            window.FindElement('-START-').Update(button_color=('black', 'yellow'))
            program_state.set_run_mode(True)
            
        # When the start button is pressed
        if event == '-STOP-':
            window.FindElement('-START-').Update(button_color=sg.theme_button_color())
            program_state.set_run_mode(False)

        # When the increase reject value is pressed
        if event == '-REJECT+-':
            handle_config.setValue('REJECT SETTINGS', 'REJECT_LEVEL', handle_config.REJECT_LEVEL + 1)
            rejectStr = str(handle_config.REJECT_LEVEL) + '%'
            window.FindElement('-REJECT-LEVEL-').update(rejectStr)
            
        # When the decrease reject value is pressed
        if event == '-REJECT--':
            handle_config.setValue('REJECT SETTINGS', 'REJECT_LEVEL', handle_config.REJECT_LEVEL - 1)
            rejectStr = str(handle_config.REJECT_LEVEL) + '%'
            window.FindElement('-REJECT-LEVEL-').update(rejectStr)

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