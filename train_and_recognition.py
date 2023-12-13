from pathlib import Path
from collections import Counter
import numpy as np
import os, face_recognition, pickle

DEFAULT_ENCODINGS_PATH = Path("db/encoding/encodings.pkl")

# Prend en paramètres une liste d'images et un nom
# Encode chaque image dans un fichier .plk appartenant au nom dans le dossier liste_personne
def encode_images_faces(name, images,
    model: str = "hog") -> None:
    
    encodings = []
    names = []
    name = name.split(" ")
    name = name[0] + "_" + name[1]
    encodings_location: str = Path(f"db/encoding/liste_personne/{name}.plk") 

    for image_file in images:

        face_reco_image = face_recognition.load_image_file(image_file)
        face_locations = face_recognition.face_locations(face_reco_image, model=model)
        face_encodings = face_recognition.face_encodings(face_reco_image, face_locations)

        #Normalement 1 seul visage sur l'image donc pas necessaire le for
        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)
        
    names_encodings = {"names": names, "encodings": encodings}

    with encodings_location.open(mode="wb") as f:
        pickle.dump(names_encodings, f)
    
    return encodings_location

# Parcours le dossier liste_personne et va ajouter l'encodage de chaque fichier dans une liste afin de créer un encodage unique
def encode_tout(encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    path = Path("db/encoding/liste_personne")
    liste_personne = os.listdir(path)
    names = []
    encodings = []

    for personne in liste_personne:
        path_personne = Path(str(path) + '/' + str(personne))
        print(path_personne)
        
        if(os.path.isfile(path_personne)):
            with path_personne.open(mode="rb") as f:
                loaded_encodings = pickle.load(f)
                print(loaded_encodings['names'])
                for name in loaded_encodings['names']:
                    names.append(name)
                for encode in loaded_encodings['encodings']:
                    encodings.append(encode)

        else:
            print("NO file encode.plk")

    names_encodings = {"names": names, "encodings": encodings}   

    with encodings_location.open(mode="wb") as f:
        pickle.dump(names_encodings, f)

# Fonction qui va comparé la frame de la caméra avec le fichier d'encodage
def _recognize_face_video(unknown_encoding, loaded_encodings):
    unknown_encoding = np.array(unknown_encoding)
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    # Distance qui renvoie la difference de caracterstique entre la frame et chaque données de visage stocké dans l'encodage
    distance = face_recognition.face_distance(loaded_encodings["encodings"], unknown_encoding)
    list_distance = list(map(lambda x: round(x * 100), distance))

    # Calcul la précision entre la frame et chaque données de visage stocké dans l'encodage
    list_precision = list(map((lambda x: 100 - x), list_distance))

    # Créer une liste qui pour chaque précision du visage dans l'encodage, est vrai si il est strictement supérieur à 50
    # sinon faux
    list_validation = list(
        map((lambda ac: True if ac >= 50 else False),list_precision))
    
    # Créer un dictionnaire des noms présent dans l'encodage
    name_precision = {name: [] for name in loaded_encodings["names"]}

    # Associer chaque precision à son nom correspondant
    for precision, name, is_valid in zip(list_precision,
                                        loaded_encodings["names"],
                                        list_validation):
        if is_valid:
            name_precision[name].append(precision)
            
    # Calculer la moyenne des précision pour chaque nom
    moyenne_precisions = {name: sum(accuracies) / len(accuracies) for name, accuracies in name_precision.items() if accuracies}

    if moyenne_precisions:
        return  list(moyenne_precisions.items())[0]
    else:
        return ('Inconnu', '?')

# Fonction chapeau qui va appelé la fonction _recognize_face_video, il retourne soit le visage reconnu soit 'Inconnu'
def recognize_faces_video(im,
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    with encodings_location.open(mode="rb") as f:
        loaded_encodings = pickle.load(f)

    face_encodings = face_recognition.face_encodings(im)

    for unknown_encoding in zip(face_encodings):
        name = _recognize_face_video(unknown_encoding, loaded_encodings)
        return name