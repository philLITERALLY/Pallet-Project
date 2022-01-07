'''This module determines if a given plank is a pass or fail'''

import image_handling
import handle_config

def calibrate(camera):
    frame = camera.read()
    _, _, side1CamWhite, side2CamWhite = image_handling.main(frame, True)

    # Update variables
    handle_config.setValue('REJECT SETTINGS', 'SIDE1_PERC', side1CamWhite)
    handle_config.setValue('REJECT SETTINGS', 'SIDE2_PERC', side2CamWhite)

def main(camera, side, window, ignoreflags):
    
    frame = camera.read()

    if side == 1:
        cam, _, camWhite, _ = image_handling.main(frame, ignoreflags)
        camWhite = round(camWhite / handle_config.SIDE1_PERC * 100, 2)
    else:
        _, cam, _, camWhite = image_handling.main(frame, ignoreflags)
        camWhite = round(camWhite / handle_config.SIDE2_PERC * 100, 2)

    window.find_element("-SIDE-{0}-".format(side)).update(data=cam)  # update img for side

    if camWhite < handle_config.REJECT_LEVEL:                                                              # if side is a reject show fail
        window.find_element("-SIDE{0}-STATUS-".format(side)).update('\nFAIL', background_color=("red"))
    elif camWhite < handle_config.BORDERLINE_LEVEL:                                                        # if side is borderline show warning
        window.find_element("-SIDE{0}-STATUS-".format(side)).update('\nBORDERLINE', background_color=("orange"))
    else:                                                                                                   # if side is good show pass
        window.find_element('-SIDE{0}-STATUS-'.format(side)).update('\nPASS', background_color=('green'))

    window.find_element("-%-BARK-{0}-".format(side)).update('\nSIDE ' + str(side) + ': ' + str(camWhite) + '% WHITE') # update white count
    
    if side == 1:
        return camWhite, _
    else:
        return _, camWhite