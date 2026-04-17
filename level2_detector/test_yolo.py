from ultralytics import YOLO
import cv2

# Load pretrained YOLO model
model = YOLO("best.pt")   # nano version (fast)

# Test image
image_path = "test.png"  # put any garbage image here

# Run detection
results = model(image_path)

# Get result image with boxes drawn
annotated_frame = results[0].plot()

# Show result
cv2.imshow("Detection", annotated_frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print object details
for box in results[0].boxes:
    cls_id = int(box.cls[0])
    label = model.names[cls_id]
    confidence = float(box.conf[0])
    coords = box.xyxy[0].tolist()

    print(label, confidence)

    print(f"Object: {label}")
    print(f"Confidence: {confidence:.2f}")
    print(f"Bounding Box: {coords}")
    print("------")