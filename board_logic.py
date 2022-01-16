'''This module determines if a given plank is a pass or fail'''

import image_handling
import handle_config

def calibrate(camera):
    frame = camera.read()
    _, _, \
    side1White, side1A, side1B, side1C, \
    side2White, side2A, side2B, side2C \
        = image_handling.main(frame, True)

    # Update variables
    handle_config.setValue('REJECT SETTINGS', 'SIDE1_PERC', side1White)
    handle_config.setValue('REJECT SETTINGS', 'SIDE1A_PERC', side1A)
    handle_config.setValue('REJECT SETTINGS', 'SIDE1B_PERC', side1B)
    handle_config.setValue('REJECT SETTINGS', 'SIDE1C_PERC', side1C)
    handle_config.setValue('REJECT SETTINGS', 'SIDE2_PERC', side2White)
    handle_config.setValue('REJECT SETTINGS', 'SIDE2A_PERC', side2A)
    handle_config.setValue('REJECT SETTINGS', 'SIDE2B_PERC', side2B)
    handle_config.setValue('REJECT SETTINGS', 'SIDE2C_PERC', side2C)

def main(camera, side, window, ignoreflags):
    
    frame = camera.read()

    if side == 1:
        cam, _, totalWhite, colA, colB, colC, _, _, _, _ = image_handling.main(frame, ignoreflags)
        totalWhite = round(totalWhite / handle_config.SIDE1_PERC * 100, 2)
        colAWhite = round(colA / handle_config.SIDE1A_PERC * 100, 2)
        colBWhite = round(colB / handle_config.SIDE1B_PERC * 100, 2)
        colCWhite = round(colC / handle_config.SIDE1C_PERC * 100, 2)
    else:
        _, cam, _, _, _, _, totalWhite, colA, colB, colC = image_handling.main(frame, ignoreflags)
        totalWhite = round(totalWhite / handle_config.SIDE2_PERC * 100, 2)
        colAWhite = round(colA / handle_config.SIDE2A_PERC * 100, 2)
        colBWhite = round(colB / handle_config.SIDE2B_PERC * 100, 2)
        colCWhite = round(colC / handle_config.SIDE2C_PERC * 100, 2)
    window.find_element("-SIDE-{0}-".format(side)).update(data=cam)                                         # update img for side

    if colBWhite < handle_config.REJECT_LEVEL:                                                              # if side is a reject show fail
        window.find_element("-SIDE{0}-STATUS-".format(side)).update('\nFAIL', background_color=("red"))
    else:                                                                                                   # if side is good show pass
        window.find_element('-SIDE{0}-STATUS-'.format(side)).update('\nPASS', background_color=('green'))
    
    edgesWhite = round((colAWhite + colCWhite) / 2, 2)                                                      # calculate edges total

    window.find_element("-%-BARK-{0}-".format(side)).update('SIDE ' + str(side) + '\nMID: ' + str(colBWhite) + '% || EDGES: ' + str(edgesWhite) + '%') # update white count

    return colBWhite, edgesWhite