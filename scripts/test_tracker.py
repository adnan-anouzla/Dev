from ultralytics import YOLO

# Load an official or custom model
model = YOLO("yolo11n.pt")  # Load an official Detect model


# Perform tracking with the model

results = model.track(source ='C:/Users/Adnan/Downloads/1.mp4', show=True, tracker="C:/Users/Adnan/Downloads/bytetrack_vehicle_config.yaml")  # with ByteTrack