'''This module handles the main threads'''

import threading
import time
from tkinter import Event
import PySimpleGUI as sg
import cv2
from os import listdir
from os.path import isfile, join

# my modules
import layouts          # UI Layouts
import program_state    # Programs State
import image_handling   # Handles image
# import aio
import gui              # gui function

# sg.theme('Light Brown 3')

REJECT = 10
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
    
    camera1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    camera2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    camera1.set(3, 3840)
    camera1.set(4, 2160)
    camera2.set(3, 3840)
    camera2.set(4, 2160)

    try:
        while not program_state.STOP_PROGRAM:         
            if program_state.RUN_MODE:                                                     # if running
                window.FindElement('-OUT-0-').Update(button_color=('black', 'yellow'))     # turn converyor on
                
                rPosition = wait_flag('IN0', True)                                         # wait for board to be in position R
                lPosition = wait_flag('IN1', True)                                         # wait for board to be in position L
                # rPosition = aio.waitInputState(0, True)
                # lPosition = aio.waitInputState(1, True)           
                if not rPosition or not lPosition:                                         # if program is stopped
                    continue                                                               # exit loop

                # board in position L & R
                window.FindElement('-OUT-0-').Update(button_color=sg.theme_button_color()) # turn converyor off
                window.FindElement('-OUT-1-').Update(button_color=('black', 'yellow'))     # turn clamp on                
                time.sleep(2) # time.sleep(0.05)                                           # sleep 50 ms
                
                # clampR = aio.getInputState(7)
                # clampL = aio.getInputState(8)
                if IN7 or IN8:                                                             # if clamps are not closed okay
                    window.FindElement('-OUT-5-').Update(button_color=('black', 'yellow')) # flag fault      
                    program_state.set_run_mode(False)                                      # stop program
                    continue                                                               # exit loop

                window.FindElement('-OUT-2-').Update(button_color=('black', 'yellow'))     # turn lift on   
                
                liftUp = wait_flag('IN3', True)                                            # wait for lift up
                # liftUp = aio.waitInputState(3, True)
                if not liftUp:                                                             # if program is stopped
                    continue                                                               # exit loop
                
                # _, frame1 = camera1.read()
                # _, frame2 = camera2.read()
                frame1 = cv2.imread(CAM1_IMG)                                              # grab camera 1
                frame2 = cv2.imread(CAM2_IMG)                                              # grab camera 2            
                    
                side1cam1, side1cam1Bark = image_handling.handle_img(frame1, 1)            # process camera 1
                side1cam2, side1cam2Bark = image_handling.handle_img(frame2, 2)            # process camera 2
                side1Bark = round((side1cam1Bark + side1cam2Bark) / 2, 2)

                window['-SIDE-1-CAM-1-'].update(data=side1cam1)                            # update img for side 1 camera 1
                window['-SIDE-1-CAM-2-'].update(data=side1cam2)                            # update img for side 1 camera 2
                    
                window['-%-BARK-1-'].update("\nSIDE 1:- % BARK " + str(side1Bark))

                if side1Bark > REJECT:
                    window['-SIDE1-STATUS-'].update("\nFAIL", background_color=('red'))
                else:
                    window['-SIDE1-STATUS-'].update("\nPASS", background_color=('green'))

                IMG_NUM += 1
                if IMG_NUM > len(cam1_imgs):
                    IMG_NUM = 0
                CAM1_IMG = cam1_path + cam1_imgs[IMG_NUM]
                CAM2_IMG = cam2_path + cam2_imgs[IMG_NUM]

                # currentCCW = aio.getInputState(4)
                # currentCW = aio.getInputState(5)
                if OUT3:                                                                    # Change Rotate state
                    window.FindElement('-OUT-3-').Update(button_color=sg.theme_button_color())     
                    OUT3 = False
                else:
                    window.FindElement('-OUT-3-').Update(button_color=('black', 'yellow'))
                    OUT3 = True

                ccwState = wait_flag('IN4', not IN4)                                       # wait for CCW state change
                cwState = wait_flag('IN5', not IN5)                                        # wait for CW state change
                # ccwState = aio.waitInputState(4, not currentCCW)
                # cwState = aio.waitInputState(5, not currentCW)
                if not ccwState or not cwState:                                            # if program is stopped
                    continue                                                               # exit loop
                
                # _, frame1 = camera1.read()
                # _, frame2 = camera2.read()
                frame1 = cv2.imread(CAM1_IMG)                                              # grab camera 1
                frame2 = cv2.imread(CAM2_IMG)                                              # grab camera 2
                    
                side2cam1, side2cam1Bark = image_handling.handle_img(frame1, 1)            # process camera 1
                side2cam2, side2cam2Bark = image_handling.handle_img(frame2, 2)            # process camera 2
                side2Bark = round((side2cam1Bark + side2cam2Bark) / 2, 2)

                window['-SIDE-2-CAM-1-'].update(data=side2cam1)                            # update img for side 2 camera 1
                window['-SIDE-2-CAM-2-'].update(data=side2cam2)                            # update img for side 2 camera 2
                
                window['-%-BARK-2-'].update("\nSIDE 2:- % BARK " + str(side2Bark))

                if side2Bark > REJECT:
                    window['-SIDE2-STATUS-'].update("\nFAIL", background_color=('red'))
                else:
                    window['-SIDE2-STATUS-'].update("\nPASS", background_color=('green'))

                IMG_NUM += 1
                if IMG_NUM > len(cam1_imgs):
                    IMG_NUM = 0
                CAM1_IMG = cam1_path + cam1_imgs[IMG_NUM]
                CAM2_IMG = cam2_path + cam2_imgs[IMG_NUM]

                # PICK BEST SIDE OR REJECT ON

                time.sleep(2)

                # if either side is over REJECT (10%) then it's a reject
                if side1Bark > REJECT or side2Bark > REJECT:
                    window.FindElement('-OUT-4-').Update(button_color=('black', 'yellow'))      # turn reject on  
                    time.sleep(2)                                                               # sleep for a bit
                    window.FindElement('-OUT-4-').Update(button_color=sg.theme_button_color())  # turn reject off
                    program_state.set_run_mode(False)                                           # stop running
                    continue

                # if side 1
                elif side1Bark < side2Bark:
                    if OUT3:                                                                    # Change Rotate state
                        window.FindElement('-OUT-3-').Update(button_color=sg.theme_button_color())     
                        OUT3 = False
                    else:
                        window.FindElement('-OUT-3-').Update(button_color=('black', 'yellow'))
                        OUT3 = True

                    # currentCCW = aio.getInputState(4)
                    # currentCW = aio.getInputState(5)
                    ccwState = wait_flag('IN4', not IN4)                                       # wait for CCW state change
                    cwState = wait_flag('IN5', not IN5)                                        # wait for CW state change
                    # ccwState = aio.waitInputState(4, not currentCCW)
                    # cwState = aio.waitInputState(5, not currentCW)
                    if not ccwState or not cwState:                                            # if program is stopped
                        continue                                                               # exit loop

                # if side 1 or 2
                window.FindElement('-OUT-2-').Update(button_color=sg.theme_button_color()) # turn lift off
                liftDown = wait_flag('IN2', True)                                          # wait for lift down            
                # liftDown = aio.waitInputState(2, True)
                if not liftDown:                                                           # if program is stopped
                    continue                                                               # exit loop

                window.FindElement('-OUT-1-').Update(button_color=sg.theme_button_color()) # turn clamp off  
                clampOpen = wait_flag('IN6', True)                                         # wait for clamp open
                # clampOpen = aio.waitInputState(6, True)
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

                if program_state.THRESH_MODE or program_state.THRESH_BOX_MODE or program_state.SHOW_TRANSFORM:                
                    # _, frame1 = camera1.read()
                    # _, frame2 = camera2.read()
                    frame1 = cv2.imread(CAM1_IMG)                                            # grab camera 1
                    frame2 = cv2.imread(CAM2_IMG)                                            # grab camera 2
                    
                    cam1Orig, _ = image_handling.handle_img(frame1, 1, True)                 # process camera 1
                    cam2Orig, _ = image_handling.handle_img(frame2, 2, True)                 # process camera 2

                    window['-SIDE-1-CAM-1-'].update(data=cam1Orig)                           # update img for side 1 camera 1
                    window['-SIDE-1-CAM-2-'].update(data=cam2Orig)                           # update img for side 1 camera 2
                    
                    cam1Mod, cam1BarkPerc = image_handling.handle_img(frame1, 1, False)      # process camera 1
                    cam2Mod, cam2BarkPerc = image_handling.handle_img(frame2, 2, False)      # process camera 2

                    window['-SIDE-2-CAM-1-'].update(data=cam1Mod)                            # update img for side 1 camera 1
                    window['-SIDE-2-CAM-2-'].update(data=cam2Mod)                            # update img for side 1 camera 2
                    
                    window['-%-BARK-1-'].update("\nCAM 1:- % BARK " + str(cam1BarkPerc))
                    window['-%-BARK-2-'].update("\nCAM 2:- % BARK " + str(cam2BarkPerc))

                    if cam1BarkPerc > REJECT:
                        window['-SIDE1-STATUS-'].update("\nFAIL", background_color=('red'))
                    else:
                        window['-SIDE1-STATUS-'].update("\nPASS", background_color=('green'))

                    if cam2BarkPerc > REJECT:
                        window['-SIDE2-STATUS-'].update("\nFAIL", background_color=('red'))
                    else:
                        window['-SIDE2-STATUS-'].update("\nPASS", background_color=('green'))
                else:
                    window.FindElement('-SIDE-1-CAM-1-').Update('', size=(layouts.half_width, layouts.row_size))
                    window.FindElement('-SIDE-1-CAM-2-').Update('', size=(layouts.half_width, layouts.row_size))
                    window.FindElement('-SIDE-2-CAM-1-').Update('', size=(layouts.half_width, layouts.row_size))
                    window.FindElement('-SIDE-2-CAM-2-').Update('', size=(layouts.half_width, layouts.row_size))

                    window['-%-BARK-1-'].update("\nSIDE 1:- % BARK XXX")
                    window['-%-BARK-2-'].update("\nSIDE 2:- % BARK XXX")
                    window['-SIDE1-STATUS-'].update("\nXXX", background_color=('blue'))
                    window['-SIDE2-STATUS-'].update("\nXXX", background_color=('blue'))
    
    except Exception as e:
        print('Exception: ', e)

    camera1.release()
    camera2.release()

# get image files
cam1_path = 'C:/Users/The Beast/Documents/Paul Pallet/Pallet Project/final_cam/cam1/'
cam1_imgs = [f for f in listdir(cam1_path) if isfile(join(cam1_path, f))]
cam2_path = 'C:/Users/The Beast/Documents/Paul Pallet/Pallet Project/final_cam/cam2/'
cam2_imgs = [f for f in listdir(cam2_path) if isfile(join(cam2_path, f))]

# DUMMY IMGS
CAM1_IMG = cam1_path + cam1_imgs[IMG_NUM]
CAM2_IMG = cam2_path + cam2_imgs[IMG_NUM]

if __name__ == '__main__':
   
    window = layouts.window # UI Window
    threads = []            # array to hold threads
    
    # collect all threads
    threads.append(threading.Thread(target=main_thread, args=(window,), daemon=True))

    # start all threads
    for thread in threads:
        thread.start()

    # The function that builds the UI and listens for events
    gui.the_gui(window)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print('Exiting Program')