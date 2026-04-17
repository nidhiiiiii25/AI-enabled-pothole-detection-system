# ================================================
# config.py - All settings in one place
# ================================================

import os
from datetime import datetime

# ========================= PATHS =========================
# Change these paths according to your laptop / Raspberry Pi

MODEL_PATH = "best.onnx"                    # Put best.onnx in the same folder

VIDEO_PATH = "v2.mp4"                       # Your test video (put it here or give full path)

OUT_DIR    = "output"                       # All results will be saved here
FRAMES_DIR = os.path.join(OUT_DIR, "frames")
BEST_DIR   = os.path.join(OUT_DIR, "best_frames")

LOG_SENSOR   = os.path.join(OUT_DIR, "all_sensor.jsonl")
LOG_POTHOLES = os.path.join(OUT_DIR, "best_potholes.jsonl")
GPS_LAST_FILE = os.path.join(OUT_DIR, "gps_last.json")

# Create output folders automatically
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(BEST_DIR, exist_ok=True)

# ====================== SENSOR CONFIG ======================
LIDAR_PORT = "/dev/ttyUSB0"
LIDAR_BAUD = 115200

GPS_PORT   = "/dev/serial0"
GPS_BAUD   = 9600

# ====================== ML CONFIG ======================
CONFIDENCE_THRESHOLD = 0.45
NMS_THRESHOLD        = 0.45

# ====================== OTHER SETTINGS ======================
FPS_FALLBACK = 25.0   # Used if video FPS cannot be read

# Human readable timestamp function
def human_time(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")