import cv2 as cv
import numpy as np

class ImageTransform:
    def nothing(x):
        pass
    def __init__(self, windowName, x1, y1, x2, y2, x3, y3, x4, y4, sourceW, sourceH, targetW, targetH):
        self.windowName = windowName 
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        self.targetW = targetW
        self.targetH = targetH
        cv.namedWindow(self.windowName, cv.WINDOW_AUTOSIZE)
        cv.createTrackbar("x1", self.windowName , 0, sourceW, self.nothing)
        cv.createTrackbar("y1", self.windowName , 0, sourceH, self.nothing)
        cv.createTrackbar("x2", self.windowName , 0, sourceW, self.nothing)
        cv.createTrackbar("y2", self.windowName , 0, sourceH, self.nothing)
        cv.createTrackbar("x3", self.windowName , 0, sourceW, self.nothing)
        cv.createTrackbar("y3", self.windowName , 0, sourceH, self.nothing)
        cv.createTrackbar("x4", self.windowName , 0, sourceW, self.nothing)
        cv.createTrackbar("y4", self.windowName , 0, sourceH, self.nothing)

        cv.setTrackbarPos("x1", self.windowName, x1)
        cv.setTrackbarPos("x2", self.windowName, x2)
        cv.setTrackbarPos("x3", self.windowName, x3)
        cv.setTrackbarPos("x4", self.windowName, x4)
        cv.setTrackbarPos("y1", self.windowName, y1)
        cv.setTrackbarPos("y2", self.windowName, y2)
        cv.setTrackbarPos("y3", self.windowName, y3)
        cv.setTrackbarPos("y4", self.windowName, y4)

    def transform(self, img):

        self.x1 = cv.getTrackbarPos("x1",self.windowName)
        self.x2 = cv.getTrackbarPos("x2",self.windowName)
        self.x3 = cv.getTrackbarPos("x3",self.windowName)
        self.x4 = cv.getTrackbarPos("x4",self.windowName)
        self.y1 = cv.getTrackbarPos("y1",self.windowName)
        self.y2 = cv.getTrackbarPos("y2",self.windowName)
        self.y3 = cv.getTrackbarPos("y3",self.windowName)
        self.y4 = cv.getTrackbarPos("y4",self.windowName)

        pts1 = np.float32([[self.x1,self.y1],[self.x2,self.y2],[self.x3,self.y3],[self.x4,self.y4]]) #lu ru ld rd
        pts2 = np.float32([[0,0],[self.targetW,0],[0,self.targetH],[self.targetW,self.targetH]])
        M = cv.getPerspectiveTransform(pts1,pts2)
        return cv.warpPerspective(img,M,(self.targetW,self.targetH))

