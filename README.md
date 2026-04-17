# AI-enabled-pothole-detection-system
Real-time AI Pothole Detection using YOLOv5 + LiDAR + GPS on Raspberry Pi


# 🚧 AI-Enabled Pothole Detection System

**Real-time pothole detection using YOLOv5 + LiDAR + GPS on Raspberry Pi 4**  
Edge AI | Multi-sensor fusion | Live web dashboard for smart cities

![System Overview](docs/architecture-diagram.png)

## 🎯 The Problem
Potholes cause thousands of accidents every year in India, especially for two-wheeler riders. Manual surveys are slow, citizen apps depend on people manually reporting, and most potholes go undetected until damage happens.

## ✨ Our Solution
A **vehicle-mounted prototype** that automatically:
- Detects potholes in real-time using a camera
- Measures actual **depth** with LiDAR
- Adds precise **GPS location**
- Synchronizes all data with timestamps
- Sends everything to a clean web dashboard

The entire system runs on a low-cost Raspberry Pi and is designed for real-world municipal and fleet use.

## 🔥 Key Features
- Real-time video processing while the vehicle is moving
- Timestamp-based fusion of camera, LiDAR & GPS data
- Accurate depth estimation for severity
- Automatic JSON logging + cloud upload
- Interactive map dashboard with images, depth, location & confidence
- Comment/reporting system for road maintenance teams

## 🛠️ Tech Stack

| Layer           | Technology                                      |
|-----------------|-------------------------------------------------|
| Hardware        | Raspberry Pi 4, USB Webcam, TF-Luna LiDAR, u-blox NEO-6M GPS |
| AI Model        | YOLOv5 exported as ONNX (`best.onnx`)           |
| Edge Software   | Python + OpenCV + ONNX Runtime + pySerial      |
| Backend         | Node.js + Express + MongoDB Atlas + Cloudinary |
| Frontend        | HTML/CSS/JS + Leaflet.js (interactive map)     |
| Deployment      | Edge device + Cloud dashboard                   |

## 📁 Project Structure
- `edge-device/` → All Raspberry Pi code + ONNX model
- `hardware/` → Photos, wiring & bill of materials
- `backend/` → Node.js server (if available)
- `frontend/` → Dashboard screenshots
- `results/` → Detection images, logs & performance
- `docs/` → Full project report & diagrams

## 📊 Results & Demo
- System successfully detects potholes in real-time
- LiDAR provides physical depth validation (reduces false positives from shadows/tar)
- GPS geo-tagging works reliably
- Web dashboard shows live map with pothole cards

**Detection Examples** → [`results/detection-examples/`](results/detection-examples/)

**Dashboard Screenshots** → [`frontend/dashboard-screenshots/`](frontend/dashboard-screenshots/)

**Full Project Report** → [`docs/project-report.pdf`](docs/project-report.pdf)

## 🧪 How to Run (Edge Device)

Detailed instructions are inside [`edge-device/README.md`](edge-device/README.md)

## 🔮 Future / Startup Vision
This prototype is ready for:
- Larger field trials on municipal vehicles
- Severity classification (minor/moderate/severe)
- Fleet-scale deployment
- Predictive maintenance analytics

We built this as a complete end-to-end system — from hardware to cloud — to prove that affordable, made-in-India road monitoring is possible.



---



[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-4-orange.svg)]()
[![YOLOv5](https://img.shields.io/badge/YOLOv5-ONNX-green.svg)]()
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
