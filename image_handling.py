'''This module handles the image'''

import cv2
import numpy as np
import PIL.Image

# my modules
import layouts          # UI Layouts

# transform positions
topLeftX, topLeftY = 0, 50
topRightX, topRightY = 0, 232
bottomLeftY, bottomRightY = 20, 278

# plot circles on image
def plotCircles(origImg):
    _, width, _ = origImg.shape # img size

    cv2.circle(origImg, (topLeftX, topLeftY), 5, (0, 0, 255), 2)   # Top-Left
    cv2.circle(origImg, (topRightX, topRightY), 5, (0, 0, 255), 2)  # Top-Right
    cv2.circle(origImg, (width, bottomLeftY), 5, (0, 0, 255), 2)  # Bottom-Left
    cv2.circle(origImg, (width, bottomRightY), 5, (0, 0, 255), 2) # Bottom-Right
    
    cv2.line(origImg, (topLeftX, topLeftY), (width, bottomLeftY), (255,0,0), 1) # Top-Left to Bottom-Left
    cv2.line(origImg, (topRightX, topRightY), (width, bottomRightY), (255,0,0), 1) # Top-Right to Bottom-Right
    
    return origImg

# transform white light image
def transform(origImg):
    height, width, _ = origImg.shape # img size

    pts1 = np.float32([[topLeftX, topLeftY], [width, bottomLeftY], [topRightX, topRightY], [width, bottomRightY]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    transformed = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(origImg, transformed, (width, height))

def hangle_img(origImg): 
    # height of orig img
    origHeight = origImg.shape[0]
    origWidth = origImg.shape[1]

    test1 = int(origWidth / 2 - 340)
    test2 = int(origWidth / 2 + 240)

    origImg = origImg[0:origHeight, test1:test2]
    origImg = cv2.transpose(origImg) # rotate image
    
    # heigh, width and ratio of cropped and rotated img
    newHeight = origImg.shape[0]
    newWidth = origImg.shape[1]
    ratio = newHeight / newWidth
    
    # adjust width to image ratio
    new_width = int(layouts.row_size / ratio)

    # resize image to fit window
    origImg = cv2.resize(origImg, (new_width, layouts.row_size), PIL.Image.ANTIALIAS)

    # show transform
    # origImg = plotCircles(origImg)

    # perform transform
    origImg = transform(origImg)

    return cv2.imencode('.png', origImg)[1].tobytes()