import os
from PIL import Image
from collections import defaultdict

# Dossier contenant les images modifiées
base_dir = r"C:/Users/Adnan/Desktop/resized_images"

# Extensions d'images acceptées
image_exts = {".jpg", ".jpeg", ".png", ".bmp"}

# Stocker les résolutions
resolutions = defaultdict(list)

# Parcours des dossiers train et val
for subfolder in ['train', 'val']:
    folder_path = os.path.join(base_dir, subfolder)
    if not os.path.exists(folder_path):
        print(f"⚠️ Le dossier {folder_path} n'existe pas.")
        continue

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext in image_exts:
            try:
                with Image.open(filepath) as img:
                    size = img.size  # (width, height)
                    resolutions[size].append(filename)
            except Exception as e:
                print(f"Erreur lors de l'ouverture de {filename} : {e}")

# Affichage des résultats
print("\n📏 Résolutions détectées :")
for res, files in resolutions.items():
    print(f"- {res[0]}x{res[1]} : {len(files)} images")

if len(resolutions) == 1:
    print("\n✅ Toutes les images ont la même résolution.")
else:
    print("\n❗ Certaines images ont des résolutions différentes.")
