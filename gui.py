'''This module does handles the UI and UI events'''

import PySimpleGUI as sg

# my modules
import program_state    # Programs State
import handle_events    # handles the UI button events
import handle_config    # module to handle config settings

def main(window):
    while not program_state.STOP_PROGRAM:
        event, values = window.read()
        
        # When window is closed
        if event in (sg.WIN_CLOSED, 'Exit'):
            program_state.stop_program()
            break

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
        if event in ('-CAM1-LEFT-', '-CAM1-RIGHT-', '-SIDE1-UP-', '-SIDE1-DOWN-', '-CAM2-LEFT-', '-CAM2-RIGHT-', '-CAM2-UP-', '-CAM2-DOWN-'):
            handle_events.boxes(event)

        # thresh events
        if event in ('-CAM1-THRESH--', '-CAM1-THRESH+-', '-CAM2-THRESH--', '-CAM2-THRESH+-'):
            handle_events.thresh(event, window)

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