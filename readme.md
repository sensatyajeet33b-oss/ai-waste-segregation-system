# 🤖 Smart IoT Waste Segregation System

AI-powered waste detection and segregation system using:

- YOLOv8 for object detection
- CNN (MobileNetV2) for wet/dry classification
- Flask web app
- IoT robotic arm simulation

## Architecture

Image → YOLO → Rule Engine → CNN → Center Coordinates → IoT Simulation

## Features

- Hybrid detection system
- Rule-based + Deep Learning classification
- Robotic arm simulation
- Smart bin segregation
- Progress tracking
- IoT-style dashboard UI

## How to Run

1. Clone repository
2. Create virtual environment
3. Install requirements: pip install -r requirements.txt
4. Run:
python web_app/app.py
Copy code

## Future Improvements

- Custom YOLO training
- Real IoT hardware integration
- Bin capacity monitoring


# AI-Enabled Waste Segregation System

## Features
- Level 1: Image Classification
- Level 2: Object Detection (YOLO)
- Web Interface for interaction

## Tech Stack
- Python
- TensorFlow / PyTorch
- Flask
- YOLO

## How to Run
1. Clone repo
2. Install dependencies
3. Run app.py