'''This module handles the view when in admin mode'''

# my modules
import image_handling   # handles image
import program_state    # Programs State

def main(camera1, camera2, window):
    _, frame1 = camera1.read()
    _, frame2 = camera2.read()
    
    cam1Orig, _ = image_handling.main(frame1, 1, True)                                  # process camera 1 no mods
    cam2Orig, _ = image_handling.main(frame2, 2, True)                                  # process camera 2 no mods

    window.FindElement('-SIDE-1-CAM-1-').update(data=cam1Orig)                           # update img for side 1 camera 1
    window.FindElement('-SIDE-1-CAM-2-').update(data=cam2Orig)                           # update img for side 1 camera 2
    
    cam1Mod, cam1BarkPerc = image_handling.main(frame1, 1, False)                       # process camera 1 with mods
    cam2Mod, cam2BarkPerc = image_handling.main(frame2, 2, False)                       # process camera 2 with mods

    window.FindElement('-SIDE-2-CAM-1-').update(data=cam1Mod)                            # update img for side 1 camera 1
    window.FindElement('-SIDE-2-CAM-2-').update(data=cam2Mod)                            # update img for side 1 camera 2
    
    window.FindElement('-%-BARK-1-').update('\nCAM 1:- % BARK ' + str(cam1BarkPerc))
    window.FindElement('-%-BARK-2-').update('\nCAM 2:- % BARK ' + str(cam2BarkPerc))

    if cam1BarkPerc > program_state.REJECT_LIMIT:
        window.FindElement('-SIDE1-STATUS-').update('\nFAIL', background_color=('red'))
    else:
        window.FindElement('-SIDE1-STATUS-').update('\nPASS', background_color=('green'))

    if cam2BarkPerc > program_state.REJECT_LIMIT:
        window.FindElement('-SIDE2-STATUS-').update('\nFAIL', background_color=('red'))
    else:
        window.FindElement('-SIDE2-STATUS-').update('\nPASS', background_color=('green'))