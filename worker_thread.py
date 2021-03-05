'''This module does the heavy lifting, organises the workflow'''

import PySimpleGUI as sg
import time
from os import listdir
from os.path import isfile, join

# my modules
import layouts          # UI Layouts
import program_state    # programs State
import camera_setup     # camera setup function
import aio              # handles the aio
import image_handling   # handles image
import handle_count     # handles count of stats
import admin_view       # handles UI when in admin mode
import reset_view       # clears the UI

camera1 = camera_setup.main(0)  # setup camera one
camera2 = camera_setup.main(1)  # setup camera two

def main(window):
    try:
        while not program_state.STOP_PROGRAM:         
            if program_state.RUN_MODE:                                                     # if running

                aio.setOutput(10, 1)                                                       # turn running light on
                aio.setOutput(0, 1)                                                        # turn converyor on
                
                rPosition = aio.waitInputState(0, True)                                    # wait for board to be in position R
                lPosition = aio.waitInputState(1, True)                                    # wait for board to be in position L     
                if not rPosition or not lPosition:                                         # if program is stopped
                    continue                                                               # exit loop

                # board in position L & R
                aio.setOutput(0, 0)                                                        # turn converyor off
                aio.setOutput(1, 1)                                                        # turn clamp on
                time.sleep(2) # time.sleep(0.05)                                           # sleep 50 ms REMOVE
                
                clampR = aio.getInputState(7)
                clampL = aio.getInputState(8)
                if clampL or clampR:                                                       # if clamps are not closed
                    aio.setOutput(5, 1)                                                    # turn fault on
                    program_state.set_fault(True)                                          # let program know we have fault
                    window.write_event_value('-FAULT-', True)                              # let gui know we have fault

                    while program_state.FAULT:                                             # while program is at fault
                        aio.pulseOutput(10, 0)                                             # pulse light off
                        time.sleep(0.5)                                                    # sleep for 500ms

                    continue                                                               # running loop

                aio.setOutput(2, 1)                                                        # turn lift on
                
                liftUp = aio.waitInputState(3, True)                                       # wait for lift up
                if not liftUp:                                                             # if program is stopped
                    continue                                                               # exit loop
                
                _, frame1 = camera1.read()                                           # grab camera 1
                _, frame2 = camera2.read()                                           # grab camera 2                    
                side1cam1, side1cam1Bark = image_handling.main(frame1, 1)            # process camera 1
                side1cam2, side1cam2Bark = image_handling.main(frame2, 2)            # process camera 2
                side1Bark = round((side1cam1Bark + side1cam2Bark) / 2, 2)            # calculate bark count

                window.FindElement('-SIDE-1-CAM-1-').update(data=side1cam1)                            # update img for side 1 camera 1
                window.FindElement('-SIDE-1-CAM-2-').update(data=side1cam2)                            # update img for side 1 camera 2                    
                window.FindElement('-%-BARK-1-').update('\nSIDE 1:- % BARK ' + str(side1Bark))         # update count of bark count for side 1

                if side1Bark > program_state.REJECT_LIMIT:
                    window.FindElement('-SIDE1-STATUS-').update('\nFAIL', background_color=('red'))
                else:
                    window.FindElement('-SIDE1-STATUS-').update('\nPASS', background_color=('green'))

                currentCCW = aio.getInputState(4)                                          # get current CCW state                                
                currentCW = aio.getInputState(5)                                           # get current CW state

                program_state.toggle_rotate_state()                                        # change rotate state
                aio.setOutput(3, program_state.ROTATE_STATE)                               # send new rotate state

                ccwState = aio.waitInputState(4, not currentCCW)                           # wait for CCW state change
                cwState = aio.waitInputState(5, not currentCW)                             # wait for CW state change
                if not ccwState or not cwState:                                            # if program is stopped
                    continue                                                               # exit loop
                
                _, frame1 = camera1.read()                                                 # grab camera 1
                _, frame2 = camera2.read()                                                 # grab camera 2                    
                side2cam1, side2cam1Bark = image_handling.main(frame1, 1)                  # process camera 1
                side2cam2, side2cam2Bark = image_handling.main(frame2, 2)                  # process camera 2
                side2Bark = round((side2cam1Bark + side2cam2Bark) / 2, 2)                  # calculate bark count

                window.FindElement('-SIDE-2-CAM-1-').update(data=side2cam1)                            # update img for side 2 camera 1
                window.FindElement('-SIDE-2-CAM-2-').update(data=side2cam2)                            # update img for side 2 camera 2                
                window.FindElement('-%-BARK-2-').update('\nSIDE 2:- % BARK ' + str(side2Bark))         # update count of bark count for side 2

                if side2Bark > program_state.REJECT_LIMIT:
                    window.FindElement('-SIDE2-STATUS-').update('\nFAIL', background_color=('red'))    # update flag for side 2 to fail
                else:
                    window.FindElement('-SIDE2-STATUS-').update('\nPASS', background_color=('green'))  # update flag for side 2 to pass

                time.sleep(2)                                                                          # SLEEP FOR A BIT REMOVE

                # if either side is over REJECT (10%) then it's a reject
                if side1Bark > program_state.REJECT_LIMIT or side2Bark > program_state.REJECT_LIMIT:
                    aio.setOutput(4, 1)                                                         # turn reject on
                    time.sleep(2)                                                               # sleep for a bit
                    aio.setOutput(4, 0)                                                         # turn reject off

                    handle_count.plankFail(window)                                              # update stats
                    program_state.set_run_mode(False)                                           # stop running

                    continue

                # if side 1
                elif side1Bark < side2Bark:
                    currentCCW = aio.getInputState(4)                                          # get current CCW state
                    currentCW = aio.getInputState(5)                                           # get current CW state

                    program_state.toggle_rotate_state()                                        # change rotate state
                    aio.setOutput(3, program_state.ROTATE_STATE)                               # send new rotate state

                    ccwState = aio.waitInputState(4, not currentCCW)                           # wait for CCW state change
                    cwState = aio.waitInputState(5, not currentCW)                             # wait for CW state change
                    if not ccwState or not cwState:                                            # if program is stopped
                        continue                                                               # exit loop

                # if side 1 or 2
                handle_count.plankPass(window)                                                 # update stats

                # continue with plank
                aio.setOutput(2, 0)                                                        # turn lift off
                liftDown = aio.waitInputState(2, True)                                     # wait for lift down
                if not liftDown:                                                           # if program is stopped
                    continue                                                               # exit loop

                aio.setOutput(1, 0)                                                        # turn clamp off
                clampOpen = aio.waitInputState(6, True)                                    # wait for clamp open
                if not clampOpen:                                                          # if program is stopped
                    continue                                                               # exit loop  
            
            else:                                                                          

                window.FindElement('-START-').Update(button_color=sg.theme_button_color()) # turn start button off

                aio.setOutput(0, 0)                                                        # when stopped turn converyor off
                aio.setOutput(1, 0)                                                        # when stopped turn clamp off
                aio.setOutput(2, 0)                                                        # when stopped turn lift off
                ## if program_state.ROTATE_STATE == 1:                                          # when stopped turn rotate off
                ##     program_state.toggle_rotate_state()
                ##     aio.setOutput(3, program_state.ROTATE_STATE)
                aio.setOutput(4, 0)                                                        # when stopped turn reject off
                aio.setOutput(5, 0)                                                        # when stopped turn fault off

                if program_state.THRESH_MODE or program_state.THRESH_BOX_MODE or program_state.SHOW_TRANSFORM:         
                    admin_view.main(camera1, camera2, window)
                else:
                    reset_view.main(window)
    
    except Exception as e:
        print('Exception: ', e)

    camera1.release()
    camera2.release()