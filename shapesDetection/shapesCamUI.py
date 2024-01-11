import cv2 as cv
import numpy as np
import time
import tkinter as tk
from  hsvTrackbar import HsvTrackbar 

stream_url = f"http://192.168.0.100:81/stream"

# Utwórz obiekt VideoCapture do odbierania strumienia
# cap = cv.VideoCapture(stream_url)

window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
crop_minH = "crop min h"
crop_maxH = "crop max h"
crop_minW = "crop min W"
crop_maxW = "crop max W"
aprox_contur = "aprox contur"
t_tresh = "tresh"
dilateIter = "DilateIter"
erodeIter = "ErodeIter"
kernelSize = "KernelSize"



def contur(img, contours):
    for contur in contours:
        approx = cv.approxPolyDP(contur, cv.getTrackbarPos(aprox_contur, window_detection_name)* cv.arcLength(contur, True) / 1000.0, True)
        cv.drawContours(img, [approx], 0, (0,100,0), 3)
        x = approx.ravel()[0]
        y = approx.ravel()[1]
        if len(approx) == 3:
            cv.putText(img, "Triangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
        elif len(approx) == 4:
            x, y, w, h = cv.boundingRect(approx)
            aspectRatio = float(w)/h
            # print(aspectRatio)
            x = int(x + w / 2)
            y = int(y + h / 2)
            if aspectRatio >= 0.95 and aspectRatio < 1.05:
                cv.putText(img, "Square", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
            else:
                cv.putText(img, "rectangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
        else:
            cv.putText(img, "Circle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))

def nothing(x):
    pass

cv.namedWindow(window_detection_name, cv.WINDOW_NORMAL)
cv.createTrackbar(crop_minH,window_detection_name,0 , 600, nothing)
cv.createTrackbar(crop_maxH,window_detection_name,0 , 600, nothing)

cv.createTrackbar(crop_minW,window_detection_name,0 , 800, nothing)
cv.createTrackbar(crop_maxW,window_detection_name,0 , 800, nothing)
cv.createTrackbar(aprox_contur, window_detection_name, 1, 100, nothing)
cv.createTrackbar(t_tresh, window_detection_name, 1, 255, nothing)

cv.createTrackbar(dilateIter, window_detection_name, 1, 5, nothing)
cv.createTrackbar(erodeIter, window_detection_name, 1, 5, nothing)
cv.createTrackbar(kernelSize, window_detection_name, 1, 30, nothing)

cv.setTrackbarPos(aprox_contur, window_detection_name, 10)
cv.setTrackbarPos(crop_minH, window_detection_name, 130)
cv.setTrackbarPos(crop_maxH, window_detection_name, 430)
cv.setTrackbarPos(crop_minW, window_detection_name, 212)
cv.setTrackbarPos(crop_maxW, window_detection_name, 615)
cv.setTrackbarPos(t_tresh, window_detection_name , 100)

cv.setTrackbarPos(dilateIter, window_detection_name , 1)
cv.setTrackbarPos(erodeIter, window_detection_name , 1)
cv.setTrackbarPos(kernelSize, window_detection_name , 1)

def erDil(srcImg):
    kSize = cv.getTrackbarPos(kernelSize,window_detection_name)
    kernel = np.ones((kSize,kSize),np.uint8)
    erodedImg = cv.erode(srcImg, kernel, iterations= cv.getTrackbarPos(erodeIter,window_detection_name))
    dilatedImg = cv.dilate(erodedImg,kernel,iterations= cv.getTrackbarPos(dilateIter,window_detection_name))
    return dilatedImg
redTrackBar = HsvTrackbar("red trackbar", 114, 143, 104, 206, 28, 108)

while True:
    # Odczytaj klatkę z strumienia
    # ret, frame = cap.read()

    # if not ret:
    #     print("Błąd podczas odczytu klatki")
    #     break

    # Wyświetl klatkę
    # cv.imshow("Kamera ESP", frame)
    # img = frame 
    img =  cv.imread('jpgOdPawela.jpg')
    # imgR = img[1]
    # cv.imshow("r",imgR)
    # imgHSV = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    wm = cv.getTrackbarPos(crop_minH,window_detection_name)
    wM = cv.getTrackbarPos(crop_maxH,window_detection_name)
    hm = cv.getTrackbarPos(crop_minW,window_detection_name)
    hM = cv.getTrackbarPos(crop_maxW,window_detection_name)
    img = img[wm:wM,hm:hM]
    imgHSV = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    # imgHSV = erDil(imgHSV)
    cv.imshow('imgHSV',imgHSV)

    frame_threshold = cv.inRange(imgHSV, (redTrackBar.low_H, redTrackBar.low_S, redTrackBar.low_V), (redTrackBar.high_H, redTrackBar.high_S, redTrackBar.high_V))

    cv.imshow('frame_threshold',frame_threshold)

    k = cv.getTrackbarPos(kernelSize,window_detection_name)
    k = 2 * k + 1
    thrash = cv.GaussianBlur(frame_threshold,(k,k),0)
   
    cv.imshow("withGausse", thrash)
    _, thrash = cv.threshold(thrash, cv.getTrackbarPos(t_tresh,window_detection_name),255, cv.CHAIN_APPROX_NONE)
    cv.imshow('trash', thrash)
    contours , _ = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    contur(img, contours) 

    cv.imshow('shapes_detection', img)
    
    # Przerwij pętlę po naciśnięciu klawisza 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnij zasoby
# cap.release()
cv.destroyAllWindows()

