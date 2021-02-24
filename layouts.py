'''This module contains the UI Layouts'''

import PySimpleGUI as sg

default_vert_padding = 3
default_horz_padding = 8
text_pad = 20

screen_width, screen_height = sg.Window.get_screen_size()

# calculate row size
row_padding = default_vert_padding * 5
row_size = int((screen_height - row_padding) / 5)

# calculate col size
full_width = screen_width - (default_horz_padding * 2)

col_padding = default_horz_padding * 3
col_width = int((full_width - col_padding) / 4)

side1_layout = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [sg.Text('SIDE 1')],
    [
        sg.Text('% BARK\t\t'),
        sg.Text('100%', key='-%-BARK-1-')
    ],
    [
        sg.Text('% REJECT\t'), 
        sg.Text('100%', key='-%-REJECT-1-')
    ],
]

side2_layout = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [sg.Text('SIDE 2')],
    [
        sg.Text('% BARK\t\t'),
        sg.Text('100%', key='-%-BARK-2-')
    ],
    [
        sg.Text('% REJECT\t'), 
        sg.Text('100%', key='-%-REJECT-2-')
    ],
]

reject_layout = [
    [
        sg.Button('START', key='-START-'),
        sg.Button('STOP', key='-STOP-')
    ],
    [sg.Image(size=(col_width, 10))], # to help center items
    [sg.Text('WHICH SIDE')], # REJECT LEVEL')],
    [
        sg.Button('-', key='-REJECT--', size=(4, 2)),
        sg.Text('0', key='-REJECT-LEVEL-'),
        sg.Button('+', key='-REJECT+-', size=(4, 2))
    ],
]

button_layout = [
    # [sg.Button('RESET COUNT', key='-RESET-', size=(15, 4))]
    [sg.Image(size=(col_width, 1))], # to help center items
    [sg.Text('INPUTS')],
    [
        sg.Button('R', key='-IN-0-'),
        sg.Button('L', key='-IN-1-'),
        sg.Button('DWN', key='-IN-2-'),
        sg.Button('UP', key='-IN-3-'),
        sg.Button('CCW', key='-IN-4-', button_color=('black', 'yellow'))
    ],
    [
        sg.Button('CW', key='-IN-5-'),
        sg.Button('OPN', key='-IN-6-'),
        sg.Button('CLDR', key='-IN-7-'),
        sg.Button('CLDL', key='-IN-8-')
    ],
    [sg.Text('OUTPUTS')],
    [
        sg.Button('CVYR', key='-OUT-0-'),
        sg.Button('CLMP', key='-OUT-1-'),
        sg.Button('LIFT', key='-OUT-2-'),
        sg.Button('ROT', key='-OUT-3-'),
        sg.Button('REJ', key='-OUT-4-'),
        sg.Button('FLT', key='-OUT-5-')
    ]
]

main_layout = [
    [sg.Image(key='-SIDE-1-CAM-1-', size=(full_width, row_size))],
    [sg.Image(key='-SIDE-1-CAM-2-', size=(full_width, row_size))],
    [sg.Image(key='-SIDE-2-CAM-1-', size=(full_width, row_size))],
    [sg.Image(key='-SIDE-2-CAM-2-', size=(full_width, row_size))],
    [
        sg.Column(side1_layout, element_justification='c', size=(col_width, row_size)),
        sg.Column(side2_layout, element_justification='c', size=(col_width, row_size)),
        sg.Column(reject_layout, element_justification='c', size=(col_width, row_size)),
        sg.Column(button_layout, element_justification='c', size=(col_width, row_size)),
    ],
]

font_size = int(screen_height / 75) # FIX
sg.theme('Light Brown 3')
window = sg.Window(
    'Pallet Project', 
    main_layout, 
    no_titlebar=True, 
    location=(0,0), 
    size=(screen_width,screen_height), 
    # keep_on_top=True,
    element_justification='center',
    font=("Helvetica", font_size),
    finalize=True
)