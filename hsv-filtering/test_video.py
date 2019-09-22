import cv2
import numpy as np
import os
import time
from utils.segment import segment_test

IMG_RESIZE = [256, 256]

# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('2019-09-22 17-51-26.avi')
# cap = cv2.VideoCapture(1)
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video stream or file")
 
# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret == True:
        # Display the resulting frame
        start = time.time()

        img_resize = cv2.resize(frame, (IMG_RESIZE[0], IMG_RESIZE[1]))
        result = segment_test(img_resize)
        yuv = cv2.cvtColor(result, cv2.COLOR_BGR2YUV)
        y, u, v = cv2.split(yuv)

        # for i in range(IMG_RESIZE[0]):
        #     for j in range(IMG_RESIZE[0]):
        #         if y[i][j] > 100:
        #             result[i][j][:] = 255
        #         else:
        #             result[i][j][:] = 0
        ret, thresh_u = cv2.threshold(u, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        ret, thresh_v = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        cv2.imshow('frame', frame)
        cv2.imshow('seg', result)
        cv2.imshow('y', y)
        cv2.imshow('u', u)
        cv2.imshow('v', v)
        cv2.imshow('thresh_otsu_u', thresh_u)
        cv2.imshow('thresh_otsu_v', thresh_v)

        print(time.time() - start)

        while(True):
            ch = cv2.waitKey(1)
            if ch == 27:
                break

cv2.destroyAllWindows()
cap.release()