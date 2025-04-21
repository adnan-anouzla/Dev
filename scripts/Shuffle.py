import os
import random
import shutil

def shuffle_and_rename_split(img_dir, lbl_dir, out_img_dir, out_lbl_dir, split_name):
    os.makedirs(out_img_dir, exist_ok=True)
    os.makedirs(out_lbl_dir, exist_ok=True)

    valid_exts = {'.jpg', '.jpeg', '.png'}
    paired_files = []

    for img_file in os.listdir(img_dir):
        ext = os.path.splitext(img_file)[1].lower()
        if ext in valid_exts:
            base = os.path.splitext(img_file)[0]
            lbl_file = base + ".txt"
            img_path = os.path.join(img_dir, img_file)
            lbl_path = os.path.join(lbl_dir, lbl_file)
            if os.path.exists(lbl_path):
                paired_files.append((img_path, lbl_path))

    print(f"[{split_name.upper()}] Paires valides : {len(paired_files)}")

    random.shuffle(paired_files)

    for idx, (img_path, lbl_path) in enumerate(paired_files):
        new_name = f"{idx+1:06d}"
        img_ext = os.path.splitext(img_path)[1].lower()
        img_out_path = os.path.join(out_img_dir, new_name + img_ext)
        lbl_out_path = os.path.join(out_lbl_dir, new_name + ".txt")

        shutil.copy2(img_path, img_out_path)
        shutil.copy2(lbl_path, lbl_out_path)

    print(f"[{split_name.upper()}] ✅ Shuffle & renommage terminé.\n")

def main():
    base_input = r"C:/Users/Adnan/Desktop/merged_dataset/dataset_shuffled/kitti"
    base_output = r"C:/Users/Adnan/Desktop/merged_dataset/all_dataset_shuffled"

    for split in ["train", "val"]:
        img_in = os.path.join(base_input, "images", split)
        lbl_in = os.path.join(base_input, "labels", split)
        img_out = os.path.join(base_output, "images", split)
        lbl_out = os.path.join(base_output, "labels", split)

        shuffle_and_rename_split(img_in, lbl_in, img_out, lbl_out, split)

if __name__ == "__main__":
    main()
