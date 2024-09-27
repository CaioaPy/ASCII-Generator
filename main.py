import cv2
import ascii_magic
import imgkit
import os

#create folders
os.mkdir("images")
os.mkdir("acii")
os.mkdir("html")

#get video
video = ""
video_obj = cv2.VideoCapture(video)

count = 0
flag = 1
while flag:
    flag, image = video_obj.read()
    try:
        cv2.imwrite("images/frame$d.jpg" % count, image)
    except:
        break
    count += 1