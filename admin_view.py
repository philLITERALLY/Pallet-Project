'''This module handles the view when in admin mode'''

# my modules
import image_handling   # handles image
import program_state    # module to handle program state
import handle_config    # module to handle config settings
import board_logic      # checks if board is pass or fail

def main(camera1, camera2, window):
    reject1Flag, reject2Flag = False, False

    frame1 = camera1.read()
    frame2 = camera2.read()

    # if program_state.LIVE_MODE:
    #     side1Cam1, side2Cam1, \
    #         side1Cam1columnA, side1Cam1columnB, side1Cam1columnC, \
    #         side2Cam1columnA, side2Cam1columnB, side2Cam1columnC = image_handling.main(frame1, 1, True)            # process camera 1 no mods
    #     side1Cam2, side2Cam2, \
    #         side1Cam2columnA, side1Cam2columnB, side1Cam2columnC, \
    #         side2Cam2columnA, side2Cam2columnB, side2Cam2columnC = image_handling.main(frame2, 2, True)            # process camera 2 no mods
    # else:
    side1Cam1, side2Cam1, \
        side1Cam1columnA, side1Cam1columnB, side1Cam1columnC, \
        side2Cam1columnA, side2Cam1columnB, side2Cam1columnC = image_handling.main(frame1, 1, program_state.LIVE_MODE) # process camera 1 mods
    side1Cam2, side2Cam2, \
        side1Cam2columnA, side1Cam2columnB, side1Cam2columnC, \
        side2Cam2columnA, side2Cam2columnB, side2Cam2columnC = image_handling.main(frame2, 2, program_state.LIVE_MODE) # process camera 2 mods

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

    side1failState = []
    side1ColAFlip, side1ColAReject, side1ColAPerc = board_logic.main(side1ColABark, 1, 'A')
    if side1ColAReject:
        side1failState.append('COL A')
        reject1Flag = True
    elif side1ColAFlip:
        side1failState.append('FLIP COL A')

    _, side1ColBReject, side1ColBPerc = board_logic.main(side1ColBBark, 1, 'B')
    if side1ColBReject:
        side1failState.append('COL B')
        reject1Flag = True

    side1ColCFlip, side1ColCReject, side1ColCPerc = board_logic.main(side1ColCBark, 1, 'C')
    if side1ColCReject:
        side1failState.append('COL C')
        reject1Flag = True
    elif side1ColCFlip:
        side1failState.append('FLIP COL C')

    window.find_element('-%-BARK-1-').update('\nSIDE 1 (% BARK)  ||  A: ' + str(side1ColAPerc) + '  ||  B: ' + str(side1ColBPerc) + '  ||  C: ' + str(side1ColCPerc))
    if len(side1failState) > 0:
        colour = 'orange'
        if reject1Flag:
            colour = 'red'
        window.find_element('-SIDE1-STATUS-').update('\n' + ' || '.join(side1failState), background_color=(colour))
    else:
        window.find_element('-SIDE1-STATUS-').update('\nPASS', background_color=('green'))

    side2failState = []
    side2ColAFlip, side2ColAReject, side2ColAPerc = board_logic.main(side2ColABark, 2, 'A')
    if side2ColAReject:
        side2failState.append('COL A')
        reject2Flag = True
    elif side2ColAFlip:
        side2failState.append('FLIP COL A')

    _, side2ColBReject, side2ColBPerc = board_logic.main(side2ColBBark, 2, 'B')
    if side2ColBReject:
        side2failState.append('COL B')
        reject2Flag = True

    side2ColCFlip, side2ColCReject, side2ColCPerc = board_logic.main(side2ColCBark, 2, 'C')
    if side2ColCReject:
        side2failState.append('COL C')
        reject2Flag = True
    elif side2ColCFlip:
        side2failState.append('FLIP COL C')

    window.find_element('-%-BARK-2-').update('\nSIDE 2 (% BARK)  ||  A: ' + str(side2ColAPerc) + '  ||  B: ' + str(side2ColBPerc) + '  ||  C: ' + str(side2ColCPerc))
    if len(side2failState) > 0:
        colour = 'orange'
        if reject2Flag:
            colour = 'red'
        window.find_element('-SIDE2-STATUS-').update('\n' + ' || '.join(side2failState), background_color=(colour))
    else:
        window.find_element('-SIDE2-STATUS-').update('\nPASS', background_color=('green'))