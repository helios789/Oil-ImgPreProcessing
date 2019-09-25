import cv2
import numpy as np
import os
import time
from utils.segment import segment_test

def mouse_callback(event, x, y, flags, param):
    global point_list, count, img_original


    # 마우스 왼쪽 버튼 누를 때마다 좌표를 리스트에 저장
    if event == cv2.EVENT_LBUTTONDOWN:
        print("(%d, %d)" % (x, y))
        point_list.append([x, y])

        print(point_list)
        cv2.circle(img_original, (x, y), 3, (0, 0, 255), -1)

IMG_RESIZE = (256, 256)
point_list = []
count = 0


#cap = cv2.VideoCapture(0)
cap = cv2.VideoCapture('1.mp4')

if (cap.isOpened()== False): 
    print("Error opening video stream or file")
cap.set(cv2.CAP_PROP_POS_MSEC,1*60*1000)  

cv2.namedWindow('original')
cv2.setMouseCallback('original', mouse_callback)
ret, img_original = cap.read()
img_original = cv2.resize(img_original, (IMG_RESIZE[0], IMG_RESIZE[1]))

while(cap.isOpened()):
    ret, img_original = cap.read()
    img_original = cv2.resize(img_original, (IMG_RESIZE[0], IMG_RESIZE[1]))
    cv2.imshow('original', img_original)
    height, weight = img_original.shape[:2]


    if cv2.waitKey(1)&0xFF == 27:
        break

temp = np.zeros(img_original.shape, dtype=np.uint8)
pts = np.array(point_list, np.int32)
rect = cv2.boundingRect(pts)
x, y, w, h = rect

thresh = 60
fast = 1000
fast_flag = False

ret, frame = cap.read()
frame = cv2.resize(frame, (IMG_RESIZE[0], IMG_RESIZE[1]))
# tracker = cv2.cv2.TrackerCSRT_create()
# tracker = cv2.cv2.TrackerTLD_create()
# bbox = cv2.selectROI(frame, False)
# ok = tracker.init(frame, bbox)

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # ok, bbox = tracker.update(frame)
    # if ok:
    #     # Tracking success
    #     p1 = (int(bbox[0]), int(bbox[1]))
    #     p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        
    #     cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    #     # cv2.rectangle(frame, p1, p2, (255,0,0), -1) 
    # else :
    #     # Tracking failure
    #     print("Tracking failure detected")


    # cv2.rectangle(frame, p1, p2, (0,123,180), -1)

    if ret == True:    
        if fast_flag == True:
            if fast > 0:
                fast -= 1
                continue
            else:
                fast = 100
                fast_flag = False

        frame = cv2.resize(frame, (IMG_RESIZE[0], IMG_RESIZE[1]))
        cv2.imshow('original', cv2.resize(frame, (512, 512)))
        frame = cv2.GaussianBlur(frame, (7,7), 0)


        start = time.time()
        cropped = frame[y: y+h, x:x+w].copy()
        
        # bbox = tracker.update(frame)
        # cv2.imshow('crop', cropped)

        ## (2) make mask
        pts = pts - pts.min(axis=0)

        mask = np.zeros(cropped.shape[:2], np.uint8)
        cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

        ## (3) do bit-op
        dst = cv2.bitwise_and(cropped, cropped, mask=mask)
        # cv2.imshow("mask", mask)
        # cv2.imshow("dst", dst)

        ## (4) add the white background
        bg = np.ones_like(cropped, np.uint8)*255
        cv2.bitwise_not(bg,bg, mask=mask)
        dst2 = bg+ dst
        # cv2.imshow("dst2", dst2)

        result = segment_test(dst2)
        cv2.imshow('seg', result)

        yuv = cv2.cvtColor(result, cv2.COLOR_BGR2YUV)

        cv2.imshow('y', yuv[:,:,0])
        cv2.imshow('u', yuv[:,:,1])
        cv2.imshow('v', yuv[:,:,2])

        # thresh_y = cv2.adaptiveThreshold(yuv[:, :, 0], 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 51, 11)
        _, thresh_y = cv2.threshold(yuv[:,:,0], thresh, 255, cv2.THRESH_TOZERO)
        cv2.imshow('treshold', cv2.resize(thresh_y, (400, 512)))


        # ret, thresh_y = cv2.threshold(yuv[:,:,0], 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)


        print(time.time() - start)
        ch = cv2.waitKey(1)
        print('thresh: ', thresh)
        if ch == 113:    # 'Q'
            thresh += 1
        elif ch == 97:  # 'A'
            thresh -= 1
        elif ch == 102:  # 'F'
            fast_flag = True
        elif ch == 27:
            break
        # 좌표 순서 - 상단왼쪽 끝, 상단오른쪽 끝, 하단왼쪽 끝, 하단오른쪽 끝

        # cv2.fillPoly(temp, [pts], (255, 255, 255))
        # cv2.imshow('temp', temp)

cv2.destroyAllWindows()
cap.release()