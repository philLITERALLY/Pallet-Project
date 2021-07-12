'''This module does the heavy lifting, organises the workflow'''

import PySimpleGUI as sg
import time
from os import listdir
from os.path import isfile, join

# my modules
import handle_config    # module to handle config settings
import program_state    # programs State
import camera_setup     # camera setup function
import aio              # handles the aio
import image_handling   # handles image
import handle_count     # handles count of stats
import admin_view       # handles UI when in admin mode
import reset_view       # clears the UI

global camera1, camera2

camera1 = camera_setup.VideoCapture(0)  # setup camera one
camera2 = camera_setup.VideoCapture(1)  # setup camera two

def main(window):
    firstRun = True                                                                # set up "first run" state
    nextSide1Cam1, nextSide1Cam1Bark = None, None
    nextSide1Cam2, nextSide1Cam2Bark = None, None
    side1Cam1, side1Cam1Bark = None, None
    side1Cam2, side1Cam2Bark = None, None
    side2Cam1, side2Cam1Bark = None, None
    side2Cam2, side2Cam2Bark = None, None
    side1Bark, side2Bark = None, None

    try:
        while not program_state.STOP_PROGRAM:
            if program_state.RUN_MODE:                                             # if running

                reset_view.main(window)                                            # clear images and plank stats

                aio.setOutput(8, 1, window)                                        # turn running light on

                # FOR TESTS
                aio.setOutput(1, 1, window)
                # FOR TESTS

                time.sleep(handle_config.START_DELAY)                              # wait before starting the next loop

                boardIn = aio.waitInputState(0, True, window)                      # wait for board in place
                if not boardIn:                                                    # if program is stopped
                    return False                                                   # exit loop

                # FOR TESTS
                aio.setOutput(1, 0, window)
                # FOR TESTS

                if not firstRun:                                                   # use previous capture for current plank
                    side1Cam1, side1Cam1Bark = nextSide1Cam1, nextSide1Cam1Bark
                    side1Cam2, side1Cam2Bark = nextSide1Cam2, nextSide1Cam2Bark
                    side1Bark = round((side1Cam1Bark + side1Cam2Bark) / 2, 2)      # calculate bark count

                frame1 = camera1.read()                                                    # grab camera 1
                frame2 = camera2.read()                                                    # grab camera 2
                nextSide1Cam1, nextSide1Cam1Bark = image_handling.main(frame1, 1, 1, True) # process camera 1 left side
                nextSide1Cam2, nextSide1Cam2Bark = image_handling.main(frame2, 2, 1, True) # process camera 2 left side
                
                if not firstRun:
                    side2Cam1, side2Cam1Bark = image_handling.main(frame1, 1, 2, True) # process camera 1 right side
                    side2Cam2, side2Cam2Bark = image_handling.main(frame2, 2, 2, True) # process camera 2 right side
                    side2Bark = round((side2Cam1Bark + side2Cam2Bark) / 2, 2)          # calculate bark count
                
                # FOR TESTS
                aio.setOutput(1, 1, window)
                # aio.pulseOutput(1, 1, window)                                      # request flip
                # FOR TESTS

                if firstRun:
                    firstRun = False                                               # change "first run" state
                    continue
               
                window.FindElement('-SIDE-1-CAM-1-').update(data=side1Cam1)                    # update img for side 1 camera 1
                window.FindElement('-SIDE-1-CAM-2-').update(data=side1Cam2)                    # update img for side 1 camera 2                    
                window.FindElement('-%-BARK-1-').update('\nSIDE 1:- % BARK ' + str(side1Bark)) # update count of bark count for side 1

                if side1Bark > handle_config.REJECT_LEVEL:
                    window.FindElement('-SIDE1-STATUS-').update('\nFAIL', background_color=('red'))
                else:
                    window.FindElement('-SIDE1-STATUS-').update('\nPASS', background_color=('green'))

                window.FindElement('-SIDE-2-CAM-1-').update(data=side2Cam1)                    # update img for side 2 camera 1
                window.FindElement('-SIDE-2-CAM-2-').update(data=side2Cam2)                    # update img for side 2 camera 2
                window.FindElement('-%-BARK-2-').update('\nSIDE 2:- % BARK ' + str(side2Bark)) # update count of bark count for side 2

                if side2Bark > handle_config.REJECT_LEVEL:
                    window.FindElement('-SIDE2-STATUS-').update('\nFAIL', background_color=('red'))   # update flag for side 2 to fail
                else:
                    window.FindElement('-SIDE2-STATUS-').update('\nPASS', background_color=('green')) # update flag for side 2 to pass

                # if either side is over REJECT (10%) then it's a reject                
                reject = side1Bark > handle_config.REJECT_LEVEL or side2Bark > handle_config.REJECT_LEVEL

                if reject:
                    aio.pulseOutput(4, 1, window)                                      # pulse reject
                elif side1Bark < side2Bark:
                    aio.pulseOutput(2, 1, window)                                      # pulse good
                else:
                    aio.pulseOutput(3, 1, window)                                      # pulse flip

                time.sleep(handle_config.AFTER_GRAB)                               # wait after image grab

            else:

                firstRun = True                               # reset "first run" state
                nextSide1Cam1, nextSide1Cam1Bark = None, None # clear images
                nextSide1Cam2, nextSide1Cam2Bark = None, None # clear images
                side1Cam1, side1Cam1Bark = None, None         # clear images
                side1Cam2, side1Cam2Bark = None, None         # clear images
                side2Cam1, side2Cam1Bark = None, None         # clear images
                side2Cam2, side2Cam2Bark = None, None         # clear images
                side1Bark, side2Bark = None, None             # reset stats

                window.FindElement('-START-').Update(button_color=sg.theme_button_color()) # turn start button off

                if program_state.THRESH_MODE or \
                    program_state.THRESH_BOX_1_MODE or \
                    program_state.THRESH_BOX_2_MODE or \
                    program_state.SHOW_TRANSFORM:
                    admin_view.main(camera1, camera2, window)
                else:
                    reset_view.main(window)
                    
                    # Reset Outputs
                    aio.setOutput(0, 0, window)                                       # when stopped turn 0 off
                    aio.setOutput(1, 0, window)                                       # when stopped turn 1 off
                    aio.setOutput(2, 0, window)                                       # when stopped turn 2 off
                    aio.setOutput(3, 0, window)                                       # when stopped turn 3 off
                    aio.setOutput(4, 0, window)                                       # when stopped turn 4 off
                    aio.setOutput(5, 0, window)                                       # when stopped turn 5 off
                    aio.setOutput(7, 0, window)                                       # when stopped turn 6 off
                    aio.setOutput(7, 0, window)                                       # when stopped turn 7 off
                    aio.setOutput(8, 0, window)                                       # when stopped turn 8 off
    
    except Exception as e:
        print('Exception: ', e)

    camera1.release()
    camera2.release()