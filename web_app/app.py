from flask import Flask, render_template, request, jsonify
import os
import sys
import time

# Import detector
sys.path.append("../level2_detector")
from hybrid_detector import detect_and_classify

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index1.html")


# ✅ MULTI OBJECT (DETECTION)
@app.route("/detect", methods=["POST"])
def detect():
    try:
        file = request.files["image"]

        filename = str(int(time.time())) + "_" + file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        results = detect_and_classify(filepath)

        # 🔥 Convert to UI expected format
        detections = []
        for i, d in enumerate(results["detections"]):
            detections.append({
                "id": i + 1,
                "det_label": d["object"],
                "cls_label": d["waste_type"].lower(),
                "cls_conf": d["confidence"] / 100,
                "det_conf": 0.9,  # placeholder (YOLO conf not stored)
                "crop_b64": d["crop_image"]  # already path
            })

        return jsonify({
            "total": len(detections),
            "detections": detections,
            "annotated_image": results["result_image"]
        })

    except Exception as e:
        return jsonify({"error": str(e)})


# ✅ SINGLE OBJECT (CLASSIFICATION)
@app.route("/classify", methods=["POST"])
def classify():
    try:
        file = request.files["image"]

        filename = str(int(time.time())) + "_" + file.filename
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        results = detect_and_classify(filepath)

        # Take first result
        d = results["detections"][0]

        label = d["waste_type"].lower()
        confidence = d["confidence"] / 100

        return jsonify({
            "label": label,
            "confidence": confidence,
            "color": "#3B82F6" if label == "wet" else "#F97316",
            "top5": [
                {"label": "wet", "confidence": confidence if label=="wet" else 1-confidence},
                {"label": "dry", "confidence": confidence if label=="dry" else 1-confidence}
            ]
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)