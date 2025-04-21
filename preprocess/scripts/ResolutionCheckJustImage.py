import os
import random
from PIL import Image

# Dossier contenant les images modifiées
base_dir = r"C:/Users/Adnan/Desktop/resized_images"

# Extensions d'images acceptées
image_exts = {".jpg", ".jpeg", ".png", ".bmp"}

# Rassembler toutes les images disponibles dans train et val
all_images = []

for subfolder in ['train', 'val']:
    folder_path = os.path.join(base_dir, subfolder)
    if not os.path.exists(folder_path):
        print(f"⚠️ Le dossier {folder_path} n'existe pas.")
        continue

    for filename in os.listdir(folder_path):
        if os.path.splitext(filename)[1].lower() in image_exts:
            all_images.append(os.path.join(folder_path, filename))

# Sélectionner et afficher une image aléatoire
if all_images:
    image_path = random.choice(all_images)
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            print(f"📸 Image sélectionnée : {image_path}")
            print(f"📏 Résolution : {width} x {height}")
    except Exception as e:
        print(f"❌ Erreur lors de l'ouverture de l'image : {e}")
else:
    print("❌ Aucune image trouvée dans les dossiers.")
