'''This module does the heavy lifting, organises the workflow'''

import PySimpleGUI as sg
import time
import keyboard

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

manualTesting = False

if manualTesting:
    camera1 = camera_setup.StaticImage(0)   # setup static image one
    camera2 = camera_setup.StaticImage(1)   # setup static image two
else:
    camera1 = camera_setup.VideoCapture(0)  # setup camera one
    camera2 = camera_setup.VideoCapture(1)  # setup camera two

def waitKey():
    while True:
        if not (program_state.LIVE_MODE or program_state.SHOW_TRANSFORM or program_state.COLUMN_MODE or program_state.THRESH_MODE) and not program_state.RUN_MODE:
            program_state.set_run_mode(False)
            return False

        if keyboard.is_pressed('n'):
            program_state.set_run_mode(False)
            return False

        if keyboard.is_pressed('y'):
            return True


def runProgram(window):
    firstRun = True
    nextSide1Cam1, nextSide1Cam1BarkA, nextSide1Cam1BarkB, nextSide1Cam1BarkC = None, None, None, None
    nextSide1Cam2, nextSide1Cam2BarkA, nextSide1Cam2BarkB, nextSide1Cam2BarkC = None, None, None, None
    side1Cam1, side1Cam1BarkA, side1Cam1BarkB, side1Cam1BarkC = None, None, None, None
    side1Cam2, side1Cam2BarkA, side1Cam2BarkB, side1Cam2BarkC = None, None, None, None
    side2Cam1, side2Cam1BarkA, side2Cam1BarkB, side2Cam1BarkC = None, None, None, None
    side2Cam2, side2Cam2BarkA, side2Cam2BarkB, side2Cam2BarkC = None, None, None, None

    while not program_state.STOP_PROGRAM:
        if program_state.RUN_MODE:                                             # if running

            reset_view.main(window)                                            # clear images and plank stats

            aio.setOutput(8, 1, window)                                        # turn running light on

            # FOR TESTS
            aio.setOutput(1, 1, window)
            # FOR TESTS

            time.sleep(handle_config.START_DELAY)                              # wait before starting the next loop

            if manualTesting:
                boardIn = waitKey()                                             # wait for board in place
                if not boardIn:
                    continue
            else:
                boardIn = aio.waitInputState(0, True, window)                  # wait for board in place
                if not boardIn:
                    continue

            # FOR TESTS
            aio.setOutput(1, 0, window)
            # FOR TESTS

            if not firstRun:                                                   # use previous capture for current plank
                side1Cam1, side1Cam1BarkA, side1Cam1BarkB, side1Cam1BarkC = nextSide1Cam1, nextSide1Cam1BarkA, nextSide1Cam1BarkB, nextSide1Cam1BarkC
                side1Cam2, side1Cam2BarkA, side1Cam2BarkB, side1Cam2BarkC = nextSide1Cam2, nextSide1Cam2BarkA, nextSide1Cam2BarkB, nextSide1Cam2BarkC

            frame1 = camera1.read()                                                    # grab camera 1
            frame2 = camera2.read()                                                    # grab camera 2
            if firstRun:
                nextSide1Cam1, _, nextSide1Cam1BarkA, nextSide1Cam1BarkB, nextSide1Cam1BarkC, _, _, _ = image_handling.main(frame1, 1, True)
                nextSide1Cam2, _, nextSide1Cam2BarkA, nextSide1Cam2BarkB, nextSide1Cam2BarkC, _, _, _ = image_handling.main(frame2, 2, True)
            else:
                nextSide1Cam1, side2Cam1, nextSide1Cam1BarkA, nextSide1Cam1BarkB, nextSide1Cam1BarkC, side2Cam1BarkA, side2Cam1BarkB, side2Cam1BarkC = image_handling.main(frame1, 1, True)
                nextSide1Cam2, side2Cam2, nextSide1Cam2BarkA, nextSide1Cam2BarkB, nextSide1Cam2BarkC, side2Cam2BarkA, side2Cam2BarkB, side2Cam2BarkC = image_handling.main(frame2, 2, True)

            
            # FOR TESTS
            aio.setOutput(1, 1, window)
            # aio.pulseOutput(1, 1, window)                                      # request flip
            # FOR TESTS

            if firstRun:
                firstRun = False                                               # change "first run" state
                continue
            
            window.FindElement('-SIDE-1-CAM-1-').update(data=side1Cam1)                    # update img for side 1 camera 1
            window.FindElement('-SIDE-1-CAM-2-').update(data=side1Cam2)                    # update img for side 1 camera 2
            
            side1ColABark = round((side1Cam1BarkA + side1Cam2BarkA) / 2, 2)
            side1ColBBark = round((side1Cam1BarkB + side1Cam2BarkB) / 2, 2)
            side1ColCBark = round((side1Cam1BarkC + side1Cam2BarkC) / 2, 2)
            window.FindElement('-%-BARK-1-').update('\nSIDE 1 (% BARK)  ||  A: ' + str(side1ColABark) + '  ||  B: ' + str(side1ColBBark) + '  ||  C: ' + str(side1ColCBark)) # update count of bark count for side 1

            side1failState = []
            if side1ColABark > handle_config.EDGE_REJECT_LEVEL:
                side1failState.append('COL A')
            if side1ColBBark > handle_config.MID_REJECT_LEVEL:
                side1failState.append('COL B')
            if side1ColCBark > handle_config.EDGE_REJECT_LEVEL:
                side1failState.append('COL C')

            if len(side1failState) > 0:
                window.FindElement('-SIDE1-STATUS-').update('\n' + ' || '.join(side1failState), background_color=('red'))
            else:
                window.FindElement('-SIDE1-STATUS-').update('\nPASS', background_color=('green'))

            window.FindElement('-SIDE-2-CAM-1-').update(data=side2Cam1)                    # update img for side 2 camera 1
            window.FindElement('-SIDE-2-CAM-2-').update(data=side2Cam2)                    # update img for side 2 camera 2

            side2ColABark = round((side2Cam1BarkA + side2Cam2BarkA) / 2, 2)
            side2ColBBark = round((side2Cam1BarkB + side2Cam2BarkB) / 2, 2)
            side2ColCBark = round((side2Cam1BarkC + side2Cam2BarkC) / 2, 2)
            window.FindElement('-%-BARK-2-').update('\nSIDE 2 (% BARK)  ||  A: ' + str(side2ColABark) + '  ||  B: ' + str(side2ColBBark) + '  ||  C: ' + str(side2ColCBark)) # update count of bark count for side 2

            side2failState = []
            if side2ColABark > handle_config.EDGE_REJECT_LEVEL:
                side2failState.append('COL A')
            if side2ColBBark > handle_config.MID_REJECT_LEVEL:
                side2failState.append('COL B')
            if side2ColCBark > handle_config.EDGE_REJECT_LEVEL:
                side2failState.append('COL C')

            if len(side2failState) > 0:
                window.FindElement('-SIDE2-STATUS-').update('\n' + ' || '.join(side2failState), background_color=('red'))
            else:
                window.FindElement('-SIDE2-STATUS-').update('\nPASS', background_color=('green'))

            # if side 1 fails
            if len(side1failState) > 0:
                # and side 2 col b is less than reject level
                if side2ColBBark < handle_config.MID_REJECT_LEVEL:
                    print('GOOD 1')
                    handle_count.plankPass(window)                                     # update stats
                    aio.pulseOutput(2, 1, window)                                      # pulse good

                else:
                    print('REJECT 1')
                    handle_count.plankFail(window)                                     # update stats
                    aio.pulseOutput(4, 1, window)                                      # pulse reject
            else:
                # if side 2 col b is more than reject level
                if side2ColBBark > handle_config.MID_REJECT_LEVEL:
                    print('REJECT 2')
                    handle_count.plankFail(window)                                     # update stats
                    aio.pulseOutput(4, 1, window)                                      # pulse reject

                # else if col a and/or col c is more than reject level
                elif len(side2failState) > 0:
                    print('FLIP 2')
                    handle_count.plankPass(window)                                     # update stats
                    aio.pulseOutput(3, 1, window)                                      # pulse flip

                else:
                    print('GOOD 2')
                    handle_count.plankPass(window)                                     # update stats
                    aio.pulseOutput(2, 1, window)                                      # pulse good

            time.sleep(handle_config.AFTER_GRAB)                               # wait after image grab

        else:

            firstRun = True                               # reset "first run" state
            nextSide1Cam1, nextSide1Cam1BarkA, nextSide1Cam1BarkB, nextSide1Cam1BarkC = None, None, None, None
            nextSide1Cam2, nextSide1Cam2BarkA, nextSide1Cam2BarkB, nextSide1Cam2BarkC = None, None, None, None
            side1Cam1, side1Cam1BarkA, side1Cam1BarkB, side1Cam1BarkC = None, None, None, None
            side1Cam2, side1Cam2BarkA, side1Cam2BarkB, side1Cam2BarkC = None, None, None, None
            side2Cam1, side2Cam1BarkA, side2Cam1BarkB, side2Cam1BarkC = None, None, None, None
            side2Cam2, side2Cam2BarkA, side2Cam2BarkB, side2Cam2BarkC = None, None, None, None

            window.FindElement('-START-').Update(button_color=sg.theme_button_color()) # turn start button off

            if program_state.LIVE_MODE or \
                program_state.SHOW_TRANSFORM or \
                program_state.COLUMN_MODE or \
                program_state.THRESH_MODE:
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

def main(window):

    if manualTesting:
        runProgram(window)
    else:
        try:
            runProgram(window)
        except Exception as e:
            print('Exception: ', e)

    camera1.release()
    camera2.release()