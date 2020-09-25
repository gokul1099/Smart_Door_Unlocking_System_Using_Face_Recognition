import face_recognition
import cv2
import numpy as np
import os
import time
#import RPi.GPIO as GPIO
from send_mail import sendmail
from recieve_mail import receivemail
video_capture = cv2.VideoCapture(0)
#GPIO.cleanup()

known_face_encodings = []
path=r"saved_faces"
for i in os.listdir(path):
    img_path=os.path.join(path,i)
    img=face_recognition.load_image_file(img_path)
    #print(img)
    encoding=[]
    encoding = face_recognition.face_encodings(img)[0]
    known_face_encodings.append(encoding)
known_face_names = []
for i in os.listdir(path):
    name=i.split('.')[0]
    known_face_names.append(name)

# Initialize some variables
def capture():
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    count=0
    flag=0
    name = "Unknown"


    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        bw = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(bw,1.3,5)
        crop_img = []
        for x,y,w,h in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),3)
            crop_img = frame[y:y+h,x:x+w]
            cv2.imwrite("detected_face/temp.png",crop_img)
#             image = face_recognition.load_image_file("detected_face/temp.png")
        # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
        

            # Only process every other frame of video to save time
            #if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            #face_encoding = face_recognition.face_encodings(image)

            face_names = []
            for face_encoding in face_encodings:
                try:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                        #name = "Unknown"
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    else:
                        name = "Unknown"
                    #face_names.append(name)
                except ValueError:
                    pass
            
            cv2.imshow("performing_face_Detection",frame)
            k = cv2.waitKey(33)
                
            if name == "Unknown":
                count = count + 1
                if count == 10:
                    video_capture.release()
                    cv2.destroyAllWindows()
                    sendmail()
                    
                    #giving user some time to reply for server
                    print('giving user an 30 seconds time to reply for mail')
                    for i in range(1,31):
                        print('#'*i,i)
                        time.sleep(1)
                    #time.sleep(60)
                            
                    ans = receivemail()
                            
                    if ans == 'A' or ans == 'a':
                        print('Authority replied "ALLOW" opening the lock now')
                        time.sleep(1)
                        os.system('python3 lock.py')
                        #print('1')
                        flag=1
                        break
                    
                    elif ans == None:
                        flag = 1
                        print("Authority doesn't replied\nLOCK WILL NOT OPEN")
                                
                    else:
                        print('Authority replied "DENY" lock will not be opened')
                        flag=1
                        break
                        
                else:
                    continue
                
            elif name != "Unknown":
                os.system('python3 lock.py')
                #print('2')
                print(name)
                flag=1
                break
            
            os.remove("detected_face/temp.png")
            
        cv2.imshow("performing_face_Detection",frame)
            
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        if flag == 1:
            break
        
        #os.remove("faces/temp.png")
            
        #process_this_frame = not process_this_frame
        


    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()                

capture()
