import cv2                                                                       #importing computer vision library

nPlateCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')
# faceCascade=cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")
img = cv2.imread("C:/Users/PC/PycharmProjects/OpenCVPython/Resources/B_99.jpg", 1)
minArea=500
color=(255,0,255)
cap=cv2.VideoCapture(0)                                                            #To capture video from webcam
cap.set(3,640)
cap.set(4,480)
cap.set(10,150)
count=0



while True:
    success,img=cap.read()                              #Reading an image
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)     #Converting image to Grayscale
    # faces = faceCascade.detectMultiScale(imgGray,2,1)
    numberPlates = nPlateCascade.detectMultiScale(imgGray, 1.1, 4)  #Fucntion which detects faces will detect number plates

    for (x, y, w, h) in numberPlates:           #To draw a rectangle around it
        area=w*h                                #Finding area to add filter
        if area>minArea:                        #Condition for detecting rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2) #Draw Rectangle around detected object
            cv2.putText(img,"Number Plate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2) #Label the object
            imgRoi=img[y:y+h,x:x+w]             #Cropping out the region of interest
            cv2.imshow("ROI",imgRoi)            #Display image only when number plate is detected
    cv2.imshow("Result",img)
    if cv2.waitKey(1) & 0xFF==ord('s'):
        cv2.imwrite("Resources/Scanned/NoPlate_"+str(count)+".jpg",imgRoi)  #To save image
        cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)  #Create rectangle around image
        cv2.putText(img,"Scan Saved",(150,265),cv2.FONT_HERSHEY_DUPLEX,2,(0,0,255),2) #Display with text on it
        cv2.imshow("Result",img)
        cv2.waitKey(500)
        count+=1
