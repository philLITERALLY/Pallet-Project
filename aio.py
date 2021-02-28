'''This module handles all aio'''

import os
import clr # Needed to import AIO dll
import random
import time

# my modules
import program_state    # Programs State

my_path = os.path.abspath(os.path.dirname(__file__))
AIO_DLL = clr.AddReference(my_path + '\AIOWDMNet.dll')

from AIOWDMNet import AIOWDM # pylint: disable=E0401
AIO_INSTANCE = AIOWDM()
AIO_INSTANCE.RelOutPort(0, 0, 0) # Reset AIO to empty

def inputState(inputs, inPort):
    binary = format(inputs, 'b').zfill(9) # get binary for inputs
    reversedBin = binary[::-1]            # reverse binary so 0 input is first        
    return reversedBin[inPort] == '1'     # check if input is "on"

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