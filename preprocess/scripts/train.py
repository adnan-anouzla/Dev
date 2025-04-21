from ultralytics import YOLO

# Load a pretrained model
model = YOLO("yolo11n.pt")

# Link: https://www.swisstransfer.com/d/71e730f9-84ba-4533-b197-815af0edfb85
# Train the model on your custom dataset
model.train(data="dataset.yaml", 
            epochs= 150, 
            imgsz= 640, 
            batch = 16, 
            device = 0, 
            lr0 = 0.005, # Compromis entre 0.01 et 0.001 pour une convergence stable sans risque de divergence trop agressive. 0.001 trés stable mais la convergence est très lente. 0.01 Convergence rapide mais risque d'oscilation
            lrf = 0.01 ,  # Réduit fotement le lr en fin de training, mais peut rendre le taux final trop faible et stopper learning en phase finale 
            optimizer = "SGD", # Bonne généralisation et une stabilité pour gros dataset, mais nécessite un tuning comme l'ajout de momentum et peut conveger lentement
            momentum = 0.937, 
            weight_decay =0.0005, # 0.001 renforce la régularisation qui est utile pour nano, mais peut introduire underfitting en cas de régularisation trop forte 
            augment = True,
            mosaic=0.5, 
            scale=0.3,
            mixup=0.2, 
            patience=20, 
            freeze=0,
 )


"""
mosaic=0.5–1.0 : mélange de 4 images, très utile pour casser la structure de l’image.

mixup=0.2–0.3 : mélange pixel à pixel de 2 images → force le modèle à être robuste à du bruit de fond.

scale=0.4, translate=0.1–0.2, shear=2–5 : simule du zoom, des translations latérales, etc.

perspective=0.001–0.01 : ajoute un effet de parallaxe pour simuler des angles.

🎨 Colorimétriques :
hsv_h=0.015, hsv_s=0.7, hsv_v=0.4 : pour changer la teinte et les contrastes.

random brightness/contrast ou CLAHE (amélioration locale de contraste adaptatif).

Inversion canal (BGR->RGB) sur une fraction."""