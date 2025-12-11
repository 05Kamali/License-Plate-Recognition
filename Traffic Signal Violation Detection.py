import cv2
import os
from ultralytics import YOLO
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

import time
import re


os.chdir(r"C:\Users\Kamali J\OneDrive\Project\DNN\Traffic.py")




RedLight = np.array([[998, 125],[998, 155],[972, 152],[970, 127]])
GreenLight = np.array([[971, 200],[996, 200],[1001, 228],[971, 230]])
ROI = np.array([[910, 372],[388, 365],[338, 428],[917, 441]])


model = YOLO("yolov8m.pt")
coco = model.model.names

TargetLabels = ["bicycle", "car", "motorcycle", "bus", "truck", "traffic light"]

# Check if light is on
def is_region_light(image, polygon, brightness_threshold=128):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(gray_image)
    cv2.fillPoly(mask, [np.array(polygon)], 255)
    roi = cv2.bitwise_and(gray_image, gray_image, mask=mask)
    mean_brightness = cv2.mean(roi, mask=mask)[0]
    return mean_brightness > brightness_threshold


def draw_text_with_background(frame, text, position, font, scale, text_color, background_color, border_color, thickness=2, padding=5):
    (text_width, text_height), baseline = cv2.getTextSize(text, font, scale, thickness)
    x, y = position
    cv2.rectangle(frame, (x - padding, y - text_height - padding), (x + text_width + padding, y + baseline + padding), background_color, cv2.FILLED)
    cv2.rectangle(frame, (x - padding, y - text_height - padding), (x + text_width + padding, y + baseline + padding), border_color, thickness)
    cv2.putText(frame, text, (x, y), font, scale, text_color, thickness, lineType=cv2.LINE_AA)


def extract_number_plate_text(frame, box):
    x, y, w, h = box
    
    vehicle_roi = frame[y:h, x:w]
    gray = cv2.cvtColor(vehicle_roi, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    custom_config = r'--oem 3 --psm 7'
    text = pytesseract.image_to_string(thresh, config=custom_config)
    # Clean OCR output
    text = re.sub(r'[^A-Z0-9]', '', text.upper())
    return text.strip()

# Start video capture
cap = cv2.VideoCapture("tr.mp4")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Number of frames have finished.")
        break
    frame = cv2.resize(frame, (1100, 700))
    cv2.polylines(frame, [RedLight], True, [0, 0, 255], 1)
    cv2.polylines(frame, [GreenLight], True, [0, 255, 0], 1)
    cv2.polylines(frame, [ROI], True, [255, 0, 0], 2)

    # YOLO prediction
    results = model.predict(frame, conf=0.75)
    for result in results:
        boxes = result.boxes.xyxy
        confs = result.boxes.conf
        classes = result.boxes.cls

        for box, conf, cls in zip(boxes, confs, classes):
            if coco[int(cls)] in TargetLabels:
                x, y, w, h = box
                x, y, w, h = int(x), int(y), int(w), int(h)
                cv2.rectangle(frame, (x, y), (w, h), [0, 255, 0], 2)
                draw_text_with_background(frame, 
                                          f"{coco[int(cls)].capitalize()}, conf:{(conf)*100:0.2f}%", 
                                          (x, y - 10), 
                                          cv2.FONT_HERSHEY_COMPLEX, 
                                          0.6, 
                                          (255, 255, 255),  
                                          (0, 0, 0),  
                                          (0, 0, 255))  

                # Check for traffic violation
                if is_region_light(frame, RedLight):
                    if cv2.pointPolygonTest(ROI, (x, y), False) >= 0 or cv2.pointPolygonTest(ROI, (w, h), False) >= 0:
                        draw_text_with_background(frame, 
                                                  f"The {coco[int(cls)].capitalize()} violated the traffic signal.", 
                                                  (10, 30), 
                                                  cv2.FONT_HERSHEY_COMPLEX, 
                                                  0.6, 
                                                  (255, 255, 255),  
                                                  (0, 0, 0),  
                                                  (0, 0, 255))  
                        cv2.polylines(frame, [ROI], True, [0, 0, 255], 2)
                        cv2.rectangle(frame, (x, y), (w, h), [0, 0, 255], 2)

                        # Extract number plate
                        plate_text = extract_number_plate_text(frame, (x, y, w, h))
                        if plate_text:
                            draw_text_with_background(frame, 
                                                      f"Number Plate: {plate_text}", 
                                                      (x, h + 20), 
                                                      cv2.FONT_HERSHEY_COMPLEX, 
                                                      0.6, 
                                                      (255, 255, 255),
                                                      (0, 0, 0),
                                                      (0, 255, 0))

    cv2.imshow("frame", frame)
    if cv2.waitKey(1) == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
