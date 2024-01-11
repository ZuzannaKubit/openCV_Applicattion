import cv2 as cv
import numpy as np
import time
import tkinter as tk

stream_url = f"http://192.168.0.100:81/stream"

# Utwórz obiekt VideoCapture do odbierania strumienia
cap = cv.VideoCapture(stream_url)

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value
window_capture_name = 'Video Capture'
window_detection_name = 'Object Detection'
low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'
crop_minH = "crop min h"
crop_maxH = "crop max h"
crop_minW = "crop min W"
crop_maxW = "crop max W"
aprox_contur = "aprox contur"
t_tresh = "tresh"
dilateIter = "DilateIter"
erodeIter = "ErodeIter"
kernelSize = "KernelSize"
def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)


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
cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)
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
cv.setTrackbarPos(low_H_name, window_detection_name , 114)
cv.setTrackbarPos(high_H_name, window_detection_name , 143)
cv.setTrackbarPos(low_S_name, window_detection_name , 104)
cv.setTrackbarPos(high_S_name, window_detection_name , 206)
cv.setTrackbarPos(low_V_name, window_detection_name , 28)
cv.setTrackbarPos(high_V_name, window_detection_name , 108)
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

while True:
    # Odczytaj klatkę z strumienia
    ret, frame = cap.read()

    if not ret:
        print("Błąd podczas odczytu klatki")
        break

    # Wyświetl klatkę
    # cv.imshow("Kamera ESP", frame)
    img = frame 
    # img =  cv.imread('jpgOdPawela.jpg')
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

    frame_threshold = cv.inRange(imgHSV, (low_H, low_S, low_V), (high_H, high_S, high_V))

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
cap.release()
cv.destroyAllWindows()

