import cv2
import numpy as np
import os
import time

path_dir = os.getcwd() + "/injae/"
file_list_all = os.listdir(path_dir)
file_list_all.sort()
file_list = list(filter(lambda x : "mask" not in x, file_list_all))

print("총 " + str(len(file_list)) + " 개의 이미지 로드")

img_resize = (1280, 720)

img = cv2.imread(path_dir + file_list[0])
img = cv2.resize(img, img_resize)

img_copy = img.copy()

mask = cv2.imread(path_dir+ '/mask ' + file_list[0])
mask = cv2.resize(mask, img_resize)

ret, maskTreshold = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)


circle_size = 20
circle_color = (0, 0, 255)

mouse_x = 0
mouse_y = 0

draw = False
remove = False
all_remove = False

mask_alpha = 0.6

time_all = 0

def mouse_callback(event, x, y, flags, param):
    global mouse_x, mouse_y, draw, remove, all_remove, img, maskTreshold

    if draw == True:
        img_temp = img_copy.copy()

        cv2.circle(maskTreshold,(x,y),circle_size, circle_color, -1)  

        img = cv2.addWeighted(maskTreshold, mask_alpha, img_temp, 1 - mask_alpha, 0)

        cv2.imshow('mask', maskTreshold)
        cv2.imshow('img', img)


    if remove == True:
        img_temp = img_copy.copy()
        
        circle_mask = np.ones((img.shape[0], img.shape[1], 1), np.uint8)

        cv2.circle(circle_mask, (x,y), circle_size, (0), -1)  
        maskTreshold = cv2.bitwise_or(maskTreshold, maskTreshold, mask=circle_mask)

        img = cv2.addWeighted(maskTreshold, mask_alpha, img_temp, 1 - mask_alpha, 0)

        cv2.imshow('mask', maskTreshold)
        cv2.imshow('img', img)


    if all_remove == True:
        img_temp = img_copy.copy()
        
        circle_mask = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)

        cv2.circle(circle_mask, (x,y), circle_size, (1), -1)
        maskTreshold = cv2.bitwise_and(maskTreshold, maskTreshold, mask=circle_mask)

        img = cv2.addWeighted(maskTreshold, mask_alpha, img_temp, 1 - mask_alpha, 0)

        cv2.imshow('mask', maskTreshold)
        cv2.imshow('img', img)

        all_remove = False


    if event == cv2.EVENT_MOUSEMOVE: # 마우스 이동

        mouse_x = x
        mouse_y = y

        img_temp = img.copy()
        img_temp = cv2.circle(img_temp,(x,y),circle_size, circle_color, -1)
        cv2.imshow('img', img_temp)
            

    if event == cv2.EVENT_LBUTTONDOWN: #마우스를 누른 상태
        draw = True 


    if event == cv2.EVENT_LBUTTONUP:
        draw = False     


cv2.namedWindow('img')
cv2.setMouseCallback('img', mouse_callback)


for idx, filename in enumerate(file_list):


    print("진행 : ", idx + 1 , " / ", len(file_list))

    img = cv2.imread(path_dir + filename)
    mask = cv2.imread(path_dir+  '/mask ' + filename)

    img = cv2.resize(img, img_resize)
    mask = cv2.resize(mask, img_resize)

    img_copy = img.copy()

    ret, maskTreshold = cv2.threshold(mask, 50, 255, cv2.THRESH_BINARY)

    
    for i in range(maskTreshold.shape[0]):
        for j in range(maskTreshold.shape[1]):

            # mask On
            if maskTreshold[i][j][2] == 255:
                
                # mask color: red
                maskTreshold[i][j][0] = 0
                maskTreshold[i][j][1] = 0
                maskTreshold[i][j][2] = 255

                # add alpha on origin rgb image
                # img[i][j][2] = (mask_alpha * maskTreshold[i][j][2]) + ((1 - mask_alpha) * img[i][j][2])
    
    img = cv2.addWeighted(maskTreshold, mask_alpha, img, 1 - mask_alpha, 0)

    cv2.imshow('mask', maskTreshold)
    cv2.imshow('img', img)
    cv2.imshow('origin', img_copy)


    start = time.time()

    while (1):
        
        Q = 113
        A = 97
        R = 114
        T = 116
        X = 120

        esc = 27
        spacebar = 32
        tab = 9

        inputKey = cv2.waitKey(0)

        if inputKey == spacebar: # save
            remove = False

            cv2.imwrite(path_dir + "colormask " + filename, maskTreshold)

            os.remove(path_dir + filename)
            os.remove(path_dir + "mask " + filename)

            end = time.time()
            timer = end - start
            time_all += timer
            print('경과시간 : ', int(timer), 's, 총 소요시간 : ', int(time_all), 's')
            

            break

        if inputKey == esc:
            exit()

        if inputKey == tab: # pass
            remove = False

            end = time.time()
            timer = end - start
            time_all += timer
            print('경과시간 : ', int(timer), 's, 총 소요시간 : ', int(time_all), 's')
            break


        if inputKey == R:   # remove
            if remove == True:
                remove = False
                print('Remove OFF')

            else:
                remove = True
                print('Remove ON')

        if inputKey == T:   # 정해진 영역 제외 제거
            if all_remove == False:
                all_remove = True


        if inputKey == Q:
            circle_size += 5

            img_temp = img.copy()
            img_temp = cv2.circle(img_temp,(mouse_x,mouse_y),circle_size, circle_color, -1)
            cv2.imshow('img', img_temp)
    
        if inputKey == A:
            if circle_size > 8:
                circle_size -= 3

            elif circle_size <= 8 and circle_size > 1:
                circle_size -= 1
            
            elif circle_size <= 1:
                circle_size = 1
            
            img_temp = img.copy()
            img_temp = cv2.circle(img_temp,(mouse_x,mouse_y),circle_size, circle_color, -1)
            cv2.imshow('img', img_temp)

        if inputKey == X:
            img_temp = img_copy.copy()

            kernel = np.ones((5, 5), np.uint8)
            maskTreshold = cv2.morphologyEx(maskTreshold, cv2.MORPH_OPEN, kernel)

            img = cv2.addWeighted(maskTreshold, mask_alpha, img_temp, 1 - mask_alpha, 0)

            cv2.imshow('mask', maskTreshold)
            cv2.imshow('img', img)




            

