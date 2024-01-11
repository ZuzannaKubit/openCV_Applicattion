import cv2 as cv

class HsvTrackbar:
    def on_low_H_thresh_trackbar(self,val):
        self.low_H = val
        self.low_H = min(self.high_H-1, self.low_H)
        cv.setTrackbarPos(self.low_H_name, self.windowName, self.low_H)

    def on_high_H_thresh_trackbar(self,val):
        self.high_H = val
        self.high_H = max(self.high_H, self.low_H+1)
        cv.setTrackbarPos(self.high_H_name, self.windowName, self.high_H)

    def on_low_S_thresh_trackbar(self,val):
        self.low_S = val
        self.low_S = min(self.high_S-1, self.low_S)
        cv.setTrackbarPos(self.low_S_name, self.windowName, self.low_S)

    def on_high_S_thresh_trackbar(self,val):
        self.high_S = val
        self.high_S = max(self.high_S, self.low_S+1)
        cv.setTrackbarPos(self.high_S_name, self.windowName, self.high_S)

    def on_low_V_thresh_trackbar(self,val):
        self.low_V = val
        self.low_V = min(self.high_V-1, self.low_V)
        cv.setTrackbarPos(self.low_V_name, self.windowName, self.low_V)

    def on_high_V_thresh_trackbar(self,val):
        self.high_V = val
        self.high_V = max(self.high_V, self.low_V+1)
        cv.setTrackbarPos(self.high_V_name, self.windowName, self.high_V)

    def __init__(self, windowName, dhl = 0, dhh = 180, dsl = 0, dsh = 255, dvl = 0, dvh = 255):
        self.windowName = windowName
        self.max_value = 255
        self.max_value_H = 360//2
        self.low_H = 0
        self.low_S = 0
        self.low_V = 0
        self.high_H = self.max_value_H
        self.high_S = self.max_value
        self.high_V = self.max_value
        self.low_H_name = 'Low H'
        self.low_S_name = 'Low S'
        self.low_V_name = 'Low V'
        self.high_H_name = 'High H'
        self.high_S_name = 'High S'
        self.high_V_name = 'High V'


        cv.namedWindow(self.windowName, cv.WINDOW_NORMAL)
        cv.createTrackbar(self.low_H_name, self.windowName , self.low_H, self.max_value_H, self.on_low_H_thresh_trackbar)
        cv.createTrackbar(self.high_H_name, self.windowName , self.high_H, self.max_value_H, self.on_high_H_thresh_trackbar)
        cv.createTrackbar(self.low_S_name, self.windowName , self.low_S, self.max_value, self.on_low_S_thresh_trackbar)
        cv.createTrackbar(self.high_S_name, self.windowName , self.high_S, self.max_value, self.on_high_S_thresh_trackbar)
        cv.createTrackbar(self.low_V_name, self.windowName , self.low_V, self.max_value, self.on_low_V_thresh_trackbar)
        cv.createTrackbar(self.high_V_name, self.windowName , self.high_V, self.max_value, self.on_high_V_thresh_trackbar)
        
        cv.setTrackbarPos(self.low_H_name, self.windowName , dhl)
        cv.setTrackbarPos(self.high_H_name, self.windowName , dhh)
        cv.setTrackbarPos(self.low_S_name, self.windowName , dsl)
        cv.setTrackbarPos(self.high_S_name, self.windowName , dsh)
        cv.setTrackbarPos(self.low_V_name, self.windowName , dvl)
        cv.setTrackbarPos(self.high_V_name, self.windowName , dvh)
         
        