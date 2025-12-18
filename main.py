# from ultralytics import YOLO

# # Load YOLOv8 nano model (fast & lightweight)
# model = YOLO("yolov8n.pt")

# # Run detection on video
# model("traffic.mp4", show=True)
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model(
    "Traphic.mp4",
    show=True,
    imgsz=640,      # force proper scaling
    conf=0.25       # confidence threshold
)
