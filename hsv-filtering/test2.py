import cv2
import numpy as np
import os
import time
from utils.img_preprocess_util import add_hsv_trackbar, equlizeHistogram, convertRGBtoHSV
from utils.segment import segment_test

IMG_RESIZE = [256, 256]




img_rgb = cv2.imread('sample.jpg')
img_resize = cv2.resize(img_rgb, (IMG_RESIZE[0], IMG_RESIZE[1]))

# add_hsv_trackbar(img_resize)
start = time.time()
result = segment_test(img_resize)
cv2.imshow('result', result)
print(time.time() - start)

while(True):
    ch = cv2.waitKey(1)
    if ch == 27:
        break

cv2.destroyAllWindows()