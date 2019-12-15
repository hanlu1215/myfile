# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import copy
import pywt
import pywt.data
'''
def test_pywt():
    rec=cv.imread('lena.jpg',0)
    titles=['Approximation','Horizontal detail','Vertical detail','Diagonal detail']
    LL,(LH,HL,HH)=pywt.dwt2(rec,'bior1.3')
    fig=plt.figure(figsize=(12,3))
    for k,a in enumerate([LL,LH,HL,HH]):
        ax=fig.add_subplot(1,4,k+1)
        ax.imshow(a,interpolation="nearest",cmap=plt.cm.gray)
        ax.set_title(titles[k],fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    plt.show()
#读取图像数据
src = cv.imread('exp06.jpg',0)

"""
以下为练习部分
"""
ecg=pywt.data.ecg()
index=[]
data=[]
for k in range(len(ecg)-1):
    X=float(k)
    Y=float(ecg[k])
    index.append(X)
    data.append(Y)
w=pywt.Wavelet('db8')
maxlev=pywt.dwt_max_level(len(data),w.dec_len)
print("maximum level is"+str(maxlev))
threshold=0.04

coeffs=pywt.wavedec(data,'db8',level=maxlev)
plt.figure()
for k in range(1,len(coeffs)):
    coeffs[k]=pywt.threshold(coeffs[k],threshold*max(coeffs[k]))

datarec = pywt.waverec(coeffs,'db8')
mintime=0
maxtime=mintime+len(data)+1
plt.figure()
plt.subplot(2,1,1)
plt.plot(index[mintime:maxtime],data[mintime:maxtime])
plt.xlabel('time(s)')
plt.ylabel('microvolts(uV)')
plt.title('raw signal')
plt.subplot(2,1,2)
plt.plot(index[mintime:maxtime-1],datarec[mintime:maxtime-1])
plt.show()


"""
第二个练习
"""
test_pywt()
''' 
"""
实验作业
"""
def img2wavedec2(img):#定义了一个可以处理单通道的小波变换函数，将一级和二级压缩图像直接输出
    coeffs=pywt.wavedec2(img,'haar',level=1)
    ca1,(ch1,cv1,cd1)=coeffs
    ah1=np.concatenate([ca1,ch1+510],axis=1)
    vd1=np.concatenate([cv1+510,cd1+510],axis=1)
    img1=np.concatenate([ah1,vd1],axis=0)
    coeffs2=pywt.wavedec2(ca1,'haar',level=1)
    ca2,(ch2,cv2,cd2)=coeffs2
    ah2=np.concatenate([ca2,ch2+510],axis=1)
    vd2=np.concatenate([cv2+510,cd2+510],axis=1)
    temp=np.concatenate([ah2,vd2],axis=0)
    ah22=np.concatenate([temp,ch1+510],axis=1)
    img2=np.concatenate([ah22,vd1],axis=0)
    img1=img1/np.max(img1)*255
    img2=img2/np.max(img2)*255
    img1=np.uint8(img1)
    img2=np.uint8(img2)
    return ca1,ca2

#读取图像，对每一通道进行小波变换
img=cv.imread('lena.jpg',1)
img0=img[:,:,0]
imgb1,imgb2=img2wavedec2(img0)
img1=img[:,:,1]
imgg1,imgg2=img2wavedec2(img1)
img2=img[:,:,2]
imgr1,imgr2=img2wavedec2(img2)
#将三个通道进行合并，注意后边用plt函数进行绘图和cv的函数三通道顺序不一样
img_1=cv.merge([imgr1,imgg1,imgb1])
img_2=cv.merge([imgr2,imgg2,imgb2])

img_1=np.uint8(img_1/np.max(img_1)*255)
img_2=np.uint8(img_2/np.max(img_2)*255)

plt.figure()
plt.imshow(img_1)
plt.figure()
plt.imshow(img_2)
plt.show()
img_1=cv.merge([imgb1,imgg1,imgr1])
img_2=cv.merge([imgb2,imgg2,imgr2])

img_1=np.uint8(img_1/np.max(img_1)*255)
img_2=np.uint8(img_2/np.max(img_2)*255)

cv.imwrite('wavedec1.jpg',img_1)
cv.imwrite('wavedec2.jpg',img_2)












