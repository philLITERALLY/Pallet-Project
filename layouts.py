'''This module contains the UI Layouts'''

import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column

# my modules
import handle_config  # Programs Configuration

default_vert_padding = 3
default_horz_padding = 8
text_pad = 20

# screen_width, screen_height = sg.Window.get_screen_size()
screen_width, screen_height = 1280, 1024

# calculate row size
row_padding = default_vert_padding * 5
row_size = int((screen_height - row_padding) / 3)

# calculate col size
full_width = screen_width - (default_horz_padding * 2)
half_width = int((screen_width - (default_horz_padding * 3)) / 2)

img_width = full_width / 2
col_padding = default_horz_padding * 3
col_width = int((full_width - col_padding) / 4)
sm_col_width = int(col_width * 0.9)
bg_col_width = int(col_width * 1.3)

# view layouts
board_settings = [
    [sg.Image(size=(sm_col_width, 1))], # to help center items
    [sg.Text('BOARD WIDTH')],
    [
        sg.Button('70', key='-WIDTH-70-', size=(4, 2)),
        sg.Button('96', key='-WIDTH-96-', size=(4, 2), button_color=('black', 'yellow')), # default value
        sg.Button('120', key='-WIDTH-120-', size=(4, 2))
    ],
    [sg.Text('BOARD LENGTH')],
    [
        sg.Button('-', key='-LENGTH--', size=(4, 2)),
        sg.Text(handle_config.BOARD_LENGTH, key='-BOARD-LENGTH-'),
        sg.Button('+', key='-LENGTH+-', size=(4, 2))
    ],
]

stats_layout = [
    [sg.Image(size=(sm_col_width, 1))], # to help center items
    [sg.Button('RESET', key='-RESET-', size=(8, 2))],
    [sg.Image(size=(sm_col_width, 20))], # extra padding
    [
        sg.Text('% PASSED:- '),
        sg.Text('0', key='-TOTAL-PASSED-', size=(14, 1))
    ],
    [
        sg.Text('TOTAL INSPECTED:- '),
        sg.Text('0', key='-TOTAL-INSPECTED-', size=(20, 1))
    ],
]

reject_layout = [
    [sg.Image(size=(bg_col_width, 10))], # to help center items
    [sg.Text('REJECT COL A + C || REJECT COLUMN B')],
    [
        sg.Button('-', key='-EDGE-REJECT--', size=(4, 2)),
        sg.Text(str(handle_config.EDGE_REJECT_LEVEL) + '%', key='-EDGE-REJECT-LEVEL-'),
        sg.Button('+', key='-EDGE-REJECT+-', size=(4, 2)),
        sg.Button('-', key='-MID-REJECT--', size=(4, 2)),
        sg.Text(str(handle_config.MID_REJECT_LEVEL) + '%', key='-MID-REJECT-LEVEL-'),
        sg.Button('+', key='-MID-REJECT+-', size=(4, 2))
    ],
    [sg.Image(size=(bg_col_width, 10))], # to help center items
    [
        sg.Button('START', key='-START-', size=(15, 2)),
        sg.Button('STOP', key='-STOP-', size=(15, 2))
    ]
]

setup_layout = [
    [sg.Image(size=(sm_col_width, 10))], # to help center items
    [sg.Button('SETUP', key='-SETUP-', size=(15, 3))],
    [sg.Text('INPUT: 0 0 0 0 0 0 0 0 0', key='-AIO-INPUT-')],
    [sg.Text('OUTPUT: 0 0 0 0 0 0 0 0 0', key='-AIO-OUTPUT-')],
    [sg.Text('', key='-SLEEP-', size=(11, 1))]
]

# admin layouts
admin_mode = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [
        sg.Button('LIVE VIEW', key='-LIVE-MODE-', size=(15, 2)),
        sg.Button('TRANSFORM', key='-TRANSFORM-MODE-', size=(15, 2)),
    ],
    [
        sg.Button('COLUMNS', key='-COLUMN-MODE-', size=(15, 2)),
        sg.Button('BARK', key='-BARK-MODE-', size=(15, 2))
    ],
    [
        sg.Button('CANCEL', key='-CANCEL-', size=(15, 2)),
        sg.Button('SHUT DOWN', key='-SHUT-DOWN-', size=(15, 2), button_color=('black', 'red')),
    ]
]

admin_box1 = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [sg.Text('ALL BOXES', key='-ADMIN-BOX1-TEXT-')],
    [sg.Image(size=(col_width, 10))], # extra padding
    [
        sg.Column([
            [
                sg.Button('-', key='-CAM1-THRESH--', size=(4, 2)),
                sg.Text(' ' + str(handle_config.CAM1_THRESH) + ' ', key='-CAM1-THRESH-', size=(4, 1), justification='c'),
                sg.Button('+', key='-CAM1-THRESH+-', size=(4, 2))
            ]
        ], key='-CAM1-THRESH-LAYOUT-', visible=False),
    ],
]

admin_box2 = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [sg.Text('SELECT BOX', key='-ADMIN-BOX2-TEXT-')],
    [sg.Image(size=(col_width, 10))], # extra padding
    [
        sg.Column([[
            sg.Button('-', key='-CAM2-THRESH--', size=(4, 2)),
                sg.Text(' ' + str(handle_config.CAM2_THRESH) + ' ', key='-CAM2-THRESH-', size=(4, 1), justification='c'),
            sg.Button('+', key='-CAM2-THRESH+-', size=(4, 2))
        ]], key='-CAM2-THRESH-LAYOUT-', visible=False),
    ],
]

boxes_layout = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [        
        sg.Column([
            [
                sg.Button('GRAB', key='-GRAB-', size=(10, 2)),
                sg.Button('CAMERA FLIP', key='-CAMERA-', size=(18, 2)),
            ],
            [sg.Text('FILENAME (W/O FILE TYPE): ', key='-FILENAME-TXT-')],
            [sg.InputText(key='-FILENAME-IN-')],
            [sg.Text('INPUT: 0 0 0 0 0 0 0 0 0', key='-AIO-INPUT-2-')],
            [sg.Text('OUTPUT: 0 0 0 0 0 0 0 0 0', key='-AIO-OUTPUT-2-')],
        ], key='-IO-LAYOUT-', visible=False),
    ]
]

view = False
admin = True

main_layout = [
    [
        sg.Image(key='-SIDE-1-CAM-1-', pad=(0, 0), size=(half_width, row_size)),
        sg.Image(key='-SIDE-1-CAM-2-', pad=(0, 0), size=(half_width, row_size)),
    ],
    [
        sg.Text('\nSIDE 1 (% BARK)  ||  A: XXX  ||  B: XXX  ||  C: XXX', key='-%-BARK-1-', size=(60, 3), justification='center', pad=((0, 200), (0, 0))),
        sg.Text('\nXXX', key='-SIDE1-STATUS-', size=(30, 3), justification='center', background_color=('blue'))
    ],
    [
        sg.Image(key='-SIDE-2-CAM-1-', pad=(0, 0), size=(half_width, row_size)),
        sg.Image(key='-SIDE-2-CAM-2-', pad=(0, 0), size=(half_width, row_size)),
    ],
    [
        sg.Column([[
            sg.Text('\nSIDE 2 (% BARK)  ||  A: XXX  ||  B: XXX  ||  C: XXX', key='-%-BARK-2-', size=(60, 3), justification='center', pad=((0, 200), (0, 0))),
            sg.Text('\nXXX', key='-SIDE2-STATUS-', size=(30, 3), justification='center', background_color=('blue'))
        ]], key='-SIDE2-STATS-')
    ],
    [sg.Image(size=(full_width, 10))], # padding
    [
        # view layout
        sg.Column([[
            sg.Column(setup_layout, element_justification='c', size=(sm_col_width, row_size), visible=True),   # admin setup button
            sg.Column(board_settings, element_justification='c', size=(sm_col_width, row_size)), # board settings (width/height)
            sg.Column(stats_layout, element_justification='c', size=(sm_col_width, row_size)),   # stats of current run
            sg.Column(reject_layout, element_justification='c', size=(bg_col_width, row_size)),  # bark reject settings
        ]], key='-VIEW-LAYOUT-', visible=True),
        # admin layout
        sg.Column([[
            sg.Column(admin_mode, element_justification='c', size=(col_width, row_size)),    # which admin mode
            sg.Column(admin_box1, element_justification='c', size=(col_width, row_size)),  # board 1 settings
            sg.Column(admin_box2, element_justification='c', size=(col_width, row_size)),  # board 2 settings
            sg.Column(boxes_layout, element_justification='c', size=(col_width, row_size)), # cancel setup button
        ]], key='-ADMIN-LAYOUT-', visible=False)
    ],
]

font_size = int(screen_height / 75) # FIX
window = sg.Window(
    'Pallet Project', 
    main_layout, 
    no_titlebar=True, 
    location=(0,0), 
    margins=(0,0),
    size=(screen_width,screen_height), 
    # keep_on_top=True,
    element_justification='center',
    font=('Helvetica', font_size),
    finalize=True
)