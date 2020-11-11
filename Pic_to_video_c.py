# coding=utf-8
import cv2
import os
fps = 10

file_name = input("Input file_name: ")
img_dir = os.getcwd()+'\\'+ file_name +'\\'
video_dir = os.getcwd()+'\\' + file_name + '.avi'

k_max = len(os.listdir(img_dir))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
img = cv2.imread(img_dir + str(1) +'.jpg')
x,y,_ = img.shape
videoWriter = cv2.VideoWriter(video_dir,fourcc,fps,(y,x),True)
for i in range(1, k_max+1):
    image_number = i
    img = cv2.imread(img_dir + str(i) +'.jpg')
    cv2.imshow('img', img)
    cv2.waitKey(10)
    videoWriter.write(img)
    print(str(i)+'/'+str(k_max)+'is ok')
videoWriter.release()
