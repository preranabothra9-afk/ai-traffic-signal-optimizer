# ===================== IMPORTS =====================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from typing import Dict
import threading
import time
import random
import cv2
import os

# ===================== APP =====================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== SYSTEM STATE =====================
system_state = {
    "mode": "AUTO",
    "lanes": {
        "north": {"count": 0, "signal": "red", "green_time": 0},
        "east":  {"count": 0, "signal": "red", "green_time": 0},
        "south": {"count": 0, "signal": "red", "green_time": 0},
        "west":  {"count": 0, "signal": "red", "green_time": 0},
    },
    "emergency_lane": None
}

LANE_ORDER = ["north", "east", "south", "west"]
current_lane_index = 0

FIXED_GREEN_TIME = 30
MIN_GREEN = 10
MAX_GREEN = 60
SMART_THRESHOLD = 15

# ===================== SIGNAL LOGIC =====================
def apply_normal_mode():
    global current_lane_index
    active_lane = LANE_ORDER[current_lane_index]

    for lane in system_state["lanes"]:
        system_state["lanes"][lane]["signal"] = "red"
        system_state["lanes"][lane]["green_time"] = 0

    system_state["lanes"][active_lane]["signal"] = "green"
    system_state["lanes"][active_lane]["green_time"] = FIXED_GREEN_TIME

    current_lane_index = (current_lane_index + 1) % len(LANE_ORDER)

def apply_smart_mode():
    lanes = system_state["lanes"]
    max_count = max(lanes[l]["count"] for l in lanes)
    busiest_lane = max(lanes, key=lambda l: lanes[l]["count"])

    for lane in lanes:
        lanes[lane]["signal"] = "red"
        lanes[lane]["green_time"] = 0

    green_time = MIN_GREEN if max_count == 0 else min(MAX_GREEN, max(MIN_GREEN, max_count * 3))
    lanes[busiest_lane]["signal"] = "green"
    lanes[busiest_lane]["green_time"] = green_time

def apply_auto_mode():
    if system_state["mode"] == "EMERGENCY":
        return

    max_count = max(l["count"] for l in system_state["lanes"].values())

    if max_count >= SMART_THRESHOLD:
        system_state["mode"] = "SMART"
        apply_smart_mode()
    else:
        system_state["mode"] = "NORMAL"
        apply_normal_mode()

def apply_emergency_mode(lane):
    if lane not in system_state["lanes"]:
        return

    system_state["mode"] = "EMERGENCY"
    system_state["emergency_lane"] = lane

    for l in system_state["lanes"]:
        system_state["lanes"][l]["signal"] = "red"
        system_state["lanes"][l]["green_time"] = 0

    system_state["lanes"][lane]["signal"] = "green"
    system_state["lanes"][lane]["green_time"] = 999

# ===================== API ROUTES =====================
@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/state")
def get_state():
    return system_state

@app.post("/traffic/update")
def update_traffic(counts: Dict[str, int]):
    for lane in system_state["lanes"]:
        if lane in counts:
            system_state["lanes"][lane]["count"] = counts[lane]

    if system_state["mode"] != "EMERGENCY":
        apply_auto_mode()

    return {"status": "updated"}

@app.post("/emergency/detect")
def emergency(data: Dict[str, str]):
    lane = data.get("lane")
    apply_emergency_mode(lane)
    return {"status": "emergency", "lane": lane}

# ===================== SIMULATED TRAFFIC =====================
def simulate_traffic():
    while True:
        for lane in system_state["lanes"]:
            system_state["lanes"][lane]["count"] = random.randint(0, 40)

        if system_state["mode"] != "EMERGENCY":
            apply_auto_mode()

        time.sleep(2)

threading.Thread(target=simulate_traffic, daemon=True).start()

# ===================== VIDEO STREAM =====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_PATH = os.path.join(BASE_DIR, "..", "cv", "Sample_video.mp4")

cap = cv2.VideoCapture(VIDEO_PATH)

if cap.isOpened():
    print("✅ Video stream opened")
else:
    print("❌ Video not opened")

def generate_frames():
    while True:
        success, frame = cap.read()
        if not success:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue

        _, buffer = cv2.imencode(".jpg", frame)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )

@app.get("/video")
def video_feed():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
