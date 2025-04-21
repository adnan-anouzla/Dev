import os

def cleanup_dataset(images_dir, annots_dir):
    """
    Parcourt les dossiers d'images et d'annotations et supprime les images sans annotation
    et les annotations sans image. Retourne le nombre d'images et d'annotations supprimées.

    Args:
        images_dir (str): Chemin du dossier contenant les images.
        annots_dir (str): Chemin du dossier contenant les annotations (.txt).

    Returns:
        tuple: (n_images_deleted, n_annots_deleted)
    """
    n_images_deleted = 0
    n_annots_deleted = 0

    # Filtrer les images par extension
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    image_files = [f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in image_extensions]
    
    # Supprimer les images sans annotation correspondante
    for image_file in image_files:
        base, _ = os.path.splitext(image_file)
        annot_file = base + ".txt"
        annot_path = os.path.join(annots_dir, annot_file)
        if not os.path.exists(annot_path):
            image_path = os.path.join(images_dir, image_file)
            try:
                os.remove(image_path)
                print(f"Image supprimée: {image_file} (pas d'annotation)")
                n_images_deleted += 1
            except Exception as e:
                print(f"Erreur lors de la suppression de {image_file}: {e}")

    # Filtrer les annotations au format .txt
    annot_files = [f for f in os.listdir(annots_dir) if os.path.splitext(f)[1].lower() == ".txt"]

    # Supprimer les annotations sans image correspondante
    for annot_file in annot_files:
        base, _ = os.path.splitext(annot_file)
        # On vérifie toutes les extensions possibles pour trouver l'image correspondante
        image_found = False
        for ext in image_extensions:
            image_filename = base + ext
            image_path = os.path.join(images_dir, image_filename)
            if os.path.exists(image_path):
                image_found = True
                break
        if not image_found:
            annot_path = os.path.join(annots_dir, annot_file)
            try:
                os.remove(annot_path)
                print(f"Annotation supprimée: {annot_file} (pas d'image correspondante)")
                n_annots_deleted += 1
            except Exception as e:
                print(f"Erreur lors de la suppression de {annot_file}: {e}")
    
    return n_images_deleted, n_annots_deleted

# Exemple d'utilisation :
if __name__ == "__main__":
    images_directory = "chemin/vers/train/images"      # À adapter selon votre dossier
    annotations_directory = "chemin/vers/train/annotations"  # À adapter selon votre dossier
    
    images_deleted, annots_deleted = cleanup_dataset(images_directory, annotations_directory)
    print(f"Nombre d'images supprimées : {images_deleted}")
    print(f"Nombre d'annotations supprimées : {annots_deleted}")
