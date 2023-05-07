# -*- coding: utf-8 -*-
import re
import os
import time
import subprocess
import requests
import pathlib
import json
file_path = ".//data.a//"
file_path = "I://gdg//"
print("1:"+file_path)
file_path = "I://music//"
print("2:"+file_path)
file_path = "I://DownloadV//a//"
print("3:"+file_path)

file_path =os.getcwd()+ "//"
print("4:"+file_path)
file_path = "I://DownloadV//"
print("_:"+file_path)

flag_path = input("file_path num:")
if flag_path == "1":
    file_path = "I://gdg//"
elif flag_path == "2":
    file_path = "I://music//"
elif flag_path == "3":
    file_path = "I://DownloadV//a//"
elif flag_path == "4":
    file_path = ".//"
else:
    file_path = "I://DownloadV//"
print("file_path: "+file_path)

url_paths = []
p1 = input("input url:")
url_paths.append(p1)
flag_media = input("input file format: [mp3 flac video(v) m3u8(38) concat_ts(c) cctv] :")
if input("flag_replace_name(1)  : ")=="1":
    flag_replace_name = True
    print("flag_replace_name:True")
else:
    flag_replace_name = False
    print("flag_replace_name:False")


def re_emojis(text):
    emoji_pattern = re.compile("["
           u"\U0001F600-\U0001F64F"
           u"\U0001F300-\U0001F5FF"
           u"\U0001F680-\U0001F6FF"
           u"\U0001F1E0-\U0001F1FF"
           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r' ', text)
def filter_str(desstr, restr=''):
    # 过滤除中英文及数字以外的其他字符
    res = re.compile("[^\\u4e00-\\u9fa5^a-z^A-Z^0-9.://]")
    return res.sub(restr, desstr)

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")

def getFileName(path):
    ''' 获取指定目录下的所有指定后缀的文件名 '''
    output_list = []
    folder = os.path.exists(path)
    if  folder:
        f_list = os.listdir(path)
        for i in f_list:
            # os.path.splitext():分离文件名与扩展名
            if os.path.splitext(i)[1] in [".mp4",".mkv",".avi",".flv",".webm",".mp3"]:
                output_list.append(path+"//"+i)
    else :
         print("---  There is no file!  ---")
    return output_list

def replace_name(file_path):
    file_names = getFileName(file_path)
    for name in file_names:
        print(name)
        # name2 = re_emojis(name)
        # print(name2)
        name3 = filter_str(name)
        print(name3)
        os.rename(name,name3)
def download_youtube_v(url_path,file_path):
    webm2mkv = " --remux-video webm>mkv"
    webm2mkv = ""
    cmd = "yt-dlp.exe "+url_path+webm2mkv+" -P "+file_path
    subprocess.run(cmd)

def download_youtube_a(url_path,file_path,file_format):
    cmd = "yt-dlp.exe -f ba "+url_path+" -P "+file_path + file_format
    # os.system(cmd)
    subprocess.run(cmd)
    
def download_m3u8(url_path,file_path):
    cmd = "ffmpeg -user_agent \"Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36\" -i "
    cmd += url_path+" -c copy "+file_path + str(time.time())+".mp4"
    subprocess.run(cmd)

def download_m3u8_2(url,file_path):
    ti = str(time.time())
    os.chdir(file_path)
    file_path = os.getcwd()+"//"
    temp_dir = "temp"+ti
    output_name = os.getcwd()+"//" + ti +".mp4"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
    }
    # 获取m3u8文件内容
    m3u8 = requests.get(url, headers=headers).text
    print("-------------m3u8---------------")
    # print(m3u8)
    print("----------------------------")
    # 获取ts文件列表
    # ts_list = [url.rsplit("/", 1)[0] + "/" + i for i in m3u8.split("\n") if i.endswith(".ts")]
    ts_list = [url.rsplit("/", 1)[0] + "/" + i for i in m3u8.split("\n") if ".ts" in i]
    # 下载ts文件
    print("------------开始下载：----------------")
    mkdir(temp_dir)
    pathlib.Path(temp_dir+"//.ignore").touch()
    txt_path = temp_dir+"\\list.txt"
    f_txt = open(txt_path,"a")
    kk=0
    for ts_url in ts_list:
        # ts_name = ts_url.rsplit("/", 1)[-1]
        kk = kk +1
        ts_name = str(kk).zfill(4)+".ts"
        print("----------------------------")
        print(ts_url)
        print("----------------------------")
        ki = 0
        while(ki<10):
            ki = ki +1
            sub1 = subprocess.run(["wget", "-O", temp_dir + "//" + ts_name, ts_url,"-U","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"])
            print(sub1.returncode)
            if sub1.returncode == 0 and os.path.getsize(temp_dir+"//"+ts_name)>0:
                break
            if sub1.returncode ==8 :
                print("资源有可能过期或者打不开了，请重新获取资源")
                os.system("pause")
            print("try:"+str(ki))
        print("++++++++++++")
        print(sub1.returncode)
        if sub1.returncode == 0 and os.path.getsize(temp_dir+"//"+ts_name)>0:
            txt_data = "file \'"+ts_name+"\'\n"
            f_txt.write(txt_data)
        print("++++++++++++")
    f_txt.close()
    # 合并ts文件为mp4文件
    os.chdir(temp_dir)
    subprocess.run(["ffmpeg", "-y","-f", "concat", "-safe","0","-i","list.txt","-c", "copy", output_name])
    os.chdir(file_path)
    print("完成："+output_name)
    # 删除临时文件：
    delete_temp = input("delete .ts files intput(1) : ")
    if delete_temp=="1":
        print("delete_temp")
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.removedirs(temp_dir)

def concat_ts(url_path,file_path):
    temp_dir = url_path
    os.chdir(file_path)
    file_path = os.getcwd()+"//"
    folder = os.path.exists(temp_dir)
    print("folder:")
    print(folder)
    if  folder:
        f_list = os.listdir(temp_dir)
        f_list.sort(key=lambda file: os.path.getmtime(os.path.join(temp_dir, file)))
        output_name = file_path + temp_dir +".mp4"
        txt_path = temp_dir+"//" + "list.txt"
        f_txt = open(txt_path,"w")
        print("open txt")
        for i in f_list:
            if os.path.splitext(i)[1] in [".ts"] and os.path.getsize(temp_dir+"//"+i)>0:
                txt_data = "file \'"+i+"\'\n"
                f_txt.write(txt_data)
        f_txt.close()
        # os.chdir(temp_dir)
        subprocess.run(["ffmpeg","-y","-f", "concat", "-safe","0","-i",txt_path,"-c", "copy", output_name])
        # os.chdir(file_path)
        print("完成："+output_name)
        # 删除临时文件：
        delete_temp = input("delete .ts files intput(1) : ")
        if delete_temp=="1":
            print("delete_temp")
            for f in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, f))
            os.removedirs(temp_dir)

def download_cctv_v(url_main,file_path):
    # url:getHttpVideoInfo
    ti = str(time.time())
    os.chdir(file_path)
    file_path = os.getcwd()+"//"
    temp_dir = "temp"+ti    
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
    }
    # 获取url文件内容
    url_txt = requests.get(url_main, headers=headers).text
    print("-------------url_json[video]key:---------------")
    url_json = json.loads(url_txt)
    if "title" in url_json:
        output_name = os.getcwd()+"//" + url_json["title"] +".mp4"
    else:
        output_name = os.getcwd()+"//" + input("save name:") +".mp4"
    print("output_name:"+output_name)
    for key in url_json["video"]:
        print(key)
    chaptersn = "chapters"+input("which chapters[]:")
    chaptersn_jsons = url_json["video"][chaptersn]
    while chaptersn_jsons == []:
        chaptersn = "chapters"+input("which chapters[]:")
        chaptersn_jsons = url_json["video"][chaptersn]
    urls = []
    for chaptersn_json in chaptersn_jsons:
        urls.append(chaptersn_json["url"])
    print("------------开始下载：----------------")
    mkdir(temp_dir)
    pathlib.Path(temp_dir+"//.ignore").touch()
    txt_path = temp_dir+"\\list.txt"
    f_txt = open(txt_path,"a")
    kk=0
    for mp4_url in urls:
        kk = kk +1
        mp4_name = str(kk).zfill(4)+".mp4"
        print("----------------------------")
        print(mp4_url)
        print("----------------------------")
        ki = 0
        while(ki<10):
            ki = ki +1
            sub1 = subprocess.run(["wget", "-O", temp_dir + "//" + mp4_name, mp4_url,"-U","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"])
            print(sub1.returncode)
            if sub1.returncode == 0 and os.path.getsize(temp_dir+"//"+mp4_name)>0:
                break
            if sub1.returncode ==8 :
                print("资源有可能过期或者打不开了，请重新获取资源")
                os.system("pause")
            print("try:"+str(ki))
        print("++++++++++++")
        print(sub1.returncode)
        if sub1.returncode == 0 and os.path.getsize(temp_dir+"//"+mp4_name)>0:
            txt_data = "file \'"+mp4_name+"\'\n"
            f_txt.write(txt_data)
        print("++++++++++++")
    f_txt.close()
    # 合并ts文件为mp4文件
    os.chdir(temp_dir)
    subprocess.run(["ffmpeg", "-y","-f", "concat", "-safe","0","-i","list.txt","-c", "copy", output_name])
    os.chdir(file_path)
    print("完成："+output_name)
    # 删除临时文件：
    delete_temp = input("delete temp files intput(1) : ")
    if delete_temp=="1":
        print("delete_temp")
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.removedirs(temp_dir)

def webm2mp3(name):
    cmd = "ffmpeg -i "+name+" -vn "+os.path.splitext(name)[0]+".mp3"
    subprocess.run(cmd)
if __name__ == '__main__':
    if flag_media in ["video","v"]:
        for url_path in url_paths:
            download_youtube_v(url_path,file_path)
    if flag_media in ["mp3","flac"]:
        file_format = " -x --audio-format "+flag_media
        for url_path in url_paths:
            download_youtube_a(url_path,file_path,file_format)
    if flag_media in ["m3u8","38"]:
        for url_path in url_paths:
            download_m3u8_2(url_path,file_path)
    if flag_media in ["concat_ts","c"]:
        print("concat_ts")
        for url_path in url_paths:
            concat_ts(url_path,file_path)
    if flag_media in ["cctv"]:
        print("download cctv video:")
        for url_path in url_paths:
            download_cctv_v(url_path,file_path)
    if flag_replace_name:
        replace_name(file_path)
    print("处理完成")
    os.system("pause")
