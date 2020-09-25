import cv2 
import numpy as np
import os
import time
import sys

if not os.path.exists("saved_faces"):
    os.mkdir("saved_faces")
name=str(sys.argv[1])

show_user,crop_img = None, None

# font 
font = cv2.FONT_HERSHEY_SIMPLEX 
  
# org 
org = (50, 50) 
  
# fontScale 
fontScale = 1
   
# Blue color in BGR 
color = (0, 255, 0) 
  
# Line thickness of 2 px 
thickness = 2

def detect_face(img,count):
    bw = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(bw,1.3,5)
    for x,y,w,h in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),3)
        cv2.putText(img,"Stay Still", (x-10,y-10), font, fontScale, color, thickness, cv2.LINE_AA)
        crop_img = frame[y:y+h,x:x+w]
        cv2.imwrite("saved_faces/"+name+".png",crop_img)
    return img 
count=0
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
resize = None

start_time = int(time.time())+10
#print(start_time+5,int(time.time()))

while True:
    ret,frame = cap.read()
    count+=1
    #frame = cv2.addWeighted(frame,2,np.zeros(frame.shape,frame.dtype),0,50)
    canvas = detect_face(frame,count)
    resize = cv2.resize(canvas,(600,480))
    cv2.imshow("capturing face...",frame)
    #if time.time() > start + exec_time:
    if canvas.all() != None and start_time == int(time.time()):
        break
    if cv2.waitKey(1)=='q':
        break
    
cap.release()
cv2.destroyWindow("capturing face...")
time.sleep(1)
img = cv2.imread(r"saved_faces/"+name+".png", cv2.IMREAD_COLOR)
cv2.namedWindow('Restart to retake image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Restart to retake image', 400,300)
cv2.imshow('Restart to retake image', img)

k = cv2.waitKey(33)

if k == 27:
    pass

time.sleep(5)
cv2.destroyWindow("Restart to retake image")

