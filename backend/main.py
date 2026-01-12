from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.get("/health")
def health():
    return {"ok": True}

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

@app.get("/state")
def get_state():
    return system_state
