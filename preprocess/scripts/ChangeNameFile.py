import os

def rename_files_with_suffix(base_path, suffix):
    image_dirs = [
        os.path.join(base_path, "images", "train"),
        os.path.join(base_path, "images", "val")
    ]
    label_dirs = [
        os.path.join(base_path, "labels", "train"),
        os.path.join(base_path, "labels", "val")
    ]

    for img_dir, lbl_dir in zip(image_dirs, label_dirs):
        print(f"Processing directory: {img_dir}")

        for filename in os.listdir(img_dir):
            if filename.lower().endswith(".jpg"):
                base_name = os.path.splitext(filename)[0]
                new_base_name = f"{base_name}_{suffix}"

                old_img_path = os.path.join(img_dir, filename)
                new_img_path = os.path.join(img_dir, new_base_name + ".jpg")

                old_lbl_path = os.path.join(lbl_dir, base_name + ".txt")
                new_lbl_path = os.path.join(lbl_dir, new_base_name + ".txt")

                # Rename image file
                os.rename(old_img_path, new_img_path)

                # Rename label file only if it exists
                if os.path.exists(old_lbl_path):
                    os.rename(old_lbl_path, new_lbl_path)
                    print(f"Renamed: {filename} & {base_name}.txt → {new_base_name}")
                else:
                    print(f"Warning: No label file for {base_name}. Skipping label.")

    print("✅ Renaming completed.")

# === CONFIGURE HERE ===
base_folder = r"C:/Users/Adnan/Desktop/merged_dataset/dataset_shuffled/shuffled_dawn"
suffix_to_add = "dawn"

rename_files_with_suffix(base_folder, suffix_to_add)
