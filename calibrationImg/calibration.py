import numpy as np
import cv2 as cv
import glob

width = 8
hight = 4

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
#object points
obj = np.zeros((width*hight,3), np.float32)
obj[:, :2] = np.mgrid[0:width, 0:hight].T.reshape(-1,2)

objPoints = []
imgPoints = []

images = glob.glob('*jpg')

for fname in images:
    print(fname)
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    cv.imshow('image', gray)
    cv.waitKey(500)

    #find the chess board corners:
    result, corners = cv.findChessboardCorners(img, (width,hight), None) #cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE
        #+ cv.CALIB_CB_FAST_CHECK
    print(result)
    

    if result == True:
        objPoints.append(obj)

        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgPoints.append(corners2)

        #draw and display corners:
        cv.drawChessboardCorners(img, (width,hight), corners2, result)
        cv.imshow('img', img)
        cv.waitKey(500)
        
        # while True:
        #     if cv.waitKey(1) & 0xFF == ord('q'):
        #         break

cv.destroyAllWindows()

#calibration
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)

img = cv.imread(images[0])
h, w = img.shape[:2]
newCameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
dst = cv.undistort(img, mtx, dist, None, newCameramtx)

cv.imshow('undist',dst)
cv.imshow('dist',img)

while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cv.destroyAllWindows()