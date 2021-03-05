'''This module handles the image'''

import cv2
import numpy as np
import PIL.Image

# my modules
import layouts          # UI Layouts
import program_state    # Programs State
import admin_settings   # Admin settings

plankWidth = 300
midOffsetCam1 = -40
midOffsetCam2 = -20
planeOffset = 100

topBoxBound = 100
botBoxBound = 120

# thresh settings for camera 1
def cam1BoxThresh():
    return [
        80 + admin_settings.CAM1_THRESH,
        80 + admin_settings.CAM1_THRESH,
        100 + admin_settings.CAM1_THRESH,
        100 + admin_settings.CAM1_THRESH,
        120 + admin_settings.CAM1_THRESH, 
        120 + admin_settings.CAM1_THRESH, 
        120 + admin_settings.CAM1_THRESH,
        120 + admin_settings.CAM1_THRESH, 
        120 + admin_settings.CAM1_THRESH,
        120 + admin_settings.CAM1_THRESH,
        120 + admin_settings.CAM1_THRESH,
        120 + admin_settings.CAM1_THRESH,
        120 + admin_settings.CAM1_THRESH,
        120 + admin_settings.CAM1_THRESH,
        120 + admin_settings.CAM1_THRESH,
        120 + admin_settings.CAM1_THRESH
    ]
def cam1LeftPositions():
    return [
        225 + admin_settings.CAM1_BOX_POS_LR,
        345 + admin_settings.CAM1_BOX_POS_LR,
        465 + admin_settings.CAM1_BOX_POS_LR,
        590 + admin_settings.CAM1_BOX_POS_LR,
        715 + admin_settings.CAM1_BOX_POS_LR,
        845 + admin_settings.CAM1_BOX_POS_LR,
        970 + admin_settings.CAM1_BOX_POS_LR,
        1100 + admin_settings.CAM1_BOX_POS_LR,
        1225 + admin_settings.CAM1_BOX_POS_LR,
        1355 + admin_settings.CAM1_BOX_POS_LR,
        1485 + admin_settings.CAM1_BOX_POS_LR,
        1615 + admin_settings.CAM1_BOX_POS_LR,
        1740 + admin_settings.CAM1_BOX_POS_LR,
        1865 + admin_settings.CAM1_BOX_POS_LR,
        1990 + admin_settings.CAM1_BOX_POS_LR,
        2111 + admin_settings.CAM1_BOX_POS_LR
    ]
def cam1RightPositions():
    return [
        315 + admin_settings.CAM1_BOX_POS_LR,
        435 + admin_settings.CAM1_BOX_POS_LR,
        555 + admin_settings.CAM1_BOX_POS_LR,
        680 + admin_settings.CAM1_BOX_POS_LR,
        810 + admin_settings.CAM1_BOX_POS_LR,
        930 + admin_settings.CAM1_BOX_POS_LR,
        1060 + admin_settings.CAM1_BOX_POS_LR,
        1185 + admin_settings.CAM1_BOX_POS_LR,
        1318 + admin_settings.CAM1_BOX_POS_LR,
        1448 + admin_settings.CAM1_BOX_POS_LR,
        1575 + admin_settings.CAM1_BOX_POS_LR,
        1700 + admin_settings.CAM1_BOX_POS_LR,
        1830 + admin_settings.CAM1_BOX_POS_LR,
        1951 + admin_settings.CAM1_BOX_POS_LR,
        2081 + admin_settings.CAM1_BOX_POS_LR,
        2175 + admin_settings.CAM1_BOX_POS_LR
    ]
def cam1TopBound():
    return topBoxBound + admin_settings.CAM1_BOX_POS_UD - admin_settings.BOARD_WIDTH
def cam1BotBound():
    return botBoxBound - admin_settings.CAM1_BOX_POS_UD - admin_settings.BOARD_WIDTH

# thresh settings for camera 2
def cam2BoxThresh():
    return [
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        120 + admin_settings.CAM2_THRESH,
        100 + admin_settings.CAM2_THRESH,
        100 + admin_settings.CAM2_THRESH,
        80 + admin_settings.CAM2_THRESH,
        80 + admin_settings.CAM2_THRESH,
        80 + admin_settings.CAM2_THRESH
    ]
def cam2LeftPositons():
    return [
        0 + admin_settings.CAM2_BOX_POS_LR,
        55 + admin_settings.CAM2_BOX_POS_LR,
        175 + admin_settings.CAM2_BOX_POS_LR,
        300 + admin_settings.CAM2_BOX_POS_LR,
        430 + admin_settings.CAM2_BOX_POS_LR,
        560 + admin_settings.CAM2_BOX_POS_LR,
        682 + admin_settings.CAM2_BOX_POS_LR,
        820 + admin_settings.CAM2_BOX_POS_LR,
        950 + admin_settings.CAM2_BOX_POS_LR,
        1080 + admin_settings.CAM2_BOX_POS_LR,
        1210 + admin_settings.CAM2_BOX_POS_LR,
        1335 + admin_settings.CAM2_BOX_POS_LR,
        1468 + admin_settings.CAM2_BOX_POS_LR,
        1595 + admin_settings.CAM2_BOX_POS_LR,
        1723 + admin_settings.CAM2_BOX_POS_LR,
        1851 + admin_settings.CAM2_BOX_POS_LR,
        1973 + admin_settings.CAM2_BOX_POS_LR
    ]
def cam2RightPositions():
    return [
        25 + admin_settings.CAM2_BOX_POS_LR,
        150 + admin_settings.CAM2_BOX_POS_LR,
        270 + admin_settings.CAM2_BOX_POS_LR,
        400 + admin_settings.CAM2_BOX_POS_LR,
        520 + admin_settings.CAM2_BOX_POS_LR,
        650 + admin_settings.CAM2_BOX_POS_LR,
        790 + admin_settings.CAM2_BOX_POS_LR, 
        915 + admin_settings.CAM2_BOX_POS_LR,
        1045 + admin_settings.CAM2_BOX_POS_LR,
        1180 + admin_settings.CAM2_BOX_POS_LR,
        1310 + admin_settings.CAM2_BOX_POS_LR,
        1435 + admin_settings.CAM2_BOX_POS_LR,
        1565 + admin_settings.CAM2_BOX_POS_LR,
        1690 + admin_settings.CAM2_BOX_POS_LR,
        1818 + admin_settings.CAM2_BOX_POS_LR,
        1941 + admin_settings.CAM2_BOX_POS_LR,
        2038 + admin_settings.CAM2_BOX_POS_LR
    ]
def cam2TopBound():
    return topBoxBound + admin_settings.CAM2_BOX_POS_UD - admin_settings.BOARD_WIDTH
def cam2BotBound():
    return botBoxBound - admin_settings.CAM2_BOX_POS_UD - admin_settings.BOARD_WIDTH

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
    
    leftOffset = admin_settings.CAM1_TRANS_LEFT
    rightOffset = width - admin_settings.CAM1_TRANS_RIGHT
            
    if camera == 2:
        leftOffset = admin_settings.CAM2_TRANS_LEFT
        rightOffset = width - admin_settings.CAM2_TRANS_RIGHT

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
    
    leftOffset = admin_settings.CAM1_TRANS_LEFT
    rightOffset = width - admin_settings.CAM1_TRANS_RIGHT
            
    if camera == 2:
        leftOffset = admin_settings.CAM2_TRANS_LEFT
        rightOffset = width - admin_settings.CAM2_TRANS_RIGHT

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
    height, width, _ = origImg.shape

    # grey image
    greyImg = cv2.cvtColor(origImg, cv2.COLOR_BGR2GRAY)
    threshImg = None

    # draw thresh boxes
    if camera == 1:
        possibleBoxes = len(cam1BoxThresh())
        for x in range(possibleBoxes - admin_settings.CAM1_BOX_COUNT, possibleBoxes):
            if not ignoreFlags and program_state.THRESH_BOX_MODE:
                cv2.rectangle(origImg, (cam1LeftPositions()[x], cam1TopBound()), (cam1RightPositions()[x], height - cam1BotBound()), (255, 0, 0), 5)
                        
            newThresh = greyImg[cam1TopBound():height - cam1BotBound(), cam1LeftPositions()[x]:cam1RightPositions()[x]].copy()
            _, newThresh = cv2.threshold(newThresh, cam1BoxThresh()[x], 255, 0)

            if threshImg is None:
                threshImg = newThresh
            else:
                threshImg = cv2.hconcat([threshImg, newThresh])
    else:
        for x in range(0, admin_settings.CAM2_BOX_COUNT):
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
def main(origImg, camera, ignoreFlags): 

    # # crop image to plank
    # origImg = cropImg(origImg, camera)

    # # show transform
    # if not ignoreFlags and program_state.SHOW_TRANSFORM:
    #     origImg = plotCircles(origImg, camera)

    # # perform transform
    # if ignoreFlags or not program_state.SHOW_TRANSFORM:
    #     origImg = transform(origImg, camera)
    
    # # crop image to plank
    # origImg = rotateImg(origImg, camera)

    if camera == 1:        
        origImg = cv2.imread("left_side_ruler.png")
    else:
        origImg = cv2.imread("right_side_ruler.png")

    # calculate thresh values
    threshedImg, barkPercent = threshImg(origImg, camera, ignoreFlags)

    # crop image to plank
    origImg = resizeImg(origImg)

    # if thresh mode show thresh image
    if not ignoreFlags and program_state.THRESH_MODE:
        origImg = resizeImg(threshedImg)
        cv2.imwrite('camera' + str(camera) + '.png', origImg) 

    return cv2.imencode('.png', origImg)[1].tobytes(), barkPercent