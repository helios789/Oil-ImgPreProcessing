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
    # img = equlizeHistogram(img)

    # img_blur = cv2.bilateralFilter(img,9,100,100)
    img_blur = cv2.GaussianBlur(img,(9, 9),0)
    cv2.imshow('blur', img_blur)
    
    hsv_img = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv_img)

    img_yuv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2YUV)
    Y, U, V = cv2.split(img_yuv)

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

        # _, h_threshold = cv2.threshold(h, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # _, s_threshold = cv2.threshold(s, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # _, v_threshold = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # kernel = np.ones((9, 9), np.uint8)
        # h_morph = cv2.morphologyEx(h_threshold, cv2.MORPH_OPEN, kernel)
        # s_morph = cv2.morphologyEx(s_threshold, cv2.MORPH_OPEN, kernel)
        # v_morph = cv2.morphologyEx(v_threshold, cv2.MORPH_OPEN, kernel)

        # h_morph = cv2.morphologyEx(h_morph, cv2.MORPH_CLOSE, kernel)
        # s_morph = cv2.morphologyEx(s_morph, cv2.MORPH_CLOSE, kernel)
        # v_morph = cv2.morphologyEx(v_morph, cv2.MORPH_CLOSE, kernel)

        # cv2.imshow('h_threshold_morph', h_morph)
        # cv2.imshow('s_threshold_morph', s_morph)
        # cv2.imshow('v_threshold_morph', v_morph)

        # h_histogram = draw_histogram(h)
        # s_histogram = draw_histogram(s)
        # v_histogram = draw_histogram(v)
        # Y_histogram = draw_histogram(Y)
        # U_histogram = draw_histogram(U)
        # V_histogram = draw_histogram(V)

        cv2.imshow('Y', Y)
        cv2.imshow('U', U)
        cv2.imshow('V', V)

        cv2.imshow('h', h)
        cv2.imshow('s', s)
        cv2.imshow('v', v)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(15, 15))
        v_equalHist = clahe.apply(v)
        cv2.imshow('equalHist', v_equalHist)

        # cv2.imshow('Y_hist', Y_histogram)
        # cv2.imshow('U_hist', U_histogram)
        # cv2.imshow('V_hist', V_histogram)

        # cv2.imshow('h_hist', h_histogram)
        # cv2.imshow('s_hist', s_histogram)
        # cv2.imshow('v_hist', v_histogram)


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

def draw_histogram(img):

    h = np.zeros((img.shape[0], 256), dtype=np.uint8)

    hist_item = cv2.calcHist([img],[0],None,[256],[0,256])
    cv2.normalize(hist_item,hist_item,0,255,cv2.NORM_MINMAX)
    hist=np.int32(np.around(hist_item))
    for x,y in enumerate(hist):
        cv2.line(h,(x,0+10),(x,y+10),(255,255,255))

    cv2.line(h, (0, 0 + 10), (0, 5), (255, 255, 255) )
    cv2.line(h, (255, 0 + 10), (255, 5), (255, 255, 255))
    y = np.flipud(h)

    return y