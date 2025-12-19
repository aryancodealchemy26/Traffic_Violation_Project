from ultralytics import YOLO
import cv2
import easyocr
import re
import numpy as np

model = YOLO("yolov8n.pt")
reader = easyocr.Reader(['en'], gpu=False)

cap = cv2.VideoCapture("Traphic.mp4")

def preprocess_plate(plate):
    # Convert to grayscale
    gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)

    # Increase contrast
    gray = cv2.equalizeHist(gray)

    # Reduce noise
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Adaptive threshold
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11, 2
    )

    return thresh


def extract_plate_text(plate_img):
    results = reader.readtext(
        plate_img,
        allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    )

    for (_, text, prob) in results:
        text = text.replace(" ", "").upper()

        # Indian plate loose pattern
        if len(text) >= 8:
            return text

    return None


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, imgsz=640, conf=0.4, verbose=False)

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label not in ["car", "motorbike"]:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            vehicle = frame[y1:y2, x1:x2]

            if vehicle.size == 0:
                continue

            h, w, _ = vehicle.shape

            # Bottom-central region (plate zone)
            plate_region = vehicle[int(h*0.65):h, int(w*0.2):int(w*0.8)]

            if plate_region.size == 0:
                continue

            processed_plate = preprocess_plate(plate_region)
            plate_text = extract_plate_text(processed_plate)

            # Show plate region for debugging (VERY IMPORTANT)
            cv2.imshow("Plate ROI", processed_plate)

            if plate_text:
                cv2.putText(
                    frame,
                    f"Plate: {plate_text}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2
                )

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow("Plate Recognition", frame)

    if cv2.waitKey(15) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
