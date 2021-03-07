'''This module handles all aio'''

import os
import clr # Needed to import AIO dll
import time

# my modules
import program_state  # Programs State
import variables      # Programs Variables

import mock_aio

my_path = os.path.abspath(os.path.dirname(__file__))
AIO_DLL = clr.AddReference(my_path + '\AIOWDMNet.dll')

from AIOWDMNet import AIOWDM # pylint: disable=E0401
AIO_INSTANCE = AIOWDM()

IN_STATE = [0, 0, 0, 0, 0, 0, 0, 0, 0]
OUT_STATE = [0, 0, 0, 0, 0, 0, 0]

try:
    AIO_INSTANCE.RelOutPort(0, 0, 0) # Reset AIO to empty
except Exception as e:
    print('Using mock AIO')
    AIO_INSTANCE = mock_aio          # use mock aio so program doesn't crash

def updateInState(window):
    inStr = 'INPUT: ' + \
        str(IN_STATE[0]) + ' ' + \
        str(IN_STATE[1]) + ' ' + \
        str(IN_STATE[2]) + ' ' + \
        str(IN_STATE[3]) + ' ' + \
        str(IN_STATE[4]) + ' ' + \
        str(IN_STATE[5]) + ' ' + \
        str(IN_STATE[6]) + ' ' + \
        str(IN_STATE[7]) + ' ' + \
        str(IN_STATE[8])
    print(inStr)
    window.FindElement('-AIO-INPUT-').update(inStr)

def updateOutState(window):
    outStr = 'OUTPUT: ' + \
        str(OUT_STATE[0]) + ' ' + \
        str(OUT_STATE[1]) + ' ' + \
        str(OUT_STATE[2]) + ' ' + \
        str(OUT_STATE[3]) + ' ' + \
        str(OUT_STATE[4]) + ' ' + \
        str(OUT_STATE[5]) + ' ... ' + \
        str(OUT_STATE[6])
    print(outStr)
    window.FindElement('-AIO-OUTPUT-').update(outStr)

def inputState(inputs, inPort):
    binary = format(inputs, 'b').zfill(9) # get binary for inputs
    reversedBin = binary[::-1]            # reverse binary so 0 input is first        
    return reversedBin[inPort] == '1'     # check if input is 'on'

def waitInputState(inPort, state, window):
    currentAIO = AIO_INSTANCE.RelInPortB(0, 4)          # Port for listening to flags
    currentInState = inputState(currentAIO, inPort)     # get state of given input
    IN_STATE[inPort] = currentInState
    updateInState(window)

    while currentInState != state:                      # while state of input doesn't equal given state keep checking
        if not program_state.RUN_MODE:                  # if user requests program stop break out of the check
            return False
        
        time.sleep(0.01)                                # sleep before checking inputs again
        
        currentAIO = AIO_INSTANCE.RelInPortB(0, 4)      # Port for listening to flags
        currentInState = inputState(currentAIO, inPort) # get state of given input
        IN_STATE[inPort] = currentInState
        updateInState(window)

    return True                                         # when input matches requested state return true

def getInputState(inPort, window):
    currentAIO = AIO_INSTANCE.RelInPortB(0, 4)          # Port for listening to flags
    currentInState = inputState(currentAIO, inPort)     # get state of given input
    IN_STATE[inPort] = currentInState
    updateInState(window)
    return currentInState

OUT0 = 0
OUT1 = 0
OUT2 = 0
OUT3 = 0
OUT4 = 0
OUT5 = 0
OUT10 = 0

# Changes IO array to value
def calculateIOValue(values):
    returnVal = values[:]
    returnVal.reverse()                                   # reverse array    
    returnVal = ''.join(map(str, returnVal))              # turn array into string    
    return int(returnVal, 2)                              # return binary string converted to decimal

# Change a given output state
def setOutput(outPort, state, window):
    global OUT0, OUT1, OUT2, OUT3, OUT4, OUT5, OUT10

    globals()['OUT' + str(outPort)] = state                          # update global variable to new state
    OUT_STATE[outPort] = state

    output = [OUT0, OUT1, OUT2, OUT3, OUT4, OUT5, 0, 0, 0, 0, OUT10] # create output array
    AIO_INSTANCE.RelOutPort(0, 0, calculateIOValue(output))          # send output
    updateOutState(window)

# Pulse a given output
def pulseOutput(outPort, state, window):
    global OUT0, OUT1, OUT2, OUT3, OUT4, OUT5, OUT10

    initialState = [OUT0, OUT1, OUT2, OUT3, OUT4, OUT5, 0, 0, 0, 0, OUT10] # create current state
    pulseState = initialState[:]                                           # clone current state
    pulseState[outPort] = state                                            # modify with pulse value

    AIO_INSTANCE.RelOutPort(0, 0, calculateIOValue(pulseState))            # send pulse state
    OUT_STATE[outPort] = state
    updateOutState(window)
    time.sleep(variables.AIO_WAIT)                                         # sleep for 100 ms
    AIO_INSTANCE.RelOutPort(0, 0, calculateIOValue(initialState))          # set back to initial state
    OUT_STATE[outPort] = state
    updateOutState(window)