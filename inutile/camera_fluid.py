import cv2

# Chargement du classificateur pour la reconnaissance faciale
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialisation de la capture vidéo
cap = cv2.VideoCapture(0)  # L'argument 0 indique la caméra par défaut

# Ajustement des paramètres de la caméra pour augmenter les FPS
# cap.set(cv2.CAP_PROP_FPS, 60)  # Remplace 60 par le nombre de FPS souhaité
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
while True:
    # Capture d'une image de la caméra
    ret, frame = cap.read()

    # Convertir l'image en niveaux de gris pour la détection faciale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Détection des visages
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Dessiner des rectangles autour des visages détectés
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Affichage du résultat
    cv2.imshow('Video', frame)

    # Sortir de la boucle si la touche 'q' est enfoncée
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libération des ressources
cap.release()
cv2.destroyAllWindows()
