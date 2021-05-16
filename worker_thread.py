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

def setup_for_image(window):
    
    aio.setOutput(0, 1, window)                                       # turn board stop on

    currentRPosition = aio.getInputState(0, window)                   # get current R Position
    currentLPosition = aio.getInputState(1, window)                   # get current L Position
    if currentRPosition or currentLPosition:                          # if board already in position wait for it to clear first
        rPosition = aio.waitInputState(0, False, window)              # wait for board to leave position R
        lPosition = aio.waitInputState(1, False, window)              # wait for board to leave position L
        if not rPosition or not lPosition:                            # if program is stopped
            return False                                              # exit loop

        time.sleep(handle_config.jam_delay)                           # sleep to ensure jam doesn't happen
    
    # once board has cleared position 
    rPosition = aio.waitInputState(0, True, window)                   # wait for board to be in position R
    lPosition = aio.waitInputState(1, True, window)                   # wait for board to be in position L
    if not rPosition or not lPosition:                                # if program is stopped
        return False                                                  # exit loop

    # board in position L & R
    aio.setOutput(1, 1, window)                                       # turn clamp on
    time.sleep(0.05)                                                  # sleep 50 ms
    
    clampR = aio.getInputState(7, window)
    clampL = aio.getInputState(8, window)
    if clampL or clampR:                                              # if clamps are not closed
        aio.setOutput(5, 1, window)                                   # turn fault on
        program_state.set_fault(True)                                 # let program know we have fault
        window.write_event_value('-FAULT-', True)                     # let gui know we have fault

        while program_state.FAULT:                                    # while program is at fault
            aio.pulseOutput(6, 0, window)                             # pulse light off
            time.sleep(0.5)                                           # sleep for 500ms

        return False                                                  # running loop

    aio.setOutput(2, 1, window)                                       # turn lift on
    
    liftUp = aio.waitInputState(3, True, window)                      # wait for lift up
    if not liftUp:                                                    # if program is stopped
        return False                                                  # exit loop

    aio.setOutput(0, 0, window)                                       # turn board stop on

    return True

def drop_plank(window):
    aio.setOutput(2, 0, window)                                       # turn lift off
    liftDown = aio.waitInputState(2, True, window)                    # wait for lift down
    if not liftDown:                                                  # if program is stopped
        return False                                                  # exit loop

    aio.setOutput(1, 0, window)                                       # turn clamp off
    clampOpen = aio.waitInputState(6, True, window)                   # wait for clamp open
    if not clampOpen:                                                 # if program is stopped
        return False                                                  # exit loop

    return True

def main(window):
    try:
        while not program_state.STOP_PROGRAM:
            if program_state.RUN_MODE:                                            # if running

                time.sleep(handle_config.START_DELAY)                             # wait before starting the next loop

                reset_view.main(window)                                           # clear images and plank stats

                aio.setOutput(8, 1, window)                                       # turn running light on

                setup_ok = setup_for_image(window)                                # get set up to take image
                if not setup_ok:
                    continue
                
                time.sleep(handle_config.WAIT_GRAB)                               # wait before image grab

                frame1 = camera1.read()                                           # grab camera 1
                frame2 = camera2.read()                                           # grab camera 2
                side1cam1, side1cam1Bark = image_handling.main(frame1, 1, 1, True)   # process camera 1 side 1
                side1cam2, side1cam2Bark = image_handling.main(frame2, 2, 1, True)   # process camera 2 side 1
                side1Bark = round((side1cam1Bark + side1cam2Bark) / 2, 2)         # calculate bark count

                window.FindElement('-SIDE-1-CAM-1-').update(data=side1cam1)                    # update img for side 1 camera 1
                window.FindElement('-SIDE-1-CAM-2-').update(data=side1cam2)                    # update img for side 1 camera 2                    
                window.FindElement('-%-BARK-1-').update('\nSIDE 1:- % BARK ' + str(side1Bark)) # update count of bark count for side 1

                if side1Bark > handle_config.REJECT_LEVEL:
                    window.FindElement('-SIDE1-STATUS-').update('\nFAIL', background_color=('red'))
                else:
                    window.FindElement('-SIDE1-STATUS-').update('\nPASS', background_color=('green'))

                time.sleep(handle_config.AFTER_GRAB)                              # wait after image grab

                currentCCW = aio.getInputState(4, window)                         # get current CCW state
                currentCW = aio.getInputState(5, window)                          # get current CW state

                time.sleep(0.2)                                                   # wait 200 ms before rotating plank

                program_state.toggle_rotate_state()                               # change rotate state
                aio.setOutput(3, program_state.ROTATE_STATE, window)              # send new rotate state

                ccwState = aio.waitInputState(4, not currentCCW, window)          # wait for CCW state change
                cwState = aio.waitInputState(5, not currentCW, window)            # wait for CW state change
                if not ccwState or not cwState:                                   # if program is stopped
                    continue                                                      # exit loop

                time.sleep(handle_config.WAIT_GRAB)                               # wait before image grab

                frame1 = camera1.read()                                           # grab camera 1
                frame2 = camera2.read()                                           # grab camera 2
                side2cam1, side2cam1Bark = image_handling.main(frame1, 1, 2, True)   # process camera 1 side 2
                side2cam2, side2cam2Bark = image_handling.main(frame2, 2, 2, True)   # process camera 2 side 2
                side2Bark = round((side2cam1Bark + side2cam2Bark) / 2, 2)         # calculate bark count

                window.FindElement('-SIDE-2-CAM-1-').update(data=side2cam1)                    # update img for side 2 camera 1
                window.FindElement('-SIDE-2-CAM-2-').update(data=side2cam2)                    # update img for side 2 camera 2
                window.FindElement('-%-BARK-2-').update('\nSIDE 2:- % BARK ' + str(side2Bark)) # update count of bark count for side 2

                if side2Bark > handle_config.REJECT_LEVEL:
                    window.FindElement('-SIDE2-STATUS-').update('\nFAIL', background_color=('red'))   # update flag for side 2 to fail
                else:
                    window.FindElement('-SIDE2-STATUS-').update('\nPASS', background_color=('green')) # update flag for side 2 to pass

                time.sleep(handle_config.AFTER_GRAB)                              # wait after image grab

                # if either side is over REJECT (10%) then it's a reject                
                reject = side1Bark > handle_config.REJECT_LEVEL or side2Bark > handle_config.REJECT_LEVEL

                # if plank isn't a reject and is side 1
                if not reject and side1Bark < side2Bark:
                    currentCCW = aio.getInputState(4, window)                     # get current CCW state
                    currentCW = aio.getInputState(5, window)                      # get current CW state

                    time.sleep(0.2)                                                   # wait 200 ms before rotating plank

                    program_state.toggle_rotate_state()                           # change rotate state
                    aio.setOutput(3, program_state.ROTATE_STATE, window)          # send new rotate state

                    ccwState = aio.waitInputState(4, not currentCCW, window)      # wait for CCW state change
                    cwState = aio.waitInputState(5, not currentCW, window)        # wait for CW state change
                    if not ccwState or not cwState:                               # if program is stopped
                        continue                                                  # exit loop

                drop_ok = drop_plank(window)                                      # drop plank
                if not drop_ok:
                    continue                

                if reject:
                    aio.setOutput(4, 1, window)                                   # turn reject on
                    time.sleep(0.2)                                               # sleep for 20ms
                    aio.setOutput(4, 0, window)                                   # turn reject off       

                    handle_count.plankFail(window)                                # update stats
                else:
                    aio.setOutput(7, 1, window)                                   # turn good board on
                    time.sleep(0.2)                                               # sleep for 20ms
                    aio.setOutput(7, 0, window)                                   # turn good board off       
                    
                    handle_count.plankPass(window)                                # update stats
    
            else:                                                                          

                window.FindElement('-START-').Update(button_color=sg.theme_button_color()) # turn start button off

                if program_state.THRESH_MODE or \
                    program_state.THRESH_BOX_1_MODE or \
                    program_state.THRESH_BOX_2_MODE or \
                    program_state.SHOW_TRANSFORM:
                    admin_view.main(camera1, camera2, window)
                else:
                    reset_view.main(window)
                    
                    # Reset Outputs
                    aio.setOutput(0, 0, window)                                       # when stopped turn board stop off
                    aio.setOutput(1, 0, window)                                       # when stopped turn clamp off
                    aio.setOutput(2, 0, window)                                       # when stopped turn lift off
                    ## if program_state.ROTATE_STATE == 1:                            # when stopped turn rotate off
                    ##     program_state.toggle_rotate_state()
                    ##     aio.setOutput(3, program_state.ROTATE_STATE)
                    aio.setOutput(4, 0, window)                                       # when stopped turn reject off
                    aio.setOutput(5, 0, window)                                       # when stopped turn fault off
                    aio.setOutput(7, 0, window)                                       # when stopped turn good board off
                    aio.setOutput(8, 0, window)                                       # when stopped turn light off

                if program_state.SETUP_PLANK:
                    program_state.setup_plank(False)

                    window.FindElement('-SINGLE-').Update('IN PROGRESS', button_color=('black', 'red'))

                    setup_ok = setup_for_image(window)
                    if not setup_ok:
                        continue

                    window.FindElement('-SINGLE-').Update('SINGLE', button_color=('black', 'yellow'))

                if program_state.DROP_PLANK:
                    program_state.drop_plank(False)

                    window.FindElement('-SINGLE-').Update(button_color=sg.theme_button_color())
                    drop_ok = drop_plank(window)
                    if not drop_ok:
                        continue
    
    except Exception as e:
        print('Exception: ', e)

    camera1.release()
    camera2.release()