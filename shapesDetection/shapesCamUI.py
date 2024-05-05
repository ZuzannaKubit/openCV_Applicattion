import cv2 as cv
import numpy as np
import time
import tkinter as tk
import socket
from blockData import*
from  hsvTrackbar import HsvTrackbar 
from imageTransform import ImageTransform
from screenToWorld import ScreenToWorld

stream_url = f"http://192.168.0.101:81/stream"

# Utwórz obiekt VideoCapture do odbierania strumienia
cap = cv.VideoCapture(stream_url)

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

send_pos = False

screenToWorld = ScreenToWorld(190, 280, 200, 300)
def send_data(sock, message):
    try:
        sock.sendall(message.encode("UTF-8"))  # Wysyłanie danych
    except BlockingIOError:
        # Brak dostępnych miejsca w buforze
        pass

def contur(img, contours, sock):
    global send_pos
    for contur in contours:
        approx = cv.approxPolyDP(contur, cv.getTrackbarPos(aprox_contur, window_detection_name)* cv.arcLength(contur, True) / 1000.0, True)
        
        area = cv.contourArea(contur)
        #todo: dodać suwaczki <3
        xl, yl = screenToWorld.transformToScreen(5,5)
        xu, yu = screenToWorld.transformToScreen(100,100)

        al = xl * yl
        au = xu * yu 

        if(area < al or area > au):
            continue 
        cv.drawContours(img, [approx], 0, (0,100,0), 3)
        x, y, w, h = cv.boundingRect(approx)

        
        centerX = int(x + w / 2)
        centerY = int(y + h / 2)

        worldX, worldY = screenToWorld.transformToWorld(centerX,centerY)
        
        coord = "x: " + str(round(worldX, 1)) + " y:  " + str(round(worldY,1))
        cv.putText(img,coord, (x,y - int(h/2) ), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))


        if len(approx) == 3:
            cv.putText(img, "Triangle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
            shape = int(BlockType.Triangle)
        elif len(approx) == 4:
            
            # print(aspectRatio)
            x = int(x + w / 2)
            y = int(y + h / 2)
            
            shape = int(BlockType.Square)
            cv.putText(img, "Square", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
        else:
            cv.putText(img, "Circle", (x, y), cv.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0))
            
            shape = int(BlockType.Circle)

        if send_pos == True:
            pos = Vector3(float(worldX),0,float(worldY))
            data = BlockData(pos, shape, int(BlockColor.Red))
            message = json.dumps(data, cls=BlockDataEncoder)
            send_data(sock, message)
            send_pos = False 


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
ImgTransform = ImageTransform("image transform",241,122,639,129,241,397,633,404,800,600,300,200)

def create_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    return sock

def connect_to_server(sock, host, port):
    try:
        sock.connect((host, port))
        print("connected")
    except BlockingIOError:
        pass

def receive_data(sock):
    global send_pos
    try:
        data = sock.recv(1024)
        if data:
            print(f"odebrano: {data.decode()}")
            msg = data.decode()
            #trim 
            msg = msg.strip()
            #jeśli data to "send_pos()"
            if msg == "sendBlock":
                send_pos = True
            #wtedy ustaw bool że trzeba wysłać 
    except BlockingIOError:
        pass            

#values for socket:
host = "127.0.0.1"
    
port = 25001
client_socket = create_socket()
print("connecting")
connect_to_server(client_socket, host, port)

while True:

    receive_data(client_socket)

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
    # img = img[wm:wM,hm:hM]
    img = ImgTransform.transform(img)
    imgHSV = cv.cvtColor(img, cv.COLOR_RGB2HSV)
    # imgHSV = erDil(imgHSV)
    # cv.imshow('imgHSV',imgHSV)

    frame_threshold = cv.inRange(imgHSV, (redTrackBar.low_H, redTrackBar.low_S, redTrackBar.low_V), (redTrackBar.high_H, redTrackBar.high_S, redTrackBar.high_V))

    cv.imshow('frame_threshold',frame_threshold)

    k = cv.getTrackbarPos(kernelSize,window_detection_name)
    k = 2 * k + 1
    thrash = cv.GaussianBlur(frame_threshold,(k,k),0)
   
    # cv.imshow("withGausse", thrash)
    _, thrash = cv.threshold(thrash, cv.getTrackbarPos(t_tresh,window_detection_name),255, cv.CHAIN_APPROX_NONE)
    # cv.imshow('trash', thrash)
    contours , _ = cv.findContours(thrash, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    contur(img, contours, client_socket) 

    cv.imshow('shapes_detection', img)
    
    # Przerwij pętlę po naciśnięciu klawisza 'q'
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Zwolnij zasoby
cap.release()
cv.destroyAllWindows()

