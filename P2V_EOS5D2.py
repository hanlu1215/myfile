# coding=utf-8
import cv2, os, time, sys
from tqdm import tqdm
fps = 24
show_now = False

file_name = input("Input file_name: ")
img_dir = '.\\'+ file_name +'\\'
video_dir = '.\\' + file_name + '.mp4'
# img_dir = os.getcwd()+'\\'+ file_name +'\\'
# video_dir = os.getcwd()+'\\' + file_name + '.mp4'

# k = int(input("Start num: "))
# img_name = img_dir + '_MG_'
# TT = img_name + str(k)+'.JPG'
# i_max = len(os.listdir(img_dir))
# img = cv2.imread(TT)

img_names = os.listdir(img_dir)
img_names.sort()
img = cv2.imread(img_dir+img_names[0])

x,y,_ = img.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
videoWriter = cv2.VideoWriter(video_dir,fourcc,fps,(y,x),True)

if show_now:
    cv2.namedWindow("img",0)

# for i in tqdm(range(i_max)):
#     TT = img_name + str(k)+'.JPG'
#     k=k+1
#     img = cv2.imread(TT)
#     try:
#         img.shape 
#     except:
#         print('fail to read ' + TT)
#         continue
#     if show_now:
#         cv2.imshow('img', img)
#         cv2.waitKey(10)
#     videoWriter.write(img)

for img_name in tqdm(img_names):
    img = cv2.imread(img_dir+img_name)
    try:
        img.shape 
    except:
        print('fail to read ' + img_name)
        continue
    if show_now:
        cv2.imshow('img', img)
        cv2.waitKey(10)
    videoWriter.write(img)

videoWriter.release()
# os.system('pause')