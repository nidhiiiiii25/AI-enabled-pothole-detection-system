#!/usr/bin/env python3
"""
FINAL_INTEGRATION_STORED_VIDEO.py

Stored video + YOLO + LiDAR + GPS + JSON
Best pothole only + folium map
Last-known-GPS memory + human-readable timestamps
"""

import cv2, json, os, numpy as np, threading, time, serial, math
from datetime import datetime, timezone
from gps_utils import parse_nmea_line
import folium

# ========================== CONFIG ==========================
MODEL_PATH = "/home/pi2/Desktop/best.onnx"
VIDEO_PATH = "/home/pi2/Desktop/v2.mp4"

OUT_DIR    = "/home/pi2/Desktop/really_final_output"
FRAMES_DIR = os.path.join(OUT_DIR, "frames")
BEST_DIR   = os.path.join(OUT_DIR, "best_frames")

LOG_SENSOR   = os.path.join(OUT_DIR, "all_sensor.jsonl")
LOG_POTHOLES = os.path.join(OUT_DIR, "best_potholes.jsonl")

GPS_LAST_FILE = os.path.join(OUT_DIR, "gps_last.json")

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(BEST_DIR, exist_ok=True)

# Serial ports
LIDAR_PORT = "/dev/ttyUSB0"
LIDAR_BAUD = 115200
GPS_PORT   = "/dev/serial0"
GPS_BAUD   = 9600

# ML runtime
import onnxruntime as ort
session    = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name

current_depth = None
current_gps   = (None, None)
stop_event    = threading.Event()

# ============================================================
#          LOAD & SAVE LAST GOOD GPS
# ============================================================
def load_last_saved_gps():
    if os.path.exists(GPS_LAST_FILE):
        try:
            with open(GPS_LAST_FILE, "r") as f:
                d = json.load(f)
                return (d.get("lat"), d.get("lon"))
        except:
            pass
    return (None, None)

def save_last_gps(lat, lon):
    try:
        with open(GPS_LAST_FILE, "w") as f:
            json.dump({"lat": lat, "lon": lon}, f)
    except:
        pass

last_good_gps = load_last_saved_gps()

# ======================= TIMESTAMP FIX =======================
def human_time(ts):
    """Convert numeric timestamp to human-readable time."""
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

# ======================= LiDAR THREAD ========================
baseline_height = None
pothole_depth = 0
current_depth = 0

class LidarThread(threading.Thread):
    def run(self):
        global current_depth, baseline_height, pothole_depth
        try:
            ser = serial.Serial(LIDAR_PORT, LIDAR_BAUD, timeout=1)
        except:
            print("LIDAR not found")
            return

        while not stop_event.is_set():
            d = ser.read(9)
            if len(d) >= 9 and d[0] == 0x59 and d[1] == 0x59:
                raw = d[2] + (d[3] << 8)
                current_depth = int(raw)

                if baseline_height is None:
                    baseline_height = current_depth
                    print("Baseline:", baseline_height)
                    continue

                pothole_depth = current_depth - baseline_height
                if pothole_depth < 5:
                    pothole_depth = 0

                print("Current:", current_depth,
                      "| Base:", baseline_height,
                      "| Depth:", pothole_depth)

lidar_thread = LidarThread()


# ======================== GPS THREAD ========================
class GPSThread(threading.Thread):
    def run(self):
        global current_gps, last_good_gps

        try:
            gps = serial.Serial(GPS_PORT, GPS_BAUD, timeout=1)
            print("[GPS] Opened")
        except:
            print("[GPS] Can't open")
            return

        dbg = open(os.path.join(OUT_DIR, "gps_raw.log"), "a")

        while not stop_event.is_set():
            try:
                line = gps.readline().decode("ascii", errors="ignore").strip()
                if not line:
                    continue

                dbg.write(line + "\n"); dbg.flush()

                info = parse_nmea_line(line)

                if info.get("fix") and "lat" in info and "lon" in info:
                    lat, lon = info["lat"], info["lon"]

                    current_gps = (lat, lon)
                    last_good_gps = (lat, lon)
                    save_last_gps(lat, lon)

                    print("[GPS FIX]", lat, lon)

            except:
                time.sleep(0.05)

        dbg.close()

gps_thread = GPSThread()


# ========================= ML HELPERS ========================
def preprocess(img):
    r = cv2.resize(img, (640, 640))
    n = r / 255.0
    t = n.transpose(2,0,1)
    return np.expand_dims(t.astype(np.float32),0), r

def score(box, conf):
    x,y,w,h = box
    return (w*h)*conf

def postprocess(preds, conf_thresh=0.45, nms_thresh=0.45):
    preds = preds[0]
    boxes, confs = [], []

    for p in preds:
        conf = float(p[4])
        if conf < conf_thresh:
            continue
        cls = int(np.argmax(p[5:]))
        if cls != 0:
            continue

        x,y,w,h = p[0],p[1],p[2],p[3]
        x1 = int(x - w/2); y1 = int(y - h/2)

        boxes.append([x1,y1,int(w),int(h)])
        confs.append(conf)

    if not boxes:
        return []

    idx = cv2.dnn.NMSBoxes(boxes, confs, conf_thresh, nms_thresh)
    return [(boxes[i], confs[i]) for i in idx.flatten()] if len(idx)>0 else []

video_start_time = datetime.now(timezone.utc)
def frame_timestamp(fc,fps):
    return video_start_time.timestamp() + fc/fps


# ============= Safe GPS Getter (uses last_good) =============
def get_safe_gps():
    lat, lon = current_gps
    if lat is not None:
        return (lat, lon)
    return last_good_gps


# ==================== MAP BUILDER ===========================
def build_map(best_json):
    if not best_json:
        print("[MAP] No pothole data")
        return

    lat, lon = best_json["gps_lat"], best_json["gps_lon"]

    if lat is None:
        print("[MAP] Using last known GPS")
        lat, lon = last_good_gps

    if lat is None:
        lat, lon = 0.0, 0.0

    m = folium.Map(location=[lat, lon], zoom_start=19)

    popup = f"""
    <b>Best Pothole</b><br>
    Confidence: {best_json['confidence']:.2f}<br>
    Depth: {best_json['depth_of_pothole']} cm<br>
    Lat: {lat}<br>
    Lon: {lon}<br>
    """

    if "image" in best_json:
        popup += f"<img src='{best_json['image']}' width='250'>"

    folium.Marker([lat,lon],
        popup=folium.Popup(popup,max_width=300),
        icon=folium.Icon(color="red")
    ).add_to(m)

    out = os.path.join(OUT_DIR, "best_pothole_map.html")
    m.save(out)
    print("[MAP] Saved:", out)


# =========================== MAIN ===========================
def main():

    print("\nStarting STORED VIDEO detection...\n")

    lidar_thread.start()
    gps_thread.start()

    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print("Video error")
        return

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0

    best_frame = None
    best_score = -1
    frame_no = 0
    stable = 0
    best_json = None

    fs = open(LOG_SENSOR,"w")
    fp = open(LOG_POTHOLES,"w")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_no += 1
        inp, img = preprocess(frame)
        preds = session.run(None,{input_name:inp})[0]
        dets = postprocess(preds)

        lat, lon = get_safe_gps()

        ts = frame_timestamp(frame_no, fps)
        ts_hr = human_time(ts)

        fs.write(json.dumps({
            "timestamp": ts_hr,
            "depth_of_pothole": pothole_depth,
            "gps_lat": lat,
            "gps_lon": lon
        }) + "\n")

        if dets: stable += 1
        else:    stable = 0

        if stable < 2:
            continue

        for box, conf in dets:
            x,y,w,h = box
            if y+h > 640*0.75:
                continue

            disp = img.copy()
            cv2.rectangle(disp, (x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(disp, f"POTHOLE ({conf:.2f})",
                        (x,y-10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,(0,255,0),2)

            cv2.imwrite(os.path.join(FRAMES_DIR,f"frame_{frame_no}.jpg"), disp)

            s = score(box,conf)
            if s > best_score:
                best_score = s
                best_frame = disp.copy()
                best_json = {
                    "timestamp": ts_hr,
                    "depth_of_pothole": pothole_depth,
                    "gps_lat": lat,
                    "gps_lon": lon,
                    "confidence": float(conf),
                    "score": float(s)
                }

    if best_frame is not None:
        best_path = os.path.join(BEST_DIR,"best_final.jpg")
        cv2.imwrite(best_path, best_frame)
        print("Best frame saved:", best_path)
        best_json["image"] = best_path

    if best_json is not None:
        fp.write(json.dumps(best_json) + "\n")

    fs.close()
    fp.close()
    cap.release()
    stop_event.set()

    print("DONE:", OUT_DIR)

    build_map(best_json)


if __name__ == "__main__":
    main()
