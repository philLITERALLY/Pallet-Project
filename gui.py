
import PySimpleGUI as sg

# my modules
import program_state
import handle_events

def the_gui(window):
    global REJECT, IMG_NUM, CAM1_IMG, CAM2_IMG
    global IN0, IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8

    # --------------------- EVENT LOOP ---------------------
    while not program_state.STOP_PROGRAM:
        event, values = window.read()
        
        # When window is closed
        if event in (sg.WIN_CLOSED, 'Exit'):
            program_state.stop_program()
            break

        # admin events
        if event in ('-SETUP-', '-CANCEL-', '-TRANSFORM-MODE-', '-BOXES-MODE-', '-THRESH-MODE-'):
            handle_events.admin(event, window)

        # board events
        if event in ('-WIDTH-X-', '-WIDTH-96-', '-WIDTH-120-', '-LENGTH--', '-LENGTH+-'):
            handle_events.board(event, window)

        # transform events
        if event in ('-CAM1-TOP--', '-CAM1-TOP+-', '-CAM1-BOT--', '-CAM1-BOT+-', '-CAM2-TOP--', '-CAM2-TOP+-', '-CAM2-BOT--', '-CAM2-BOT+-'):
            handle_events.transform(event, window)
            
        # box position events
        if event in ('-CAM1-LEFT-', '-CAM1-RIGHT-', '-CAM1-UP-', '-CAM1-DOWN-', '-CAM2-LEFT-', '-CAM2-RIGHT-', '-CAM2-UP-', '-CAM2-DOWN-'):
            handle_events.boxes(event)

        # thresh events
        if event in ('-CAM1-THRESH--', '-CAM1-THRESH+-', '-CAM2-THRESH--', '-CAM2-THRESH+-'):
            handle_events.thresh(event, window)

        # When the reset button is pressed
        if event == '-RESET-':
            program_state.stop_program()
            break
            
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
            REJECT += 1
            rejectStr = str(REJECT) + '%'
            window['-REJECT-LEVEL-'].update(rejectStr)
            
        # When the decrease reject value is pressed
        if event == '-REJECT--':
            REJECT -= 1
            rejectStr = str(REJECT) + '%'
            window['-REJECT-LEVEL-'].update(rejectStr)

        if program_state.RUN_MODE:
            if event == '-IN-0-':
                if IN0:
                    IN0 = False
                    window.FindElement('-IN-0-').Update(button_color=sg.theme_button_color())
                else:
                    IN0 = True
                    window.FindElement('-IN-0-').Update(button_color=('black', 'yellow'))
            if event == '-IN-1-':
                if IN1:
                    IN1 = False
                    window.FindElement('-IN-1-').Update(button_color=sg.theme_button_color())
                else:
                    IN1 = True
                    window.FindElement('-IN-1-').Update(button_color=('black', 'yellow'))
            if event == '-IN-2-':
                if IN2:
                    IN2 = False
                    window.FindElement('-IN-2-').Update(button_color=sg.theme_button_color())
                else:
                    IN2 = True
                    window.FindElement('-IN-2-').Update(button_color=('black', 'yellow'))
            if event == '-IN-3-':
                if IN3:
                    IN3 = False
                    window.FindElement('-IN-3-').Update(button_color=sg.theme_button_color())
                else:
                    IN3 = True
                    window.FindElement('-IN-3-').Update(button_color=('black', 'yellow'))
            if event == '-IN-4-':
                if IN4:
                    IN4 = False
                    window.FindElement('-IN-4-').Update(button_color=sg.theme_button_color())
                else:
                    IN4 = True
                    window.FindElement('-IN-4-').Update(button_color=('black', 'yellow'))
            if event == '-IN-5-':
                if IN5:
                    IN5 = False
                    window.FindElement('-IN-5-').Update(button_color=sg.theme_button_color())
                else:
                    IN5 = True
                    window.FindElement('-IN-5-').Update(button_color=('black', 'yellow'))
            if event == '-IN-6-':
                if IN6:
                    IN6 = False
                    window.FindElement('-IN-6-').Update(button_color=sg.theme_button_color())
                else:
                    IN6 = True
                    window.FindElement('-IN-6-').Update(button_color=('black', 'yellow'))
            if event == '-IN-7-':
                if IN7:
                    IN7 = False
                    window.FindElement('-IN-7-').Update(button_color=sg.theme_button_color())
                else:
                    IN7 = True
                    window.FindElement('-IN-7-').Update(button_color=('black', 'yellow'))
            if event == '-IN-8-':
                if IN8:
                    IN8 = False
                    window.FindElement('-IN-8-').Update(button_color=sg.theme_button_color())
                else:
                    IN8 = True
                    window.FindElement('-IN-8-').Update(button_color=('black', 'yellow'))

    # if user exits the window, then close the window and exit the GUI func
    window.close()