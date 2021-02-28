'''This module handles the image'''

import cv2
import numpy as np
import PIL.Image

# my modules
import layouts          # UI Layouts

plankWidth = 300
midOffsetCam1 = -40
midOffsetCam2 = -20
planeOffset = 100

topBoxBound = 100
botBoxBound = 120

# thresh settings for camera 1
cam1BoxCount = 12
cam1BoxThresh = [
    80,
    80,
    100,
    100,
    120, 
    120, 
    120,
    120, 
    120,
    120,
    120,
    120,
    120,
    120,
    120,
    120
]
cam1LeftPositons = [
    195,
    315,
    435,
    560,
    690,
    820,
    950,
    1075,
    1205,
    1335,
    1470,
    1600,
    1725,
    1850,
    1975,
    2096
]
cam1RightPositions = [
    285,
    400,
    520,
    645,
    775, 
    900, 
    1040,
    1165, 
    1298,
    1428,
    1560,
    1685,
    1815,
    1936,
    2066,
    2160
]

# thresh settings for camera 2
cam2BoxCount = 15
cam2BoxThresh = [
    120, 
    120, 
    120,
    120, 
    120,
    120,
    120,
    120,
    120,
    120,
    120,
    120,
    100,
    100,
    80,
    80,
    80
]
cam2LeftPositons = [
    0,
    55,
    175,
    300,
    430,
    560,
    682,
    820,
    950,
    1080,
    1210,
    1335,
    1475,
    1600,
    1720,
    1845,
    1965
]
cam2RightPositions = [
    25,
    150,
    270,
    400,
    520,
    650,
    790, 
    915,
    1045,
    1180,
    1310,
    1440,
    1570,
    1700,
    1815,
    1935,
    2030
]

# crop image to plank based on offset
def cropImg(origImg, camera):
    origHeight, origWidth, _ = origImg.shape

    if camera == 1:
        midPoint = int(origWidth / 2) + midOffsetCam1
    else:
        midPoint = int(origWidth / 2) + midOffsetCam2

    leftBound = midPoint - plankWidth
    rightBound = midPoint + plankWidth

    # draw on boundaries
    # cv2.line(origImg, (leftBound, 0), (leftBound, origHeight), (255,0,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (midPoint, 0), (midPoint, origHeight), (0,255,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (rightBound, 0), (rightBound, origHeight), (0,0,255), 5) # Top-Left to Bottom-Left

    origImg = origImg[0:origHeight, leftBound:rightBound]

    return origImg

# plot transformation circles on image
def plotCircles(origImg, camera):
    height, width, _ = origImg.shape # img size
    
    leftOffset = 90
    rightOffset = width - 85
            
    if camera == 2:
        leftOffset = 60
        rightOffset = width - 110

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
    
    leftOffset = 110
    rightOffset = width - 105
            
    if camera == 2:
        leftOffset = 90
        rightOffset = width - 130

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
def threshImg(origImg, camera):
    origHeight, _, _ = origImg.shape

    # grey image
    greyImg = cv2.cvtColor(origImg, cv2.COLOR_BGR2GRAY)
    threshImg = None

    # draw thresh boxes
    if camera == 1:
        possibleBoxes = len(cam1BoxThresh)
        for x in range(possibleBoxes - cam1BoxCount, possibleBoxes):
            origImg = cv2.rectangle(origImg, (cam1LeftPositons[x], topBoxBound), (cam1RightPositions[x], origHeight - botBoxBound), (255, 0, 0), 5)
            
            newThresh = greyImg[topBoxBound:origHeight - botBoxBound, cam1LeftPositons[x]:cam1RightPositions[x]].copy()
            _, newThresh = cv2.threshold(newThresh, cam1BoxThresh[x], 255, 0)

            if threshImg is None:
                threshImg = newThresh
            else:
                threshImg = cv2.hconcat([threshImg, newThresh])
    else:
        for x in range(0, cam2BoxCount):
            origImg = cv2.rectangle(origImg, (cam2LeftPositons[x], topBoxBound), (cam2RightPositions[x], origHeight - botBoxBound), (255, 0, 0), 5)
            
            newThresh = greyImg[topBoxBound:origHeight - botBoxBound, cam2LeftPositons[x]:cam2RightPositions[x]].copy()
            _, newThresh = cv2.threshold(newThresh, cam2BoxThresh[x], 255, 0)

            if threshImg is None:
                threshImg = newThresh
            else:
                threshImg = cv2.hconcat([threshImg, newThresh])

    totalPixels = threshImg.size
    whitePixels = cv2.countNonZero(threshImg)
    blackPixels = totalPixels - whitePixels

    return threshImg, str(round(blackPixels / totalPixels * 100, 2)) + '%'

# resize img to fit ui
def resizeImg(origImg):    
    # heigh, width and ratio of cropped and rotated img
    origHeight, origWidth = origImg.shape[0], origImg.shape[1]
    ratio = origHeight / origWidth
    
    # adjust width to image ratio
    newWidth = int(layouts.row_size / ratio)
    newHeight = int(origWidth * ratio)

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

def handle_img(origImg, camera): 

    # crop image to plank
    origImg = cropImg(origImg, camera)

    # show transform
    # origImg = plotCircles(origImg, camera)

    # perform transform
    origImg = transform(origImg, camera)
    
    # crop image to plank
    origImg = rotateImg(origImg, camera)

    # calculate thresh values
    threshedImg, barkPercent = threshImg(origImg, camera)

    # crop image to plank
    origImg = resizeImg(origImg)
    # origImg = resizeImg(threshedImg)

    return cv2.imencode('.png', origImg)[1].tobytes(), barkPercent