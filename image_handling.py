'''This module handles the image'''

import cv2
import numpy as np
import PIL.Image

# my modules
import layouts          # UI Layouts
import program_state    # Programs State
import handle_config    # Programs Configuration

def transformCoords(origImg, camera, side):
    _, width, _ = origImg.shape # img size

    if camera == 1 and side == 1:
        coord1 = 210
        coord2 = width - 10
        coord3 = 0
        coord4 = width - 20
    elif camera == 1 and side == 2:
        coord1 = 0
        coord2 = width - 310
        coord3 = 110
        coord4 = width
    elif camera == 2 and side == 1:
        coord1 = 280
        coord2 = width - 20
        coord3 = 35
        coord4 = width - 70
    elif camera == 2 and side == 2:
        coord1 = 20
        coord2 = width - 300
        coord3 = 90
        coord4 = width - 20
    
    return coord1, coord2, coord3, coord4

def cropToWidth(origImg, camera):
    height, _, _ = origImg.shape

    if camera == 1:
        left1Bound = 1410
        right1Bound = 1980
        left2Bound = 2155
        right2Bound = 2815
    else:
        left1Bound = 1290
        right1Bound = 1910
        left2Bound = 2055
        right2Bound = 2705

    # calculate mid points
    # side1Mid = int(left1Bound + (right1Bound - left1Bound) / 2)
    # side2Mid = int(left2Bound + (right2Bound - left2Bound) / 2)

    # draw side 1 boundaries
    # cv2.line(origImg, (left1Bound, 0), (left1Bound, height), (255,0,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (side1Mid, 0), (side1Mid, height), (0,255,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (right1Bound, 0), (right1Bound, height), (0,0,255), 5) # Top-Left to Bottom-Left

    # draw side 2 boundaries
    # cv2.line(origImg, (left2Bound, 0), (left2Bound, height), (255,0,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (side2Mid, 0), (side2Mid, height), (0,255,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (right2Bound, 0), (right2Bound, height), (0,0,255), 5) # Top-Left to Bottom-Left

    side1 = origImg[0:height, left1Bound:right1Bound].copy()
    side2 = origImg[0:height, left2Bound:right2Bound].copy()

    return side1, side2

# plot transformation circles on image
def plotCircles(origImg, camera, side):
    height, _, _ = origImg.shape # img size

    coord1, coord2, coord3, coord4 = transformCoords(origImg, camera, side)
    
    cv2.circle(origImg, (coord1, 0), 5, (0, 0, 255), 2)   # Top-Left
    cv2.circle(origImg, (coord2, 0), 5, (0, 0, 255), 2)  # Top-Right
    cv2.circle(origImg, (coord3, height), 5, (0, 0, 255), 2)  # Bottom-Left
    cv2.circle(origImg, (coord4, height), 5, (0, 0, 255), 2) # Bottom-Right
    
    cv2.line(origImg, (coord1, 0), (coord3, height), (0, 0, 255), 2) # Top-Left to Bottom-Left
    cv2.line(origImg, (coord2, 0), (coord4, height), (0, 0, 255), 2) # Top-Right to Bottom-Right
    
    return origImg

# transform image to plane
def transform(origImg, camera, side):
    height, width, _ = origImg.shape # img size

    coord1, coord2, coord3, coord4 = transformCoords(origImg, camera, side)
    
    pts1 = np.float32([[coord1, 0], [coord2, 0], [coord3, height], [coord4, height]])
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

def cropToLength(origImg, camera):
    height, width, _ = origImg.shape

    cam1Length = 1460
    cam2Length = 1310

    if camera == 1:
        crop = width - int(cam1Length / 1200 * handle_config.BOARD_LENGTH)
        # cv2.line(origImg, (crop, 0), (crop, height), (255,0,0), 5) # Top-Left to Bottom-Left
        origImg = origImg[0:height, crop:width].copy()
    elif camera == 2:
        crop = int(cam2Length / 1200 * handle_config.BOARD_LENGTH)
        # cv2.line(origImg, (crop, 0), (crop, height), (255,255,255), 5) # Top-Left to Bottom-Left
        origImg = origImg[0:height, 0:crop].copy()

    return origImg

# thresh box image and return black vs white count
def threshImg(origImg, camera):
    # grey image
    greyImg = cv2.cvtColor(origImg, cv2.COLOR_BGR2GRAY)

    # draw thresh boxes
    if camera == 1:
        _, threshImg = cv2.threshold(greyImg, handle_config.CAM1_THRESH, 255, 0)
    else:
        _, threshImg = cv2.threshold(greyImg, handle_config.CAM2_THRESH, 255, 0)

    return threshImg

# calculate percentage of black pixels in given img
def barkCalc(origImg):
    totalPixels = origImg.size
    whitePixels = cv2.countNonZero(origImg)
    blackPixels = totalPixels - whitePixels
    return round(blackPixels / totalPixels * 100, 2)

# gather bark percentages for the three columns
def analyseImg(origImg, threshImg):
    height, width, _ = origImg.shape

    midWidth = int(width / 2)

    quarter = int(height / 4)
    threeQuarter = quarter * 3

    columnA = threshImg[0:quarter, 0:width].copy()
    columnB = threshImg[quarter:threeQuarter, 0:width].copy()
    columnC = threshImg[threeQuarter:height, 0:width].copy()

    columnAPerc = barkCalc(columnA)
    columnBPerc = barkCalc(columnB)
    columnCPerc = barkCalc(columnC)
    
    # if not thresh or transform mode show columns
    if not program_state.THRESH_MODE and not program_state.SHOW_TRANSFORM:
        cv2.line(origImg, (0, quarter), (width, quarter), (0, 0, 255), 5) # 25% line
        cv2.line(origImg, (0, threeQuarter), (width, threeQuarter), (0, 0, 255), 5) # 75% line

        _, textHeight = cv2.getTextSize("A", cv2.FONT_HERSHEY_SIMPLEX, 3, 3)
        quarterTxt = int(quarter / 2) + textHeight
        midText = quarter * 2 + textHeight
        threeQuarterTxt = threeQuarter + quarterTxt

        cv2.putText(origImg, "A", (midWidth, quarterTxt), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
        cv2.putText(origImg, "B", (midWidth, midText), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)
        cv2.putText(origImg, "C", (midWidth, threeQuarterTxt), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 3)

    return origImg, columnAPerc, columnBPerc, columnCPerc

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

def main(origImg, camera, ignoreFlags):
    # crop image to plank width
    side1, side2 = cropToWidth(origImg, camera)

    # show transform
    if not ignoreFlags and program_state.SHOW_TRANSFORM:
        side1 = plotCircles(side1, camera, 1)
        side2 = plotCircles(side2, camera, 2)

    # perform transform
    if ignoreFlags or not program_state.SHOW_TRANSFORM:
        side1 = transform(side1, camera, 1)
        side2 = transform(side2, camera, 2)
    
    # rotate image
    side1 = rotateImg(side1, camera)
    side2 = rotateImg(side2, camera)

    # crop image to plank length
    if not program_state.SHOW_TRANSFORM:
        side1 = cropToLength(side1, camera)
        side2 = cropToLength(side2, camera)

    # calculate box thresh values
    threshedSide1Img = threshImg(side1, camera)
    threshedSide2Img = threshImg(side2, camera)

    side1, side1columnAPerc, side1columnBPerc, side1columnCPerc = analyseImg(side1, threshedSide1Img)
    side2, side2columnAPerc, side2columnBPerc, side2columnCPerc = analyseImg(side2, threshedSide2Img)

    # resize image
    side1 = resizeImg(side1)
    side2 = resizeImg(side2)

    # # if thresh mode show thresh image
    if not ignoreFlags and program_state.THRESH_MODE:
        side1 = resizeImg(threshedSide1Img)
        side2 = resizeImg(threshedSide2Img)

    if camera == 2:
        return cv2.imencode('.png', side1)[1].tobytes(), \
            cv2.imencode('.png', side2)[1].tobytes(), \
            side1columnAPerc, side1columnBPerc, side1columnCPerc, \
            side2columnAPerc, side2columnBPerc, side2columnCPerc
    else: 
        return cv2.imencode('.png', side2)[1].tobytes(), \
            cv2.imencode('.png', side1)[1].tobytes(), \
            side2columnAPerc, side2columnBPerc, side2columnCPerc, \
            side1columnAPerc, side1columnBPerc, side1columnCPerc