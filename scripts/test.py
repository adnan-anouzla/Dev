import lap
import numpy as np
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

#results = model.predict(source = 'C:/Users/Adnan/Desktop/T/1.jpg', show = True, save = True)
#results = model.predict(source = "C:/Users/Adnan/Desktop/T/2.mp4", show = True)
import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Webcam non accessible")
else:
    print("✅ Webcam OK")
    ret, frame = cap.read()
    if ret:
        cv2.imshow("Test", frame)
        cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()
