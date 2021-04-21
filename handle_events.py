
import PySimpleGUI as sg

# my modules
import program_state    # Programs State
import admin_settings   # Admin settings
import handle_config    # Programs Configuration

def updateBoxDetailsText(window, side):
    # Figure out what CAM and BOX we're on
    cam = 1
    box = program_state.CAM1_BOX_MODIFY
    if program_state.CAM2_BOX_MODIFY != None:
        cam = 2
        box = program_state.CAM2_BOX_MODIFY

    # Get boxes details
    leftPos = getattr(handle_config, 'SIDE' + str(side) + '_CAM' + str(cam) + '_BOX' + str(box) + '_LEFT')
    rightPos = getattr(handle_config, 'SIDE' + str(side) + '_CAM' + str(cam) + '_BOX' + str(box) + '_RIGHT')

    # Update text for what width of box we're modifying
    window.FindElement('-SIDE' + str(side) + '-BOX-WIDTH-').Update(str(rightPos - leftPos))

    # Update text for what start position of box we're modifying
    window.FindElement('-SIDE' + str(side) + '-BOX-POS-').Update(str(leftPos))

def admin(event, window):
    window.FindElement('-TRANSFORM-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-BOXES-1-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-BOXES-2-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-BARK-MODE-').Update(button_color=sg.theme_button_color())
    window.FindElement('-CAM1-TRANSFORM-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM2-TRANSFORM-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM1-THRESH-LAYOUT-').Update(visible=False)
    window.FindElement('-CAM2-THRESH-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE1-VERTICAL-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE2-VERTICAL-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE1-BOX-SELECT-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE2-BOX-SELECT-LAYOUT-').Update(visible=False)
    window.FindElement('-BOX-POS-TEXT-').Update(visible=False)
    window.FindElement('-SIDE1-BOXES-LAYOUT-').Update(visible=False)
    window.FindElement('-SIDE2-BOXES-LAYOUT-').Update(visible=False)
    window.FindElement('-ADMIN-BOX1-TEXT-').Update('CAM 1')
    window.FindElement('-ADMIN-BOX2-TEXT-').Update('CAM 2')
        
    # When the setup button is pressed
    if event == '-SETUP-':
        # change to admin view
        window.FindElement('-VIEW-LAYOUT-').Update(visible=False)
        window.FindElement('-ADMIN-LAYOUT-').Update(visible=True)
        
        # default state to transform mode
        program_state.set_transform(True)

        # turn transform button on
        window.FindElement('-TRANSFORM-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-TRANSFORM-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-TRANSFORM-LAYOUT-').Update(visible=True)
        
    # When the cancel button is pressed
    if event == '-CANCEL-':
        window.FindElement('-VIEW-LAYOUT-').Update(visible=True)
        window.FindElement('-ADMIN-LAYOUT-').Update(visible=False)
        
        # make sure admin modes are off
        program_state.set_thresh_boxes_1(False)
        program_state.set_thresh(False)
        program_state.set_thresh_boxes_2(False)
        program_state.set_transform(False)

    # When transform mode button is pressed
    if event == '-TRANSFORM-MODE-':
        program_state.set_transform(True)     # turn on transform view mode

        # turn transform button on
        window.FindElement('-TRANSFORM-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-TRANSFORM-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-TRANSFORM-LAYOUT-').Update(visible=True)

    # When bark thresh mode button is pressed
    if event == '-BARK-MODE-':
        program_state.set_thresh(True)       # turn on box thresh mode

        # turn thresh button on
        window.FindElement('-BARK-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-CAM1-THRESH-LAYOUT-').Update(visible=True)
        window.FindElement('-CAM2-THRESH-LAYOUT-').Update(visible=True)

    # When boxes mode button is pressed
    if event == '-BOXES-1-MODE-':
        program_state.set_thresh_boxes_1(True)  # turn on boxes mode

        # turn boxes button on
        window.FindElement('-BOXES-1-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-ADMIN-BOX1-TEXT-').Update('ALL BOXES')
        window.FindElement('-ADMIN-BOX2-TEXT-').Update('SELECT BOX')
        window.FindElement('-SIDE1-VERTICAL-LAYOUT-').Update(visible=True)
        window.FindElement('-SIDE1-BOX-SELECT-LAYOUT-').Update(visible=True)
        window.FindElement('-SIDE1-BOXES-LAYOUT-').Update(visible=True)
        window.FindElement('-BOX-POS-TEXT-').Update(visible=True)
        
        # Get boxes details
        leftPos = getattr(handle_config, 'SIDE1_CAM1_BOX0_LEFT')
        rightPos = getattr(handle_config, 'SIDE1_CAM1_BOX0_RIGHT')
        window.FindElement('-SIDE1-BOX-').Update('0')
        window.FindElement('-SIDE1-BOX-WIDTH-').Update(str(rightPos - leftPos))
        window.FindElement('-SIDE1-BOX-POS-').Update(str(leftPos))

    # When boxes 2 mode button is pressed
    if event == '-BOXES-2-MODE-':
        program_state.set_thresh_boxes_2(True)       # turn on line thresh mode

        # turn thresh button on
        window.FindElement('-BOXES-2-MODE-').Update(button_color=('black', 'yellow'))
        window.FindElement('-ADMIN-BOX1-TEXT-').Update('ALL BOXES')
        window.FindElement('-ADMIN-BOX2-TEXT-').Update('SELECT BOX')
        window.FindElement('-SIDE2-VERTICAL-LAYOUT-').Update(visible=True)
        window.FindElement('-SIDE2-BOX-SELECT-LAYOUT-').Update(visible=True)
        window.FindElement('-SIDE2-BOXES-LAYOUT-').Update(visible=True)
        window.FindElement('-BOX-POS-TEXT-').Update(visible=True)

        # Get boxes details
        leftPos = getattr(handle_config, 'SIDE2_CAM1_BOX0_LEFT')
        rightPos = getattr(handle_config, 'SIDE2_CAM1_BOX0_RIGHT')
        window.FindElement('-SIDE2-BOX-').Update('0')
        window.FindElement('-SIDE2-BOX-WIDTH-').Update(str(rightPos - leftPos))
        window.FindElement('-SIDE2-BOX-POS-').Update(str(leftPos))

def board(event, window):
    if event == '-WIDTH-70-': # 70
        admin_settings.set_board_width(-52)
        window.FindElement('-WIDTH-70-').Update(button_color=('black', 'yellow'))

        window.FindElement('-WIDTH-96-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-120-').Update(button_color=sg.theme_button_color())
    
    if event == '-WIDTH-96-':
        admin_settings.set_board_width(0) # 0 is neutral
        window.FindElement('-WIDTH-96-').Update(button_color=('black', 'yellow'))
        
        window.FindElement('-WIDTH-70-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-120-').Update(button_color=sg.theme_button_color())
    
    if event == '-WIDTH-120-':
        admin_settings.set_board_width(47)
        window.FindElement('-WIDTH-120-').Update(button_color=('black', 'yellow'))
        
        window.FindElement('-WIDTH-70-').Update(button_color=sg.theme_button_color())
        window.FindElement('-WIDTH-96-').Update(button_color=sg.theme_button_color())

    if event == '-LENGTH--':
        newLength = admin_settings.BOARD_LENGTH - 10
        admin_settings.set_board_length(newLength)
        window.FindElement('-BOARD-LENGTH-').update(str(newLength))

    if event == '-LENGTH+-':
        newLength = admin_settings.BOARD_LENGTH + 10
        admin_settings.set_board_length(newLength)
        window.FindElement('-BOARD-LENGTH-').update(str(newLength))

def transform(event, window):
    if event == '-CAM1-TOP--':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM1_TRANS_RIGHT', handle_config.CAM1_TRANS_RIGHT + 2)

    if event == '-CAM1-TOP+-':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM1_TRANS_RIGHT', handle_config.CAM1_TRANS_RIGHT - 2)

    if event == '-CAM1-BOT--':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM1_TRANS_LEFT', handle_config.CAM1_TRANS_LEFT - 2)

    if event == '-CAM1-BOT+-':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM1_TRANS_LEFT', handle_config.CAM1_TRANS_LEFT + 2)

    if event == '-CAM2-TOP--':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM2_TRANS_LEFT', handle_config.CAM2_TRANS_LEFT + 2)

    if event == '-CAM2-TOP+-':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM2_TRANS_LEFT', handle_config.CAM2_TRANS_LEFT - 2)

    if event == '-CAM2-BOT--':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM2_TRANS_RIGHT', handle_config.CAM2_TRANS_RIGHT - 2)

    if event == '-CAM2-BOT+-':
        handle_config.setValue('TRANSFORM SETTINGS', 'CAM2_TRANS_RIGHT', handle_config.CAM2_TRANS_RIGHT + 2)

    window.FindElement('-CAM1-TOP-').update(str(handle_config.CAM1_TRANS_RIGHT))
    window.FindElement('-CAM1-BOT-').update(str(handle_config.CAM1_TRANS_LEFT))
    window.FindElement('-CAM2-TOP-').update(str(handle_config.CAM2_TRANS_LEFT))
    window.FindElement('-CAM2-BOT-').update(str(handle_config.CAM2_TRANS_RIGHT))

def boxes(event, window):
    if event == '-SIDE1-LEFT-':
        # update side 1 cam 1 box positions
        for box in range(16):                                                   # VARIABLE?!
            leftPos = 'SIDE1_CAM1_BOX' + str(box) + '_LEFT'
            rightPos = 'SIDE1_CAM1_BOX' + str(box) + '_RIGHT'

            currentLeft = getattr(handle_config, leftPos)
            currentRight = getattr(handle_config, rightPos)

            handle_config.setValue('BOX POSITIONING', leftPos, currentLeft - 5)
            if box != 15:                                                       # The last box cam 1 right side is the edge of the screen so doesn't need changed
                handle_config.setValue('BOX POSITIONING', rightPos, currentRight - 5)

        # Get side 1 cam 2 box positions
        for box in range(17):                                                   # VARIABLE?!
            leftPos = 'SIDE1_CAM2_BOX' + str(box) + '_LEFT'
            rightPos = 'SIDE1_CAM2_BOX' + str(box) + '_RIGHT'

            currentLeft = getattr(handle_config, leftPos)
            currentRight = getattr(handle_config, rightPos)

            if box != 0:                                                       # The first box cam 2 left side is the edge of the screen so doesn't need changed
                handle_config.setValue('BOX POSITIONING', leftPos, currentLeft - 5)
            handle_config.setValue('BOX POSITIONING', rightPos, currentRight - 5)

        # Update details of selected box
        updateBoxDetailsText(window, 1)

    if event == '-SIDE1-RIGHT-':
        # update side 1 cam 1 box positions
        for box in range(16):                                                   # VARIABLE?!
            leftPos = 'SIDE1_CAM1_BOX' + str(box) + '_LEFT'
            rightPos = 'SIDE1_CAM1_BOX' + str(box) + '_RIGHT'

            currentLeft = getattr(handle_config, leftPos)
            currentRight = getattr(handle_config, rightPos)

            handle_config.setValue('BOX POSITIONING', leftPos, currentLeft + 5)
            if box != 15:                                                       # The last box cam 1 right side is the edge of the screen so doesn't need changed
                handle_config.setValue('BOX POSITIONING', rightPos, currentRight + 5)

        # Get side 1 cam 2 box positions
        for box in range(17):                                                   # VARIABLE?!
            leftPos = 'SIDE1_CAM2_BOX' + str(box) + '_LEFT'
            rightPos = 'SIDE1_CAM2_BOX' + str(box) + '_RIGHT'

            currentLeft = getattr(handle_config, leftPos)
            currentRight = getattr(handle_config, rightPos)

            if box != 0:                                                       # The first box cam 2 left side is the edge of the screen so doesn't need changed
                handle_config.setValue('BOX POSITIONING', leftPos, currentLeft + 5)
            handle_config.setValue('BOX POSITIONING', rightPos, currentRight + 5)

        # Update details of selected box
        updateBoxDetailsText(window, 1)

    if event == '-SIDE1-UP-':
        handle_config.setValue('BOX POSITIONING', 'SIDE1_VERT', handle_config.SIDE1_VERT - 5)

    if event == '-SIDE1-DOWN-':
        handle_config.setValue('BOX POSITIONING', 'SIDE1_VERT', handle_config.SIDE1_VERT + 5)

    if event == '-SIDE2-LEFT-':
        # update side 1 cam 1 box positions
        for box in range(16):                                                   # VARIABLE?!
            leftPos = 'SIDE2_CAM1_BOX' + str(box) + '_LEFT'
            rightPos = 'SIDE2_CAM1_BOX' + str(box) + '_RIGHT'

            currentLeft = getattr(handle_config, leftPos)
            currentRight = getattr(handle_config, rightPos)

            handle_config.setValue('BOX POSITIONING', leftPos, currentLeft - 5)
            if box != 15:                                                       # The last box cam 1 right side is the edge of the screen so doesn't need changed
                handle_config.setValue('BOX POSITIONING', rightPos, currentRight - 5)

        # Get side 1 cam 2 box positions
        for box in range(17):                                                   # VARIABLE?!
            leftPos = 'SIDE2_CAM2_BOX' + str(box) + '_LEFT'
            rightPos = 'SIDE2_CAM2_BOX' + str(box) + '_RIGHT'

            currentLeft = getattr(handle_config, leftPos)
            currentRight = getattr(handle_config, rightPos)

            if box != 0:                                                       # The first box cam 2 left side is the edge of the screen so doesn't need changed
                handle_config.setValue('BOX POSITIONING', leftPos, currentLeft - 5)
            handle_config.setValue('BOX POSITIONING', rightPos, currentRight - 5)

        # Update details of selected box
        updateBoxDetailsText(window, 2)

    if event == '-SIDE2-RIGHT-':

        # update side 1 cam 1 box positions
        for box in range(16):                                                   # VARIABLE?!
            leftPos = 'SIDE2_CAM1_BOX' + str(box) + '_LEFT'
            rightPos = 'SIDE2_CAM1_BOX' + str(box) + '_RIGHT'

            currentLeft = getattr(handle_config, leftPos)
            currentRight = getattr(handle_config, rightPos)

            handle_config.setValue('BOX POSITIONING', leftPos, currentLeft + 5)
            if box != 15:                                                       # The last box cam 1 right side is the edge of the screen so doesn't need changed
                handle_config.setValue('BOX POSITIONING', rightPos, currentRight + 5)

        # Get side 1 cam 2 box positions
        for box in range(17):                                                   # VARIABLE?!
            leftPos = 'SIDE2_CAM2_BOX' + str(box) + '_LEFT'
            rightPos = 'SIDE2_CAM2_BOX' + str(box) + '_RIGHT'

            currentLeft = getattr(handle_config, leftPos)
            currentRight = getattr(handle_config, rightPos)

            if box != 0:                                                       # The first box cam 2 left side is the edge of the screen so doesn't need changed
                handle_config.setValue('BOX POSITIONING', leftPos, currentLeft + 5)
            handle_config.setValue('BOX POSITIONING', rightPos, currentRight + 5)

        # Update details of selected box
        updateBoxDetailsText(window, 2)

    if event == '-SIDE2-UP-':
        handle_config.setValue('BOX POSITIONING', 'SIDE2_VERT', handle_config.SIDE2_VERT - 5)

    if event == '-SIDE2-DOWN-':
        handle_config.setValue('BOX POSITIONING', 'SIDE2_VERT', handle_config.SIDE2_VERT + 5)

def thresh(event, window):
    if event == '-CAM1-THRESH--':
        handle_config.setValue('THRESH SETTINGS', 'CAM1_THRESH', handle_config.CAM1_THRESH - 5)

    if event == '-CAM1-THRESH+-':
        handle_config.setValue('THRESH SETTINGS', 'CAM1_THRESH', handle_config.CAM1_THRESH + 5)

    if event == '-CAM2-THRESH--':
        handle_config.setValue('THRESH SETTINGS', 'CAM2_THRESH', handle_config.CAM2_THRESH - 5)

    if event == '-CAM2-THRESH+-':
        handle_config.setValue('THRESH SETTINGS', 'CAM2_THRESH', handle_config.CAM2_THRESH + 5)
    
    window.FindElement('-CAM1-THRESH-').update(str(handle_config.CAM1_THRESH))
    window.FindElement('-CAM2-THRESH-').update(str(handle_config.CAM2_THRESH))

def boxChange(event, window, side, value):
    program_state.admin_box_change(program_state.BOX_MODIFY + value)

    # Update text for what box we're modifying
    window.FindElement('-SIDE' + str(side) + '-BOX-').Update(str(program_state.BOX_MODIFY))

    updateBoxDetailsText(window, side)

def modifyBox(event, window, side, value):
    # Figure out what CAM and BOX we're on
    cam = 1
    box = program_state.CAM1_BOX_MODIFY
    if program_state.CAM2_BOX_MODIFY != None:
        cam = 2
        box = program_state.CAM2_BOX_MODIFY

    # Get details of box
    leftPos = 'SIDE' + str(side) + '_CAM' + str(cam) + '_BOX' + str(box) + '_LEFT'
    rightPos = 'SIDE' + str(side) + '_CAM' + str(cam) + '_BOX' + str(box) + '_RIGHT'
    currentLeft = getattr(handle_config, leftPos)
    currentRight = getattr(handle_config, rightPos)

    # if moving position
    if 'BOX-POS' in event:
        if not (cam == 2 and box == 0):                                                  # The first box cam 2 left side is the edge of the screen so doesn't need changed
            handle_config.setValue('BOX POSITIONING', leftPos, currentLeft + value)
        if not (cam == 1 and box == 15):                                                 # The last box cam 1 right side is the edge of the screen so doesn't need changed
            handle_config.setValue('BOX POSITIONING', rightPos, currentRight + value)

    # if changing width
    if 'BOX-WIDTH' in event:
        if not (cam == 1 and box == 15):                                                 # The last box cam 1 right side is the edge of the screen so doesn't need changed
            handle_config.setValue('BOX POSITIONING', rightPos, currentRight + value)

    updateBoxDetailsText(window, side)
