from ultralytics import YOLO
import cv2
from severity import get_severity
from logger import log_violation

model = YOLO("yolov8n.pt")
cap = cv2.VideoCapture("Traphic.mp4")

violation_logged = False  # to avoid logging same violation repeatedly

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, imgsz=640, conf=0.4, verbose=False)

    bike_found = False
    person_found = False

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]

            if label == "motorbike":
                bike_found = True
            elif label == "person":
                person_found = True

    # Heuristic violation condition
    if bike_found and person_found and not violation_logged:
        violation_type = "no_helmet"
        severity = get_severity(violation_type)

        # Dummy plate for now (OCR comes later)
        plate_number = "UP32XX0000"

        log_violation(plate_number, violation_type)

        violation_logged = True

        cv2.putText(
            frame,
            f"VIOLATION: {violation_type.upper()} ({severity})",
            (40, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    cv2.imshow("Traffic Violation Pipeline", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
