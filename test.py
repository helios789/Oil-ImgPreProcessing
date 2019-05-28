import cv2
import numpy as np

img_rgb = cv2.imread("./img/2019-05-16 10:47:52:cam2.jpg");
img_resize = cv2.resize(img_rgb, (512, 512), interpolation=cv2.INTER_AREA)

img_hsv = cv2.cvtColor(img_resize, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(img_hsv)
hsv = np.concatenate((h, s, v), axis=1)


# TODO: 여러개의 lower, upper 필터를 설정하여 
# 여러개의 output 을 출력 후 한개를 마우스로 클릭하여 저장하는 기능 추가

lower_darkoil = (95, 50, 0)
upper_darkoil = (179, 255, 200)

# lower_darkoil = (0, 0, 0)
# upper_darkoil = (255, 255, 80)

mask = cv2.inRange(img_hsv, lower_darkoil, upper_darkoil)
overlap = cv2.bitwise_and(img_resize, img_resize, mask = mask)
result = np.concatenate((img_resize, img_hsv, overlap), axis=1)


cv2.imshow('hsv', hsv)
cv2.imshow('result', result)
cv2.imshow('mask', mask)

# cv2.imwrite('./mask.jpg', mask);


cv2.waitKey(0)
cv2.destroyAllWindows()