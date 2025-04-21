import os
import time
from PIL import Image
from tqdm import tqdm  # barre de progression

# Dossier source
source_dir = r"C:/Users/Adnan/Desktop/ATNa/dataset/vehicles/UA_DETRAC_Copie/content/UA-DETRAC/DETRAC_Upload/images/"

# Dossier destination
output_dir = r"C:/Users/Adnan/Desktop/resized_960_544"

# Dimensions cibles
target_size = (960, 544)

# Récupérer toutes les images à traiter
image_exts = (".jpg", ".jpeg", ".png", ".bmp")
image_paths = []
for root, dirs, files in os.walk(source_dir):
    for file in files:
        if file.lower().endswith(image_exts):
            full_path = os.path.join(root, file)
            image_paths.append(full_path)

# Traitement avec barre de progression
start_time = time.time()
for img_path in tqdm(image_paths, desc="🔄 Redimensionnement en cours"):
    relative_path = os.path.relpath(img_path, source_dir)
    output_path = os.path.join(output_dir, relative_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with Image.open(img_path) as img:
            resized_img = img.resize(target_size, Image.LANCZOS)
            resized_img.save(output_path)
    except Exception as e:
        print(f"❌ Erreur avec {img_path} : {e}")

elapsed_time = time.time() - start_time
print(f"\n✅ {len(image_paths)} images redimensionnées en {elapsed_time:.2f} secondes.")
