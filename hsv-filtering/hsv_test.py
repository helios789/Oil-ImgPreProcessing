import cv2
import numpy as np
import os
from utils.img_preprocess_util import add_hsv_trackbar, equlizeHistogram, convertRGBtoHSV
from utils.segment import segment

IMG_RESIZE = [512, 512]




img_rgb = cv2.imread('sample.jpg')
img_resize = cv2.resize(img_rgb, (IMG_RESIZE[0], IMG_RESIZE[1]))

# add_hsv_trackbar(img_resize)
segment(img_resize)


cv2.destroyAllWindows()