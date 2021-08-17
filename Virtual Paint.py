import cv2                                          #importing computer vision library
import numpy as np                                  #importing numpy
cap=cv2.VideoCapture(0)                             #To capture video from webcam
cap.set(3,640)                                      #To set width of capture screen
cap.set(4,480)                                      #To set height of capture screen
cap.set(10,150)                                     #To set brightness of video captured

myColors=[[5,107,0,19,255,255],                     #Array defining hue(min & max),saturation(min & max) and value of color(min & max)
          [133,56,0,159,156,255],
          [57,76,0,100,255,255],
          [2,64,0,77,255,0],
          [0,88,132,255,0,255],
          [0,74,0,138,194,255],
          [90,48,0,118,255,255],
          [95 ,108 ,102, 150, 229, 255],
          [24,97,90,255,75,255],
          [98,137,114,232,121,255],
          [124,229,110,253,109,255]]

myColorValues=[[51,153,255],                       #Array defining BGR color code
               [255,0,255],
               [0,255,0],[255,255,0],
               [200,255,0],
               [255,255,0],
               [255,0,0],
               [204,204,0],
               [76,155,0],
               [255,0,0],
               [0,0,153]]

myPoints=[]                                          #Defining a list


def findColor(img,myColors,myColorValues):         #Function to creation of trail of virtual paint on screen
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)     #Conversion to HSV image provides a numerical readout of the image
    count=0                                        #variable to keep track of points
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)        #Masking of image
        x,y=getContours(mask)                           #Calling function which calculates position of the circular point
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)      #Creation of circular point once colour is detected
        if x!=0 and y!=0:
            newPoints.append([x,y,count])                                   #Creation of array with new points to follow trail
        count+=1                                                            #Increment of count as points increase
        # cv2.imshow(str(color[0]),mask)
    return newPoints                                                        #returns value of New points

def getContours(img):                                                       #Passing image to the function
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area=cv2.contourArea(cnt)                                           #Calculation of area
        if area>500:                                                        #Condition for display of circular point
            #cv2.drawContours(imgResult, cnt, -1, (0, 255, 255), 6)
            peri=cv2.arcLength(cnt,True)                                    #Calculation of perimeter
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)                                #Bounding perimeter to draw circular point
    return x+w//2,y                                                         #Returning position of first circular point

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)    #For drawing the next point and follow trails


while True:
    success,img=cap.read()                                                  #Reading the image for displaying
    imgResult=img.copy()                                                    #Copying the image
    newPoints = findColor(img, myColors,myColorValues)                      #Calling function to identify colour
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints)!= 0:
        drawOnCanvas(myPoints,myColorValues)                                #calling function which draws on screen virtually
    cv2.imshow("Video",imgResult)                                           #Display of pain on screen
    if cv2.waitKey(1) & 0xFF==ord('q'):                                     #To stop painting press 'q'
            break