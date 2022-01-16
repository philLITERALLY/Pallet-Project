'''This module resets the view'''

# my modules
import layouts          # UI Layouts

def main(window):    
    window.find_element('-SIDE-1-').Update('', size=(layouts.full_width, layouts.row_size))
    window.find_element('-SIDE-2-').Update('', size=(layouts.full_width, layouts.row_size))

    window.find_element('-%-BARK-1-').update('SIDE 1\nMID: XX.XX% || EDGES: XX.XX%')
    window.find_element('-%-BARK-2-').update('SIDE 2\nMID: XX.XX% || EDGES: XX.XX%')
    window.find_element('-SIDE1-STATUS-').update('\nXXX', background_color=('blue'))
    window.find_element('-SIDE2-STATUS-').update('\nXXX', background_color=('blue'))