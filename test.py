import tkinter as tk    
from tkinter import messagebox

# Fonction pour simuler l'ajout d'une personne à la base de données
def ajouter_personne(nom):
    # Ajoute le nom à la base de données (simulé ici)
    # Remplace cela par la logique réelle pour ajouter une personne à la base de données
    liste_noms.append(nom)

# Fonction pour mettre à jour la Listbox avec les noms de la base de données
def mettre_a_jour_listbox():
    liste_box.delete(0, tk.END)  # Efface tous les éléments actuels

    # Ajoute les noms actualisés à la Listbox
    for nom in liste_noms:
        liste_box.insert(tk.END, nom)

# Fonction appelée lors du clic sur le bouton "Ajouter Personne"
def afficher_fenetre_ajout_personne():
    # Ajouter ici la logique pour afficher la fenêtre d'ajout de personne
    # Après avoir ajouté une personne, appelle mettre_a_jour_listbox()
    ajouter_personne("Nouvelle Personne")
    mettre_a_jour_listbox()

# Initialisation de la liste des noms (simulée ici)
liste_noms = ["Nom1", "Nom2", "Nom3"]

# Fonction pour créer la fenêtre principale
def creer_fenetre_principale():
    global db_fenetre, liste_box

    db_fenetre = tk.Tk()
    db_fenetre.title("Base de Données")

    liste_box = tk.Listbox(db_fenetre)
    for nom in liste_noms:
        liste_box.insert(tk.END, nom)
    liste_box.pack()

    bouton_ajout_personne = tk.Button(db_fenetre, text="Ajouter Personne", command=afficher_fenetre_ajout_personne)
    bouton_ajout_personne.pack()

# Créer la fenêtre principale
creer_fenetre_principale()

# Lancer la boucle principale
db_fenetre.mainloop()