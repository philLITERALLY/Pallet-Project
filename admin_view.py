'''This module handles the view when in admin mode'''

# my modules
import image_handling   # handles image
import program_state    # module to handle program state
import handle_config    # module to handle config settings

def main(camera1, camera2, window):
    frame1 = camera1.read()
    frame2 = camera2.read()
    
    side1Cam1, side2Cam1, side1Cam1Bark, side2Cam1Bark = image_handling.main(frame1, 1, True)            # process camera 1 no mods
    side1Cam2, side2Cam2, side1Cam2Bark, side2Cam2Bark = image_handling.main(frame2, 2, True)            # process camera 2 no mods

    if program_state.LIVE_MODE:
        window.FindElement('-SIDE-1-CAM-1-').update(data=side1Cam1)                              # update img for side 1 camera 1
        window.FindElement('-SIDE-1-CAM-2-').update(data=side1Cam2)                              # update img for side 1 camera 2
        window.FindElement('-SIDE-2-CAM-1-').update(data=side2Cam1)                               # update img for side 1 camera 1
        window.FindElement('-SIDE-2-CAM-2-').update(data=side2Cam2)                               # update img for side 1 camera 2
    else:
        side1Cam1Mod, side2Cam1Mod, side1Cam1Bark, side2Cam1Bark = image_handling.main(frame1, 1, False) # process camera 1 with mods
        side1Cam2Mod, side2Cam2Mod, side1Cam2Bark, side2Cam2Bark = image_handling.main(frame2, 2, False) # process camera 2 with mods
        window.FindElement('-SIDE-1-CAM-1-').update(data=side1Cam1Mod)                              # update img for side 1 camera 1
        window.FindElement('-SIDE-1-CAM-2-').update(data=side1Cam2Mod)                              # update img for side 1 camera 2
        window.FindElement('-SIDE-2-CAM-1-').update(data=side2Cam1Mod)                               # update img for side 1 camera 1
        window.FindElement('-SIDE-2-CAM-2-').update(data=side2Cam2Mod)                               # update img for side 1 camera 2

    side1Bark = round((side1Cam1Bark + side1Cam2Bark) / 2, 2)
    side2Bark = round((side2Cam1Bark + side2Cam2Bark) / 2, 2)
    
    window.FindElement('-%-BARK-1-').update('\nSIDE 1:- % BARK ' + str(side1Bark))
    window.FindElement('-%-BARK-2-').update('\nSIDE 2:- % BARK ' + str(side2Bark))

    if side1Bark > handle_config.REJECT_LEVEL:
        window.FindElement('-SIDE1-STATUS-').update('\nFAIL', background_color=('red'))
    else:
        window.FindElement('-SIDE1-STATUS-').update('\nPASS', background_color=('green'))

    if side2Bark > handle_config.REJECT_LEVEL:
        window.FindElement('-SIDE2-STATUS-').update('\nFAIL', background_color=('red'))
    else:
        window.FindElement('-SIDE2-STATUS-').update('\nPASS', background_color=('green'))