import os

def extract_scene_ids(images_dir, output_txt):
    """
    Parcourt le dossier d'images, extrait les identifiants de scène (la partie avant "_img")
    et enregistre la liste unique de ces identifiants dans un fichier texte.

    Args:
        images_dir (str): Chemin du dossier contenant les images.
        output_txt (str): Chemin du fichier texte de sortie.
    """
    scene_ids = set()
    
    # Liste des extensions d'images acceptées (à adapter si besoin)
    valid_ext = {'.jpg', '.jpeg', '.png', '.bmp'}
    
    # Parcourt le dossier images
    for file_name in os.listdir(images_dir):
        ext = os.path.splitext(file_name)[1].lower()
        if ext in valid_ext:
            if "_img" in file_name:
                # Extraction de la partie avant "_img"
                scene_id = file_name.split("_img")[0]
                scene_ids.add(scene_id)
            else:
                # Si le format de nommage est différent, il faudra adapter
                print(f"Format inattendu pour le fichier : {file_name}")
    
    # Écriture des identifiants de scènes dans le fichier texte
    with open(output_txt, 'w') as f:
        for scene_id in sorted(scene_ids):
            f.write(scene_id + "\n")
    
    print(f"{len(scene_ids)} scènes ont été enregistrées dans {output_txt}")

if __name__ == "__main__":
    # Chemin du dossier contenant les images
    images_directory = r"C:\Users\Adnan\Desktop\ATNa\dataset\vehicles\UA_DETRAC_Orig\content\UA-DETRAC\DETRAC_Upload\images\train"
    # Nom et chemin du fichier de sortie
    output_file = r"scenes_list.txt"
    
    extract_scene_ids(images_directory, output_file)