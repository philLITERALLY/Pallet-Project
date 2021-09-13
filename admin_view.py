'''This module handles the view when in admin mode'''

# my modules
import image_handling   # handles image
import program_state    # module to handle program state
import handle_config    # module to handle config settings

def main(camera1, camera2, window):
    reject1Flag, reject2Flag = False, False

    frame1 = camera1.read()
    frame2 = camera2.read()

    if program_state.LIVE_MODE:
        side1Cam1, side2Cam1, \
            side1Cam1columnA, side1Cam1columnB, side1Cam1columnC, \
            side2Cam1columnA, side2Cam1columnB, side2Cam1columnC = image_handling.main(frame1, 1, True)            # process camera 1 no mods
        side1Cam2, side2Cam2, \
            side1Cam2columnA, side1Cam2columnB, side1Cam2columnC, \
            side2Cam2columnA, side2Cam2columnB, side2Cam2columnC = image_handling.main(frame2, 2, True)            # process camera 2 no mods
    else:
        side1Cam1, side2Cam1, \
            side1Cam1columnA, side1Cam1columnB, side1Cam1columnC, \
            side2Cam1columnA, side2Cam1columnB, side2Cam1columnC = image_handling.main(frame1, 1, False)            # process camera 1 mods
        side1Cam2, side2Cam2, \
            side1Cam2columnA, side1Cam2columnB, side1Cam2columnC, \
            side2Cam2columnA, side2Cam2columnB, side2Cam2columnC = image_handling.main(frame2, 2, False)            # process camera 2 mods

    window.find_element('-SIDE-1-CAM-1-').update(data=side1Cam1)                              # update img for side 1 camera 1
    window.find_element('-SIDE-1-CAM-2-').update(data=side1Cam2)                              # update img for side 1 camera 2
    window.find_element('-SIDE-2-CAM-1-').update(data=side2Cam1)                               # update img for side 1 camera 1
    window.find_element('-SIDE-2-CAM-2-').update(data=side2Cam2)                               # update img for side 1 camera 2

    side1Bark = round((side1Cam1columnA + side1Cam1columnB + side1Cam1columnC + side1Cam2columnA + side1Cam2columnB + side1Cam2columnC) / 6, 2)
    side2Bark = round((side2Cam1columnA + side2Cam1columnB + side2Cam1columnC + side2Cam2columnA + side2Cam2columnB + side2Cam2columnC) / 6, 2)

    side1ColABark = round((side1Cam1columnA + side1Cam2columnA) / 2, 2)
    side1ColBBark = round((side1Cam1columnB + side1Cam2columnB) / 2, 2)
    side1ColCBark = round((side1Cam1columnC + side1Cam2columnC) / 2, 2)

    side2ColABark = round((side2Cam1columnA + side2Cam2columnA) / 2, 2)
    side2ColBBark = round((side2Cam1columnB + side2Cam2columnB) / 2, 2)
    side2ColCBark = round((side2Cam1columnC + side2Cam2columnC) / 2, 2)
    
    window.find_element('-%-BARK-1-').update('\nSIDE 1 (% BARK)  ||  A: ' + str(side1ColABark) + '  ||  B: ' + str(side1ColBBark) + '  ||  C: ' + str(side1ColCBark))
    window.find_element('-%-BARK-2-').update('\nSIDE 2 (% BARK)  ||  A: ' + str(side2ColABark) + '  ||  B: ' + str(side2ColBBark) + '  ||  C: ' + str(side2ColCBark))

    side1failState = []
    if side1ColABark > handle_config.EDGE_REJECT_LEVEL:
        side1failState.append('COL A')
        reject1Flag = True
    elif side1ColABark > handle_config.EDGE_FLIP_LEVEL:
        side1failState.append('FLIP COL A')

    if side1ColBBark > handle_config.MID_REJECT_LEVEL:
        side1failState.append('COL B')
        reject1Flag = True

    if side1ColCBark > handle_config.EDGE_REJECT_LEVEL:
        side1failState.append('COL C')
        reject1Flag = True
    elif side1ColCBark > handle_config.EDGE_FLIP_LEVEL:
        side1failState.append('FLIP COL C')

    if len(side1failState) > 0:
        colour = 'orange'
        if reject1Flag:
            colour = 'red'
        window.find_element('-SIDE1-STATUS-').update('\n' + ' || '.join(side1failState), background_color=(colour))
    else:
        window.find_element('-SIDE1-STATUS-').update('\nPASS', background_color=('green'))

    side2failState = []
    if side2ColABark > handle_config.EDGE_REJECT_LEVEL:
        side2failState.append('COL A')
        reject2Flag = True
    elif side2ColABark > handle_config.EDGE_FLIP_LEVEL:
        side2failState.append('FLIP COL A')

    if side2ColBBark > handle_config.MID_REJECT_LEVEL:
        side2failState.append('COL B')
        reject2Flag = True

    if side2ColCBark > handle_config.EDGE_REJECT_LEVEL:
        side2failState.append('COL C')
        reject2Flag = True
    elif side2ColCBark > handle_config.EDGE_FLIP_LEVEL:
        side2failState.append('FLIP COL C')

    if len(side2failState) > 0:
        colour = 'orange'
        if reject2Flag:
            colour = 'red'
        window.find_element('-SIDE2-STATUS-').update('\n' + ' || '.join(side2failState), background_color=(colour))
    else:
        window.find_element('-SIDE2-STATUS-').update('\nPASS', background_color=('green'))