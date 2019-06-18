import cv2
import numpy as np

def nothing(x):
    pass


def add_hsv_trackbar(img):
    filename='hsvTrackbar'
    cv2.namedWindow(filename)

    #set trackbar
    hh = 'hue high'
    hl = 'hue low'
    sh = 'saturation high'
    sl = 'saturation low'
    vh = 'value high'
    vl = 'value low'

    #set ranges    
    cv2.createTrackbar(hl, filename, 0, 179, nothing)
    cv2.createTrackbar(hh, filename, 0, 179, nothing)
    cv2.createTrackbar(sl, filename, 0, 255, nothing)
    cv2.createTrackbar(sh, filename, 0, 255, nothing)
    cv2.createTrackbar(vl, filename, 0, 255, nothing)
    cv2.createTrackbar(vh, filename, 0, 255, nothing)

    # set initial value

    cv2.setTrackbarPos(hl, filename, 0)    
    cv2.setTrackbarPos(hh, filename, 179)
    cv2.setTrackbarPos(sl, filename, 0)
    cv2.setTrackbarPos(sh, filename, 255)
    cv2.setTrackbarPos(vl, filename, 0)
    cv2.setTrackbarPos(vh, filename, 255)


    #convert rgb to hsv
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    while True:
        hul= cv2.getTrackbarPos(hl, filename)
        huh= cv2.getTrackbarPos(hh, filename)
        sal= cv2.getTrackbarPos(sl, filename)
        sah= cv2.getTrackbarPos(sh, filename)
        val= cv2.getTrackbarPos(vl, filename)
        vah= cv2.getTrackbarPos(vh, filename)

        hsvl = np.array([hul, sal, val], np.uint8)
        hsvh = np.array([huh, sah, vah], np.uint8) 

        mask = cv2.inRange(hsv_img, hsvl, hsvh)
        res = cv2.bitwise_and(img, img, mask=mask)

        cv2.imshow(filename, mask)
        cv2.imshow('img', res) 

        ch = cv2.waitKey(1)
        if ch== 27:
            break


def equlizeHistogram(img):
    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])
    img_equalHist = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

    return img_equalHist


def convertRGBtoHSV(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img_hsv)
    hsv = np.concatenate((h, s, v), axis=1)

    return hsv