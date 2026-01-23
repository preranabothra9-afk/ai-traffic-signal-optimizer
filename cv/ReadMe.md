# Computer Vision Module – AI Traffic Signal Optimiser

## Overview
This module performs vehicle detection and lane-wise vehicle counting
using computer vision. The output is used by the backend to decide
traffic signal timings.

## Model Used
- YOLOv8 (Ultralytics)
- Pre-trained model: yolov8n.pt
- No training performed

## Detection Classes
The following vehicle classes are detected:
- Car
- Motorcycle
- Bus
- Truck

## Lane Definition
The video frame is manually divided into four rectangular regions:
- North
- East
- South
- West

Each detected vehicle is assigned to a lane based on the center of its
bounding box.

## Output
The system outputs lane-wise vehicle counts in the following format
once per second:

```json
{
  "north": 10,
  "east": 6,
  "south": 14,
  "west": 4
}
