# coding=utf-8
import time
import cv2
import os
import pyperclip
k_max = 10*360*4
delay_time = 2.5
file_name = time.strftime('%Y_%m_%d_%H_%M_%S')
img_dir = os.getcwd()+'\\'+file_name+'\\'
os.mkdir(img_dir)
print("save img to " + img_dir)
cap=cv2.VideoCapture(0)#获取摄像头的参数
cv2.namedWindow('img')
for k in range(1, k_max+1):
    ret,src=cap.read(0)
    name = img_dir+ str(k) +'.jpg'
    cv2.imwrite(name,src)
    cv2.imshow("img",src)
    
    kk=cv2.waitKey(int(1000*delay_time))
    if kk==113:
        break
    print(str(k)+'/'+str(k_max)+" is ok")
    #print(time.strftime('%Y_%m_%d_%H_%M_%S'))
    #time.sleep(delay_time-10/1000)
cv2.destroyAllWindows()
cap.release()
pyperclip.copy(file_name)
