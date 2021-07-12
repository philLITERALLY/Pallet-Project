'''This module handles the image'''

import cv2
import numpy as np
import PIL.Image

# my modules
# import layouts          # UI Layouts
class layouts:
    row_size = 475
    img_width = 1272.0

import program_state    # Programs State
import handle_config    # Programs Configuration
handle_config.init()    # config settings need loaded

midOffsetCam1 = -40
midOffsetCam2 = -20
planeOffset = 100

topBoxBound = 100
botBoxBound = 120

# thresh settings for camera 1
def cam1BoxThresh():
    return [
        80 + handle_config.CAM1_THRESH,
        80 + handle_config.CAM1_THRESH,
        100 + handle_config.CAM1_THRESH,
        100 + handle_config.CAM1_THRESH,
        120 + handle_config.CAM1_THRESH, 
        120 + handle_config.CAM1_THRESH, 
        120 + handle_config.CAM1_THRESH,
        120 + handle_config.CAM1_THRESH, 
        120 + handle_config.CAM1_THRESH,
        120 + handle_config.CAM1_THRESH,
        120 + handle_config.CAM1_THRESH,
        120 + handle_config.CAM1_THRESH,
        120 + handle_config.CAM1_THRESH,
        120 + handle_config.CAM1_THRESH,
        120 + handle_config.CAM1_THRESH,
        120 + handle_config.CAM1_THRESH
    ]

# thresh settings for camera 2
def cam2BoxThresh():
    return [
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        120 + handle_config.CAM2_THRESH,
        100 + handle_config.CAM2_THRESH,
        100 + handle_config.CAM2_THRESH,
        80 + handle_config.CAM2_THRESH,
        80 + handle_config.CAM2_THRESH,
        80 + handle_config.CAM2_THRESH
    ]

# Get vertical positions
def topBound(side):
    vertPos = getattr(handle_config, 'SIDE' + str(side) + '_VERT')
    return topBoxBound + vertPos - handle_config.BOARD_WIDTH
def botBound(side):
    vertPos = getattr(handle_config, 'SIDE' + str(side) + '_VERT')
    return botBoxBound - vertPos - handle_config.BOARD_WIDTH

# crop image to plank based on offset
def cropImg(origImg, camera, side):
    height, width, _ = origImg.shape

    if side == 1:
        midPoint = 1210
    else:
        midPoint = 2530

    leftBound = midPoint - handle_config.FRAME_WIDTH
    rightBound = midPoint + handle_config.FRAME_WIDTH

    # # draw on boundaries
    # cv2.line(origImg, (leftBound, 0), (leftBound, height), (255,0,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (midPoint, 0), (midPoint, height), (0,255,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (rightBound, 0), (rightBound, height), (0,0,255), 5) # Top-Left to Bottom-Left

    origImg = origImg[0:height, leftBound:rightBound]

    return origImg

# plot transformation circles on image
def plotCircles(origImg, camera, side):
    height, width, _ = origImg.shape # img size
    
    leftOffset = handle_config.CAM1_TRANS_LEFT
    rightOffset = width - handle_config.CAM1_TRANS_RIGHT
            
    if side == 2:
        leftOffset = handle_config.CAM2_TRANS_LEFT
        rightOffset = width - handle_config.CAM2_TRANS_RIGHT
    
    side1option1 = 380
    side1option2 = width
    side1option3 = 850
    side2option1 = 650
    side2option2 = 100
    side2option3 = width

    if side == 1:
        cv2.circle(origImg, (side1option1, 0), 5, (0, 0, 255), 2)   # Top-Left
        cv2.circle(origImg, (side1option2, 0), 5, (0, 0, 255), 2)  # Top-Right
        cv2.circle(origImg, (0, height), 5, (0, 0, 255), 2)  # Bottom-Left
        cv2.circle(origImg, (side1option3, height), 5, (0, 0, 255), 2) # Bottom-Right
        
        cv2.line(origImg, (side1option1, 0), (0, height), (0, 0, 255), 2) # Top-Left to Bottom-Left
        cv2.line(origImg, (side1option2, 0), (side1option3, height), (0, 0, 255), 2) # Top-Right to Bottom-Right

    else:
        cv2.circle(origImg, (0, 0), 5, (0, 0, 255), 2)   # Top-Left
        cv2.circle(origImg, (side2option1, 0), 5, (0, 0, 255), 2)  # Top-Right
        cv2.circle(origImg, (side2option2, height), 5, (0, 0, 255), 2)  # Bottom-Left
        cv2.circle(origImg, (side2option3, height), 5, (0, 0, 255), 2) # Bottom-Right
        
        cv2.line(origImg, (0, 0), (side2option2, height), (0, 0, 255), 2) # Top-Left to Bottom-Left
        cv2.line(origImg, (side2option1, 0), (side2option3, height), (0, 0, 255), 2) # Top-Right to Bottom-Right
    
    return origImg

# transform image to plane
def transform(origImg, camera, side):
    height, width, _ = origImg.shape # img size
    
    leftOffset = handle_config.CAM1_TRANS_LEFT
    rightOffset = width - handle_config.CAM1_TRANS_RIGHT
            
    if camera == 2:
        leftOffset = handle_config.CAM2_TRANS_LEFT
        rightOffset = width - handle_config.CAM2_TRANS_RIGHT
    
    side1option1 = 380
    side1option2 = width
    side1option3 = 850
    side2option1 = 650
    side2option2 = 100
    side2option3 = width

    if side == 1:
        pts1 = np.float32([[side1option1, 0], [side1option2, 0], [0, height], [side1option3, height]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    else:
        pts1 = np.float32([[0, 0], [side2option1, 0], [side2option2, height], [side2option3, height]])
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

# thresh box image and return black vs white count
def threshImg(origImg, camera, side, ignoreFlags):
    height, width, _ = origImg.shape

    # grey image
    greyImg = cv2.cvtColor(origImg, cv2.COLOR_BGR2GRAY)
    threshImg = None

    # draw thresh boxes
    if camera == 1:
        possibleBoxes = len(cam1BoxThresh())
        for x in range(0, possibleBoxes):
            inUse = x > possibleBoxes - handle_config.CAM1_BOX_COUNT # boxes that are used in current thresh
            modifying = program_state.CAM1_BOX_MODIFY                 # box that user is currently modifying

            leftPos = getattr(handle_config, 'SIDE' + str(side) + '_CAM1_BOX' + str(x) + '_LEFT') 
            rightPos = getattr(handle_config, 'SIDE' + str(side) + '_CAM1_BOX' + str(x) + '_RIGHT')

            if not ignoreFlags and (program_state.THRESH_BOX_1_MODE or program_state.THRESH_BOX_2_MODE):
                rectColour = (255, 0, 0)

                if x == modifying:
                    rectColour = (0, 255, 0)

                if inUse:
                    cv2.rectangle(origImg, (leftPos, topBound(side)), (rightPos, height - botBound(side)), rectColour, 5)
                else:
                    cv2.rectangle(origImg, (leftPos, topBound(side)), (rightPos, height - botBound(side)), rectColour, -1)

            if inUse:
                newThresh = greyImg[topBound(side):height - botBound(side), leftPos:rightPos].copy()
                _, newThresh = cv2.threshold(newThresh, cam1BoxThresh()[x], 255, 0)

                if threshImg is None:
                    threshImg = newThresh
                else:
                    threshImg = cv2.hconcat([threshImg, newThresh])
    else:
        possibleBoxes = len(cam2BoxThresh())
        for x in range(0, possibleBoxes):            
            inUse = x < handle_config.CAM2_BOX_COUNT # boxes that are used in current thresh
            modifying = program_state.CAM2_BOX_MODIFY # box that user is currently modifying

            leftPos = getattr(handle_config, 'SIDE' + str(side) + '_CAM2_BOX' + str(x) + '_LEFT') 
            rightPos = getattr(handle_config, 'SIDE' + str(side) + '_CAM2_BOX' + str(x) + '_RIGHT')

            if not ignoreFlags and (program_state.THRESH_BOX_1_MODE or program_state.THRESH_BOX_2_MODE):
                rectColour = (255, 0, 0)

                if x == modifying:
                    rectColour = (0, 255, 0)

                if inUse:
                    cv2.rectangle(origImg, (leftPos, topBound(side)), (rightPos, height - botBound(side)), rectColour, 5)
                else:
                    cv2.rectangle(origImg, (leftPos, topBound(side)), (rightPos, height - botBound(side)), rectColour, -1)

            if inUse:    
                newThresh = greyImg[topBound(side):height - botBound(side), leftPos:rightPos].copy()
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
    newHeight = int(newWidth * ratio)

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
def main(origImg, camera, side, ignoreFlags): 

    # crop image to plank
    origImg = cropImg(origImg, camera, side)
    barkPercent = 0

    # show transform
    if not ignoreFlags and program_state.SHOW_TRANSFORM:
        origImg = plotCircles(origImg, camera, side)

    # perform transform
    if ignoreFlags or not program_state.SHOW_TRANSFORM:
        origImg = transform(origImg, camera, side)
    
    # crop image to plank
    origImg = rotateImg(origImg, camera)

    # calculate box thresh values
    threshedImg, barkPercent = threshImg(origImg, camera, side, ignoreFlags)

    # crop image to plank
    origImg = resizeImg(origImg)

    # if thresh mode show thresh image
    if True:
        origImg = resizeImg(threshedImg)

    return cv2.imencode('.png', origImg)[1].tobytes(), barkPercent