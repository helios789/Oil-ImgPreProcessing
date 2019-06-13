import cv2
import numpy as np
import os

path_dir = os.getcwd() + "/cam2-0.08/"
file_list = os.listdir(path_dir)
file_list.sort()


print("총 " + str(len(file_list)) + " 개의 이미지 로드")


prevImage = cv2.imread(path_dir + "mask " + file_list[0])

for idx, filename in enumerate(file_list):
    print(idx)

    if "mask" in filename:
        currentImage = cv2.imread(path_dir + file_list[idx])

        curImg = cv2.resize (currentImage, (512, 512))
        prevImg = cv2.resize (prevImage, (512, 512))
        
        ret,curImgTreshold = cv2.threshold(curImg, 50, 255, cv2.THRESH_BINARY)
        ret,prevImgTreshold = cv2.threshold(prevImg, 50, 255, cv2.THRESH_BINARY)

        diffCount = 0
        diffLowerLimit = 0.1 * curImgTreshold.shape[0] * curImgTreshold.shape[1]

        for i in range(curImgTreshold.shape[0]):
            for j in range(curImgTreshold.shape[1]):
                if prevImgTreshold[i][j][0] != curImgTreshold[i][j][0]:
                    diffCount += 1

        if diffCount > diffLowerLimit:
            prevImage = currentImage

        else:
            os.remove(os.getcwd() +"/cam2-0.08/" + filename)
            os.remove(os.getcwd() +"/cam2-0.08/" + filename[5:])

            