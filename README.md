# AI Traffic Signal Optimizer 🚦🤖
### Using Computer Vision and Machine Learning

---

## Live Demo

http://13.49.145.10:5173/

---

## Team Details

**Team Name:** Kirmada

**Team Members:**
- Swapnil Arya
- Prerana Bothra
- Tathya Varma

---

## Domain of the Project

- Smart Cities
- Intelligent Transportation Systems
- Artificial Intelligence
- Computer Vision

---

## Abstract

Urban traffic congestion is a major challenge in modern cities, leading to increased travel time, fuel consumption, and pollution. Traditional traffic signal systems operate on fixed timings and fail to adapt to real‑time traffic conditions.

This project presents an AI‑based traffic signal optimization system that uses computer vision to detect vehicle density and dynamically control traffic lights. The system also supports emergency vehicle prioritization to ensure faster clearance of critical routes.

The solution integrates a FastAPI backend, a React‑based frontend dashboard, and a computer vision module using OpenCV and deep learning models (YOLO).

---

## Idea

Traditional traffic lights:

- Use fixed timers
- Cannot adapt to congestion
- Delay emergency vehicles

Our system:

- Detects real‑time traffic density using cameras or video
- Optimizes green signal timing dynamically
- Allows emergency lane prioritization via UI
- Provides a live monitoring dashboard

This improves:

- Traffic flow efficiency
- Emergency response time
- Road safety
- Fuel usage and pollution levels

---

## Objectives

- Reduce traffic congestion
- Minimize average waiting time
- Improve signal efficiency
- Enable emergency vehicle prioritization
- Provide real‑time monitoring dashboard
- Support scalability and cloud deployment

---

## System Architecture

### Components

- Frontend (React + Vite + Tailwind CSS)
- Backend (FastAPI + Python)
- Computer Vision Module (OpenCV + YOLO)

### Data Flow

Camera / Video → CV Module → Backend API → Frontend Dashboard → Signal Control Logic

---

## Achievements So Far

- Real‑time vehicle detection using YOLOv8
- Dynamic signal timing based on lane congestion
- Emergency mode with directional control
- Live traffic monitoring dashboard
- REST API using FastAPI
- Video streaming using OpenCV
- Cloud deployment on AWS EC2
- Full‑stack implementation using React and Python

---

## Tech Stack Used

### Frontend
- React
- Vite
- Tailwind CSS
- HTML
- CSS
- JavaScript

### Backend
- Python
- FastAPI
- Uvicorn

### Computer Vision & AI
- OpenCV
- YOLO (Ultralytics / Roboflow)

### Infrastructure & Tools
- AWS EC2 (Ubuntu)
- Git
- GitHub
- REST APIs

---

## Features

- Real‑time traffic density detection
- Automatic signal timing optimization
- Signal modes:
  - AUTO (Auto-Switch)
  - SMART (Auto-Switch)
  - EMERGENCY (Manual)
- Emergency lane selection via UI
- Emergency cancel functionality
- Live signal status display
- Vehicle count per lane
- Average wait time calculation
- Efficiency and CO₂ estimation
- Live video streaming

---

## Signal Control Logic

### NORMAL Mode
- Fixed round‑robin signal switching

### SMART Mode
- Lane with highest vehicle count gets longer green time

### EMERGENCY Mode
- Selected lane is forced green until manually cancelled

---

## How to Execute the Code (Local Setup)

Run services in this order: **Backend → Computer Vision → Frontend**

You will need **3 terminals**.

---

### Prerequisites

- Python 3.9+
- Node.js 18+
- pip
- Git

---

### Step 1 – Start Backend Server (Terminal 1)

cd backend  
pip install -r requirements.txt  
uvicorn main:app --host 0.0.0.0 --port 5000  

Backend runs at: http://localhost:5000

---

### Step 2 – Start Computer Vision Module (Terminal 2)

cd cv  
python detector.py  

This module:
- Runs YOLO vehicle detection
- Processes video or camera frames
- Sends vehicle counts to backend

---

### Step 3 – Start Frontend Application (Terminal 3)

cd frontend  
npm install  
npm run dev  

Frontend runs at: http://localhost:5173

---

## Environment Configuration

Update backend URL in:

frontend/src/services/api.js

Set:

const BASE_URL = "http://localhost:5000";

(Replace with EC2 IP when deployed)

---

## Running with Video Input

- Place video file in: backend/videos/traffic.mp4
- Ensure backend uses: cv2.VideoCapture("videos/traffic.mp4")

---

## API Endpoints

- /state – Current traffic and signal state
- /video – Live video stream
- /emergency – Activate emergency mode

---

## Code Sample (Quick Start)

Backend:  
cd backend  
uvicorn main:app --host 0.0.0.0 --port 5000  

Computer Vision:  
cd cv  
python detector.py  

Frontend:  
cd frontend  
npm run dev  

---

## Hosted Project

Frontend: http://13.49.145.10:5173  
Backend: http://13.49.145.10:5000  

GitHub Repository:  
https://github.com/preranabothra9-afk/ai-traffic-signal-optimizer

---

## Results

- Reduced waiting time in heavy traffic
- Improved lane utilization
- Immediate emergency response
- Smooth dashboard updates
- Stable real‑time performance

---

## Future Scope

- Automatic emergency vehicle detection
- Multiple camera support
- Full cloud scaling on AWS
- Database logging and analytics
- Mobile application
- Model optimization
- Smart city integration

---

## License

- Developed for academic and research purposes (IEEE Project).

---

## References

- FastAPI Documentation
- OpenCV Documentation
- React Documentation
- YOLO Object Detection
- IEEE Smart Transportation Research Papers

---

## Acknowledgements

- IEEE Student Chapter
- Ultralytics YOLO
- OpenCV Community
- FastAPI Team
- AWS Educate

---

## END OF THE DOCUMENT