# AI TRAFFIC SIGNAL OPTIMIZER #
# Using Computer Vision and Machine Learning #

# LIVE DEMO LINK

http://13.49.145.10:5173/

# Submitted by:

IEEE Project Report
Swapnil Arya
Prerana Bothra
Tathya Varma

------------------------------------------------------------

# ABSTRACT

Urban traffic congestion is a major challenge in modern cities, leading to increased travel time, fuel consumption, and pollution. Traditional traffic signal systems operate on fixed timings and fail to adapt to real‑time traffic conditions.

This project presents an AI‑based traffic signal optimization system that uses computer vision to detect vehicle density and dynamically control traffic lights. The system also supports emergency vehicle prioritization to ensure faster clearance of critical routes.

The solution integrates a FastAPI backend, a React‑based frontend dashboard, and a computer vision module using OpenCV and deep learning models.

------------------------------------------------------------

# 1. INTRODUCTION

Traffic management is an essential component of smart city infrastructure. Conventional systems are inefficient during peak hours and emergencies due to their static nature.

This project aims to build an intelligent system capable of:

• Monitoring traffic density in real time  
• Dynamically adjusting signal timings  
• Providing emergency lane prioritization  
• Displaying live system status through a dashboard  

------------------------------------------------------------

# 2. OBJECTIVES

• Reduce traffic congestion  
• Minimize average vehicle waiting time  
• Improve signal efficiency  
• Enable emergency vehicle prioritization  
• Provide real‑time monitoring dashboard  
• Support future scalability and cloud deployment  

------------------------------------------------------------

# 3. SYSTEM ARCHITECTURE

The system consists of three major components:

1. Frontend (React + Tailwind CSS)  
2. Backend (FastAPI + Python)  
3. Computer Vision Module (OpenCV + YOLO/Roboflow)

Data Flow:

Camera/Video → CV Module → Backend API → Frontend Dashboard → Signal Control Logic

------------------------------------------------------------

# 4. TECHNOLOGIES USED

Frontend:
• React
• Vite
• Tailwind CSS
• JavaScript

Backend:
• FastAPI
• Python
• Uvicorn

Computer Vision:
• OpenCV
• YOLO / Roboflow inference models

Other:
• Git & GitHub
• REST APIs

------------------------------------------------------------

# 5. FEATURES

• Real‑time traffic density detection  
• Automatic signal timing optimization  
• Modes:
  - NORMAL
  - SMART
  - EMERGENCY

• Emergency lane selection via UI  
• Cancel emergency functionality  
• Live signal status display  
• Vehicle count per lane  
• Average wait time calculation  
• Efficiency & CO₂ estimation  
• Live video streaming  

------------------------------------------------------------

# 6. SIGNAL CONTROL LOGIC

NORMAL MODE:
Fixed round‑robin signal switching

SMART MODE:
Lane with highest vehicle count gets longer green time

EMERGENCY MODE:
Selected lane is forced green until manually cancelled

------------------------------------------------------------

# 7. IMPLEMENTATION DETAILS

Backend:

• Maintains system state  
• Calculates optimal signal timing  
• Handles emergency mode activation and clearing  
• Provides REST endpoints  
• Streams video frames

Frontend:

• Polls backend every 1.5 seconds  
• Displays system statistics  
• Shows emergency control UI  
• Displays live video feed

Computer Vision:

• Processes video frames  
• Detects vehicles  
• Sends vehicle count to backend

------------------------------------------------------------

# 8. RESULTS

• Reduced waiting time in heavy traffic  
• Improved lane utilization  
• Immediate emergency response  
• Smooth real‑time dashboard updates  
• Stable system performance

------------------------------------------------------------

# 9. FUTURE SCOPE

• Automatic emergency vehicle detection  
• Multiple camera support  
• Cloud deployment on AWS  
• Database logging and analytics  
• Mobile application  
• AI model optimization  
• Integration with smart city infrastructure  

------------------------------------------------------------

# 10. CONCLUSION

The AI Traffic Signal Optimizer demonstrates how artificial intelligence and computer vision can significantly improve urban traffic management. The system adapts to real‑time conditions and prioritizes emergency vehicles, making it suitable for smart city deployment and academic research.

------------------------------------------------------------

# REFERENCES

• FastAPI Documentation  
• OpenCV Documentation  
• React Documentation  
• YOLO Object Detection  
• IEEE Smart Transportation Research Papers

------------------------------------------------------------

# END OF DOCUMENT
