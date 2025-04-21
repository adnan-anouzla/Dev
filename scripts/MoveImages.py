import os
import shutil

def move_images_and_labels(base_dir, count=1000):
    img_train_dir = os.path.join(base_dir, "images", "train")
    img_val_dir   = os.path.join(base_dir, "images", "val")
    lbl_train_dir = os.path.join(base_dir, "labels", "train")
    lbl_val_dir   = os.path.join(base_dir, "labels", "val")

    # Créer les dossiers val s’ils n’existent pas
    os.makedirs(img_val_dir, exist_ok=True)
    os.makedirs(lbl_val_dir, exist_ok=True)

    # Obtenir et trier les images
    valid_ext = (".jpg", ".jpeg", ".png", ".bmp")
    images = sorted([f for f in os.listdir(img_train_dir) if f.lower().endswith(valid_ext)])

    if len(images) < count:
        print(f"❗ Seulement {len(images)} images disponibles, déplacement de toutes.")
        count = len(images)

    selected_images = images[:count]
    print(f"➡️ Déplacement de {count} images de train vers val...")

    for img_name in selected_images:
        base_name, _ = os.path.splitext(img_name)
        label_name = base_name + ".txt"

        src_img = os.path.join(img_train_dir, img_name)
        dst_img = os.path.join(img_val_dir, img_name)
        shutil.move(src_img, dst_img)

        src_lbl = os.path.join(lbl_train_dir, label_name)
        dst_lbl = os.path.join(lbl_val_dir, label_name)
        if os.path.exists(src_lbl):
            shutil.move(src_lbl, dst_lbl)
        else:
            print(f"⚠️ Annotation manquante pour : {img_name}")

    print("✅ Déplacement terminé.")

if __name__ == "__main__":
    base_dataset_dir = r"C:\Users\Adnan\Desktop\deleted\all_dataset\detrac"
    move_images_and_labels(base_dataset_dir, count=1000)
