import os
import cv2
import random

def load_yolo_labels(label_path, img_width, img_height):
    """
    Lit le fichier de label au format YOLO et retourne une liste de bounding boxes.
    Chaque ligne du fichier doit être dans le format :
      class_id x_center y_center width height
    Les valeurs x_center, y_center, width et height sont normalisées par rapport aux dimensions de l'image.
    
    Retourne une liste de tuples : (class_id, x1, y1, x2, y2)
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
        # Convertir les valeurs normalisées en coordonnées absolues
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
    Dessine les bounding boxes sur l'image.
    Chaque bbox est dessinée en vert et le numéro de classe est affiché en haut.
    """
    for (class_id, x1, y1, x2, y2) in boxes:
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, str(class_id), (x1, max(y1 - 5, 0)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    return image

def main():
    # Chemins vers les dossiers images et labels
    images_dir = r"C:/Users/Adnan/Desktop/detrac_dawn_justCar_New/detrac/images/val"  # Par exemple pour train
    labels_dir = r"C:/Users/Adnan/Desktop/detrac_dawn_justCar_New/detrac/labels/val"
    ""
    
    # Récupérer la liste de toutes les images (extensions supportées)
    valid_ext = (".jpg", ".jpeg", ".png", ".bmp")
    all_images = [f for f in os.listdir(images_dir) if f.lower().endswith(valid_ext)]
    
    if not all_images:
        print(f"Aucune image trouvée dans {images_dir}")
        return

    # Mélange de la liste (optionnel puisque nous choisirons aléatoirement par batch)
    random.shuffle(all_images)
    
    batch_size = 100
    start_index = 0
    total = len(all_images)
    
    print(f"Nombre total d'images : {total}")
    
    while start_index < total:
        end_index = start_index + batch_size
        batch = all_images[start_index:end_index]
        print(f"\nAffichage des images {start_index + 1} à {min(end_index, total)} sur {total}")
        for img_file in batch:
            img_path = os.path.join(images_dir, img_file)
            # Construire le chemin du fichier de labels correspondant (même base, extension .txt)
            label_filename = os.path.splitext(img_file)[0] + ".txt"
            label_path = os.path.join(labels_dir, label_filename)
            
            image = cv2.imread(img_path)
            if image is None:
                print(f"Erreur de chargement de l'image: {img_path}")
                continue
            
            height, width = image.shape[:2]
            if os.path.exists(label_path):
                boxes = load_yolo_labels(label_path, width, height)
                image = draw_bboxes(image, boxes)
            else:
                print(f"Aucun label trouvé pour {img_file}")
            
            cv2.imshow("Image avec BBoxes", image)
            # Attendre que l'utilisateur appuie sur une touche pour passer à l'image suivante.
            # Appuyer sur 'q' pour quitter.
            key = cv2.waitKey(0) & 0xFF
            if key == ord("q"):
                cv2.destroyAllWindows()
                return
        start_index += batch_size
        print("Batch terminé. Appuyez sur 'c' pour continuer ou 'q' pour quitter.")
        key = cv2.waitKey(0) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
