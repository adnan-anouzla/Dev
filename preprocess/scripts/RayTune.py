from ray import tune
from ultralytics import YOLO

model = YOLO("yolo11n.pt")

result_grid = model.tune(
    data="C:/RayTuneTest/dataset.yaml",
    space={
        "lr0": tune.uniform(1e-6, 1e-1),
        "lrf": tune.uniform(0.01, 1.0),
        "momentum": tune.uniform(0.4, 0.98),
        "weight_decay": tune.uniform(0.0, 0.001),
        "mosaic": tune.uniform(0.0, 1.0),
        "mixup": tune.uniform(0.0, 1.0),
    },
    epochs=150,
    use_ray=True
)