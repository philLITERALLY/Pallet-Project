'''This module contains the UI Layouts'''

import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column

default_vert_padding = 3
default_horz_padding = 8
text_pad = 20

screen_width, screen_height = sg.Window.get_screen_size()

# calculate row size
row_padding = default_vert_padding * 5
row_size = int((screen_height - row_padding) / 3)

# calculate col size
full_width = screen_width - (default_horz_padding * 2)
half_width = int((screen_width - (default_horz_padding * 3)) / 2)

img_width = full_width / 2
col_padding = default_horz_padding * 3
col_width = int((full_width - col_padding) / 4)

# view layouts
board_settings = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [sg.Text('BOARD WIDTH')],
    [
        sg.Button('70', key='-WIDTH-70-', size=(4, 2)),
        sg.Button('96', key='-WIDTH-96-', size=(4, 2), button_color=('black', 'yellow')), # default value
        sg.Button('120', key='-WIDTH-120-', size=(4, 2))
    ],
    [sg.Text('BOARD LENGTH')],
    [
        sg.Button('-', key='-LENGTH--', size=(4, 2)),
        sg.Text('1200', key='-BOARD-LENGTH-'),
        sg.Button('+', key='-LENGTH+-', size=(4, 2))
    ],
]

stats_layout = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [sg.Button('RESET', key='-RESET-', size=(8, 2))],
    [sg.Image(size=(col_width, 20))], # extra padding
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
    [sg.Image(size=(col_width, 10))], # to help center items
    [sg.Text('REJECT LEVEL')],
    [
        sg.Button('-', key='-REJECT--', size=(4, 2)),
        sg.Text('10%', key='-REJECT-LEVEL-'),
        sg.Button('+', key='-REJECT+-', size=(4, 2))
    ],
    [sg.Image(size=(col_width, 10))], # to help center items
    [
        sg.Button('START', key='-START-'),
        sg.Button('STOP', key='-STOP-')
    ]
]

setup_layout = [
    [sg.Image(size=(col_width, 10))], # to help center items
    [sg.Button('SETUP', key='-SETUP-', size=(15, 3))],
    [sg.Text('INPUT: 0 0 0 0 0 0 0 0 0', key='-AIO-INPUT-')],
    [sg.Text('OUTPUT: 0 0 0 0 0 0 ... 0', key='-AIO-OUTPUT-')],
    [sg.Text('', key='-SLEEP-', size=(11, 1))]
]

# admin layouts
admin_mode = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [sg.Button('TRANSFORM', key='-TRANSFORM-MODE-', size=(15, 2))],
    [sg.Button('BOXES', key='-BOXES-MODE-', size=(15, 2))],
    [sg.Button('THRESH', key='-THRESH-MODE-', size=(15, 2))]
]

board1_admin = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [sg.Text('CAM 1')],
    [sg.Image(size=(col_width, 20))], # extra padding
    [
        sg.Column([
            [
                sg.Text('TOP', size=(6, 1), justification='left'),
                sg.Button('-', key='-CAM1-TOP--', size=(4, 2)),
                sg.Text('90', key='-CAM1-TOP-', size=(4, 1), justification='c'),
                sg.Button('+', key='-CAM1-TOP+-', size=(4, 2))
            ], [
                sg.Text('BOT', size=(6, 1), justification='left'),
                sg.Button('-', key='-CAM1-BOT--', size=(4, 2)),
                sg.Text('60', key='-CAM1-BOT-', size=(4, 1), justification='c'),
                sg.Button('+', key='-CAM1-BOT+-', size=(4, 2))
            ]
        ], key='-CAM1-TRANSFORM-LAYOUT-', visible=False),
        sg.Column([[
            sg.Button('<', key='-CAM1-LEFT-', size=(4, 2)),
            sg.Column([
                [sg.Button('^', key='-CAM1-UP-', size=(4, 2))],
                [sg.Button('v', key='-CAM1-DOWN-', size=(4, 2))]
            ], element_justification='c'),
            sg.Button('>', key='-CAM1-RIGHT-', size=(4, 2))
        ]], key='-CAM1-BOXES-LAYOUT-', visible=False),
        sg.Column([[
            sg.Button('-', key='-CAM1-THRESH--', size=(4, 2)),
            sg.Text(' 0 ', key='-CAM1-THRESH-', size=(4, 1), justification='c'),
            sg.Button('+', key='-CAM1-THRESH+-', size=(4, 2))
        ]], key='-CAM1-THRESH-LAYOUT-', visible=False)
    ],
]

board2_admin = [
    [sg.Image(size=(col_width, 1))], # to help center items
    [sg.Text('CAM 2')],
    [sg.Image(size=(col_width, 20))], # extra padding
    [
        sg.Column([
            [
                sg.Text('TOP', size=(6, 1), justification='left'),
                sg.Button('-', key='-CAM2-TOP--', size=(4, 2)),
                sg.Text('85', key='-CAM2-TOP-', size=(4, 1), justification='c'),
                sg.Button('+', key='-CAM2-TOP+-', size=(4, 2))
            ], [
                sg.Text('BOT', size=(6, 1), justification='left'),
                sg.Button('-', key='-CAM2-BOT--', size=(4, 2)),
                sg.Text('110', key='-CAM2-BOT-', size=(4, 1), justification='c'),
                sg.Button('+', key='-CAM2-BOT+-', size=(4, 2))
            ]
        ], key='-CAM2-TRANSFORM-LAYOUT-', visible=False),
        sg.Column([[
            sg.Button('<', key='-CAM2-LEFT-', size=(4, 2)),
            sg.Column([
                [sg.Button('^', key='-CAM2-UP-', size=(4, 2))],
                [sg.Button('v', key='-CAM2-DOWN-', size=(4, 2))]
            ], element_justification='c'),
            sg.Button('>', key='-CAM2-RIGHT-', size=(4, 2))
        ]], key='-CAM2-BOXES-LAYOUT-', visible=False),
        sg.Column([[
            sg.Button('-', key='-CAM2-THRESH--', size=(4, 2)),
            sg.Text(' 0 ', key='-CAM2-THRESH-', size=(4, 1), justification='c'),
            sg.Button('+', key='-CAM2-THRESH+-', size=(4, 2))
        ]], key='-CAM2-THRESH-LAYOUT-', visible=False)
    ],
]

cancel_layout = [
    [sg.Image(size=(col_width, 10))], # to help center items
    [sg.Button('CANCEL', key='-CANCEL-', size=(15, 5))]
]

view = False
admin = True

main_layout = [
    [
        sg.Image(key='-SIDE-1-CAM-1-', pad=(0, 0), size=(half_width, row_size)),
        sg.Image(key='-SIDE-1-CAM-2-', pad=(0, 0), size=(half_width, row_size)),
    ],
    [
        sg.Text('\nSIDE 1:- % BARK XXX', key='-%-BARK-1-', size=(30, 3), justification='center', pad=((0, 200), (0, 0))),
        sg.Text('\nXXX', key='-SIDE1-STATUS-', size=(30, 3), justification='center', background_color=('blue'))
    ],
    [
        sg.Image(key='-SIDE-2-CAM-1-', pad=(0, 0), size=(half_width, row_size)),
        sg.Image(key='-SIDE-2-CAM-2-', pad=(0, 0), size=(half_width, row_size)),
    ],
    [
        sg.Column([[
            sg.Text('\nSIDE 2:- % BARK XXX', key='-%-BARK-2-', size=(30, 3), justification='center', pad=((0, 200), (0, 0))),
            sg.Text('\nXXX', key='-SIDE2-STATUS-', size=(30, 3), justification='center', background_color=('blue'))
        ]], key='-SIDE2-STATS-')
    ],
    [sg.Image(size=(full_width, 10))], # padding
    [
        # view layout
        sg.Column([[
            sg.Column(setup_layout, element_justification='c', size=(col_width, row_size), visible=True),   # admin setup button
            sg.Column(board_settings, element_justification='c', size=(col_width, row_size)), # board settings (width/height)
            sg.Column(stats_layout, element_justification='c', size=(col_width, row_size)),   # stats of current run
            sg.Column(reject_layout, element_justification='c', size=(col_width, row_size)),  # bark reject settings
        ]], key='-VIEW-LAYOUT-', visible=True),
        # admin layout
        sg.Column([[
            sg.Column(admin_mode, element_justification='c', size=(col_width, row_size)),    # which admin mode
            sg.Column(board1_admin, element_justification='c', size=(col_width, row_size)),  # board 1 settings
            sg.Column(board2_admin, element_justification='c', size=(col_width, row_size)),  # board 2 settings
            sg.Column(cancel_layout, element_justification='c', size=(col_width, row_size)), # cancel setup button
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