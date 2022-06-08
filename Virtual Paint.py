import cv2
import numpy as np
from cv2 import cv2 

cap= cv2.VideoCapture(0)
cap.set(10, 150)

myColors= [[24,142,81,42,255,255],    #lemon
           [134,131,84,163,228,255],  #purple
            [46,74,83,88,255,138],   #green
            [0,96,178,20,255,219]]   #orange
           #[133,150,31,179,243,255]  #red

myColorValues = [[102,255,255],          ## BGR
                [204,0,102],
               [0,255,0],
                [0,128,255]]

myPoints =  []  ## [x , y , colorId ]


def findcolour(img, myColors,myColorValues):
    imghsv= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count= 0
    newPoints= []
    for color in myColors:
      lower= np.array(color[0:3])
      upper= np.array(color[3:6])
      mask= cv2.inRange(imghsv, lower, upper)
      x,y= getContours(mask)
      cv2.circle(imgresult, (int(x),int(y)), 20, myColorValues[count], cv2.FILLED)
      if x!=0 and y!=0:
          newPoints.append([x,y,count])
      count +=1
      #cv2.imshow(str(color[0]), mask)
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgresult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w/2,y

def draw(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgresult, (int(point[0]),int(point[1])), 20, myColorValues[point[2]], cv2.FILLED)


while True:
    success, img= cap.read()
    imgresult= img.copy()
    newPoints= findcolour(img, myColors, myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        draw(myPoints, myColorValues)

    cv2.imshow('result', imgresult)

    if cv2.waitKey(1) & 0xFF== ord('b'):
        break
