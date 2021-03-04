'''This module handles the count after a plank passes through'''

# my modules
import program_state    # Programs State

# calculate stats and update text
def updateText(window):
    passed_perc = round(program_state.TOTAL_PASSED / program_state.TOTAL_INSPECTED * 100, 2)
    window.FindElement('-TOTAL-PASSED-').update('% PASSED:- ' + str(passed_perc))
    window.FindElement('-TOTAL-INSPECTED-').update('TOTAL INSPECTED:- ' + str(program_state.TOTAL_INSPECTED))

def plankPass(window):
    program_state.increase_total_inspected()    # add to total count
    program_state.increase_total_passed()       # add to passed count
    updateText(window)                          # update stats text

def plankFail(window):    
    program_state.increase_total_inspected()    # add to total count
    updateText(window)                          # update stats text