'''This module handles the main threads'''

import threading
import time
import PySimpleGUI as sg
import cv2
from os import listdir
from os.path import isfile, join

# my modules
import layouts          # UI Layouts
import program_state    # Programs State
import image_handling   # Handles image

sg.theme('Light Brown 3')

REJECT = 0
CAM1_IMG = ''
CAM2_IMG = ''
IMG_NUM = 0

OUT3 = False
IN0, IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8 = False, False, False, False, True, False, False, False, False

def wait_flag(flag, state):    
    while globals()[flag] != state:
        if not program_state.RUN_MODE:
            return False
        time.sleep(0.01)

    return True

def main_thread(window):
    global IMG_NUM, CAM1_IMG, CAM2_IMG
    global OUT3
    global IN0, IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8
    # camera1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    # camera2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    while not program_state.STOP_PROGRAM:
        
        # if running
        if program_state.RUN_MODE:
            window.FindElement('-OUT-0-').Update(button_color=('black', 'yellow'))     # turn converyor on
            
            rPosition = wait_flag('IN0', True)                                         # wait for board to be in position R
            lPosition = wait_flag('IN1', True)                                         # wait for board to be in position L
           
            if not rPosition or not lPosition:                                         # if board is not in position or program is stopped
                continue                                                               # exit loop

            # board in position L & R
            window.FindElement('-OUT-0-').Update(button_color=sg.theme_button_color()) # turn converyor off
            window.FindElement('-OUT-1-').Update(button_color=('black', 'yellow'))     # turn clamp on                
            time.sleep(4) # time.sleep(0.05)                                           # sleep 50 ms
            
            if IN7 or IN8:                                                             # if clamps are not closed okay
                window.FindElement('-OUT-5-').Update(button_color=('black', 'yellow')) # flag fault      
                program_state.set_run_mode(False)                                      # stop program
                continue                                                               # exit loop

            window.FindElement('-OUT-2-').Update(button_color=('black', 'yellow'))     # turn lift on   
            
            liftUp = wait_flag('IN3', True)                                            # wait for lift up
            if not liftUp:                                                             # if program is stopped
                continue                                                               # exit loop
            
            # _, frame1 = camera1.read()
            # _, frame2 = camera2.read()
            frame1 = cv2.imread(CAM2_IMG)                                              # grab camera 1
            frame2 = cv2.imread(CAM1_IMG)                                              # grab camera 2
            
            side1cam1 = image_handling.hangle_img(frame1)                              # process camera 1
            side1cam2 = image_handling.hangle_img(frame2)                              # process camera 2

            window['-SIDE-1-CAM-1-'].update(data=side1cam1)                            # update img for side 1 camera 1
            window['-SIDE-1-CAM-2-'].update(data=side1cam2)                            # update img for side 1 camera 2

            IMG_NUM += 1
            if IMG_NUM > len(cam1_imgs):
                IMG_NUM = 0
            CAM1_IMG = cam1_path + cam1_imgs[IMG_NUM]
            CAM2_IMG = cam2_path + cam2_imgs[IMG_NUM]

            if OUT3:                                                                    # Change Rotate state
                window.FindElement('-OUT-3-').Update(button_color=sg.theme_button_color())     
                OUT3 = False
            else:
                window.FindElement('-OUT-3-').Update(button_color=('black', 'yellow'))
                OUT3 = True

            ccwState = wait_flag('IN4', not IN4)                                       # wait for CCW state change
            cwState = wait_flag('IN5', not IN5)                                        # wait for CW state change
            if not ccwState or not cwState:                                            # if program is stopped
                continue                                                               # exit loop
            
            # _, frame1 = camera1.read()
            # _, frame2 = camera2.read()
            frame1 = cv2.imread(CAM2_IMG)                                              # grab camera 1
            frame2 = cv2.imread(CAM1_IMG)                                              # grab camera 2
            
            side1cam1 = image_handling.hangle_img(frame1)                              # process camera 1
            side1cam2 = image_handling.hangle_img(frame2)                              # process camera 2

            window['-SIDE-2-CAM-1-'].update(data=side1cam1)                            # update img for side 2 camera 1
            window['-SIDE-2-CAM-2-'].update(data=side1cam2)                            # update img for side 2 camera 2

            IMG_NUM += 1
            if IMG_NUM > len(cam1_imgs):
                IMG_NUM = 0
            CAM1_IMG = cam1_path + cam1_imgs[IMG_NUM]
            CAM2_IMG = cam2_path + cam2_imgs[IMG_NUM]

            # PICK BEST SIDE OR REJECT ON

            time.sleep(2)

            # if reject
            if REJECT == 0:
                window.FindElement('-OUT-4-').Update(button_color=('black', 'yellow'))      # turn reject on  
                time.sleep(2)                                                               # sleep for a bit
                window.FindElement('-OUT-4-').Update(button_color=sg.theme_button_color())  # turn reject off
                program_state.set_run_mode(False)                                           # stop running
                continue

            # if side 1
            elif REJECT == 1:
                if OUT3:                                                                    # Change Rotate state
                    window.FindElement('-OUT-3-').Update(button_color=sg.theme_button_color())     
                    OUT3 = False
                else:
                    window.FindElement('-OUT-3-').Update(button_color=('black', 'yellow'))
                    OUT3 = True

                ccwState = wait_flag('IN4', not IN4)                                       # wait for CCW state change
                cwState = wait_flag('IN5', not IN5)                                        # wait for CW state change
                if not ccwState or not cwState:                                            # if program is stopped
                    continue                                                               # exit loop

            # if side 1 or 2
            window.FindElement('-OUT-2-').Update(button_color=sg.theme_button_color()) # turn lift off
            liftDown = wait_flag('IN2', True)                                          # wait for lift down
            if not liftDown:                                                           # if program is stopped
                continue                                                               # exit loop

            window.FindElement('-OUT-1-').Update(button_color=sg.theme_button_color()) # turn clamp off  
            clampOpen = wait_flag('IN6', True)                                         # wait for clamp open
            if not clampOpen:                                                          # if program is stopped
                continue                                                               # exit loop  

            window.FindElement('-IN-0-').Update(button_color=sg.theme_button_color())  # reset board position R
            window.FindElement('-IN-1-').Update(button_color=sg.theme_button_color())  # reset board position L
            IN0, IN1 = False, False                                                    # reset board position variables
        
        else:                                                                          # when stopped turn everything off
            window.FindElement('-START-').Update(button_color=sg.theme_button_color()) # turn start button off

            window.FindElement('-OUT-0-').Update(button_color=sg.theme_button_color()) # turn converyor off
            window.FindElement('-OUT-1-').Update(button_color=sg.theme_button_color()) # turn clamp off
            window.FindElement('-OUT-2-').Update(button_color=sg.theme_button_color()) # turn lift off
            window.FindElement('-OUT-3-').Update(button_color=sg.theme_button_color()) # turn rotate off
            window.FindElement('-OUT-4-').Update(button_color=sg.theme_button_color()) # turn reject off
            window.FindElement('-OUT-5-').Update(button_color=sg.theme_button_color()) # turn fault off

            window.FindElement('-IN-0-').Update(button_color=sg.theme_button_color()) # reset inputs
            window.FindElement('-IN-1-').Update(button_color=sg.theme_button_color())
            window.FindElement('-IN-2-').Update(button_color=sg.theme_button_color())
            window.FindElement('-IN-3-').Update(button_color=sg.theme_button_color())
            window.FindElement('-IN-4-').Update(button_color=('black', 'yellow'))
            window.FindElement('-IN-5-').Update(button_color=sg.theme_button_color())
            window.FindElement('-IN-6-').Update(button_color=sg.theme_button_color())
            window.FindElement('-IN-7-').Update(button_color=sg.theme_button_color())
            window.FindElement('-IN-8-').Update(button_color=sg.theme_button_color())

            OUT3 = False
            IN0, IN1, IN2, IN3, IN4, IN5, IN6, IN7, IN8 = False, False, False, False, True, False, False, False, False

# get image files
cam1_path = 'C:/Users/The Beast/Documents/Paul Pallet/Pallet Project/final_cam/cam1/'
cam1_imgs = [f for f in listdir(cam1_path) if isfile(join(cam1_path, f))]
cam2_path = 'C:/Users/The Beast/Documents/Paul Pallet/Pallet Project/final_cam/cam2/'
cam2_imgs = [f for f in listdir(cam2_path) if isfile(join(cam2_path, f))]

# DUMMY IMGS
CAM1_IMG = cam1_path + cam1_imgs[IMG_NUM]
CAM2_IMG = cam2_path + cam2_imgs[IMG_NUM]

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
        if event == '-REJECT+-' and REJECT < 2:
            REJECT += 1
            window['-REJECT-LEVEL-'].update(REJECT)
            # rejectStr = str(REJECT) + '%'
            # window['-REJECT-LEVEL-'].update(rejectStr)
            
        # When the decrease reject value is pressed
        if event == '-REJECT--' and REJECT > 0:
            REJECT -= 1
            window['-REJECT-LEVEL-'].update(REJECT)
            # rejectStr = str(REJECT) + '%'
            # window['-REJECT-LEVEL-'].update(rejectStr)

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

if __name__ == '__main__':
   
    window = layouts.window # UI Window
    threads = []            # array to hold threads
    
    # collect all threads
    threads.append(threading.Thread(target=main_thread, args=(window,), daemon=True))
    # threads.append(threading.Thread(target=handle_camera_1, args=(window,), daemon=True))
    # threads.append(threading.Thread(target=handle_camera_2, args=(window,), daemon=True))

    # start all threads
    for thread in threads:
        thread.start()

    # The function that builds the UI and listens for events
    the_gui(window)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print('Exiting Program')