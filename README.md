# Traffic Signal Violation Detection System

## 📝 Overview
This project is an **AI-based Traffic Signal Violation Detection System** that uses the **YOLOv8 object detection model** and **OpenCV** to detect vehicles violating traffic signals in real-time.  
The system monitors traffic lights, identifies active red lights, and flags vehicles that cross a designated **Region of Interest (ROI)** during a red signal.

It is designed for **smart traffic monitoring, automated law enforcement, and intelligent transportation systems**.

---

## 🎯 Features

- **Real-time Object Detection**: Detects vehicles such as cars, bicycles, motorcycles, buses, and trucks using YOLOv8.  
- **Traffic Light Monitoring**: Determines whether the red light is active using pixel analysis.  
- **Violation Detection**: Flags vehicles crossing the ROI during a red light.  
- **Visual Feedback**: Displays bounding boxes, polygons, and text overlays on the video feed.  
- **Configurable Confidence Threshold**: Adjusts detection confidence for fine-tuning.

---

## 🧠 Methodology

1. Video frames are extracted from the input traffic video.  
2. Traffic lights are detected and classified (Red, Yellow, Green).  
3. Vehicles are detected using **YOLOv8 deep learning model**.  
4. Violations are flagged when vehicles cross the ROI during a red light.  
5. Results are visualized and optionally saved as a video.

---

## 🏗️ System Architecture

![System Architecture](demo/system_architecture.png)  
*(Replace with your architecture diagram in `demo/system_architecture.png`)*

---

> **Note:** Large files (`tr.mp4` and `yolov8m.pt`) are hosted externally due to GitHub file size limits.

---

## 🎥 Demo Video

Download or watch the demo video here:  
[tr.mp4 Demo Video](https://drive.google.com/file/d/1jLGp96o1oMsi7MxVHpQLEMnpvxY-LXsg/view?usp=drive_link)

---

## 📥 YOLOv8 Model Weights

Download the YOLOv8 model here:  
[yolov8m.pt Model](https://drive.google.com/file/d/1l_n8OrFfarn2qHrWAD_3NmXb6L53GBmB/view?usp=drive_link)  

> Place the model in the `model/` folder before running the script.

---

## 📊 Sample Output

![Violation Detection Sample](demo/output_1.png)  
*(Replace with your own output screenshot in `demo/output_1.png`)*

---

## ⚙️ Requirements

Install Python dependencies using:

```bash
pip install -r requirements.txt

## 📂 Project Structure

