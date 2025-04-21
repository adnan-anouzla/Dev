import os

def collect_unique_ids(label_dir):
    """
    Parcourt récursivement tous les fichiers .txt dans un dossier donné
    et extrait tous les IDs (le premier token de chaque ligne).

    Args:
        label_dir (str): Chemin du dossier contenant les fichiers de labels.

    Returns:
        set: Ensemble des IDs uniques (en format chaîne).
    """
    unique_ids = set()

    for root, dirs, files in os.walk(label_dir):
        for file in files:
            if file.lower().endswith(".txt"):
                label_path = os.path.join(root, file)
                try:
                    with open(label_path, "r") as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            tokens = line.split()
                            if len(tokens) >= 1:
                                class_id = tokens[0]
                                unique_ids.add(class_id)
                except Exception as e:
                    print(f"Erreur de lecture du fichier {label_path}: {e}")
    
    return unique_ids

if __name__ == "__main__":
    # Remplace ce chemin par le chemin vers ton dossier de labels
    base_labels_dir = r"C:/Users/Adnan/Desktop/c_dawn_shuffled_new\shuffled_archive/labels/train"
    ids = collect_unique_ids(base_labels_dir)
    
    if ids:
        print("IDs uniques trouvés dans les fichiers de labels :")
        print(", ".join(sorted(ids, key=int)))
    else:
        print("Aucun ID trouvé dans les fichiers de labels.")
