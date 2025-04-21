import cv2
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
import numpy as np
# Paramètres
MODEL_PATH = "C:/Users/Adnan/Desktop/yolo-models/yolo11n-vehicles.pt"  
INPUT_VIDEO = "C:/Users/Adnan/Desktop/test/7.mp4"  
OUTPUT_VIDEO = "C:/Users/Adnan/Desktop/test/7_ours.mp4"
 
# Charger le modèle YOLO
model = YOLO(MODEL_PATH)
 
# Ouvrir la source vidéo
cap = cv2.VideoCapture(INPUT_VIDEO)
if not cap.isOpened():
    print(f"Erreur: impossible d'ouvrir {INPUT_VIDEO}")
    exit(1)
 
# Récupérer les dimensions de la vidéo
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
 
# Préparer l’enregistrement de la sortie
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, fps, (width, height))
 
# Variables pour le clignotement de la bordure d'alerte
frame_count = 0
blink_period = 20         # Nombre de frames pour un cycle complet
blink_on_duration = 10    # Nombre de frames pendant lesquelles la bordure est affichée
 
while True:
    ret, frame = cap.read()
    if not ret:
        break
 
    # Exécution de YOLO sur la frame
    results = model.track(source=frame, conf=0.4, iou=0.5, persist=True, device=0, max_det=500)
 
    # Créer l'annotateur pour dessiner sur la frame
    annotator = Annotator(frame, line_width=2, example=model.names)
   
    # Pour chaque détection, dessiner la bounding box en rouge
    if len(results) > 0 and hasattr(results[0], 'boxes') and results[0].boxes is not None:
        for box in results[0].boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            bbox = list(map(int, box.xyxy[0]))  # Format xyxy
            label = f"{model.names[cls]} {conf:.2f}"
            # Dessiner la bounding box en rouge pur
            annotator.box_label(bbox, label, color=(0, 0, 255))
   
    # Obtenir la frame annotée
    frame = annotator.result()
 
    # Ajouter une ligne rouge clignotante sur le contour de la vidéo
    #if (frame_count % blink_period) < blink_on_duration:
    #   cv2.rectangle(frame, (0, 0), (width - 1, height - 1), (0, 0, 255), 20)
 
   
    # Afficher la vidéo en direct et enregistrer la frame annotée
    cv2.imshow("YOLO", frame)
    out.write(frame)
   
    #frame_count += 1
 
    # Quitter avec 'q' ou 'ESC'
    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break
 
# Libérer les ressources
cap.release()
out.release()
cv2.destroyAllWindows()
print("Vidéo enregistrée :", OUTPUT_VIDEO) 
 