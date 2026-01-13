"""
AI Traffic Signal Optimiser - Vehicle Detection Module
Detects vehicles in traffic video and counts them by lane direction.
"""

import time
import cv2
from ultralytics import YOLO


def main():
    print("Loading YOLOv8 model...")
    model = YOLO("yolov8n.pt")

    VIDEO_PATH = "Sample_video.mp4"
    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():
        print(f"Error: Could not open video file {VIDEO_PATH}")
        exit()

    VEHICLE_CLASSES = [2, 3, 5, 7]
    vehicle_names = {
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

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    last_print_time = time.time()

    print("Starting vehicle detection...")
    print("Press 'q' to quit\n")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video")
            break

        results = model(frame, verbose=False)[0]

        counts = {
            "north": 0,
            "east": 0,
            "south": 0,
            "west": 0
        }

        for box in results.boxes:
            cls = int(box.cls[0])
            
            if cls not in VEHICLE_CLASSES:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2

            for lane, (lx1, ly1, lx2, ly2) in lanes.items():
                if lx1 <= cx <= lx2 and ly1 <= cy <= ly2:
                    counts[lane] += 1
                    break

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            label = f"{vehicle_names[cls]}: {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        for lane, (lx1, ly1, lx2, ly2) in lanes.items():
            color = lane_colors[lane]
            cv2.rectangle(frame, (lx1, ly1), (lx2, ly2), color, 3)
            
            label_x = lx1 + 10
            label_y = ly1 + 30
            cv2.putText(frame, lane.upper(), (label_x, label_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        current_time = time.time()
        if current_time - last_print_time >= 1:
            print({
                "north": counts["north"],
                "east": counts["east"],
                "south": counts["south"],
                "west": counts["west"]
            })
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