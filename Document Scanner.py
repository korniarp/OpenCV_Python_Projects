import cv2                                                          #importing computer vision library
import numpy as np                                                  #importing numpy

widthImg=360                                                         #Setting width of screen
heightImg=640                                                        #Setting height of screen
cap = cv2.VideoCapture(1)                                              #To capture video from webcam
cap.set(3,widthImg)                                                 #To set width of capture screen
cap.set(4,heightImg)                                                #To set height of capture screen
cap.set(10,150)

def preProcessing(img):                                             #For preporocessing of image before finding contours
    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                    #To convert to grayscale image
    imgBlur=cv2.GaussianBlur(imgGray,(5,5),1)                       #To blur the image as edge detection is susceptible to noise
    imgCanny=cv2.Canny(imgBlur,200,200)                             #To detect the edges in the image
    kernel=np.ones((5,5))                                           #Defining kernel
    imgDial=cv2.dilate(imgCanny,kernel,iterations=2)                #For expanding image pixels
    imgThres=cv2.erode(imgDial,kernel,iterations=1)                 #TO erode away boundaries
    return imgThres                                                 #Returns the pre-processed image


def getContours(img):

    biggest=np.array([])                    #Declaring an array
    maxArea = 0                             #Assigning zero value to variable
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area=cv2.contourArea(cnt)           #Calculating area
        if area>5000:                       #Condition to calculate perimeter when area is huge
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri=cv2.arcLength(cnt,True)     #Calculation of perimeter
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            if area>maxArea and len(approx)==4:     #Checking for criteria and if contour has 4 sides
                biggest=approx                      #Storing biggest contour
                maxArea=area
    cv2.drawContours(imgContour,biggest, -1, (255, 0, 0), 20) #To draw contours around the detected shape
    return biggest                                  #Returning biggest contour


def reorder(myPoints):                          #Function to reorder corner points so that they are in order for warping
    myPoints = myPoints.reshape((4,2))          #Reshape the matrix
    myPointsNew = np.zeros((4, 1, 2),np.int32)
    add = myPoints.sum(1)                       #Summation of all the points
    # print("add",add)
    myPointsNew[0] = myPoints[np.argmin(add)]   #Calculating corners
    myPointsNew[3] = myPoints[np.argmax(add)]   #Calculating corners
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew                          #Returning reordered points



def getWarp(img,biggest):                               #Sending image and the biggest contour as parameters to this function
    print(biggest)
    # biggest=reorder(biggest)                            #Sending biggest contour to "reorder" function
    pts1 = np.float32(biggest)                          #Defining points for warping the image
    pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])
    # matrix = cv2.getPerspectiveTransform(pts1,pts2)      #Points which need to be warped
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgOutput = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) #Getting resultant image
    return imgOutput


while True:
    success, img = cap.read()                              #Reading the image for displaying
    cv2.resize(img,(widthImg,heightImg))              #Resizing the image
    imgContour = img.copy()                              #Making a copy of the original image
    imgThres=preProcessing(img)                         #Calling function
    biggest=getContours(imgThres)                       #Calling fucntion to find the biggest contour
    # print(biggest)
    imgWarped=getWarp(img,biggest)                      #Calling function to warp image
    cv2.imshow("Result",imgWarped)                       #Display the wrapped version
    if cv2.waitKey(1) & 0xFF==ord('q'):
            break