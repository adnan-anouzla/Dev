import os

# Chemin du dossier contenant les fichiers
dossier = r"C:/Users/Adnan/Devsktop/resized_images1280x734/images_shuffled/val_shuffled"

# Parcourt tous les fichiers du dossier
for nom_fichier in os.listdir(dossier):
    if nom_fichier.endswith(".txt"):
        chemin_fichier = os.path.join(dossier, nom_fichier)
        # Vérifie que c'est bien un fichier avant de le supprimer
        if os.path.isfile(chemin_fichier):
            os.remove(chemin_fichier)
            print(f"Fichier supprimé : {chemin_fichier}")
