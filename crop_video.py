# -*- coding: utf-8 -*-
import cv2,os
video_path = input("input video path:")
video_dir =os.path.splitext(video_path)[0] + "-crop" + os.path.splitext(video_path)[1]

def crop_video(video_path):
    video=cv2.VideoCapture(video_path)
    fps = int(round(video.get(cv2.CAP_PROP_FPS)))
    print("fps:"+str(fps))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    new_hight = 1080
    new_width = int(width*new_hight/height)
    cv2.namedWindow(video_path, 0)
    cv2.resizeWindow(video_path, new_width, new_hight)  # 设置窗口大小
    grabbed, frame = video.read()
    cv2.imshow(video_path,frame)
    # 选择ROI
    roi = cv2.selectROI(windowName=video_path, img=frame, showCrosshair=True, fromCenter=False)
    x, y, w, h = roi
    print(roi)
    # 显示ROI并保存图片
    if roi != (0, 0, 0, 0):
        crop = frame[y:y+h, x:x+w]
        cv2.imshow(video_path, crop)
    else:
        crop = frame
        w = width
        h = height
        cv2.imshow(video_path, crop)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter(video_dir,fourcc,fps,(w,h),True)
    videoWriter.write(crop)
    while True:
        grabbed, frame = video.read()
        crop = frame[y:y+h, x:x+w]
        cv2.imshow(video_path, crop)
        cv2.waitKey(5)
        videoWriter.write(crop)
        if not grabbed:
            print("End of video")
            break
    video.release()
    videoWriter.release()
    cv2.destroyAllWindows()
crop_video(video_path)

