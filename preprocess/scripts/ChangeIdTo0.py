import os
from tqdm import tqdm

def update_label_file(label_path):
    """
    Met à jour un fichier de labels YOLO en remplaçant l'ID de classe par "0" sur chaque ligne.
    """
    try:
        with open(label_path, "r") as fin:
            lines = fin.readlines()
    except Exception as e:
        print(f"Erreur lors de la lecture de {label_path}: {e}")
        return False

    updated_lines = []
    for line in lines:
        line = line.strip()
        if line == "":
            continue
        tokens = line.split()
        if tokens:
            tokens[0] = "0"
        updated_lines.append(" ".join(tokens) + "\n")
    
    try:
        with open(label_path, "w") as fout:
            fout.writelines(updated_lines)
        return True
    except Exception as e:
        print(f"Erreur lors de l'écriture dans {label_path}: {e}")
        return False

def process_labels(kitti_base_dir):
    """
    Parcourt les fichiers de labels dans kitti/labels/train et kitti/labels/val
    et applique la mise à jour.
    """
    splits = ["train", "val"]
    total_files = 0
    updated_files = 0

    for split in splits:
        split_label_path = os.path.join(kitti_base_dir, "labels", split)
        if not os.path.isdir(split_label_path):
            print(f"Le dossier {split_label_path} n'existe pas.")
            continue

        label_files = [f for f in os.listdir(split_label_path) if f.lower().endswith(".txt")]
        print(f"\n🔧 Traitement du dossier : {split_label_path} ({len(label_files)} fichiers)")

        for label_file in tqdm(label_files, desc=f"Traitement {split}"):
            label_path = os.path.join(split_label_path, label_file)
            total_files += 1
            if update_label_file(label_path):
                updated_files += 1

    print(f"\n✅ Mise à jour terminée : {updated_files} / {total_files} fichiers de labels modifiés.")

if __name__ == "__main__":
    # Dossier "kitti" contenant "labels/train" et "labels/val"
    kitti_base_dir = r"C:/Users/Adnan/Desktop/merged_dataset/dataset_shuffled/kitti"
    process_labels(kitti_base_dir)
