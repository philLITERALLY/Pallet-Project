'''This module resets the view'''

# my modules
import layouts          # UI Layouts

def main(window):    
    window.FindElement('-SIDE-1-CAM-1-').Update('', size=(layouts.half_width, layouts.row_size))
    window.FindElement('-SIDE-1-CAM-2-').Update('', size=(layouts.half_width, layouts.row_size))
    window.FindElement('-SIDE-2-CAM-1-').Update('', size=(layouts.half_width, layouts.row_size))
    window.FindElement('-SIDE-2-CAM-2-').Update('', size=(layouts.half_width, layouts.row_size))

    window.FindElement('-%-BARK-1-').update('\nSIDE 1:- % BARK XXX')
    window.FindElement('-%-BARK-2-').update('\nSIDE 2:- % BARK XXX')
    window.FindElement('-SIDE1-STATUS-').update('\nXXX', background_color=('blue'))
    window.FindElement('-SIDE2-STATUS-').update('\nXXX', background_color=('blue'))