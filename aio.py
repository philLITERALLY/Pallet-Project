'''This module handles all aio'''

import os
import clr # Needed to import AIO dll

# my modules
import program_state    # Programs State

my_path = os.path.abspath(os.path.dirname(__file__))
AIO_DLL = clr.AddReference(my_path + '/AIOWDMNet.dll')

from AIOWDMNet import AIOWDM # pylint: disable=E0401
AIO_INSTANCE = AIOWDM()
AIO_INSTANCE.RelOutPort(0, 0, 0) # Reset AIO to empty

def waitPulse(input, state):
    currentState = None
    while currentState != state:
        if not program_state.RUN_MODE:
            return False
        time.sleep(0.01)

    return True