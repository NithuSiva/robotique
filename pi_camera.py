import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
from train_and_recognition import *

# Fonction qui affiche la camera, et qui fait de la reconnaissance faciale
def rec_face():

    # Définie le modèle utiliser pour reconnaître un visage 

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cam = PiCamera()

    # Définie la resolution de la caméra
    cam.resolution = (512, 304)
    cam.framerate = 30
    rawCapture = PiRGBArray(cam, size=(512, 304))

    # Définie le nom, la couleur et la précision initiale lorsque aucun visage n'est reconnu
    name = "Inconnu"
    color = (255, 0, 0)
    precision = "?"
    
    while True:
        for frame in cam.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            
            image = frame.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Détecter le visage sur la frame de la caméra 
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)


            # Dessine un carré sur le visage 
            for (x, y, w, h) in faces: 
                cv2.rectangle(image, (x, y), (x + w, y + h), color, 2) 
                face = gray[y:y + h, x:x + w] 
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(image, name, (x + 6, y - 6), font, 1.0, color, 1)
            
            # Afficher la caméra
            cv2.imshow("Face Reco", image)
            rawCapture.truncate(0)
            
            key = cv2.waitKey(30) & 0xff
            leave = False

            # Lorsque on appuie sur la touche 'S' on lance l'algorithme de reconnaissance faciale
            if key == 115:
                try:
                    resultat = recognize_faces_video(image)                    
                    name = resultat[0]
                    precision = resultat[1]
                    print(name, precision)
                    print("isinstance(precision, int) ", isinstance(precision, int))
                    if precision != '?':
                        precision = round(precision)
                        name = f"{name} {precision}%"
                        color = (0, 255, 0)
                    else:
                        color = (0, 0, 255)
                except:
                    print('Erreur !')
            
            # Lorsque on appuie sur la touche 'Echap' on quitte la fenêtre de la camera afficher
            if key == 27:
                leave = True 
                break
        if leave:
            break

    cv2.destroyAllWindows()

