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

# thresh values for camera 1 boxes
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
    186,
    306,
    426,
    546,
    676,
    796,
    926,
    1056,
    1186,
    1316,
    1446,
    1576,
    1706,
    1836,
    1966,
    2096
]
cam1RightPositions = [
    266,
    386,
    506,
    626,
    756, 
    886, 
    1016,
    1146, 
    1276,
    1416,
    1546,
    1676,
    1806,
    1936,
    2066,
    2160
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
def plotCircles(origImg):
    height, width, _ = origImg.shape # img size

    leftBound = planeOffset
    rightBound = width - planeOffset

    cv2.circle(origImg, (leftBound, 0), 5, (0, 0, 255), 2)   # Top-Left
    cv2.circle(origImg, (rightBound, 0), 5, (0, 0, 255), 2)  # Top-Right
    cv2.circle(origImg, (0, height), 5, (0, 0, 255), 2)  # Bottom-Left
    cv2.circle(origImg, (width, height), 5, (0, 0, 255), 2) # Bottom-Right
    
    cv2.line(origImg, (leftBound, 0), (0, height), (0, 0, 255), 2) # Top-Left to Bottom-Left
    cv2.line(origImg, (rightBound, 0), (width, height), (0, 0, 255), 2) # Top-Right to Bottom-Right
    
    return origImg

# transform image to plane
def transform(origImg):
    height, width, _ = origImg.shape # img size

    leftBound = planeOffset
    rightBound = width - planeOffset

    pts1 = np.float32([[leftBound, 0], [rightBound, 0], [0, height], [width, height]])
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

def threshImg(origImg, camera):
    # heigh, width and ratio of cropped and rotated img
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
        _, threshImg = cv2.threshold(greyImg, 140, 255, 0)

    return threshImg, 12

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
    # origImg = plotCircles(origImg)

    # perform transform
    origImg = transform(origImg)
    
    # crop image to plank
    origImg = rotateImg(origImg, camera)

    # calculate thresh values
    threshedImg, percent = threshImg(origImg, camera)

    # crop image to plank
    # origImg = resizeImg(origImg)
    origImg = resizeImg(threshedImg)

    return cv2.imencode('.png', origImg)[1].tobytes()