import os
from ultralytics import YOLO

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "models", "yolo11n.pt")

# Load a model
model = YOLO(MODEL_PATH)  # load an official model

# Export the model
model.export(format="ncnn")
