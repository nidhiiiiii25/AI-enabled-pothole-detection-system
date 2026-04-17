# Edge Device - Raspberry Pi Code

This folder contains the complete code that runs on the **Raspberry Pi 4**.

The system does **pothole detection** using:
- YOLOv5 (ONNX model)
- LiDAR for depth measurement
- GPS for location
- Stores results as JSON + images

> **Note**: This version works with **pre-recorded video** (not live camera).  
> The code was designed to support live camera, but testing was done using stored video files.

## Files in this folder

| File              | Purpose                                      |
|-------------------|----------------------------------------------|
| `main.py`         | Main integration script                      |
| `config.py`       | All settings and paths (easy to change)      |
| `best.onnx`       | Trained YOLOv5 model                         |
| `requirements.txt`| Python packages needed                       |
| `gps_utils.py`    | Helper to parse GPS data (if you have it)    |

## How to Setup & Run

### 1. Install Dependencies
```bash
cd edge-device
pip install -r requirements.txt