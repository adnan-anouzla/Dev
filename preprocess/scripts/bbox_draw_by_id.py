import os
import cv2

def load_yolo_labels(label_path, img_width, img_height):
    """
    Lit un fichier de labels YOLO et retourne uniquement les bounding boxes avec ID 5.
    """
    boxes = []
    try:
        with open(label_path, "r") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Erreur lors de la lecture de {label_path}: {e}")
        return boxes

    for line in lines:
        line = line.strip()
        if not line:
            continue
        tokens = line.split()
        if len(tokens) != 5:
            continue
        class_id, x_center, y_center, w, h = map(float, tokens)

        if int(class_id) != 3:
            continue  # Ignorer toutes les autres classes

        x_center_abs = x_center * img_width
        y_center_abs = y_center * img_height
        w_abs = w * img_width
        h_abs = h * img_height

        x1 = int(x_center_abs - w_abs / 2)
        y1 = int(y_center_abs - h_abs / 2)
        x2 = int(x_center_abs + w_abs / 2)
        y2 = int(y_center_abs + h_abs / 2)

        boxes.append((int(class_id), x1, y1, x2, y2))
    return boxes

def draw_bboxes(image, boxes):
    """
    Dessine les bounding boxes pour ID 5.
    """
    for (class_id, x1, y1, x2, y2) in boxes:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, str(class_id), (x1, max(y1 - 5, 0)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return image

def main():
    images_dir = r"C:/Users/Adnan/Desktop/merged_dataset/detrac/images/train"
    labels_dir = r"C:/Users/Adnan/Desktop/merged_dataset/detrac/labels/train"

    valid_ext = (".jpg", ".jpeg", ".png", ".bmp")
    all_images = [f for f in os.listdir(images_dir) if f.lower().endswith(valid_ext)]
    total = len(all_images)
    
    print(f"Nombre total d'images : {total}")
    images_with_id5 = []

    # Étape 1 : filtrer les images contenant ID 5
    for img_file in all_images:
        label_filename = os.path.splitext(img_file)[0] + ".txt"
        label_path = os.path.join(labels_dir, label_filename)
        img_path = os.path.join(images_dir, img_file)

        if not os.path.exists(label_path):
            continue

        image = cv2.imread(img_path)
        if image is None:
            continue

        height, width = image.shape[:2]
        boxes = load_yolo_labels(label_path, width, height)
        if boxes:
            images_with_id5.append((img_path, boxes))

    print(f"Images contenant ID 0 : {len(images_with_id5)}")

    # Étape 2 : affichage des images contenant l'ID 5
    for img_path, boxes in images_with_id5:
        image = cv2.imread(img_path)
        if image is None:
            continue
        image = draw_bboxes(image, boxes)
        cv2.imshow("Image - ID 0 uniquement", image)

        print(f"Affichage de {os.path.basename(img_path)} - Appuyez sur 'c' pour continuer, 'q' pour quitter.")
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()