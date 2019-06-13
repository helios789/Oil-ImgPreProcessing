import cv2
import numpy as np
import os


def mouse_callback(event, x, y ,flags, param):

    # mouse Left button clicked
    if event == cv2.EVENT_FLAG_MBUTTON and flags == cv2.EVENT_LBUTTONDOWN:
        X = x / 256
        Y = y / 256
        print(X,", ",Y)

cv2.namedWindow('mask')
cv2.setMouseCallback('mask', mouse_callback)

filter_list_row = 2
filter_list_col = 6
hsv_darkoil_filter_list = [
    #[(lower_bound_h, s, v), (upper_bound_h, s, v)]
    [(0, 0, 0), (179, 255, 200)],    
    [(0, 0, 0), (179, 130, 150)],    
    [(0, 0, 0), (179, 90, 120)],    
    [(50, 80, 0), (179, 255, 200)],
    [(70, 70, 0), (179, 255, 200)],    
    [(95, 50, 0), (179, 255, 200)],

    [(0, 0, 0), (179, 180, 120)],    
    [(0, 0, 0), (179, 150, 150)],    
    [(0, 0, 0), (179, 120, 180)],    
    [(70, 100, 0), (179, 255, 200)],
    [(85, 85, 0), (179, 255, 200)],    
    [(105, 70, 0), (179, 255, 200)],
]

path_dir = os.getcwd() + "/img/"
file_name = "2019-05-16 11:39:15:cam1.jpg"

img_rgb = cv2.imread(path_dir + file_name)
img_resize = cv2.resize(img_rgb, (256, 256), interpolation=cv2.INTER_AREA)

img_hsv = cv2.cvtColor(img_resize, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(img_hsv)
hsv = np.concatenate((h, s, v), axis=1)


mask_list = []

for index, filter in enumerate(hsv_darkoil_filter_list):
    hsv_lower_bound = filter[0]
    hsv_uppter_bound = filter[1]

    mask = cv2.inRange(img_hsv, hsv_lower_bound, hsv_uppter_bound)
    mask_list.append(mask)


temp = []

for i in range(filter_list_row):
    temp.append(np.concatenate(mask_list [filter_list_col*i : filter_list_col*(i+1)], axis=1))
result = np.concatenate(temp, axis=0)


cv2.imshow('hsv', hsv)
cv2.imshow('mask', result)
cv2.imshow('origin', img_resize)

# cv2.imwrite('./mask.jpg', mask);
cv2.waitKey(0)


cv2.destroyAllWindows()