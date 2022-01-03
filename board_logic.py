'''This module determines if a given plank is a pass or fail'''

import image_handling
import handle_config

def main(camera1, camera2, side, window, ignoreflags):
    
    frame1 = camera1.read()
    frame2 = camera2.read()

    if side == 1:
        cam1, _, cam1Bark, _ = image_handling.main(frame1, 1, ignoreflags)
        cam2, _, cam2Bark, _ = image_handling.main(frame2, 2, ignoreflags)
    else:
        _, cam1, _, cam1Bark = image_handling.main(frame1, 1, ignoreflags)
        _, cam2, _, cam2Bark = image_handling.main(frame2, 2, ignoreflags)

    window.find_element("-SIDE-{0}-CAM-1-".format(side)).update(data=cam1)  # update img for sides camera 1
    window.find_element("-SIDE-{0}-CAM-2-".format(side)).update(data=cam2)  # update img for sides camera 2

    plankPerc = round((cam1Bark + cam2Bark) / 200 * 100, 2)                 # calculate total plank white percentage

    if plankPerc < handle_config.REJECT_LEVEL:                                                              # if side is a reject show fail
        window.find_element("-SIDE{0}-STATUS-".format(side)).update('\nFAIL', background_color=("red"))
    elif plankPerc < handle_config.BORDERLINE_LEVEL:                                                        # if side is borderline show warning
        window.find_element("-SIDE{0}-STATUS-".format(side)).update('\nBORDERLINE', background_color=("orange"))
    else:                                                                                                   # if side is good show pass
        window.find_element('-SIDE{0}-STATUS-'.format(side)).update('\nPASS', background_color=('green'))

    window.find_element("-%-BARK-{0}-".format(side)).update('\nSIDE ' + str(side) + ': ' + str(plankPerc) + '% WHITE') # update white count
    
    if side == 1:
        return plankPerc, _
    else:
        return _, plankPerc