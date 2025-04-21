import os
import shutil

# Chemins de base pour les images et les annotations
images_path = r"C:/Users/Adnan/Desktop/dataset_modified/images"
labels_path = r"C:/Users/Adnan/Desktop/dataset_modified/labels"

# Dossiers "train" et "val" pour les images
images_val_dir = os.path.join(images_path, "val")
images_train_dir = os.path.join(images_path, "train")

# Dossiers "train" et "val" pour les labels
labels_val_dir = os.path.join(labels_path, "val")
labels_train_dir = os.path.join(labels_path, "train")

# Extensions d'image acceptées
image_extensions = [".jpg", ".jpeg", ".png", ".bmp"]

# Récupère la liste des fichiers images dans le dossier "val"
all_images = [f for f in os.listdir(images_val_dir) if os.path.splitext(f)[1].lower() in image_extensions]
print(f"Nombre d'images dans 'val' : {len(all_images)}")

# Nombre d'images à déplacer
num_to_move = 14691

# Si moins d'images sont disponibles, on ajuste le nombre à déplacer
if len(all_images) < num_to_move:
    print(f"Il n'y a pas assez d'images dans 'val' pour déplacer {num_to_move}. On déplacera {len(all_images)} images.")
    num_to_move = len(all_images)

# Tri (optionnel) et sélection des images à déplacer
all_images.sort()
selected_images = all_images[:num_to_move]

# Parcours et déplacement des images et annotations correspondantes
for image_file in selected_images:
    # Chemin source et destination pour l'image
    src_image = os.path.join(images_val_dir, image_file)
    dst_image = os.path.join(images_train_dir, image_file)
    shutil.move(src_image, dst_image)
    print(f"Image déplacée : {image_file}")

    # Construction du nom de l'annotation associée (même base, extension .txt)
    base_name = os.path.splitext(image_file)[0]
    annotation_file = base_name + ".txt"
    src_label = os.path.join(labels_val_dir, annotation_file)
    dst_label = os.path.join(labels_train_dir, annotation_file)

    # Déplacer le label s'il existe
    if os.path.exists(src_label):
        shutil.move(src_label, dst_label)
        print(f"Annotation déplacée : {annotation_file}")
    else:
        print(f"Aucune annotation trouvée pour {image_file}")

print("Déplacement terminé.")
