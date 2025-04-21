import os

# Dossier contenant les sous-dossiers images/ et labels/ (chacun ayant train/ et val/)
base_dir = r"C:/Users/Adnan/Desktop/merged_dataset/dataset_shuffled/kitti"

def check_images_and_labels(image_folder, label_folder):
    print(f"\n--- Vérification dans {os.path.basename(image_folder)} ---")

    image_exts = {".jpg", ".jpeg", ".png", ".bmp"}
    image_files = []
    label_files = []

    for f in os.listdir(image_folder):
        if os.path.isfile(os.path.join(image_folder, f)):
            ext = os.path.splitext(f)[1].lower()
            if ext in image_exts:
                image_files.append(os.path.splitext(f)[0])

    for f in os.listdir(label_folder):
        if os.path.isfile(os.path.join(label_folder, f)) and f.lower().endswith(".txt"):
            label_files.append(os.path.splitext(f)[0])

    image_set = set(image_files)
    label_set = set(label_files)

    missing_labels = image_set - label_set
    missing_images = label_set - image_set

    if missing_labels:
        print(f"❌ Images sans annotations : {len(missing_labels)}")
        for name in sorted(missing_labels):
            print(f"  - {name}")
    else:
        print("✅ Toutes les images ont des annotations.")

    if missing_images:
        print(f"❌ Annotations sans images : {len(missing_images)}")
        for name in sorted(missing_images):
            print(f"  - {name}")
    else:
        print("✅ Toutes les annotations ont des images.")

# Vérifier pour train et val
for split in ['train', 'val']:
    image_path = os.path.join(base_dir, 'images', split)
    label_path = os.path.join(base_dir, 'labels', split)

    if os.path.exists(image_path) and os.path.exists(label_path):
        check_images_and_labels(image_path, label_path)
    else:
        print(f"⚠️ Dossier manquant pour {split} : {image_path} ou {label_path}")