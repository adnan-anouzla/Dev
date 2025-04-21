import os
import shutil
import random
import math

def shuffle_and_select_subset(images_dir, labels_dir, output_images_dir, output_labels_dir, fraction=0.08):
    """
    Mélange tout le dataset (images + annotations), renomme de façon unique, puis extrait aléatoirement 8%.

    Args:
        images_dir (str): Dossier contenant toutes les images (train + val fusionnés si besoin).
        labels_dir (str): Dossier contenant les fichiers de labels correspondants.
        output_images_dir (str): Dossier de sortie pour les images sélectionnées.
        output_labels_dir (str): Dossier de sortie pour les labels sélectionnés.
        fraction (float): Fraction du dataset à extraire.
    """
    valid_ext = {'.jpg', '.jpeg', '.png', '.bmp'}
    os.makedirs(output_images_dir, exist_ok=True)
    os.makedirs(output_labels_dir, exist_ok=True)

    # Étape 1 : Associer les couples (image, label) valides
    all_pairs = []
    for file in os.listdir(images_dir):
        ext = os.path.splitext(file)[1].lower()
        if ext in valid_ext:
            base = os.path.splitext(file)[0]
            img_path = os.path.join(images_dir, file)
            lbl_path = os.path.join(labels_dir, base + '.txt')
            if os.path.exists(lbl_path):
                all_pairs.append((img_path, lbl_path))
            else:
                print(f"⚠️ Label manquant pour : {file}")

    print(f"Nombre total d'images valides trouvées : {len(all_pairs)}")

    if len(all_pairs) == 0:
        print("Aucune paire image + label valide trouvée.")
        return

    # Étape 2 : Shuffle complet
    random.shuffle(all_pairs)

    # Étape 3 : Sélection aléatoire de 8%
    n_select = math.ceil(len(all_pairs) * fraction)
    selected_pairs = random.sample(all_pairs, n_select)
    print(f"Nombre d’éléments sélectionnés : {n_select} ({fraction*100:.1f}%)")

    # Étape 4 : Copie avec renommage (img_00001.jpg / img_00001.txt, etc.)
    for idx, (img_path, lbl_path) in enumerate(selected_pairs, 1):
        new_name = f"img_{idx:05d}"
        img_ext = os.path.splitext(img_path)[1].lower()

        new_img_name = new_name + img_ext
        new_lbl_name = new_name + ".txt"

        shutil.copy2(img_path, os.path.join(output_images_dir, new_img_name))
        shutil.copy2(lbl_path, os.path.join(output_labels_dir, new_lbl_name))

    print("✅ Sous-ensemble extrait avec succès.")

if __name__ == "__main__":
    # === 📂 Dossiers à configurer ===
    images_dir = r"C:/Users\Adnan\Desktop\ATNa\dataset/vehicles/UA_DETRAC_Orig/content/UA-DETRAC\DETRAC_Upload/images/val"
    labels_dir = r"C:/Users\Adnan\Desktop\ATNa\dataset/vehicles/UA_DETRAC_Orig/content/UA-DETRAC\DETRAC_Upload/labels/val"

    output_images_dir = r"C:/Users\Adnan\Desktop/Subset9/images"
    output_labels_dir = r"C:/Users\Adnan\Desktop/Subset9/labels"

    shuffle_and_select_subset(images_dir, labels_dir, output_images_dir, output_labels_dir, fraction=0.08)
