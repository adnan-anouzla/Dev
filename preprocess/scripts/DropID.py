import os

def update_label_file_excluding_ids(label_path, excluded_ids={"0", "2", "3"}):
    """
    Supprime entièrement les lignes d’un fichier YOLO dont l’ID de classe (premier token)
    est présent dans excluded_ids.

    Args:
        label_path (str): Chemin vers le fichier de label.
        excluded_ids (set): IDs de classe à exclure, sous forme de chaînes.

    Returns:
        bool: True si le fichier a été modifié, False sinon.
    """
    try:
        with open(label_path, "r") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Erreur de lecture {label_path}: {e}")
        return False

    new_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        tokens = line.split()

        # Vérifie que la ligne contient au moins un ID
        if len(tokens) == 0:
            continue

        class_id = tokens[0]
        if class_id in excluded_ids:
            # Supprime toute la ligne si l'ID est dans la liste d'exclusion
            continue

        new_lines.append(line + "\n")

    try:
        with open(label_path, "w") as f:
            f.writelines(new_lines)
    except Exception as e:
        print(f"Erreur d'écriture dans {label_path}: {e}")
        return False

    return True

def process_labels_in_folder(base_labels_dir, excluded_ids={"0", "2", "3"}):
    """
    Traite tous les fichiers .txt dans un dossier et ses sous-dossiers,
    supprimant les lignes contenant des classes à exclure.

    Args:
        base_labels_dir (str): Dossier contenant les labels.
        excluded_ids (set): IDs à exclure.
    """
    total_files = 0
    updated_files = 0
    for root, dirs, files in os.walk(base_labels_dir):
        for file in files:
            if file.lower().endswith(".txt"):
                label_path = os.path.join(root, file)
                total_files += 1
                if update_label_file_excluding_ids(label_path, excluded_ids):
                    updated_files += 1
    print(f"\nMise à jour terminée : {updated_files} / {total_files} fichiers traités.")

if __name__ == "__main__":
    base_labels_dir = r"C:/Users/Adnan/Desktop/merged_dataset/dawn_detrac_justCar/detrac/labels"
    process_labels_in_folder(base_labels_dir, excluded_ids={"0", "2", "3"})
