'''This module handles the image'''

import cv2
import numpy as np
import PIL.Image

# my modules
import layouts          # UI Layouts
import program_state    # Programs State

plankWidth = 300
midOffsetCam1 = -40
midOffsetCam2 = -20
planeOffset = 100

topBoxBound = 100
botBoxBound = 120

# thresh settings for camera 1
cam1BoxCount = 12
def cam1BoxThresh():
    return [
        80 + program_state.CAM1_THRESH,
        80 + program_state.CAM1_THRESH,
        100 + program_state.CAM1_THRESH,
        100 + program_state.CAM1_THRESH,
        120 + program_state.CAM1_THRESH, 
        120 + program_state.CAM1_THRESH, 
        120 + program_state.CAM1_THRESH,
        120 + program_state.CAM1_THRESH, 
        120 + program_state.CAM1_THRESH,
        120 + program_state.CAM1_THRESH,
        120 + program_state.CAM1_THRESH,
        120 + program_state.CAM1_THRESH,
        120 + program_state.CAM1_THRESH,
        120 + program_state.CAM1_THRESH,
        120 + program_state.CAM1_THRESH,
        120 + program_state.CAM1_THRESH
    ]
def cam1LeftPositions():
    return [
        195 + program_state.CAM1_BOX_POS_LR,
        315 + program_state.CAM1_BOX_POS_LR,
        435 + program_state.CAM1_BOX_POS_LR,
        560 + program_state.CAM1_BOX_POS_LR,
        690 + program_state.CAM1_BOX_POS_LR,
        820 + program_state.CAM1_BOX_POS_LR,
        950 + program_state.CAM1_BOX_POS_LR,
        1075 + program_state.CAM1_BOX_POS_LR,
        1205 + program_state.CAM1_BOX_POS_LR,
        1335 + program_state.CAM1_BOX_POS_LR,
        1470 + program_state.CAM1_BOX_POS_LR,
        1600 + program_state.CAM1_BOX_POS_LR,
        1725 + program_state.CAM1_BOX_POS_LR,
        1850 + program_state.CAM1_BOX_POS_LR,
        1975 + program_state.CAM1_BOX_POS_LR,
        2096 + program_state.CAM1_BOX_POS_LR
    ]
def cam1RightPositions():
    return [
        285 + program_state.CAM1_BOX_POS_LR,
        400 + program_state.CAM1_BOX_POS_LR,
        520 + program_state.CAM1_BOX_POS_LR,
        645 + program_state.CAM1_BOX_POS_LR,
        775 + program_state.CAM1_BOX_POS_LR, 
        900 + program_state.CAM1_BOX_POS_LR, 
        1040 + program_state.CAM1_BOX_POS_LR,
        1165 + program_state.CAM1_BOX_POS_LR, 
        1298 + program_state.CAM1_BOX_POS_LR,
        1428 + program_state.CAM1_BOX_POS_LR,
        1560 + program_state.CAM1_BOX_POS_LR,
        1685 + program_state.CAM1_BOX_POS_LR,
        1815 + program_state.CAM1_BOX_POS_LR,
        1936 + program_state.CAM1_BOX_POS_LR,
        2066 + program_state.CAM1_BOX_POS_LR,
        2160 + program_state.CAM1_BOX_POS_LR
    ]
def cam1TopBound():
    return topBoxBound + program_state.CAM1_BOX_POS_UD - program_state.BOARD_WIDTH
def cam1BotBound():
    return botBoxBound - program_state.CAM1_BOX_POS_UD - program_state.BOARD_WIDTH

# thresh settings for camera 2
cam2BoxCount = 15
def cam2BoxThresh():
    return [
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        120 + program_state.CAM2_THRESH,
        100 + program_state.CAM2_THRESH,
        100 + program_state.CAM2_THRESH,
        80 + program_state.CAM2_THRESH,
        80 + program_state.CAM2_THRESH,
        80 + program_state.CAM2_THRESH
    ]
def cam2LeftPositons():
    return [
        0 + program_state.CAM2_BOX_POS_LR,
        55 + program_state.CAM2_BOX_POS_LR,
        175 + program_state.CAM2_BOX_POS_LR,
        300 + program_state.CAM2_BOX_POS_LR,
        430 + program_state.CAM2_BOX_POS_LR,
        560 + program_state.CAM2_BOX_POS_LR,
        682 + program_state.CAM2_BOX_POS_LR,
        820 + program_state.CAM2_BOX_POS_LR,
        950 + program_state.CAM2_BOX_POS_LR,
        1080 + program_state.CAM2_BOX_POS_LR,
        1210 + program_state.CAM2_BOX_POS_LR,
        1335 + program_state.CAM2_BOX_POS_LR,
        1475 + program_state.CAM2_BOX_POS_LR,
        1600 + program_state.CAM2_BOX_POS_LR,
        1720 + program_state.CAM2_BOX_POS_LR,
        1845 + program_state.CAM2_BOX_POS_LR,
        1965 + program_state.CAM2_BOX_POS_LR
    ]
def cam2RightPositions():
    return [
        25 + program_state.CAM2_BOX_POS_LR,
        150 + program_state.CAM2_BOX_POS_LR,
        270 + program_state.CAM2_BOX_POS_LR,
        400 + program_state.CAM2_BOX_POS_LR,
        520 + program_state.CAM2_BOX_POS_LR,
        650 + program_state.CAM2_BOX_POS_LR,
        790 + program_state.CAM2_BOX_POS_LR, 
        915 + program_state.CAM2_BOX_POS_LR,
        1045 + program_state.CAM2_BOX_POS_LR,
        1180 + program_state.CAM2_BOX_POS_LR,
        1310 + program_state.CAM2_BOX_POS_LR,
        1440 + program_state.CAM2_BOX_POS_LR,
        1570 + program_state.CAM2_BOX_POS_LR,
        1700 + program_state.CAM2_BOX_POS_LR,
        1815 + program_state.CAM2_BOX_POS_LR,
        1935 + program_state.CAM2_BOX_POS_LR,
        2030 + program_state.CAM2_BOX_POS_LR
    ]
def cam2TopBound():
    return topBoxBound + program_state.CAM2_BOX_POS_UD - program_state.BOARD_WIDTH
def cam2BotBound():
    return botBoxBound - program_state.CAM2_BOX_POS_UD - program_state.BOARD_WIDTH

# crop image to plank based on offset
def cropImg(origImg, camera):
    height, width, _ = origImg.shape

    if camera == 1:
        midPoint = int(width / 2) + midOffsetCam1
    else:
        midPoint = int(width / 2) + midOffsetCam2

    leftBound = midPoint - plankWidth
    rightBound = midPoint + plankWidth

    # draw on boundaries
    # cv2.line(origImg, (leftBound, 0), (leftBound, height), (255,0,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (midPoint, 0), (midPoint, height), (0,255,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (rightBound, 0), (rightBound, height), (0,0,255), 5) # Top-Left to Bottom-Left

    origImg = origImg[0:height, leftBound:rightBound]

    return origImg

# plot transformation circles on image
def plotCircles(origImg, camera):
    height, width, _ = origImg.shape # img size
    
    leftOffset = program_state.CAM1_TRANS_LEFT
    rightOffset = width - program_state.CAM1_TRANS_RIGHT
            
    if camera == 2:
        leftOffset = program_state.CAM2_TRANS_LEFT
        rightOffset = width - program_state.CAM2_TRANS_RIGHT

    cv2.circle(origImg, (leftOffset, 0), 5, (0, 0, 255), 2)   # Top-Left
    cv2.circle(origImg, (rightOffset, 0), 5, (0, 0, 255), 2)  # Top-Right
    cv2.circle(origImg, (0, height), 5, (0, 0, 255), 2)  # Bottom-Left
    cv2.circle(origImg, (width, height), 5, (0, 0, 255), 2) # Bottom-Right
    
    cv2.line(origImg, (leftOffset, 0), (0, height), (0, 0, 255), 2) # Top-Left to Bottom-Left
    cv2.line(origImg, (rightOffset, 0), (width, height), (0, 0, 255), 2) # Top-Right to Bottom-Right
    
    return origImg

# transform image to plane
def transform(origImg, camera):
    height, width, _ = origImg.shape # img size
    
    leftOffset = program_state.CAM1_TRANS_LEFT
    rightOffset = width - program_state.CAM1_TRANS_RIGHT
            
    if camera == 2:
        leftOffset = program_state.CAM2_TRANS_LEFT
        rightOffset = width - program_state.CAM2_TRANS_RIGHT

    pts1 = np.float32([[leftOffset, 0], [rightOffset, 0], [0, height], [width, height]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    transformed = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(origImg, transformed, (width, height))

# rotate image for each camera
def rotateImg(origImg, camera):    
    if camera == 1:
        origImg = cv2.rotate(origImg, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        origImg = cv2.rotate(origImg, cv2.ROTATE_90_CLOCKWISE)

    return origImg

# thresh image and return black vs white count
def threshImg(origImg, camera, ignoreFlags):
    height, _, _ = origImg.shape

    # grey image
    greyImg = cv2.cvtColor(origImg, cv2.COLOR_BGR2GRAY)
    threshImg = None

    # draw thresh boxes
    if camera == 1:
        possibleBoxes = len(cam1BoxThresh())
        for x in range(possibleBoxes - cam1BoxCount, possibleBoxes):
            if not ignoreFlags and program_state.THRESH_BOX_MODE:
                cv2.rectangle(origImg, (cam1LeftPositions()[x], cam1TopBound()), (cam1RightPositions()[x], height - cam1BotBound()), (255, 0, 0), 5)
            
            newThresh = greyImg[cam1TopBound():height - cam1BotBound(), cam1LeftPositions()[x]:cam1RightPositions()[x]].copy()
            _, newThresh = cv2.threshold(newThresh, cam1BoxThresh()[x], 255, 0)

            if threshImg is None:
                threshImg = newThresh
            else:
                threshImg = cv2.hconcat([threshImg, newThresh])
    else:
        for x in range(0, cam2BoxCount):
            if not ignoreFlags and program_state.THRESH_BOX_MODE:
                cv2.rectangle(origImg, (cam2LeftPositons()[x], cam2TopBound()), (cam2RightPositions()[x], height - cam2BotBound()), (255, 0, 0), 5)
            
            newThresh = greyImg[cam2TopBound():height - cam2BotBound(), cam2LeftPositons()[x]:cam2RightPositions()[x]].copy()
            _, newThresh = cv2.threshold(newThresh, cam2BoxThresh()[x], 255, 0)

            if threshImg is None:
                threshImg = newThresh
            else:
                threshImg = cv2.hconcat([threshImg, newThresh])

    totalPixels = threshImg.size
    whitePixels = cv2.countNonZero(threshImg)
    blackPixels = totalPixels - whitePixels

    return threshImg, round(blackPixels / totalPixels * 100, 2)

# resize img to fit ui
def resizeImg(origImg):    
    # heigh, width and ratio of cropped and rotated img
    height, width = origImg.shape[0], origImg.shape[1]
    ratio = height / width
    
    # adjust width to image ratio
    newWidth = int(layouts.row_size / ratio)
    newHeight = int(width * ratio)

    # if image too big use other variable
    if newWidth > layouts.img_width:
        newHeight = int(layouts.img_width * ratio)
        newWidth = int(newHeight / ratio)

        # resize image to fit window
        origImg = cv2.resize(origImg, (newWidth, newHeight), PIL.Image.ANTIALIAS)

        # pad to fill height
        padding = int((layouts.row_size - newHeight) / 2)
        origImg = cv2.copyMakeBorder(origImg, padding, padding, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    else:
        # resize image to fit window
        origImg = cv2.resize(origImg, (newWidth, newHeight), PIL.Image.ANTIALIAS)

        # pad to fill width
        padding = int((layouts.img_width - newWidth) / 2)
        origImg = cv2.copyMakeBorder(origImg, 0, 0, 30, 30, cv2.BORDER_CONSTANT, value=(0, 0, 0))

    return origImg

# main img function
def handle_img(origImg, camera, ignoreFlags): 

    # crop image to plank
    origImg = cropImg(origImg, camera)

    # show transform
    if not ignoreFlags and program_state.SHOW_TRANSFORM:
        origImg = plotCircles(origImg, camera)

    # perform transform
    if ignoreFlags or not program_state.SHOW_TRANSFORM:
        origImg = transform(origImg, camera)
    
    # crop image to plank
    origImg = rotateImg(origImg, camera)

    # calculate thresh values
    threshedImg, barkPercent = threshImg(origImg, camera, ignoreFlags)

    # crop image to plank
    origImg = resizeImg(origImg)

    # if thresh mode show thresh image
    if not ignoreFlags and program_state.THRESH_MODE:
        origImg = resizeImg(threshedImg)

    return cv2.imencode('.png', origImg)[1].tobytes(), barkPercent