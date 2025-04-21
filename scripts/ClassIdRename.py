import os
import yaml
from tqdm import tqdm  # Import tqdm for progress bars

# Base directory where your labels are
base_dir = r"C:/Users/Adnan/Desktop/resized_images_orig"
labels_dir = os.path.join(base_dir, "labels")
images_dir = os.path.join(base_dir, "images")  # assumes same structure for images

subdirs = ['train', 'val']

# Step 1: Convert all class IDs to 0 with progress bars
for subdir in subdirs:
    label_path = os.path.join(labels_dir, subdir)
    # Iterate with a progress bar for each file in the subdirectory
    
    for fname in tqdm(os.listdir(label_path), desc=f"Processing {subdir} labels", unit="file"):
        if fname.endswith(".txt"):
            file_path = os.path.join(label_path, fname)
            with open(file_path, "r") as f:
                lines = f.readlines()
            updated_lines = []
            for line in lines:
                parts = line.strip().split()
                if len(parts) >= 5:
                    parts[0] = '0'  # Set class ID to 0
                    updated_lines.append(" ".join(parts) + "\n")
            with open(file_path, "w") as f:
                f.writelines(updated_lines)

print("✅ All label files have been updated to class ID = 0")

# Step 2: Create dataset.yaml for YOLO
yaml_dict = {
    'train': os.path.join(images_dir, 'train').replace("\\", "/"),
    'val': os.path.join(images_dir, 'val').replace("\\", "/"),
    'nc': 1,
    'names': ['vehicle']
}

yaml_path = os.path.join(base_dir, "dataset_ID_0.yaml")
with open(yaml_path, "w") as yaml_file:
    yaml.dump(yaml_dict, yaml_file)

print(f"✅ dataset.yaml generated at:\n{yaml_path}")