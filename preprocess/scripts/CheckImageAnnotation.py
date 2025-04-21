import os
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2

def load_yolo_labels(label_path, img_width, img_height):
    boxes = []
    try:
        with open(label_path, "r") as f:
            lines = f.readlines()
        for line in lines:
            tokens = line.strip().split()
            if len(tokens) == 5:
                class_id, x_center, y_center, w, h = map(float, tokens)
                x_center_abs = x_center * img_width
                y_center_abs = y_center * img_height
                w_abs = w * img_width
                h_abs = h * img_height
                x1 = int(x_center_abs - w_abs / 2)
                y1 = int(y_center_abs - h_abs / 2)
                x2 = int(x_center_abs + w_abs / 2)
                y2 = int(y_center_abs + h_abs / 2)
                boxes.append((int(class_id), x1, y1, x2, y2))
    except Exception as e:
        print(f"Erreur lecture {label_path}: {e}")
    return boxes

def draw_bboxes_opencv(image_path, label_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"⚠️ Image non chargée : {image_path}")
        return None
    h, w = image.shape[:2]
    boxes = load_yolo_labels(label_path, w, h) if os.path.exists(label_path) else []

    for (class_id, x1, y1, x2, y2) in boxes:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, str(class_id), (x1, max(y1 - 5, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

class ImageReviewer:
    def __init__(self, images_dir, labels_dir, deleted_images_dir, deleted_labels_dir):
        self.images_dir = images_dir
        self.labels_dir = labels_dir
        self.deleted_images_dir = deleted_images_dir
        self.deleted_labels_dir = deleted_labels_dir
        self.valid_ext = (".jpg", ".jpeg", ".png", ".bmp")

        os.makedirs(deleted_images_dir, exist_ok=True)
        os.makedirs(deleted_labels_dir, exist_ok=True)

        self.images = sorted([
            f for f in os.listdir(images_dir)
            if f.lower().endswith(self.valid_ext)
        ])

        if not self.images:
            print("❌ Aucun fichier image trouvé dans :", images_dir)
            return

        self.index = 0
        self.root = tk.Tk()
        self.root.title("Revue des Images")

        self.canvas = tk.Label(self.root)
        self.canvas.pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack()

        tk.Button(button_frame, text="✅ Garder", width=20, command=self.keep_image).pack(side="left", padx=20)
        tk.Button(button_frame, text="🗑️ Supprimer", width=20, command=self.delete_image).pack(side="right", padx=20)

        self.root.bind("<Right>", lambda e: self.keep_image())
        self.root.bind("<Left>", lambda e: self.delete_image())

        self.tk_img = None
        self.show_image()
        self.root.mainloop()

    def show_image(self):
        if self.index >= len(self.images):
            messagebox.showinfo("Fini", "Toutes les images ont été traitées.")
            self.root.quit()
            return

        img_name = self.images[self.index]
        img_path = os.path.join(self.images_dir, img_name)
        label_path = os.path.join(self.labels_dir, os.path.splitext(img_name)[0] + ".txt")

        print(f"➡️ Chargement image : {img_path}")
        image_rgb = draw_bboxes_opencv(img_path, label_path)
        if image_rgb is None:
            print(f"❌ Problème d'image : {img_name}")
            self.index += 1
            self.show_image()
            return

        pil_img = Image.fromarray(image_rgb).resize((900, 550), Image.Resampling.LANCZOS
)
        self.tk_img = ImageTk.PhotoImage(pil_img)
        self.canvas.config(image=self.tk_img)
        self.root.title(f"{img_name} [{self.index + 1}/{len(self.images)}]")

    def keep_image(self):
        self.index += 1
        self.show_image()

    def delete_image(self):
        img_name = self.images[self.index]
        img_path = os.path.join(self.images_dir, img_name)
        label_name = os.path.splitext(img_name)[0] + ".txt"
        label_path = os.path.join(self.labels_dir, label_name)

        shutil.move(img_path, os.path.join(self.deleted_images_dir, img_name))
        if os.path.exists(label_path):
            shutil.move(label_path, os.path.join(self.deleted_labels_dir, label_name))

        print(f"🗑️ Supprimé : {img_name}")
        self.index += 1
        self.show_image()

# === Exécution principale ===
if __name__ == "__main__":
    images_dir = r"C:/Users/Adnan/Desktop/merged_dataset/all_dataset/kitti/images/train"
    labels_dir = r"C:/Users/Adnan/Desktop/merged_dataset/all_dataset/kitti/labels/train"
    deleted_images_dir = r"C:/Users/Adnan/Desktop/deleted/kitti/images/train"
    deleted_labels_dir = r"C:/Users/Adnan/Desktop/deleted/kitti/labels/train"

    ImageReviewer(images_dir, labels_dir, deleted_images_dir, deleted_labels_dir)
