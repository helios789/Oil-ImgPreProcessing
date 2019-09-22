import cv2
import numpy as np
import os
from utils.img_preprocess_util import add_hsv_trackbar, equlizeHistogram, convertRGBtoHSV
from utils.segment import segment

IMG_RESIZE = [256, 256]

path_dir = os.getcwd() + "/img/"
# output_path_dir = os.getcwd() +"/mask/"
file_list = os.listdir(path_dir)
file_list.sort()


for idx, file in enumerate(file_list):

    img_rgb = cv2.imread(path_dir + file)
    img_resize = cv2.resize(img_rgb, (IMG_RESIZE[0], IMG_RESIZE[1]))
    
    # add_hsv_trackbar(img_resize)
    segment(img_resize)


cv2.destroyAllWindows()