import cv2
import numpy as np
import time
import os

cam_1 = cv2.VideoCapture(1)

cam_1.set(3, 1920)
cam_1.set(4, 1080)


while True:
    _, cam1_Image = cam_1.read()
    cv2.imshow('img', cam1_Image)

    now = time.localtime()
    current_time = "%04d-%02d-%02d %02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    folder_name = "%02d%02d%02d" %(now.tm_year, now.tm_mon, now.tm_mday)


    cam1_dir = './data/'+str(folder_name) + '/cam1/'
    cam1_filename = str(cam1_dir)+str(current_time)+':cam1'+'.jpg'

    cv2.imwrite(cam1_filename, cam1_Image)

    cv2.waitKey(300)


cam1.release()
cv2.destroyAllWindows()