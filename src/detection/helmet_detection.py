from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture("Traphic.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, imgsz=640, conf=0.3, verbose=False)

    helmet_found = False
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
            elif label == "helmet":
                helmet_found = True

    if bike_found and person_found and not helmet_found:
        cv2.putText(
            frame,
            "VIOLATION: NO HELMET",
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    cv2.imshow("Helmet Detection", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
