import os

def delete_from_val_dirs(ref_image_dir, ref_label_dir, target_image_dir, target_label_dir):
    deleted = 0
    skipped = 0

    # Collecter les noms de base à supprimer (sans extension)
    ref_image_names = {
        os.path.splitext(f)[0] for f in os.listdir(ref_image_dir)
        if os.path.isfile(os.path.join(ref_image_dir, f))
    }
    ref_label_names = {
        os.path.splitext(f)[0] for f in os.listdir(ref_label_dir)
        if os.path.isfile(os.path.join(ref_label_dir, f))
    }

    to_delete = ref_image_names.union(ref_label_names)
    print(f"🗂️ Total à supprimer (basé sur noms) : {len(to_delete)}")

    for name in sorted(to_delete):
        deleted_this = False

        # Supprimer image si elle existe
        for ext in ['.jpg', '.jpeg', '.png']:
            img_path = os.path.join(target_image_dir, name + ext)
            if os.path.exists(img_path):
                os.remove(img_path)
                print(f"🗑️ Image supprimée : {img_path}")
                deleted_this = True
                break  # Ne pas supprimer plusieurs extensions à la fois

        # Supprimer le label
        lbl_path = os.path.join(target_label_dir, name + ".txt")
        if os.path.exists(lbl_path):
            os.remove(lbl_path)
            print(f"🗑️ Label supprimé : {lbl_path}")
            deleted_this = True

        if deleted_this:
            deleted += 1
        else:
            skipped += 1
            print(f"❓ Introuvable : {name}")

    print(f"\n✅ Terminé : {deleted} supprimés, {skipped} introuvables.")

# === Chemins à configurer ===
ref_image_dir = r"C:/Users/Adnan/Desktop/c_dawn_shuffled_new/shuffled_archive/images/train"
ref_label_dir = r"C:/Users/Adnan/Desktop/c_dawn_shuffled_new/shuffled_archive/images/train"

target_image_dir = r"C:/Users\Adnan\Desktop\detrac_dawn_justCar_New/archive/images/val"
target_label_dir = r"C:/Users\Adnan\Desktop\detrac_dawn_justCar_New/archive/labels/val"

delete_from_val_dirs(ref_image_dir, ref_label_dir, target_image_dir, target_label_dir)
