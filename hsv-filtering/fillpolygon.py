import cv2
import numpy as np
import os

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

cv2.namedWindow('original')
cv2.setMouseCallback('original', mouse_callback)

img_original = cv2.imread('sample.jpg')

while(True):

    cv2.imshow("original", img_original)
    height, weight = img_original.shape[:2]


    if cv2.waitKey(1)&0xFF == 27:
        break

# 좌표 순서 - 상단왼쪽 끝, 상단오른쪽 끝, 하단왼쪽 끝, 하단오른쪽 끝

temp = np.zeros(img_original.shape, dtype=np.uint8)
pts = np.array(point_list, np.int32)
rect = cv2.boundingRect(pts)
x, y, w, h = rect
cropped = img_original[y: y+h, x:x+w].copy()
cv2.imshow('crop', cropped)

## (2) make mask
pts = pts - pts.min(axis=0)

mask = np.zeros(cropped.shape[:2], np.uint8)
cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

## (3) do bit-op
dst = cv2.bitwise_and(cropped, cropped, mask=mask)
cv2.imshow("mask.png", mask)
cv2.imshow("dst.png", dst)

## (4) add the white background
bg = np.ones_like(cropped, np.uint8)*255
cv2.bitwise_not(bg,bg, mask=mask)
dst2 = bg+ dst
cv2.imshow("dst2.png", dst2)
# cv2.fillPoly(temp, [pts], (255, 255, 255))
# cv2.imshow('temp', temp)


while (True):
    if cv2.waitKey(1)&0xFF == 27:
        break

cv2.destroyAllWindows()