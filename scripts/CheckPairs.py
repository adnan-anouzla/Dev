import os

# Dossier contenant les images modifiées (avec sous-dossiers train/ et val/)
base_dir = r"C:/Users/Adnan/Desktop/dataset_merged/images"

def check_images_and_labels(folder):
    print(f"\n--- Vérification dans {folder} ---")
    
    image_exts = {".jpg", ".jpeg", ".png", ".bmp"}
    image_files = []
    label_files = []

    for f in os.listdir(folder):
        if os.path.isfile(os.path.join(folder, f)):
            ext = os.path.splitext(f)[1].lower()
            if ext in image_exts:
                image_files.append(os.path.splitext(f)[0])
            elif ext == ".txt":
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

# Vérifier train et val
for subfolder in ['train', 'val']:
    folder_path = os.path.join(base_dir, subfolder)
    if os.path.exists(folder_path):
        check_images_and_labels(folder_path)
    else:
        print(f"⚠️ Le dossier {folder_path} n'existe pas.")
