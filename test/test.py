import cv2
from ultralytics import YOLO
from pathlib import Path
import os

# ==========================
# CONFIG
# ==========================

MODEL_PATH = "best.pt"

IMAGE_FOLDER = "input"

OUTPUT_FOLDER = "output"

CONFIDENCE = 0.25

# ==========================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

model = YOLO(MODEL_PATH)

images = []

for ext in ["*.jpg", "*.jpeg", "*.png", "*.bmp"]:
    images.extend(Path(IMAGE_FOLDER).glob(ext))

print(f"Found {len(images)} images")

cv2.namedWindow("TrafficIQ Detection", cv2.WINDOW_NORMAL)

for image_path in images:

    image = cv2.imread(str(image_path))

    results = model.predict(
        image,
        conf=CONFIDENCE,
        verbose=False
    )

    result = results[0]

    # Draw bounding boxes
    annotated = result.plot()

    # Number of detections
    total = len(result.boxes)

    # Draw total count
    cv2.putText(
        annotated,
        f"Detections : {total}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    print(f"\n{image_path.name}")
    print("-"*40)

    for box in result.boxes:

        cls = int(box.cls)

        conf = float(box.conf)

        name = model.names[cls]

        print(f"{name:<15} {conf:.2f}")

    save_path = os.path.join(
        OUTPUT_FOLDER,
        image_path.name
    )

    cv2.imwrite(save_path, annotated)

    cv2.imshow("TrafficIQ Detection", annotated)

    key = cv2.waitKey(0)

    # ESC quits
    if key == 27:
        break

cv2.destroyAllWindows()