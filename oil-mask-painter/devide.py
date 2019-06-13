import cv2
import numpy as np
import os
import shutil

path_dir = os.getcwd() + "/cam2-0.1/"
file_list = os.listdir(path_dir)
file_list.sort()


print("총 " + str(len(file_list)) + " 개의 이미지 로드")

for idx, file in enumerate(file_list):
    if idx % 4 == 0:
        shutil.move(path_dir + file, os.getcwd() + "/injae/" + file)
        shutil.move(path_dir + "mask " + file, os.getcwd() + "/injae/" + "mask "+ file)

    if idx % 4 == 1:
        shutil.move(path_dir + file, os.getcwd() + "/hoon/" + file)
        shutil.move(path_dir + "mask " + file, os.getcwd() + "/hoon/" + "mask "+ file)

    if idx % 4 == 2:
        shutil.move(path_dir + file, os.getcwd() + "/kyu/" + file)
        shutil.move(path_dir + "mask " + file, os.getcwd() + "/kyu/" + "mask "+ file)

    if idx % 4 == 3:
        shutil.move(path_dir + file, os.getcwd() + "/kimkim/" + file)
        shutil.move(path_dir + "mask " + file, os.getcwd() + "/kimkim/" + "mask "+ file)