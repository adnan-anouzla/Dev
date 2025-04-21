#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de validation pour YOLO11 nano

Ce script charge un modèle pré-entraîné et exécute la validation sur un dataset
défini dans un fichier YAML (par exemple, data.yaml). Il utilise l'API de la librairie
Ultralytics pour exécuter la méthode de validation.

Usage:
    python validate.py --model yolov11n.pt --data chemin/vers/data.yaml --batch 16 --imgsz 640
"""

import argparse
from ultralytics import YOLO  # Assurez-vous d'avoir installé ultralytics (pip install ultralytics)

def main(args):
    # Chargement du modèle
    print(f"Chargement du modèle {args.model}...")
    model = YOLO(args.model)

    # Lancement de la validation
    print("Démarrage de la validation...")
    # Vous pouvez préciser d'autres paramètres si nécessaire (ex: device, etc.)
    results = model.val(
        data=args.data,
        batch=args.batch,
        imgsz=args.imgsz,
        device=args.device  # par exemple, 'cpu' ou 0 pour GPU
    )

    # Affichage des résultats (les métriques typiques sont mAP, précision, rappel, etc.)
    print("\n===== Résultats de la validation =====")
    print(results)
    
    # Vous pouvez également sauvegarder ces résultats ou les exploiter pour une analyse complémentaire.
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script de validation pour YOLO11 nano")
    parser.add_argument("--model", type=str, default="yolov11n.pt", help="Chemin vers le fichier du modèle")
    parser.add_argument("--data", type=str, required=True, help="Chemin vers le fichier YAML contenant les infos du dataset (ex: data.yaml)")
    parser.add_argument("--batch", type=int, default=16, help="Taille du batch pour la validation")
    parser.add_argument("--imgsz", type=int, default=640, help="Taille des images utilisées pour la validation")
    parser.add_argument("--device", type=str, default="0", help="Numéro du GPU (ex: '0') ou 'cpu'")
    
    args = parser.parse_args()
    main(args)
