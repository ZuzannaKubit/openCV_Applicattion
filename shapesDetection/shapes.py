import cv2 as cv
import numpy as np

img = cv.imread('testShapes2.jpg')
imgR = img[1]
cv.imshow("r",imgR)
imgGry = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
cv.imshow('gray',imgGry)

_, thrash = cv.threshold(imgGry, 159,255, cv.CHAIN_APPROX_NONE)
cv.imshow('trash', thrash)
contours , _ = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

for contur in contours:
    approx = cv.approxPolyDP(contur, 0.01* cv.arcLength(contur, True), True)
    cv.drawContours(img, [approx], 0, (0,0,0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if len(approx) == 3:
        cv.putText(img, "Triangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
    elif len(approx) == 4:
        x, y, w, h = cv.boundingRect(approx)
        aspectRatio = float(w)/h
        print(aspectRatio)
        x = int(x + w / 2)
        y = int(y + h / 2)
        if aspectRatio >= 0.95 and aspectRatio < 1.05:
            cv.putText(img, "Square", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
        else:
            cv.putText(img, "rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
    elif len(approx) == 5:
        cv.putText(img, "Pentagon", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
    elif len(approx) == 10:
        cv.putText(img, "Star", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
    else:
        cv.putText(img, "Circle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0)) 

cv.imshow('shapes_detection', img)
cv.waitKey(0)
cv.destroyAllWindows()

