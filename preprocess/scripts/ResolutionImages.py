import os
from PIL import Image
import matplotlib.pyplot as plt

def get_image_resolutions(images_dir, valid_ext=('.jpg', '.jpeg', '.png', '.bmp')):
    """
    Parcourt le dossier images_dir et retourne une liste de tuples (width, height)
    pour chaque image dont l'extension est dans valid_ext.
    """
    resolutions = []
    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(valid_ext)]
    for image_file in image_files:
        img_path = os.path.join(images_dir, image_file)
        try:
            with Image.open(img_path) as img:
                resolutions.append(img.size)  # (width, height)
        except Exception as e:
            print(f"Erreur lors de l'ouverture de {img_path}: {e}")
    return resolutions

def process_split(split_dir):
    """
    Pour un dossier de split ("train" ou "val"), renvoie la liste des résolutions.
    """
    resolutions = get_image_resolutions(split_dir)
    if not resolutions:
        print(f"Aucune image trouvée dans {split_dir}.")
        return None
    widths, heights = zip(*resolutions)
    return list(widths), list(heights)

def plot_statistics(widths, heights, split):
    """
    Affiche quelques visualisations pour un split donné.
    """
    min_width, max_width = min(widths), max(widths)
    min_height, max_height = min(heights), max(heights)
    print(f"\nSplit {split}:")
    print(f"  Largeur: min = {min_width}, max = {max_width}")
    print(f"  Hauteur: min = {min_height}, max = {max_height}")

    # Histogramme des largeurs
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.hist(widths, bins=20, color='skyblue', edgecolor='black')
    plt.title(f"Histogramme des largeurs ({split})")
    plt.xlabel("Largeur")
    plt.ylabel("Nombre d'images")

    # Histogramme des hauteurs
    plt.subplot(1, 2, 2)
    plt.hist(heights, bins=20, color='salmon', edgecolor='black')
    plt.title(f"Histogramme des hauteurs ({split})")
    plt.xlabel("Hauteur")
    plt.ylabel("Nombre d'images")

    plt.tight_layout()
    plt.show()

    # Scatter plot des résolutions
    plt.figure(figsize=(6, 6))
    plt.scatter(widths, heights, alpha=0.5, color='green', edgecolor='black')
    plt.title(f"Scatter plot des résolutions ({split})")
    plt.xlabel("Largeur")
    plt.ylabel("Hauteur")
    plt.grid(True)
    plt.show()

def main():
    base_images_dir = r"C:/Users/Adnan/Desktop/shuffle/dataset_merged/images"
    splits = ["train", "val"]
    
    for split in splits:
        split_dir = os.path.join(base_images_dir, split)
        if not os.path.isdir(split_dir):
            print(f"Le dossier {split_dir} n'existe pas.")
            continue
        result = process_split(split_dir)
        if result is None:
            continue
        widths, heights = result
        plot_statistics(widths, heights, split)

if __name__ == "__main__":
    main()
