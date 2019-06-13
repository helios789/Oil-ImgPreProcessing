import cv2
import numpy as np
import os
import shutil

path_dir = os.getcwd() + "/yoon-mask/"
file_list = os.listdir(path_dir)
file_list.sort()



print("총 " + str(len(file_list)) + " 개의 이미지 로드")

for file in file_list:
    if "cam1" in file:
        shutil.move(path_dir + file, os.getcwd() + "/cam1/" + file)

    elif "cam2" in file:
        shutil.move(path_dir + file, os.getcwd() + "/cam2/" + file)


