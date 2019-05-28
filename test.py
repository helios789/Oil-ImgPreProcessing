import cv2
import numpy as np
import os

hsv_darkoil_filter_list = [
    #[(lower_bound_h, s, v), (upper_bound_h, s, v)]
    [(0, 0, 0), (179, 255, 200)],
    [(95, 50, 0), (179, 255, 200)],
    [(0, 0, 0), (179, 130, 150)],
    [(0, 0, 0), (179, 130, 150)],
    [(0, 0, 0), (179, 130, 150)],
    [(0, 0, 0), (179, 130, 150)],

    [(0, 0, 0), (179, 255, 200)],
    [(95, 50, 0), (179, 255, 200)],
    [(0, 0, 0), (179, 130, 150)],
    [(0, 0, 0), (179, 130, 150)],
    [(0, 0, 0), (179, 130, 150)],
    [(0, 0, 0), (179, 130, 150)],

    [(0, 0, 0), (179, 255, 200)],
    [(95, 50, 0), (179, 255, 200)],
    [(0, 0, 0), (179, 130, 150)],
    [(0, 0, 0), (179, 130, 150)],
    [(0, 0, 0), (179, 130, 150)],
    [(0, 0, 0), (179, 130, 150)],
]

path_dir = os.getcwd() + "/img/"
file_list = os.listdir(path_dir)

print(file_list)

for file in file_list:
    img_rgb = cv2.imread(path_dir + file)
    img_resize = cv2.resize(img_rgb, (256, 256), interpolation=cv2.INTER_AREA)

    img_hsv = cv2.cvtColor(img_resize, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img_hsv)
    hsv = np.concatenate((h, s, v), axis=1)

    mask_list = []

    for filter in hsv_darkoil_filter_list:
        hsv_lower_bound = filter[0]
        hsv_uppter_bound = filter[1]

        mask = cv2.inRange(img_hsv, hsv_lower_bound, hsv_uppter_bound)

        mask_list.append(mask)

    
    temp = []
    mask_list_row = 3
    mask_list_col = 6

    for i in range(mask_list_row):
        temp.append(np.concatenate(mask_list [mask_list_col*i : mask_list_col*(i+1)], axis=1))
    result = np.concatenate(temp, axis=0)

    cv2.imshow('hsv', hsv)
    cv2.imshow('mask', result)
    cv2.imshow('origin', img_resize)

    # cv2.imwrite('./mask.jpg', mask);
    cv2.waitKey(0)


cv2.destroyAllWindows()