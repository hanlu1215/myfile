clear all;close all;clc
dir='C:\Users\HAN\Documents\HomeWorks\exp\data_exp01.txt';
[data,year,month,day,hour,m,s]=textread(dir,'d:  %dmm[%d-%d-%d %d:%d:%f]');
t=hour*3600+m*60+s;
t=t-min(t);
figure
plot(t,data);