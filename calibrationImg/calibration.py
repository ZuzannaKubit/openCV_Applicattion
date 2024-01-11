import numpy as np
import cv2 as cv
import glob
import pickle

width = 18
hight = 13

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
        img = cv.drawChessboardCorners(img, (width,hight), corners2, result)
        cv.imshow('ch', img)
        
        # while True:
        #     if cv.waitKey(1) & 0xFF == ord('q'):
        #         break

# cv.destroyAllWindows() 

#calibration
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)

#save the camera calibration 
pickle.dump((mtx, dist), open("calibration.pkl", "wb"))
# pickle.dump(mtx, open("cameraMatrix.pkl", "wb"))
# pickle.dump(dist, open("dist.pkl", "wb"))

with open("calibration.pkl","rb") as f:
    data = pickle.load(f)

(mtx2, dist2) = data

img = cv.imread(images[0])
h, w = img.shape[:2]
newCameramtx, roi = cv.getOptimalNewCameraMatrix(mtx2, dist2, (w, h), 1, (w, h))
print(mtx2) 
print(newCameramtx)
print(dist2)
dst = cv.undistort(img, mtx2, dist2, None, newCameramtx)
#crop the image:
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
#cv.imwrite('calibresult.png', dust)

cv.imshow('undist',dst)
cv.imshow('dist',img)

mean_error = 0
for i in range(len(objPoints)):
    imgPoints2, _ = cv.projectPoints(objPoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgPoints[i], imgPoints2, cv.NORM_L2)/len(imgPoints2)
    mean_error += error
print("total error: {}".format(mean_error/len(objPoints)))    


while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cv.destroyAllWindows()