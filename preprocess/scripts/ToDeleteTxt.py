import os

def delete_val_files_from_list(list_file_path, base_path):
    with open(list_file_path, 'r') as f:
        filenames = [line.strip() for line in f if line.strip()]

    image_val_dir = os.path.join(base_path, "images", "val")
    label_val_dir = os.path.join(base_path, "labels", "val")

    for name in filenames:
        img_path = os.path.join(image_val_dir, f"{name}.jpg")
        lbl_path = os.path.join(label_val_dir, f"{name}.txt")

        if os.path.exists(img_path):
            os.remove(img_path)
            print(f"🗑️ Deleted image: {img_path}")
        else:
            print(f"❌ Image not found: {img_path}")

        if os.path.exists(lbl_path):
            os.remove(lbl_path)
            print(f"🗑️ Deleted label: {lbl_path}")
        else:
            print(f"❌ Label not found: {lbl_path}")

    print("✅ Deletion from val complete.")

# === À MODIFIER ICI ===
list_file = r"C:/Users/Adnan/Desktop/merged_dataset/dataset_shuffled/images_sans_label.txt"
dataset_path = r"C:/Users/Adnan/Desktop/merged_dataset/dataset_shuffled/kitti"

delete_val_files_from_list(list_file, dataset_path)
