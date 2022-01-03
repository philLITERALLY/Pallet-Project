'''This module handles the image'''

import cv2
import numpy as np
import PIL.Image

# my modules
import layouts          # UI Layouts
import program_state    # Programs State
import handle_config    # Programs Configuration
handle_config.init()

def cropToWidth(origImg):
    side1 = origImg[
        handle_config.SIDE1_TOP : handle_config.SIDE1_TOP + handle_config.SIDE1_HEIGHT,
        handle_config.SIDE1_LEFT : handle_config.SIDE1_LEFT + handle_config.SIDE1_WIDTH
    ].copy()

    side2 = origImg[
        handle_config.SIDE2_TOP : handle_config.SIDE2_TOP + handle_config.SIDE2_HEIGHT, 
        handle_config.SIDE2_LEFT : handle_config.SIDE2_LEFT + handle_config.SIDE2_WIDTH
    ].copy()

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
    newWidth = int(layouts.full_width)
    newHeight = int(layouts.full_width * ratio)

    # resize image to fit window
    origImg = cv2.resize(origImg, (newWidth, newHeight), PIL.Image.ANTIALIAS)

    # pad to fill height
    padding = int((layouts.row_size - newHeight) / 2)
    origImg = cv2.copyMakeBorder(origImg, padding, padding, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

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