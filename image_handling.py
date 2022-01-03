'''This module handles the image'''

import cv2
import numpy as np
import PIL.Image

# my modules
import layouts          # UI Layouts
import program_state    # Programs State
import handle_config    # Programs Configuration
handle_config.init()

def transformCoords(origImg, side):
    _, width, _ = origImg.shape # img size

    if side == 1:
        coord1 = 200
        coord2 = width - 10
        coord3 = 0
        coord4 = width - 5
    else:
        coord1 = 0
        coord2 = width - 310
        coord3 = 130
        coord4 = width
    
    return coord1, coord2, coord3, coord4

def cropToWidth(origImg):
    height, width, _ = origImg.shape

    leftBound = 450
    rightBound = 3240
    mid = int(leftBound + (rightBound - leftBound) / 2)
    
    # # draw boundaries
    cv2.line(origImg, (leftBound, 0), (leftBound, height), (255,0,0), 5) # Left Bound
    cv2.line(origImg, (mid, 0), (mid, height), (0,255,0), 5) # Mid Line
    cv2.line(origImg, (rightBound, 0), (rightBound, height), (0,0,255), 5) # Right Bound

    side1Top = 800
    side1Bot = 1000

    cv2.line(origImg, (0, side1Top), (width, side1Top), (255,0,0), 5) # Side 1 Top Bound
    cv2.line(origImg, (0, side1Bot), (width, side1Bot), (0,0,255), 5) # Side 1 Bot Bound

    side2Top = 1200
    side2Bot = 1400

    cv2.line(origImg, (0, side2Top), (width, side2Top), (255,0,0), 5) # Side 1 Top Bound
    cv2.line(origImg, (0, side2Bot), (width, side2Bot), (0,0,255), 5) # Side 1 Bot Bound

    side1 = origImg[side1Top:side1Bot, leftBound:rightBound].copy()
    side2 = origImg[side2Top:side2Bot, leftBound:rightBound].copy()

    return side1, side2

# thresh image
def threshImg(origImg):
    # grey image
    greyImg = cv2.cvtColor(origImg, cv2.COLOR_BGR2GRAY)

    # draw thresh boxes
    _, threshImg = cv2.threshold(greyImg, handle_config.CAM_THRESH, 255, 0)

    return threshImg

# calculate percentage of white pixels in given img
def whiteCalc(origImg):
    totalPixels = origImg.size
    whitePixels = cv2.countNonZero(origImg)
    return round(whitePixels / totalPixels * 100, 2)

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

def main(origImg, ignoreFlags):

    # crop image to plank width
    side1, side2 = cropToWidth(origImg)

    # calculate box thresh values
    threshedSide1Img = threshImg(side1)
    threshedSide2Img = threshImg(side2)

    side1White = whiteCalc(threshedSide1Img)
    side2White = whiteCalc(threshedSide2Img)

    # resize image
    side1 = resizeImg(side1)
    side2 = resizeImg(side2)

    # if thresh mode show thresh image
    if not ignoreFlags and program_state.THRESH_MODE:
        side1 = resizeImg(threshedSide1Img)
        side2 = resizeImg(threshedSide2Img)
    
    return cv2.imencode('.png', side1)[1].tobytes(), \
        cv2.imencode('.png', side2)[1].tobytes(), \
        side1White, side2White