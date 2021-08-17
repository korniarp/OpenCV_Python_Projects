import cv2
import numpy as np
cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)
cap.set(10,100)
# while True:
#     success,img=cap.read()
#     cv2.imshow("Video",img)
#     if cv2.waitKey(1) & 0xFF==ord('q'):
#             break
def empty(a):
    pass

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",640,240)
cv2.createTrackbar("Hue Min","Trackbars",0,255,empty)
cv2.createTrackbar("Hue Max","Trackbars",255,255,empty)
cv2.createTrackbar("Sat Min","Trackbars",0,255,empty)
cv2.createTrackbar("Sat Max","Trackbars",255,255,empty)
cv2.createTrackbar("Val Min","Trackbars",0,255,empty)
cv2.createTrackbar("Val Max","Trackbars",255,255,empty)

while True:
    success,img=cap.read()
    cv2.imshow("Video",img)

    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat Min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat Max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val Min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val Max", "Trackbars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower=np.array([h_min,s_min,v_min])
    upper = np.array([h_max, s_max, v_max])
    # img=cv2.imread(path)
    #cv2.imshow("Original",img)
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #cv2.imshow("HSV",imgHSV)
    mask = cv2.inRange(imgHSV,lower,upper)
    #cv2.imshow("Mask",mask)
    imgResult=cv2.bitwise_and(img,img,mask=mask)
    cv2.imshow("Result",mask)

    # cv2.imshow("Stacked Images",imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break