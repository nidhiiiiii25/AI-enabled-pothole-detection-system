# AI-enabled-pothole-detection-system
Real-time AI Pothole Detection using YOLOv5 + LiDAR + GPS on Raspberry Pi

# 🚧 AI-Enabled Pothole Detection System

**Pothole detection using YOLOv5 + LiDAR + GPS on Raspberry Pi 4**  
Edge AI | Multi-sensor fusion | Web dashboard

![System Overview](docs/architecture-diagram.png)

## 🎯 The Problem
Potholes are a major safety hazard on Indian roads, causing accidents, vehicle damage, and high maintenance costs. Traditional manual surveys and citizen reporting apps are slow and inconsistent.

## ✨ Our Solution
A **portable embedded prototype** that:
- Detects potholes from video input using a camera
- Measures physical **depth** using LiDAR sensor
- Adds accurate **GPS coordinates**
- Synchronizes camera, LiDAR and GPS data using timestamps
- Logs data and displays everything on a clean web dashboard

The system was designed to accept live camera feed but was tested using pre-recorded video files for controlled evaluation.

## 🔥 Key Features
- Pothole detection using YOLOv5 computer vision model
- LiDAR-based depth estimation for better accuracy
- Timestamp-based multi-sensor data fusion
- Automatic JSON logging with GPS, depth and confidence
- Interactive web dashboard with map, images and details

## 🛠️ Tech Stack

| Layer           | Technology                                      |
|-----------------|-------------------------------------------------|
| Hardware        | Raspberry Pi 4, USB Webcam, TF-Luna LiDAR, u-blox NEO-6M GPS |
| AI Model        | YOLOv5 exported as ONNX (`best.onnx`)           |
| Edge Software   | Python + OpenCV + ONNX Runtime + pySerial      |
| Backend         | Node.js + Express + MongoDB Atlas + Cloudinary |
| Frontend        | HTML/CSS/JS + Leaflet.js (interactive map)     |

## 📁 Project Structure
- `edge-device/` → Raspberry Pi code + ONNX model
- `hardware/` → Prototype photos and wiring details
- `backend/` → Server code (if available)
- `frontend/` → Dashboard screenshots
- `results/` → Detection images, logs and outputs
- `docs/` → Full project report & diagrams

## 📊 Results & Demo
- YOLOv5 model successfully detects potholes from video input
- LiDAR provides depth validation (helps reduce false positives from shadows/tar)
- GPS geo-tagging and timestamp synchronization implemented
- System tested using pre-recorded video clips

**Detection Examples** → [`results/detection-examples/`](results/detection-examples/)

**Dashboard Screenshots** → [`frontend/dashboard-screenshots/`](frontend/dashboard-screenshots/)

**Full Project Report** → [`docs/project-report.pdf`](docs/project-report.pdf)

## 🧪 How to Run
Detailed setup instructions are inside [`edge-device/README.md`](edge-device/README.md)

## 🔮 Future Scope
This prototype can be extended for:
- Live camera testing in real-world conditions
- Vehicle or drone mounting
- Large-scale road surveys
- Severity classification (minor/moderate/severe)



[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4-orange.svg)]()
[![YOLOv5](https://img.shields.io/badge/YOLOv5-ONNX-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

