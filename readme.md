# ♻️ AI-Enabled Waste Segregation System

## 📌 Overview

This project is an **AI-powered waste classification and detection system** designed to automate the process of waste segregation. It combines **image classification** and **object detection** to identify different types of waste and assist in proper disposal.

The system is divided into two levels:

* **Level 1 (Classifier):** Classifies an input image into a waste category.
* **Level 2 (Detector):** Detects and localizes waste objects using YOLO.
* **Web App:** Provides an interactive interface for users to upload images and view results.

---

## 🎯 Problem Statement

Manual waste segregation is inefficient and error-prone. This project aims to:

* Reduce human effort
* Improve accuracy in waste classification
* Promote sustainable waste management practices

---

## 🧠 Solution Approach

### 🔹 Level 1: Image Classification

* Takes an input image
* Predicts the category (e.g., organic, recyclable, plastic, etc.)
* Built using deep learning models

### 🔹 Level 2: Object Detection

* Uses YOLO model for real-time detection
* Identifies and draws bounding boxes around waste items

### 🔹 Web Interface

* Upload image via browser
* Backend processes image using both models
* Displays classification + detection results

---

## 🏗️ Project Structure

```
.
├── level1_classifier/
│   ├── DATASET/
│   ├── model/
│   ├── train.py
│   ├── predict.py
│   └── requirements.txt
│
├── level2_detector/
│   ├── best.pt
│   ├── hybrid_detector.py
│   ├── test_yolo.py
│   └── requirements.txt
│
├── web_app/
│   ├── static/
│   │   ├── uploads/
│   │   └── results/
│   ├── templates/
│   │   └── index.html
│   └── app.py
│
├── README.md
└── requirements.txt
```

---

## ⚙️ Tech Stack

* **Languages:** Python, JavaScript, HTML, CSS
* **Frameworks:** Flask
* **Libraries:**

  * TensorFlow / PyTorch
  * OpenCV
  * NumPy
* **Model:** YOLO (for object detection)

---

## 🚀 Getting Started

### 🔧 1. Clone the Repository

```
git clone https://github.com/YOUR_USERNAME/ai-waste-segregation-system.git
cd ai-waste-segregation-system
```

---

### 📦 2. Set Up Virtual Environment

```
python -m venv venv
source venv/bin/activate     # On Linux/Mac
venv\Scripts\activate        # On Windows
```

---

### 📥 3. Install Dependencies

```
pip install -r requirements.txt
```

---

### 📁 4. Add Model Files

Due to size limitations, model weights are not included.

Download and place:

* `best.pt` → inside `level2_detector/`
* Classification model → inside `level1_classifier/model/`

---

### ▶️ 5. Run the Application

```
cd web_app
python app.py
```

---

### 🌐 6. Open in Browser

```
http://127.0.0.1:5000/
```

Upload an image and view:

* Predicted waste category
* Detected objects with bounding boxes

---

## 🧪 Example Workflow

1. Upload image (e.g., plastic bottle)
2. Classifier predicts: **Plastic Waste**
3. Detector highlights object in image
4. Output displayed on web interface

---

## 📊 Features

* Dual-stage AI pipeline (classification + detection)
* Real-time image processing
* User-friendly web interface
* Modular and scalable architecture

---

## 🔮 Future Improvements

* Add more waste categories
* Improve model accuracy with larger datasets
* Deploy on cloud (AWS / Render)
* Mobile app integration
* Real-time camera detection

---

## 👨‍💻 Contributors

* Satyajeet
* Team Members

---

## 📄 License

This project is for academic and research purposes.

---

## ⭐ Acknowledgment

Inspired by the need for smarter and sustainable waste management using AI.
