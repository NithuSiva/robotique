import cv2, face_recognition
from datetime import datetime
from train_and_recognition import *


def rec_fac():
	(width, height) = (10, 10)	 

	face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
	webcam = cv2.VideoCapture(0) 
	webcam.set(cv2.CAP_PROP_FPS, 60)
	webcam.set(cv2.CAP_PROP_BUFFERSIZE, 0)
	webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
	webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

	name = "Inconnu"
	accuracy = "?"
	color = (255, 0, 0)
	
	while True: 
		(_, im) = webcam.read() 
		
		small_frame = cv2.resize(im, (0, 0), fx=0.15, fy=0.15)
		
		gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
		faces = face_cascade.detectMultiScale(gray, 1.3, 4)
		
		for (x, y, w, h) in faces: 
			cv2.rectangle(im, (x, y), (x + w, y + h), color, 2) 
			face = gray[y:y + h, x:x + w] 
			face_resize = cv2.resize(face, (width, height)) 
			font = cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(im, name, (x + 6, y - 6), font, 1.0, color, 1)
		
		
		cv2.imshow('OpenCV', im)
		key = cv2.waitKey(10) 
		if key == 115:
			try:
				resultat = recognize_faces_video(im)
				name = resultat[0]
				accuracy = resultat[1]
				print(name, accuracy)
				print("isinstance(accuracy, int) ", isinstance(accuracy, int))
				if accuracy != '?':
					accuracy = round(accuracy)
					name = f"{name} {accuracy}%"
					color = (0, 255, 0)
				else:
					color = (0, 0, 255)
			except:
				print('Erreur !')
		if key == 27: 
			break
	
