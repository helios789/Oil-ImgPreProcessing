import cv2
import time

cap = cv2.VideoCapture(1)
now = time.localtime()
current_time = "%04d-%02d-%02d %02d-%02d-%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
cap.set(3, 1080) 
cap.set(4, 720)

# fps = 24.0
# codec = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
# out = cv2.VideoWriter(current_time + '.avi', codec, fps, (int(cap.get(3)), int(cap.get(4))))

while True:
    ret, frame = cap.read()

    if ret == True:
        # print(cap.get(3), cap.get(4))
        #out.write(frame)
        cv2.imshow('frame', frame)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()


