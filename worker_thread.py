'''This module does the heavy lifting, organises the workflow'''

import PySimpleGUI as sg
import time
import keyboard

# my modules
import handle_config    # module to handle config settings
import program_state    # programs State
import camera_setup     # camera setup function
import aio              # handles the aio
import handle_count     # handles count of stats
import reset_view       # clears the UI
import board_logic      # checks if board is pass or fail

global camera

manualTesting = False

if manualTesting:
    camera = camera_setup.StaticImage(0)   # setup static image
else:
    camera = camera_setup.VideoCapture(0)  # setup camera

def waitKey():
    while True:
        if keyboard.is_pressed('y'):
            return True

        if not program_state.RUN_MODE:
            return False

def runProgram(window):
    while not program_state.STOP_PROGRAM:
        if program_state.RUN_MODE:                                             # if running

            aio.setOutput(5, 1, window)                                        # turn running light on (OUT5 ON)
            aio.setOutput(0, 1, window)                                        # flag ready state (OUT0 ON)
            aio.setOutput(2, 1, window)                                        # lift up side 2 (OUT2 ON)

            time.sleep(handle_config.START_DELAY)                              # wait before starting the next loop

            if manualTesting:
                boardIn = waitKey()                                             # wait for board in place
                if not boardIn:
                    continue
            else:
                boardInRH = aio.waitInputState(0, True, window)                  # wait for board side 1 RH
                boardInLH = aio.waitInputState(1, True, window)                  # wait for board side 1 LH
                if not boardInRH or not boardInLH:
                    continue

            reset_view.main(window)                                            # clear images and plank stats

            side1Mid, side1Edges = board_logic.main(camera, 1, window, True)

            aio.pulseOutput(1, 1, window)                                        # pulse flip side 1 (OUT1 ON)

            if manualTesting:
                boardIn = waitKey()                                              # wait for board in place
                if not boardIn:
                    continue
            else:
                boardInRH = aio.waitInputState(2, True, window)                  # wait for board side 2 RH
                boardInLH = aio.waitInputState(3, True, window)                  # wait for board side 2 LH
                if not boardInRH or not boardInLH:
                    continue

            side2Mid, side2Edges = board_logic.main(camera, 2, window, True)

            if side1Mid < handle_config.REJECT_LEVEL and side2Mid < handle_config.REJECT_LEVEL:     # if neither side > 90% white then set reject
                aio.setOutput(7, 1, window)                                                         # set reject flag (OUT7 ON)
                handle_count.plankFail(window)                                                      # update stats

            elif side2Edges + handle_config.EDGE_VARIANCE < side1Edges:                             # if side 1 10% is better
                aio.pulseOutput(3, 1, window)                                                       # pulse flip side 2 (OUT3 ON)
                handle_count.plankPass(window)                                                      # update stats

            else:                                  # if side 2 is better
                aio.pulseOutput(2, 0, window)      # pulse lift up side 2 (OUT2 OFF)
                handle_count.plankPass(window)     # update stats

            time.sleep(handle_config.AFTER_GRAB)                               # wait after image grab

        else:

            window.find_element('-START-').Update(button_color=sg.theme_button_color()) # turn start button off

            if program_state.LIVE_MODE or program_state.THRESH_MODE:
                side1Mid, side1Edges = board_logic.main(camera, 1, window, program_state.LIVE_MODE)
                side2Mid, side2Edges = board_logic.main(camera, 2, window, program_state.LIVE_MODE)
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
    try:
        runProgram(window)
    except Exception as e:
        print('Exception: ', e)

    camera.release()