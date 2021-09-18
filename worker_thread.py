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
import board_logic      # checks if board is pass or fail

global camera1, camera2

manualTesting = True

if manualTesting:
    camera1 = camera_setup.StaticImage(0)   # setup static image one
    camera2 = camera_setup.StaticImage(1)   # setup static image two
else:
    camera1 = camera_setup.VideoCapture(0)  # setup camera one
    camera2 = camera_setup.VideoCapture(1)  # setup camera two

def waitKey():
    while True:
        if keyboard.is_pressed('y'):
            return True

        if not program_state.RUN_MODE:
            return False


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

            reject1Flag, reject2Flag, flipFlag = False, False, False
            reset_view.main(window)                                            # clear images and plank stats

            aio.setOutput(8, 1, window)                                        # turn running light on (OUT8 ON)
            aio.setOutput(0, 1, window)                                        # flag ready state (OUT0 ON)

            time.sleep(handle_config.START_DELAY)                              # wait before starting the next loop

            if manualTesting:
                boardIn = waitKey()                                             # wait for board in place
                if not boardIn:
                    continue
            else:
                boardIn = aio.waitInputState(0, True, window)                  # wait for board (IN1 Pulse)
                if not boardIn:
                    continue

            aio.setOutput(0, 0, window)                                        # stop ready state (OUT0 OFF)

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
          
            if firstRun:
                firstRun = False                                               # change "first run" state
                continue
            
            window.find_element('-SIDE-1-CAM-1-').update(data=side1Cam1)                    # update img for side 1 camera 1
            window.find_element('-SIDE-1-CAM-2-').update(data=side1Cam2)                    # update img for side 1 camera 2
            
            side1ColABark = round((side1Cam1BarkA + side1Cam2BarkA) / 2, 2)
            side1ColBBark = round((side1Cam1BarkB + side1Cam2BarkB) / 2, 2)
            side1ColCBark = round((side1Cam1BarkC + side1Cam2BarkC) / 2, 2)

            side1failState = []
            side1ColAFlip, side1ColAReject, side1ColAPerc = board_logic.main(side1ColABark, 1, 'A')
            if side1ColAReject:
                side1failState.append('COL A')
                reject1Flag = True
            elif side1ColAFlip:
                side1failState.append('FLIP COL A')
                flipFlag = True

            _, side1ColBReject, sideColBPerc = board_logic.main(side1ColBBark, 1, 'B')
            if side1ColBReject:
                side1failState.append('COL B')
                reject1Flag = True

            side1ColCFlip, side1ColCReject, sideColCPerc = board_logic.main(side1ColCBark, 1, 'C')
            if side1ColCReject:
                side1failState.append('COL C')
                reject1Flag = True
            elif side1ColCFlip:
                side1failState.append('FLIP COL C')
                flipFlag = True

            window.find_element('-%-BARK-1-').update('\nSIDE 1 (% WHITE)  ||  A: ' + str(side1ColAPerc) + '  ||  B: ' + str(sideColBPerc) + '  ||  C: ' + str(sideColCPerc)) # update count of bark count for side 1
            if len(side1failState) > 0:
                colour = 'orange'
                if reject1Flag:
                    colour = 'red'
                window.find_element('-SIDE1-STATUS-').update('\n' + ' || '.join(side1failState), background_color=(colour))
            else:
                window.find_element('-SIDE1-STATUS-').update('\nPASS', background_color=('green'))

            window.find_element('-SIDE-2-CAM-1-').update(data=side2Cam1)                    # update img for side 2 camera 1
            window.find_element('-SIDE-2-CAM-2-').update(data=side2Cam2)                    # update img for side 2 camera 2

            side2ColABark = round((side2Cam1BarkA + side2Cam2BarkA) / 2, 2)
            side2ColBBark = round((side2Cam1BarkB + side2Cam2BarkB) / 2, 2)
            side2ColCBark = round((side2Cam1BarkC + side2Cam2BarkC) / 2, 2)

            side2failState = []
            side2ColAFlip, side2ColAReject, side2ColAPerc = board_logic.main(side2ColABark, 2, 'A')
            if side2ColAReject:
                side2failState.append('COL A')
                reject2Flag = True
            elif side2ColAFlip:
                side2failState.append('FLIP COL A')
                flipFlag = True

            _, side2ColBReject, side2ColBPerc = board_logic.main(side2ColBBark, 2, 'B')
            if side2ColBReject:
                side2failState.append('COL B')
                reject2Flag = True

            side2ColCFlip, side2ColCReject, side2ColCPerc = board_logic.main(side2ColCBark, 2, 'C')
            if side2ColCReject:
                side2failState.append('COL C')
                reject2Flag = True
            elif side2ColCFlip:
                side2failState.append('FLIP COL C')
                flipFlag = True

            window.find_element('-%-BARK-2-').update('\nSIDE 2 (% WHITE)  ||  A: ' + str(side2ColAPerc) + '  ||  B: ' + str(side2ColBPerc) + '  ||  C: ' + str(side2ColCPerc)) # update count of bark count for side 2
            if len(side2failState) > 0:
                colour = 'orange'
                if reject2Flag:
                    colour = 'red'
                window.find_element('-SIDE2-STATUS-').update('\n' + ' || '.join(side2failState), background_color=(colour))
            else:
                window.find_element('-SIDE2-STATUS-').update('\nPASS', background_color=('green'))

            aio.setOutput(0, 1, window)        # flag ready state (OUT0 ON)

            if reject1Flag or reject2Flag:     # if board is a reject
                aio.pulseOutput(3, 1, window)  # pulse reject (OUT3 ON)
                handle_count.plankFail(window) # update stats

            elif flipFlag:                     # if edges are borderline on both side
                side1Total = side1ColABark + side1ColCBark
                side2Total = side2ColABark + side2ColCBark
                if side2Total > side1Total:        # if side 2 has the most bark we need to flip
                    aio.pulseOutput(2, 1, window)  # pulse flip (OUT2 ON)
                else:                              # else we leave board as is
                    aio.pulseOutput(1, 1, window)  # pulse good (OUT1 ON)
                handle_count.plankPass(window)     # update stats

            else:                              # else we have a good board
                aio.pulseOutput(1, 1, window)  # pulse good (OUT1 ON)
                handle_count.plankPass(window) # update stats

            time.sleep(handle_config.AFTER_GRAB)                               # wait after image grab

        else:

            firstRun = True                               # reset "first run" state
            nextSide1Cam1, nextSide1Cam1BarkA, nextSide1Cam1BarkB, nextSide1Cam1BarkC = None, None, None, None
            nextSide1Cam2, nextSide1Cam2BarkA, nextSide1Cam2BarkB, nextSide1Cam2BarkC = None, None, None, None
            side1Cam1, side1Cam1BarkA, side1Cam1BarkB, side1Cam1BarkC = None, None, None, None
            side1Cam2, side1Cam2BarkA, side1Cam2BarkB, side1Cam2BarkC = None, None, None, None
            side2Cam1, side2Cam1BarkA, side2Cam1BarkB, side2Cam1BarkC = None, None, None, None
            side2Cam2, side2Cam2BarkA, side2Cam2BarkB, side2Cam2BarkC = None, None, None, None

            window.find_element('-START-').Update(button_color=sg.theme_button_color()) # turn start button off

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
    # try:
    runProgram(window)
    # except Exception as e:
    #     print('Exception: ', e)

    camera1.release()
    camera2.release()