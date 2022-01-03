'''This module resets the view'''

# my modules
import layouts          # UI Layouts

def main(window):    
    window.find_element('-SIDE-1-CAM-1-').Update('', size=(layouts.half_width, layouts.row_size))
    window.find_element('-SIDE-1-CAM-2-').Update('', size=(layouts.half_width, layouts.row_size))
    window.find_element('-SIDE-2-CAM-1-').Update('', size=(layouts.half_width, layouts.row_size))
    window.find_element('-SIDE-2-CAM-2-').Update('', size=(layouts.half_width, layouts.row_size))

    window.find_element('-%-BARK-1-').update('\nSIDE 1: XX.XX% WHITE')
    window.find_element('-%-BARK-2-').update('\nSIDE 2: XX.XX% WHITE')
    window.find_element('-SIDE1-STATUS-').update('\nXXX', background_color=('blue'))
    window.find_element('-SIDE2-STATUS-').update('\nXXX', background_color=('blue'))