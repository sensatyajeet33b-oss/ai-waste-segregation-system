# import cv2
# import numpy as np
# import tensorflow as tf
# from ultralytics import YOLO
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# # ==============================
# # Load Models
# # ==============================

# yolo_model = YOLO("yolov8m.pt")

# waste_model = tf.keras.models.load_model(
#     "../level1_classifier/model/dry_wet_model.keras"
# )
# # waste_model = tf.keras.models.load_model(
# #     "../model_training/dry_wet_model.keras"
# # )

# IMG_SIZE = 160
# CONF_THRESHOLD = 0.25
# PADDING_RATIO = 0.15  # 15% padding

# # ==============================
# # RULE-BASED MAPPING
# # ==============================

# WET_CLASSES = {
#     "banana", "apple", "orange", "sandwich",
#     "broccoli", "carrot", "hot dog",
#     "pizza", "donut", "cake"
# }

# DRY_CLASSES = {
#     "bottle", "cup", "wine glass", "fork",
#     "knife", "spoon", "bowl", "chair",
#     "tv", "laptop", "mouse", "remote",
#     "keyboard", "cell phone", "refrigerator"
# }

# # ==============================
# # Helper: Add Padding
# # ==============================

# def add_padding(x1, y1, x2, y2, img_shape):
#     h, w = img_shape[:2]

#     box_width = x2 - x1
#     box_height = y2 - y1

#     pad_x = int(box_width * PADDING_RATIO)
#     pad_y = int(box_height * PADDING_RATIO)

#     x1 = max(0, x1 - pad_x)
#     y1 = max(0, y1 - pad_y)
#     x2 = min(w, x2 + pad_x)
#     y2 = min(h, y2 + pad_y)

#     return x1, y1, x2, y2


# # ==============================
# # Hybrid Detection
# # ==============================

# def detect_and_classify(image_path):

#     image = cv2.imread(image_path)

#     if image is None:
#         raise ValueError("Image not found or invalid path.")

#     original = image.copy()
#     h, w = original.shape[:2]

#     results = yolo_model(image, conf=0.2, iou=0.5, imgsz=800)

#     output_objects = []

#     for box in results[0].boxes:

#         confidence = float(box.conf[0])
#         if confidence < CONF_THRESHOLD:
#             continue

#         cls_id = int(box.cls[0])
#         label = yolo_model.names[cls_id]

#         x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

#         # Add padding safely
#         x1, y1, x2, y2 = add_padding(x1, y1, x2, y2, original.shape)

#         # Compute center (after padding)
#         center_x = int((x1 + x2) / 2)
#         center_y = int((y1 + y2) / 2)

#         waste_type = None
#         waste_conf = None

#         # ======================
#         # RULE-BASED DECISION
#         # ======================

#         if label in WET_CLASSES:
#             waste_type = "WET"
#             waste_conf = 95.0

#         elif label in DRY_CLASSES:
#             waste_type = "DRY"
#             waste_conf = 95.0

#         else:
#             # ======================
#             # Level-1 Classifier
#             # ======================

#             crop = original[y1:y2, x1:x2]

#             if crop.size == 0:
#                 continue

#             crop_resized = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
#             crop_processed = preprocess_input(crop_resized)
#             crop_processed = np.expand_dims(crop_processed, axis=0)

#             pred = waste_model.predict(crop_processed, verbose=0)[0][0]

#             if pred > 0.5:
#                 waste_type = "WET"
#                 waste_conf = float(pred * 100)
#             else:
#                 waste_type = "DRY"
#                 waste_conf = float((1 - pred) * 100)

#         output_objects.append({
#             "object": label,
#             "waste_type": waste_type,
#             "confidence": round(waste_conf, 2),
#             "center": [center_x, center_y]
#         })

#     # ==============================
#     # FULL IMAGE FALLBACK
#     # ==============================

#     if len(output_objects) == 0:

#         img_resized = cv2.resize(original, (IMG_SIZE, IMG_SIZE))
#         img_processed = preprocess_input(img_resized)
#         img_processed = np.expand_dims(img_processed, axis=0)

#         pred = waste_model.predict(img_processed, verbose=0)[0][0]

#         if pred > 0.5:
#             waste_type = "WET"
#             waste_conf = float(pred * 100)
#         else:
#             waste_type = "DRY"
#             waste_conf = float((1 - pred) * 100)

#         output_objects.append({
#             "object": "Full Image",
#             "waste_type": waste_type,
#             "confidence": round(waste_conf, 2),
#             "center": [w // 2, h // 2]  # image center
#         })

#     return output_objects



# import os
# import cv2
# import numpy as np
# import tensorflow as tf
# from ultralytics import YOLO
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# # ==============================
# # Configuration
# # ==============================

# YOLO_MODEL_PATH = "ver1.pt"
# LEVEL1_MODEL_PATH = "../level1_classifier/model/dry_wet_model_v1.keras"

# IMG_SIZE = 160
# CONF_THRESHOLD = 0.25
# PADDING_RATIO = 0.15

# OUTPUT_DIR = "static/results"
# os.makedirs(OUTPUT_DIR, exist_ok=True)

# # ==============================
# # Load Models
# # ==============================

# print("Loading YOLO...")
# yolo_model = YOLO(YOLO_MODEL_PATH)

# print("Loading Level-1 classifier...")
# waste_model = tf.keras.models.load_model(LEVEL1_MODEL_PATH)

# print("Models loaded successfully.")

# # ==============================
# # Padding Helper
# # ==============================

# def add_padding(x1, y1, x2, y2, img_shape):
#     h, w = img_shape[:2]

#     box_w = x2 - x1
#     box_h = y2 - y1

#     pad_x = int(box_w * PADDING_RATIO)
#     pad_y = int(box_h * PADDING_RATIO)

#     x1 = max(0, x1 - pad_x)
#     y1 = max(0, y1 - pad_y)
#     x2 = min(w, x2 + pad_x)
#     y2 = min(h, y2 + pad_y)

#     return x1, y1, x2, y2

# # ==============================
# # Hybrid Detection
# # ==============================

# def detect_and_classify(image_path):

#     image = cv2.imread(image_path)

#     if image is None:
#         raise ValueError("Invalid image path.")

#     original = image.copy()
#     annotated = original.copy()

#     h, w = original.shape[:2]

#     results = yolo_model(original, conf=0.2, iou=0.5, imgsz=800)

#     detections = []
#     dry_count = 0
#     wet_count = 0

#     # ==============================
#     # Process YOLO detections
#     # ==============================

#     for box in results[0].boxes:

#         confidence = float(box.conf[0])
#         if confidence < CONF_THRESHOLD:
#             continue

#         cls_id = int(box.cls[0])
#         label = yolo_model.names[cls_id]

#         x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
#         x1, y1, x2, y2 = add_padding(x1, y1, x2, y2, original.shape)

#         center_x = int((x1 + x2) / 2)
#         center_y = int((y1 + y2) / 2)

#         crop = original[y1:y2, x1:x2]
#         if crop.size == 0:
#             continue

#         # ==============================
#         # Level-1 Classification
#         # ==============================

#         crop_resized = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
#         crop_processed = preprocess_input(crop_resized)
#         crop_processed = np.expand_dims(crop_processed, axis=0)

#         pred = waste_model.predict(crop_processed, verbose=0)[0][0]

#         if pred > 0.5:
#             waste_type = "WET"
#             waste_conf = float(pred * 100)
#             wet_count += 1
#             color = (0, 0, 255)  # RED (High contrast)
#         else:
#             waste_type = "DRY"
#             waste_conf = float((1 - pred) * 100)
#             dry_count += 1
#             color = (255, 100, 0)  # Bright Blue

#         # Draw bounding box
#         cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

#         # Draw center point
#         cv2.circle(annotated, (center_x, center_y), 5, (0, 0, 255), -1)

#         # Draw label
#         text = f"{waste_type} ({round(waste_conf,1)}%)"
#         cv2.putText(
#             annotated,
#             text,
#             (x1, y1 - 10),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             0.6,
#             color,
#             2
#         )

#         detections.append({
#             "object": label,
#             "waste_type": waste_type,
#             "confidence": round(waste_conf, 2),
#             "center": [center_x, center_y]
#         })

#     # ==============================
#     # Fallback: No detections
#     # ==============================

#     if len(detections) == 0:

#         img_resized = cv2.resize(original, (IMG_SIZE, IMG_SIZE))
#         img_processed = preprocess_input(img_resized)
#         img_processed = np.expand_dims(img_processed, axis=0)

#         pred = waste_model.predict(img_processed, verbose=0)[0][0]

#         if pred > 0.5:
#             waste_type = "WET"
#             waste_conf = float(pred * 100)
#             wet_count += 1
#             color = (0, 255, 255)
#         else:
#             waste_type = "DRY"
#             waste_conf = float((1 - pred) * 100)
#             dry_count += 1
#             color = (0, 255, 0)

#         cv2.putText(
#             annotated,
#             f"{waste_type} ({round(waste_conf,1)}%)",
#             (30, 50),
#             cv2.FONT_HERSHEY_SIMPLEX,
#             1,
#             color,
#             3
#         )

#         detections.append({
#             "object": "Full Image",
#             "waste_type": waste_type,
#             "confidence": round(waste_conf, 2),
#             "center": [w // 2, h // 2]
#         })

#     # ==============================
#     # Summary on Image
#     # ==============================

#     summary_text = f"Dry: {dry_count} | Wet: {wet_count}"

#     cv2.putText(
#         annotated,
#         summary_text,
#         (20, h - 20),
#         cv2.FONT_HERSHEY_SIMPLEX,
#         0.8,
#         (255, 255, 255),
#         2
#     )

#     # ==============================
#     # Save Annotated Image
#     # ==============================

#     import time

#     filename = f"annotated_{int(time.time())}.jpg"
#     output_path = os.path.join(OUTPUT_DIR, filename)
#     cv2.imwrite(output_path, annotated)

#     return {
#         "detections": detections,
#         "dry_count": dry_count,
#         "wet_count": wet_count,
#         "result_image": output_path
#     }


import os
import cv2
import numpy as np
import tensorflow as tf
from ultralytics import YOLO
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import time

# ==============================
# Configuration
# ==============================

# YOLO_MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")
YOLO_MODEL_PATH = os.path.join(os.path.dirname(__file__), "kaustav.pt")
LEVEL1_MODEL_PATH = "../level1_classifier/model/waste_model_v2.keras"

IMG_SIZE = 224
CONF_THRESHOLD = 0.25
PADDING_RATIO = 0.15

OUTPUT_DIR = "static/results"
CROP_DIR = os.path.join(OUTPUT_DIR, "crops")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(CROP_DIR, exist_ok=True)

# ==============================
# Load Models
# ==============================

print("Loading YOLO...")
yolo_model = YOLO(YOLO_MODEL_PATH)

print("Loading Level-1 classifier...")
waste_model = tf.keras.models.load_model(LEVEL1_MODEL_PATH)

print("Models loaded successfully.")

# ==============================
# Padding Helper
# ==============================

def add_padding(x1, y1, x2, y2, img_shape):
    h, w = img_shape[:2]

    box_w = x2 - x1
    box_h = y2 - y1

    pad_x = int(box_w * PADDING_RATIO)
    pad_y = int(box_h * PADDING_RATIO)

    x1 = max(0, x1 - pad_x)
    y1 = max(0, y1 - pad_y)
    x2 = min(w, x2 + pad_x)
    y2 = min(h, y2 + pad_y)

    return x1, y1, x2, y2

# ==============================
# Hybrid Detection Function
# ==============================

def detect_and_classify(image_path):

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Invalid image path.")

    original = image.copy()
    annotated = original.copy()

    h, w = original.shape[:2]

    results = yolo_model(original, conf=0.2, iou=0.5, imgsz=800)

    detections = []
    dry_count = 0
    wet_count = 0

    # ==============================
    # Process YOLO detections
    # ==============================

    for idx, box in enumerate(results[0].boxes):

        confidence = float(box.conf[0])
        if confidence < CONF_THRESHOLD:
            continue

        cls_id = int(box.cls[0])
        label = yolo_model.names[cls_id]

        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        x1, y1, x2, y2 = add_padding(x1, y1, x2, y2, original.shape)

        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        crop = original[y1:y2, x1:x2]
        if crop.size == 0:
            continue

        # ==============================
        # SAVE CROPPED IMAGE
        # ==============================

        crop_filename = f"crop_{int(time.time()*1000)}_{idx}.jpg"
        crop_path = os.path.join(CROP_DIR, crop_filename)
        cv2.imwrite(crop_path, crop)

        # ==============================
        # Level-1 Classification
        # ==============================

        crop_resized = cv2.resize(crop, (IMG_SIZE, IMG_SIZE))
        crop_processed = preprocess_input(crop_resized)
        crop_processed = np.expand_dims(crop_processed, axis=0)

        pred = waste_model.predict(crop_processed, verbose=0)[0][0]

        if pred > 0.5:
            waste_type = "WET"
            waste_conf = float(pred * 100)
            wet_count += 1
            color = (0, 0, 255)  # Red
        else:
            waste_type = "DRY"
            waste_conf = float((1 - pred) * 100)
            dry_count += 1
            color = (255, 100, 0)  # Blue

        # ==============================
        # Draw Bounding Box + Label
        # ==============================

        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

        cv2.circle(annotated, (center_x, center_y), 5, (0, 0, 255), -1)

        text = f"{waste_type} ({round(waste_conf,1)}%)"
        cv2.putText(
            annotated,
            text,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

        detections.append({
            "object": label,
            "waste_type": waste_type,
            "confidence": round(waste_conf, 2),
            "center": [center_x, center_y],
            "crop_image": "/" + crop_path.replace("\\", "/")   # ⭐ important
        })

    # ==============================
    # Fallback (No detection)
    # ==============================

    if len(detections) == 0:

        img_resized = cv2.resize(original, (IMG_SIZE, IMG_SIZE))
        img_processed = preprocess_input(img_resized)
        img_processed = np.expand_dims(img_processed, axis=0)

        pred = waste_model.predict(img_processed, verbose=0)[0][0]

        if pred > 0.5:
            waste_type = "WET"
            waste_conf = float(pred * 100)
            wet_count += 1
            color = (0, 255, 255)
        else:
            waste_type = "DRY"
            waste_conf = float((1 - pred) * 100)
            dry_count += 1
            color = (0, 255, 0)

        cv2.putText(
            annotated,
            f"{waste_type} ({round(waste_conf,1)}%)",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            3
        )

        detections.append({
            "object": "Full Image",
            "waste_type": waste_type,
            "confidence": round(waste_conf, 2),
            "center": [w // 2, h // 2],
            "crop_image": image_path
        })

    # ==============================
    # Summary Text
    # ==============================

    summary_text = f"Dry: {dry_count} | Wet: {wet_count}"

    cv2.putText(
        annotated,
        summary_text,
        (20, h - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    # ==============================
    # Save Final Image
    # ==============================

    filename = f"annotated_{int(time.time())}.jpg"
    output_path = os.path.join(OUTPUT_DIR, filename)
    cv2.imwrite(output_path, annotated)

    return {
        "detections": detections,
        "dry_count": dry_count,
        "wet_count": wet_count,
        "result_image": "/" + output_path.replace("\\", "/")
    }