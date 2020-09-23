# coding=utf-8

import cv2
import numpy as np
ssize = 800
img = cv2.imread("C:\\Users\\hanlu\\Pictures\\test\\2.jpg")
img2=cv2.resize(img,(ssize,ssize))

gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV)
lowerblue = np.array([0,43,46],dtype = np.uint8)
upperblue = np.array([10,255,255],dtype=np.uint8)
maskblue = cv2.inRange(hsv, lowerblue, upperblue)
maskblue_inv = cv2.bitwise_not(maskblue)

# 腐蚀操作
kernel_erode = np.ones((3,3),dtype = np.uint8)
erode = cv2.erode(maskblue,kernel_erode)
# 膨胀操作
kernel_dilate = np.ones((7,7),np.uint8)
dilate = cv2.dilate(erode, kernel = kernel_dilate)

thresholdValue, two_value = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY |cv2.THRESH_OTSU)
two_value = 255 - two_value
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
closed = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)

(cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cc = sorted(cnts, key=cv2.contourArea, reverse=True)

for t in range(len(cc)):
    c = cc[t]
    # compute the rotated bounding box of the largest contour
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    # draw a bounding box arounded the detected barcode and display the image
    cv2.drawContours(img2, [box], -1, (0, 255, 0), 3)
'''
Xs = [i[0] for i in box]
Ys = [i[1] for i in box]
x1 = min(Xs)
x2 = max(Xs)
y1 = min(Ys)
y2 = max(Ys)
hight = y2 - y1
width = x2 - x1
cropImg = gray[y1:y1+hight, x1:x1+width]
'''
cv2.namedWindow("src",0)
cv2.imshow('src', img)
cv2.namedWindow("out",0)
cv2.imshow('out', img2)
cv2.namedWindow("H",0)
cv2.imshow('H', dilate)

cv2.waitKey()
cv2.destroyAllWindows()