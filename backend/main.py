from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# System state
# --------------------
system_state = {
    "mode": "AUTO",   # AUTO / NORMAL / SMART / EMERGENCY
    "lanes": {
        "north": {"count": 0, "signal": "red", "green_time": 0},
        "east":  {"count": 0, "signal": "red", "green_time": 0},
        "south": {"count": 0, "signal": "red", "green_time": 0},
        "west":  {"count": 0, "signal": "red", "green_time": 0},
    },
    "emergency_lane": None
}

# --------------------
# Normal mode config
# --------------------
LANE_ORDER = ["north", "east", "south", "west"]
current_lane_index = 0
FIXED_GREEN_TIME = 30
MIN_GREEN = 10
MAX_GREEN = 60

# --------------------
# Normal mode logic
# --------------------
def apply_normal_mode():
    global current_lane_index

    active_lane = LANE_ORDER[current_lane_index]

    # Reset all lanes
    for lane in system_state["lanes"]:
        system_state["lanes"][lane]["signal"] = "red"
        system_state["lanes"][lane]["green_time"] = 0

    # Activate current lane
    system_state["lanes"][active_lane]["signal"] = "green"
    system_state["lanes"][active_lane]["green_time"] = FIXED_GREEN_TIME

    # Move to next lane
    current_lane_index = (current_lane_index + 1) % len(LANE_ORDER)
   
def apply_smart_mode():
    lanes = system_state["lanes"]

    # safety check
    if not lanes:
        return

    max_count = max(lanes[l]["count"] for l in lanes)

    # handle tie cases
    busiest_lanes = [l for l in lanes if lanes[l]["count"] == max_count]
    busiest_lane = busiest_lanes[0]

    # reset all lanes
    for lane in lanes:
        lanes[lane]["signal"] = "red"
        lanes[lane]["green_time"] = 0

    # calculate green time
    if max_count == 0:
        green_time = MIN_GREEN
    else:
        green_time = min(MAX_GREEN, max(MIN_GREEN, max_count * 3))

    # activate busiest lane
    lanes[busiest_lane]["signal"] = "green"
    lanes[busiest_lane]["green_time"] = green_time

SMART_THRESHOLD = 15  # vehicles

def apply_auto_mode():
    lanes = system_state["lanes"]

    if not lanes:
        return

    max_count = max(lanes[l]["count"] for l in lanes)

    if max_count >= SMART_THRESHOLD:
        system_state["mode"] = "SMART"
        apply_smart_mode()
    else:
        system_state["mode"] = "NORMAL"
        apply_normal_mode()

# --------------------
# API endpoints
# --------------------
@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/state")
def get_state():
    return system_state

@app.get("/mode/normal/test")
def test_normal_mode():
    system_state["mode"] = "NORMAL"
    apply_normal_mode()
    return system_state

@app.get("/mode/smart/test")
def test_smart_mode():
    system_state["mode"] = "SMART"
    apply_smart_mode()
    return system_state

@app.get("/mode/auto/test")
def test_auto_mode():
    apply_auto_mode()
    return system_state
