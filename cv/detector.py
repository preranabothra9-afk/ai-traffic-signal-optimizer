"""
AI Traffic Signal Optimiser - Vehicle Detection Module
Detects vehicles, emergency vehicles, and pedestrians in traffic video.
"""

import time
import cv2
import requests
from datetime import datetime
from ultralytics import YOLO
from inference_sdk import InferenceHTTPClient

TRAFFIC_URL = "http://127.0.0.1:8000/traffic/update"
EMERGENCY_URL = "http://127.0.0.1:8000/emergency/detect"


def send_counts(counts):
    try:
        requests.post(TRAFFIC_URL, json=counts, timeout=1)
    except:
        pass


def is_nighttime():
    """Check if current time is night (7 PM to 6 AM)"""
    current_hour = datetime.now().hour
    return current_hour >= 19 or current_hour < 6


def calculate_traffic_density(counts):
    """Calculate overall traffic density percentage"""
    total = sum(counts.values())
    max_capacity = 50
    return min(100, (total / max_capacity) * 100)


def main():
    print("Loading YOLOv8 model...")
    model = YOLO("yolov8n.pt")
    
    print("Connecting to Roboflow emergency vehicle detector...")
    emergency_client = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="h8Zi46ltQ3V2iQGDWdjZ"
    )

    VIDEO_PATH = "Sample_video.mp4"
    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print(f"Error: Could not open video file {VIDEO_PATH}")
        exit()

    VEHICLE_CLASSES = [2, 3, 5, 7]
    PEDESTRIAN_CLASS = 0
    
    vehicle_names = {
        0: 'person',
        2: 'car',
        3: 'motorcycle',
        5: 'bus',
        7: 'truck'
    }

    ret, frame = cap.read()
    if not ret:
        print("Error reading video")
        exit()

    height, width, _ = frame.shape
    print(f"Video dimensions: {width}x{height}")

    lanes = {
        "north": (0, 0, width//2, height//2),
        "east":  (width//2, 0, width, height//2),
        "south": (0, height//2, width//2, height),
        "west":  (width//2, height//2, width, height)
    }

    lane_colors = {
        "north": (255, 0, 0),
        "east": (0, 255, 0),
        "south": (0, 0, 255),
        "west": (255, 255, 0)
    }
    
    crosswalk_zones = {
        "north_crossing": (width//4 - 50, height//4 - 50, width//4 + 50, height//4 + 50),
        "east_crossing": (3*width//4 - 50, height//4 - 50, 3*width//4 + 50, height//4 + 50),
        "south_crossing": (width//4 - 50, 3*height//4 - 50, width//4 + 50, 3*height//4 + 50),
        "west_crossing": (3*width//4 - 50, 3*height//4 - 50, 3*width//4 + 50, 3*height//4 + 50)
    }

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    last_print_time = time.time()
    frame_count = 0
    detection_failures = 0

    print("Starting vehicle detection...")
    print("Press 'q' to quit\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video")
            break

        frame_count += 1

        try:
            results = model(frame, verbose=False)[0]
            detection_failures = 0
        except Exception as e:
            detection_failures += 1
            print(f"Detection failure: {e}")
            if detection_failures > 5:
                print("⚠️  SENSOR FAILURE MODE - Using fallback timing")

        counts = {
            "north": 0,
            "east": 0,
            "south": 0,
            "west": 0
        }
        
        emergency_detected = {
            "north": False,
            "east": False,
            "south": False,
            "west": False
        }
        
        pedestrians = {
            "north_crossing": 0,
            "east_crossing": 0,
            "south_crossing": 0,
            "west_crossing": 0
        }

        for box in results.boxes:
            cls = int(box.cls[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            if cls in VEHICLE_CLASSES:
                for lane, (lx1, ly1, lx2, ly2) in lanes.items():
                    if lx1 <= cx <= lx2 and ly1 <= cy <= ly2:
                        counts[lane] += 1
                        break

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                label = f"{vehicle_names[cls]}: {conf:.2f}"
                cv2.putText(frame, label, (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            elif cls == PEDESTRIAN_CLASS and conf > 0.5:
                for crossing, (cx1, cy1, cx2, cy2) in crosswalk_zones.items():
                    if cx1 <= cx <= cx2 and cy1 <= cy <= cy2:
                        pedestrians[crossing] += 1
                        break
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 2)
                cv2.putText(frame, "PEDESTRIAN", (x1, y1 - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

        try:
            _, img_encoded = cv2.imencode('.jpg', frame)
            emergency_result = emergency_client.infer(img_encoded.tobytes(), model_id="emergency-v-qmf4g-iysi5/1")
            
            if 'predictions' in emergency_result:
                for pred in emergency_result['predictions']:
                    ex1 = int(pred['x'] - pred['width'] / 2)
                    ey1 = int(pred['y'] - pred['height'] / 2)
                    ex2 = int(pred['x'] + pred['width'] / 2)
                    ey2 = int(pred['y'] + pred['height'] / 2)
                    e_conf = pred['confidence']
                    e_class = pred['class']
                    
                    ecx = (ex1 + ex2) // 2
                    ecy = (ey1 + ey2) // 2
                    
                    for lane, (lx1, ly1, lx2, ly2) in lanes.items():
                        if lx1 <= ecx <= lx2 and ly1 <= ecy <= ly2:
                            emergency_detected[lane] = True
                            break
                    
                    cv2.rectangle(frame, (ex1, ey1), (ex2, ey2), (0, 0, 255), 3)
                    e_label = f"EMERGENCY: {e_class} {e_conf:.2f}"
                    cv2.putText(frame, e_label, (ex1, ey1 - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        except Exception as e:
            pass

        for crossing, (cx1, cy1, cx2, cy2) in crosswalk_zones.items():
            color = (255, 255, 0) if pedestrians[crossing] > 0 else (128, 128, 128)
            cv2.rectangle(frame, (cx1, cy1), (cx2, cy2), color, 2)

        for lane, (lx1, ly1, lx2, ly2) in lanes.items():
            color = lane_colors[lane]
            
            if emergency_detected[lane]:
                color = (0, 0, 255)
                thickness = 5
            else:
                thickness = 3
            
            cv2.rectangle(frame, (lx1, ly1), (lx2, ly2), color, thickness)
            
            label_x = lx1 + 10
            label_y = ly1 + 30
            
            lane_text = lane.upper()
            if emergency_detected[lane]:
                lane_text += " - EMERGENCY!"
            
            cv2.putText(frame, lane_text, (label_x, label_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            count_text = f"Vehicles: {counts[lane]}"
            cv2.putText(frame, count_text, (label_x, label_y + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        status_y = 20
        night_mode = is_nighttime()
        traffic_density = calculate_traffic_density(counts)
        
        if any(emergency_detected.values()):
            cv2.rectangle(frame, (0, 0), (width, 60), (0, 0, 255), -1)
            cv2.putText(frame, "EMERGENCY VEHICLE DETECTED!", (width//2 - 250, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
            status_y = 80
        
        if night_mode:
            cv2.putText(frame, "NIGHT MODE", (10, status_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            status_y += 30
        
        cv2.putText(frame, f"Density: {traffic_density:.1f}%", (10, status_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if detection_failures > 5:
            cv2.putText(frame, "SENSOR FAILURE - FALLBACK MODE", (10, status_y + 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        current_time = time.time()
        if current_time - last_print_time >= 1:
            output = {
                "timestamp": int(current_time * 1000),
                "lanes": {
                    "north": counts["north"],
                    "east": counts["east"],
                    "south": counts["south"],
                    "west": counts["west"]
                },
                "emergency": {
                    "detected": any(emergency_detected.values()),
                    "lanes": emergency_detected
                },
                "pedestrians": pedestrians,
                "traffic_density": round(traffic_density, 2),
                "night_mode": night_mode,
                "sensor_status": "failure" if detection_failures > 5 else "operational"
            }
            
            print(output)
            send_counts(counts)
            
            if any(emergency_detected.values()):
                lane = next(l for l, v in emergency_detected.items() if v)
                try:
                    requests.post(
                        EMERGENCY_URL,
                        json={"lane": lane},
                        timeout=1
                    )
                    print(f"🚨 Emergency sent for {lane}")
                except:
                    pass
            
            last_print_time = current_time

        cv2.imshow("AI Traffic Signal Optimiser - Vehicle Detection", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print("\nExiting...")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Detection complete.")


if __name__ == "__main__":
    main()