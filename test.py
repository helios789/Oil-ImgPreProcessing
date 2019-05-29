import cv2
import numpy as np
import os

output_img_X = 0
output_img_Y = 0

def mouse_callback(event, x, y ,flags, param):

    # mouse Left button clicked
    if event == cv2.EVENT_FLAG_MBUTTON and flags == cv2.EVENT_LBUTTONDOWN:
        global output_img_X, output_img_Y
        output_img_X = int(x / input_img_size['x'])
        output_img_Y = int(y / input_img_size['y'])
        print(int(output_img_Y)+1,"번째 줄, ", int(output_img_X)+1, " 번째 이미지 선택")

cv2.namedWindow('mask')
cv2.setMouseCallback('mask', mouse_callback)


input_img_size = {
    'x' : 256,
    'y' : 256,
}

filter_list_row = 2
filter_list_col = 6

hsv_darkoil_filter_list = [
    #[(lower_bound_h, s, v), (upper_bound_h, s, v)]
    #[(lower_bound_h, s, v), (upper_bound_h, s, v)]
    [(0, 0, 0), (179, 200, 200)],    
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
output_path_dir = os.getcwd() +"/mask/"
file_list = os.listdir(path_dir)
file_list.sort()
print(file_list)

print("총 " + str(len(file_list)) + " 개의 이미지 로드")


for idx, file in enumerate(file_list):
    img_rgb = cv2.imread(path_dir + file)
    img_resize = cv2.resize(img_rgb, (input_img_size['x'], input_img_size['y']), interpolation=cv2.INTER_AREA)

    img_hsv = cv2.cvtColor(img_resize, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(img_hsv)
    hsv = np.concatenate((h, s, v), axis=1)

    mask_list = []

    for filter in hsv_darkoil_filter_list:
        hsv_lower_bound = filter[0]
        hsv_upper_bound = filter[1]

        mask = cv2.inRange(img_hsv, hsv_lower_bound, hsv_upper_bound)

        mask_list.append(mask)

    
    temp = []

    for i in range(filter_list_row):
        temp.append(np.concatenate(mask_list [filter_list_col*i : filter_list_col*(i+1)], axis=1))
    result = np.concatenate(temp, axis=0)

    # cv2.imshow('hsv', hsv)
    cv2.imshow('mask', result)
    cv2.imshow('origin', img_resize)

    # cv2.imwrite('./mask.jpg', mask);
    while(1):
        spacebar = 32
        inputKey = cv2.waitKey(0)

        if(inputKey == spacebar):
            print(file + ' 저장.. ' + str(idx + 1) + " / " + str(len(file_list))  + " 완료\n")

            img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2HSV)

            hsv_lower_bound = hsv_darkoil_filter_list[int(output_img_Y)*filter_list_col + int(output_img_X)][0]
            hsv_upper_bound = hsv_darkoil_filter_list[int(output_img_Y)*filter_list_col + int(output_img_X)][1]

            mask = cv2.inRange(img_hsv, hsv_lower_bound, hsv_upper_bound)
 
            cv2.imwrite(output_path_dir + "mask " + file, mask)
            cv2.imwrite(output_path_dir + file, img_rgb)

            os.remove(path_dir + file)
        
            break


cv2.destroyAllWindows()