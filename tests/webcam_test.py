import numpy as np
import cv2
import time

cap1 = cv2.VideoCapture(0)
cap1.set(3, 3840)                # CAM WIDTH
cap1.set(4, 2160)               # CAM HEIGHT
cap2 = cv2.VideoCapture(1)
cap2.set(3, 3840)                # CAM WIDTH
cap2.set(4, 2160)               # CAM HEIGHT

prev_frame_time1 = 0
new_frame_time1 = 0
prev_frame_time2 = 0
new_frame_time2 = 0

while(True):
    # Capture frame-by-frame
    ret1, img1 = cap1.read()
  
    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time1 = time.time()
  
    # Calculating the fps1
  
    # fps1 will be number of frame processed in given time frame
    # since their will be most of time error of 0.001 second
    # we will be subtracting it to get more accurate result
    fps1 = 1/(new_frame_time1-prev_frame_time1)
    prev_frame_time1 = new_frame_time1
  
    # converting the fps1 into integer
    fps1 = int(fps1)
  
    # converting the fps1 to string so that we can display it on frame
    # by using putText function
    fps1 = str(fps1)
  
    # puting the FPS count on the frame
    cv2.putText(img1, fps1, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
  
    scale_percent = 20 # percent of original size
    width = int(img1.shape[1] * scale_percent / 100)
    height = int(img1.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized1 = cv2.resize(img1, dim, interpolation = cv2.INTER_AREA)

    # Capture frame-by-frame
    ret2, img2 = cap2.read()
  
    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time2 = time.time()
  
    # Calculating the fps2
  
    # fps2 will be number of frame processed in given time frame
    # since their will be most of time error of 0.002 second
    # we will be subtracting it to get more accurate result
    fps2 = 1/(new_frame_time2-prev_frame_time2)
    prev_frame_time2 = new_frame_time2
  
    # converting the fps2 into integer
    fps2 = int(fps2)
  
    # converting the fps2 to string so that we can display it on frame
    # by using putText function
    fps2 = str(fps2)
  
    # puting the FPS count on the frame
    cv2.putText(img2, fps2, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
  
    scale_percent = 20 # percent of original size
    width = int(img2.shape[1] * scale_percent / 100)
    height = int(img2.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    resized2 = cv2.resize(img2, dim, interpolation = cv2.INTER_AREA)

    # Display the resulting frame
    cv2.imshow('frame1', resized1)
    cv2.imshow('frame2', resized2)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap1.release()
cv2.destroyAllWindows()