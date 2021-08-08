'''This module handles the view when in admin mode'''

# my modules
import image_handling   # handles image
import program_state    # module to handle program state
import handle_config    # module to handle config settings

def main(camera1, camera2, window):
    frame1 = camera1.read()
    frame2 = camera2.read()

    if program_state.LIVE_MODE:
        side1Cam1, side2Cam1, \
            side1Cam1columnAPerc, side1Cam1columnBPerc, side1Cam1columnCPerc, \
            side2Cam1columnAPerc, side2Cam1columnBPerc, side2Cam1columnCPerc = image_handling.main(frame1, 1, True)            # process camera 1 no mods
        side1Cam2, side2Cam2, \
            side1Cam2columnAPerc, side1Cam2columnBPerc, side1Cam2columnCPerc, \
            side2Cam2columnAPerc, side2Cam2columnBPerc, side2Cam2columnCPerc = image_handling.main(frame2, 2, True)            # process camera 2 no mods
    else:
        side1Cam1, side2Cam1, \
            side1Cam1columnAPerc, side1Cam1columnBPerc, side1Cam1columnCPerc, \
            side2Cam1columnAPerc, side2Cam1columnBPerc, side2Cam1columnCPerc = image_handling.main(frame1, 1, False)            # process camera 1 mods
        side1Cam2, side2Cam2, \
            side1Cam2columnAPerc, side1Cam2columnBPerc, side1Cam2columnCPerc, \
            side2Cam2columnAPerc, side2Cam2columnBPerc, side2Cam2columnCPerc = image_handling.main(frame2, 2, False)            # process camera 2 mods

    window.FindElement('-SIDE-1-CAM-1-').update(data=side1Cam1)                              # update img for side 1 camera 1
    window.FindElement('-SIDE-1-CAM-2-').update(data=side1Cam2)                              # update img for side 1 camera 2
    window.FindElement('-SIDE-2-CAM-1-').update(data=side2Cam1)                               # update img for side 1 camera 1
    window.FindElement('-SIDE-2-CAM-2-').update(data=side2Cam2)                               # update img for side 1 camera 2

    side1Bark = round((side1Cam1columnAPerc + side1Cam1columnBPerc + side1Cam1columnCPerc + side1Cam2columnAPerc + side1Cam2columnBPerc + side1Cam2columnCPerc) / 6, 2)
    side2Bark = round((side2Cam1columnAPerc + side2Cam1columnBPerc + side2Cam1columnCPerc + side2Cam2columnAPerc + side2Cam2columnBPerc + side2Cam2columnCPerc) / 6, 2)

    side1ColABark = round((side1Cam1columnAPerc + side1Cam2columnAPerc) / 2, 2)
    side1ColBBark = round((side1Cam1columnBPerc + side1Cam2columnBPerc) / 2, 2)
    side1ColCBark = round((side1Cam1columnCPerc + side1Cam2columnCPerc) / 2, 2)

    side2ColABark = round((side2Cam1columnAPerc + side2Cam2columnAPerc) / 2, 2)
    side2ColBBark = round((side2Cam1columnBPerc + side2Cam2columnBPerc) / 2, 2)
    side2ColCBark = round((side2Cam1columnCPerc + side2Cam2columnCPerc) / 2, 2)
    
    window.FindElement('-%-BARK-1-').update('\nSIDE 1 (% BARK)  ||  COL-A: ' + str(side1ColABark) + '  ||  COL-B: ' + str(side1ColBBark) + '  ||  COL-C: ' + str(side1ColCBark))
    window.FindElement('-%-BARK-2-').update('\nSIDE 2 (% BARK)  ||  COL-A: ' + str(side2ColABark) + '  ||  COL-B: ' + str(side2ColBBark) + '  ||  COL-C: ' + str(side2ColCBark))

    if side1Bark > handle_config.REJECT_LEVEL:
        window.FindElement('-SIDE1-STATUS-').update('\nFAIL', background_color=('red'))
    else:
        window.FindElement('-SIDE1-STATUS-').update('\nPASS', background_color=('green'))

    if side2Bark > handle_config.REJECT_LEVEL:
        window.FindElement('-SIDE2-STATUS-').update('\nFAIL', background_color=('red'))
    else:
        window.FindElement('-SIDE2-STATUS-').update('\nPASS', background_color=('green'))