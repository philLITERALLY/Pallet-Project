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
        coord1 = 190
        coord2 = width
        coord3 = 0
        coord4 = width - 40
    elif camera == 1 and side == 2:
        coord1 = 0
        coord2 = width - 190
        coord3 = 40
        coord4 = width
    elif camera == 2 and side == 1:
        coord1 = 160
        coord2 = width - 40
        coord3 = 35
        coord4 = width - 30
    elif camera == 2 and side == 2:
        coord1 = 0
        coord2 = width - 230
        coord3 = 80
        coord4 = width
    
    return coord1, coord2, coord3, coord4

def cropToWidth(origImg, camera):
    height, _, _ = origImg.shape

    if camera == 1:
        side1Mid = 1560
        side2Mid = 2320
    else:
        side1Mid = 1690
        side2Mid = 2405

    # Handle Side 1
    left1Bound = side1Mid - handle_config.FRAME_WIDTH
    right1Bound = side1Mid + handle_config.FRAME_WIDTH

    # draw side 1 boundaries
    # cv2.line(origImg, (left1Bound, 0), (left1Bound, height), (255,0,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (side1Mid, 0), (side1Mid, height), (0,255,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (right1Bound, 0), (right1Bound, height), (0,0,255), 5) # Top-Left to Bottom-Left

    # Handle Side 2
    left2Bound = side2Mid - handle_config.FRAME_WIDTH
    right2Bound = side2Mid + handle_config.FRAME_WIDTH

    # draw side 2 boundaries
    # cv2.line(origImg, (left2Bound, 0), (left2Bound, height), (255,0,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (side2Mid, 0), (side2Mid, height), (0,255,0), 5) # Top-Left to Bottom-Left
    # cv2.line(origImg, (right2Bound, 0), (right2Bound, height), (0,0,255), 5) # Top-Left to Bottom-Left

    side1 = origImg[0:height, left1Bound:right1Bound].copy()
    side2 = origImg[0:height, left2Bound:right2Bound].copy()

    return side1, side2

# plot transformation circles on image
def plotCircles(origImg, camera, side):
    height, width, _ = origImg.shape # img size

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

    if camera == 1:
        crop = 450
        # cv2.line(origImg, (crop, 0), (crop, height), (255,255,255), 5) # Top-Left to Bottom-Left
        origImg = origImg[0:height, crop:width].copy()
    elif camera == 2:
        crop = 1550
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

    totalPixels = threshImg.size
    whitePixels = cv2.countNonZero(threshImg)
    blackPixels = totalPixels - whitePixels

    return threshImg, round(blackPixels / totalPixels * 100, 2)

# calculate percentage of black pixels in given img
def barkCalc(origImg):
    totalPixels = origImg.size
    whitePixels = cv2.countNonZero(origImg)
    blackPixels = totalPixels - whitePixels
    return round(blackPixels / totalPixels * 100, 2)

# gather bark percentages for the three columns
def analyseImg(origImg, camera, side, filename):
    height, width = origImg.shape

    quarter = int(height / 4)
    threeQuarter = quarter * 3

    columnA = origImg[0:quarter, 0:width].copy()
    columnB = origImg[quarter:threeQuarter, 0:width].copy()
    columnC = origImg[threeQuarter:height, 0:width].copy()

    cv2.imshow('Camera ' + str(camera) + ' Side ' + str(side) + ' - columnA', columnA)
    cv2.imshow('Camera ' + str(camera) + ' Side ' + str(side) + ' - columnB', columnB)
    cv2.imshow('Camera ' + str(camera) + ' Side ' + str(side) + ' - columnC', columnC)

    cv2.imwrite('tests/' + filename + '/columnA.jpg', columnA)
    cv2.imwrite('tests/' + filename + '/columnB.jpg', columnB)
    cv2.imwrite('tests/' + filename + '/columnC.jpg', columnC)

    columnAPerc = barkCalc(columnA)
    columnBPerc = barkCalc(columnB)
    columnCPerc = barkCalc(columnC)

    return columnAPerc, columnBPerc, columnCPerc

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

def main(origImg, camera, ignoreFlags, filename):
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
    side1 = cropToLength(side1, camera)
    side2 = cropToLength(side2, camera)

    # calculate box thresh values
    threshedSide1Img, side1Percent = threshImg(side1, camera)
    threshedSide2Img, side2Percent = threshImg(side2, camera)

    side1columnAPerc, side1columnBPerc, side1columnCPerc = analyseImg(threshedSide1Img, camera, 1, filename)
    # side2columnAPerc, side2columnBPerc, side2columnCPerc = analyseImg(threshedSide2Img, camera, 2)

    print(filename, ' || ', side1columnAPerc, ' || ', side1columnBPerc, ' || ', side1columnCPerc)

    # crop image to plank
    origImg = resizeImg(origImg)
    side1 = resizeImg(side1)
    side2 = resizeImg(side2)

    # # if thresh mode show thresh image
    if True: # not ignoreFlags and program_state.THRESH_MODE:
        side1 = resizeImg(threshedSide1Img)
        side2 = resizeImg(threshedSide2Img)

    # if camera == 1:
    #     return side1, side2, side1Percent, side2Percent
    # else:
    #     return side2, side1, side2Percent, side1Percent

    if camera == 1:
        return cv2.imencode('.png', side1)[1].tobytes(), \
            cv2.imencode('.png', side2)[1].tobytes(), \
            side1Percent, side2Percent
    else: 
        return cv2.imencode('.png', side2)[1].tobytes(), \
            cv2.imencode('.png', side1)[1].tobytes(), \
            side2Percent, side1Percent





handle_config.init()    # config settings need loaded

# cam1 = cv2.imread('tests/Pallet_r2_cam1.jpg')
# cam2 = cv2.imread('tests/Pallet_R2_cam2.jpg')

# cam1side1, cam1side2, cam1side1Perc, cam1side2Perc = main(cam1, 1, True)
# cam2side1, cam2side2, cam2side1Perc, cam2side2Perc = main(cam2, 2, True)

Pallet_r2_cam1 = cv2.imread('tests/Pallet_r2_cam1.jpg')
Pallet_r2_cam1_barked = cv2.imread('tests/Pallet_r2_cam1_barked.jpg')
Pallet_r2_cam1_barked_edge = cv2.imread('tests/Pallet_r2_cam1_barked_edge.jpg')
Pallet_r2_cam1_barked_single = cv2.imread('tests/Pallet_r2_cam1_barked_single.jpg')

Pallet_r2_cam1, _, _, _ = main(Pallet_r2_cam1, 1, True, 'Pallet_r2_cam1')
Pallet_r2_cam1_barked, _, _, _ = main(Pallet_r2_cam1_barked, 1, True, 'Pallet_r2_cam1_barked')
Pallet_r2_cam1_barked_edge, _, _, _ = main(Pallet_r2_cam1_barked_edge, 1, True, 'Pallet_r2_cam1_barked_edge')
Pallet_r2_cam1_barked_single, _, _, _ = main(Pallet_r2_cam1_barked_single, 1, True, 'Pallet_r2_cam1_barked_single')

# cv2.imshow('Cam 1', cam1)
# cv2.imshow('cam1side1', cam1side1)
# cv2.imshow('cam1side2', cam1side2)
# cv2.imshow('Cam 2', cam2)
# cv2.imshow('cam2side1', cam2side1)
# cv2.imshow('cam2side2', cam2side2)

cv2.waitKey(0)
cv2.destroyAllWindows()