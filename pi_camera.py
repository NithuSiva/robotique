import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
from train_and_recognition import *

def rec_face():
    (width, height) = (10, 10)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam = PiCamera()
    cam.resolution = (512, 304)
    cam.framerate = 30
    rawCapture = PiRGBArray(cam, size=(512, 304))
    
    name = "unknown"

    while True:
        for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            
        
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Detect the faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            # Draw the rectangle around each face
            #for (x, y, w, h) in faces:
                #cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
                #cv2.putText(image, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            # Display
            for (x, y, w, h) in faces: 
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2) 
                face = gray[y:y + h, x:x + w] 
                face_resize = cv2.resize(face, (width, height)) 
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, name, (x + 6, y - 6), font, 1.0, (255, 255, 255), 1)
            
            cv2.imshow("Face Reco", image)
            rawCapture.truncate(0)
            
            k = cv2.waitKey(30) & 0xff
            leave = False
            
            if k == 27:
                print("Escape")
                leave = True
                break
            if k == 115:
                print("S")
                name = recognize_faces_video(image)
        if leave:
            break
        

    cv2.destroyAllWindows()
