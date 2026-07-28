import os
from ultralytics.utils.benchmarks import benchmark

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "models", "yolo11n.pt")

# Benchmark on GPU
benchmark(model=MODEL_PATH, data="coco8.yaml", imgsz=640, half=False, device=0)

# Benchmark specific export format
# benchmark(model=MODEL_PATH, data="coco8.yaml", imgsz=640, format="mnn")
