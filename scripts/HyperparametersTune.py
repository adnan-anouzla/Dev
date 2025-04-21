from ray import tune
from ultralytics import YOLO

# Load a pretrained model
model = YOLO("yolo11n.pt")

# Define search space
search_space = {
    "lr0": tune.uniform(1e-5, 1e-1), 
    "lrf": tune.uniform(0.01, 1.0), 
    "weight_decay": tune.uniform(0.0, 0.001), 
    "momentum": (0.6, 0.98)
}

#Fine Tune
# Run Ray Tune on the model
result_grid = model.tune(
    data= "dataset.yaml",
    epochs = 150,
    optimizer= "SGD",
    momentum= 0.9,
    space= search_space,
    use_ray=True,
    plots = False,
    save = False,
    val = False
)