'''This module handles the count after a plank passes through'''

# my modules
import program_state    # Programs State

# calculate stats and update text
def updateText(window):
    passed_perc = round(program_state.TOTAL_PASSED / program_state.TOTAL_INSPECTED * 100, 2)

    passedStr = '% PASSED:- ' + str(passed_perc)
    window.FindElement('-TOTAL-PASSED-').update(passedStr)
    window.FindElement('-TOTAL-PASSED-').set_size((len(passedStr), 1))

    inspectedStr = 'TOTAL INSPECTED:- ' + str(program_state.TOTAL_INSPECTED)
    window.FindElement('-TOTAL-INSPECTED-').update(inspectedStr)
    window.FindElement('-TOTAL-INSPECTED-').set_size=((len(inspectedStr), 1))

def plankPass(window):
    program_state.increase_total_inspected()    # add to total count
    program_state.increase_total_passed()       # add to passed count
    updateText(window)                          # update stats text

def plankFail(window):    
    program_state.increase_total_inspected()    # add to total count
    updateText(window)                          # update stats text