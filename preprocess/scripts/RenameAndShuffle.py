import os
import random
import shutil
import argparse
from tqdm import tqdm  # For progress tracking

def update_label_class_ids(src_label_path, dst_label_path):
    """
    Reads the label file from src_label_path, updates the first token (class ID)
    in each non-empty line to "0", and writes the updated lines to dst_label_path.
    
    Assumes that each line is whitespace-separated and that the class ID is the first token.
    """
    try:
        with open(src_label_path, "r") as fin:
            lines = fin.readlines()
    except Exception as e:
        print(f"Error reading {src_label_path}: {e}")
        return

    updated_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        tokens = line.split()
        if tokens:
            tokens[0] = "0"  # Replace the class ID with "0"
        updated_lines.append(" ".join(tokens) + "\n")
    
    try:
        with open(dst_label_path, "w") as fout:
            fout.writelines(updated_lines)
    except Exception as e:
        print(f"Error writing to {dst_label_path}: {e}")

def process_split(split, base_dir, dest_base, image_ext, label_ext):
    """
    Processes a given dataset split by shuffling, renaming, copying images,
    and updating the corresponding label files.
    """
    # Construct source directories for images and labels for the current split.
    src_image_dir = os.path.join(base_dir, "images", split)
    src_label_dir = os.path.join(base_dir, "labels", split)
    
    # Get list of image files with the provided extension.
    image_files = [f for f in os.listdir(src_image_dir) if f.endswith(image_ext)]
    if not image_files:
        print(f"No images found in {src_image_dir} with extension {image_ext}.")
        return
    
    # Shuffle the image list to randomize sequential frames.
    random.shuffle(image_files)
    
    # Create destination directories for images and labels.
    dest_image_dir = os.path.join(dest_base, "images", split)
    dest_label_dir = os.path.join(dest_base, "labels", split)
    os.makedirs(dest_image_dir, exist_ok=True)
    os.makedirs(dest_label_dir, exist_ok=True)
    
    # Loop through files with a progress bar.
    for idx, image in enumerate(tqdm(image_files, desc=f"Processing {split} images"), start=1):
        # Create new sequential filename with zero padding (e.g. 00001.jpg).
        new_filename = f"{idx:05d}{image_ext}"
        src_image_path = os.path.join(src_image_dir, image)
        dst_image_path = os.path.join(dest_image_dir, new_filename)
        shutil.copy(src_image_path, dst_image_path)
        
        # Process the corresponding label file.
        base_name = os.path.splitext(image)[0]
        src_label_path = os.path.join(src_label_dir, base_name + label_ext)
        dst_label_path = os.path.join(dest_label_dir, f"{idx:05d}{label_ext}")
        if os.path.exists(src_label_path):
            update_label_class_ids(src_label_path, dst_label_path)
        else:
            print(f"Warning: No label found for image {image} at {src_label_path}.")
    
    print(f"Processed {len(image_files)} images for split: {split}")

def main():
    parser = argparse.ArgumentParser(
        description="Shuffle, rename, and update dawn dataset images and labels."
    )
    parser.add_argument(
        "--base_dir",
        type=str,
        default=r"C:/Users/Adnan/Desktop/merged_dataset/dataset_shuffled/kitti",
        help="Base directory of the dawn dataset."
    )
    parser.add_argument(
        "--dest_dir",
        type=str,
        default="shuffled_dawn",
        help="Name of the destination directory (created next to the base directory) for the shuffled dataset."
    )
    parser.add_argument(
        "--image_ext",
        type=str,
        default=".jpg",
        help="Extension for image files (e.g., .jpg, .png)."
    )
    parser.add_argument(
        "--label_ext",
        type=str,
        default=".txt",
        help="Extension for label files (e.g., .txt)."
    )
    args = parser.parse_args()

    # Create the destination base directory one level up from the base_dir.
    # This will result in a structure similar to:
    #   (parent of base_dir)/dawn/{images, labels}/(train, val)
    base_dir_abs = os.path.abspath(args.base_dir)
    parent_dir = os.path.dirname(base_dir_abs)
    dest_base = os.path.join(parent_dir, args.dest_dir)
    os.makedirs(dest_base, exist_ok=True)
    
    # Process both 'train' and 'val' splits.
    for split in ["train", "val"]:
        process_split(split, base_dir_abs, dest_base, args.image_ext, args.label_ext)
    
    print(f"\nShuffled and updated dataset has been saved to: {dest_base}")

if __name__ == "__main__":
    main()