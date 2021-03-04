'''This module handles all aio'''

import os
import clr # Needed to import AIO dll
import time

# my modules
import program_state  # Programs State
import variables      # Programs Variables

my_path = os.path.abspath(os.path.dirname(__file__))
AIO_DLL = clr.AddReference(my_path + '\AIOWDMNet.dll')

from AIOWDMNet import AIOWDM # pylint: disable=E0401
AIO_INSTANCE = AIOWDM()

try:
    AIO_INSTANCE.RelOutPort(0, 0, 0) # Reset AIO to empty
except Exception as e:
    print(e)

def inputState(inputs, inPort):
    binary = format(inputs, 'b').zfill(9) # get binary for inputs
    reversedBin = binary[::-1]            # reverse binary so 0 input is first        
    return reversedBin[inPort] == '1'     # check if input is 'on'

def waitInputState(inPort, state):
    currentAIO = AIO_INSTANCE.RelInPortB(0, 4)          # Port for listening to flags
    currentInState = inputState(currentAIO, inPort)     # get state of given input

    while currentInState != state:                      # while state of input doesn't equal given state keep checking
        if not program_state.RUN_MODE:                  # if user requests program stop break out of the check
            return False
        
        time.sleep(0.01)                                # sleep before checking inputs again
        
        currentAIO = AIO_INSTANCE.RelInPortB(0, 4)      # Port for listening to flags
        currentInState = inputState(currentAIO, inPort) # get state of given input

    return True                                         # when input matches requested state return true

def getInputState(inPort):
    currentAIO = AIO_INSTANCE.RelInPortB(0, 4)          # Port for listening to flags
    currentInState = inputState(currentAIO, inPort)     # get state of given input
    return currentInState

OUT0 = 0
OUT1 = 0
OUT2 = 0
OUT3 = 0
OUT4 = 0
OUT5 = 0

# Changes IO array to value
def calculateIOValue(values):
    returnVal = values[:]
    returnVal.reverse()                                   # reverse array    
    returnVal = ''.join(map(str, returnVal))              # turn array into string    
    return int(returnVal, 2)                              # return binary string converted to decimal

# Change a given output state
def setOutput(outPort, state):
    global OUT0, OUT1, OUT2, OUT3, OUT4, OUT5

    globals()['OUT' + str(outPort)] = state                         # update global variable to new state

    output = [OUT0, OUT1, OUT2, OUT3, OUT4, OUT5]                   # create output array
    AIO_INSTANCE.RelOutPort(0, 0, calculateIOValue(output))         # send output

# Pulse a given output
def pulseOutput(outPort, state):
    global OUT0, OUT1, OUT2, OUT3, OUT4, OUT5

    initialState = [OUT0, OUT1, OUT2, OUT3, OUT4, OUT5]             # create current state
    pulseState = initialState[:]                                    # clone current state
    pulseState[outPort] = state                                     # modify with pulse value

    AIO_INSTANCE.RelOutPort(0, 0, calculateIOValue(pulseState))     # send pulse state
    time.sleep(variables.AIO_WAIT)                                  # sleep for 100 ms
    AIO_INSTANCE.RelOutPort(0, 0, calculateIOValue(initialState))   # set back to initial state