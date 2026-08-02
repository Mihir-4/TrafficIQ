# 🚦 TrafficIQ: AI-Powered Smart Traffic Intelligence Platform

**TrafficIQ** is an end-to-end, real-time Computer Vision and AI-driven Smart Traffic Intelligence Platform designed for dynamic traffic monitoring, automated signal management, environmental impact tracking, and executive analytics. Powered by custom **YOLOv8** object detection models, advanced multi-object tracking, and **Mistral AI** conversational intelligence, TrafficIQ turns video feeds into actionable urban mobility insights.

---

## ✨ Key Features

- **🎯 Multi-Class Vehicle Detection & Tracking**
  - Detects and tracks **10 fine-grained vehicle classes**: *Car, Bus, Truck, Auto-rickshaw, Motorcycle, Bicycle, Scooter, Van, Ambulance, and Fire Truck*.
  - Robust multi-object tracking (BYTETracker/LAP) with unique ID assignment, trajectory mapping, directional counting, and speed estimation.

- **🚨 Emergency Vehicle Priority & Alerting**
  - Instant detection and notification for critical emergency vehicles (*Ambulances* and *Fire Trucks*).
  - Triggers signal overrides and priority routing recommendations to reduce emergency response times.

- **⏱️ Dynamic Signal Timing & Congestion Index**
  - Computes real-time congestion scores (0–100 index) based on vehicle density, queue length, and lane occupancy.
  - Generates adaptive green light allocation suggestions to optimize traffic signal cycles and minimize intersection delay.

- **🌱 Environmental & CO₂ Emissions Modeling**
  - Estimates total carbon footprint ($\text{g CO}_2$) based on fleet composition, vehicle idle times, and traffic slowdowns.
  - Provides actionable environmental analytics to assist city planners in meeting sustainability benchmarks.

- **📊 Comprehensive Executive Dashboards & PDF Reporting**
  - Interactive multi-page **Streamlit** web dashboard styled with custom dark-mode glassmorphic aesthetics.
  - Rich interactive visualizations powered by **Plotly** and **Folium** maps.
  - Automated PDF report generation (via **ReportLab**) and Excel/CSV export capabilities for historical sessions.

- **🤖 Conversational AI Traffic Assistant**
  - Integrated with **Mistral AI** to provide intelligent traffic advisory, signal optimization recommendations, and natural language analytics queries.

---

## 🏗️ System Architecture & File Structure

```text
TrafficIQ/
├── app/                          # Streamlit Multi-Page Web Application
│   ├── Home.py                   # Main Executive Dashboard & KPI Overview
│   └── pages/
│       ├── 1_📹_Video_Upload.py   # Real-Time & File Video Processing Pipeline
│       ├── 3_📊_Analytics.py      # Interactive Congestion & Emissions Analytics
│       ├── 4_📜_History_&_Reports.py # Session History, SQLite Queries & PDF Exports
│       ├── 5_🤖_AI_Assistant.py   # AI Assistant for Smart Advisory
│       └── 6_⚙️_Settings.py      # System Configurations & Model Options
├── configs/                      # Project Configuration, Colors & Class Mappings
├── database/                     # SQLite Database Management & Data Schemas
├── models/                       # YOLO Weights & Computer Vision Inference Engines
├── scripts/                      # Core Analytics, Tracking Logic & Speed Calculation
├── utils/                        # UI Glassmorphic Styling, PDF Generators & Helpers
├── requirements.txt              # Core Dependencies
└── README.md                     # Documentation
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have **Python 3.9+** installed on your system. NVIDIA GPU with CUDA support is recommended for high-FPS real-time video processing, though CPU execution is fully supported.

### 2. Clone Repository & Install Dependencies

```bash
git clone https://github.com/Mihir-4/TrafficIQ.git
cd TrafficIQ
pip install -r requirements.txt
```

### 3. Launch the Application

Run the Streamlit application from the project root:

```bash
streamlit run app/Home.py
```

The web dashboard will automatically open in your browser at `http://localhost:8501`.

---

## 🛠️ Tech Stack & Libraries

- **Computer Vision & AI**: Ultralytics YOLOv8, OpenCV, PyTorch, LAP / BYTETracker
- **Web Interface**: Streamlit, Custom Glassmorphic CSS Engine
- **Data Visualization & Mapping**: Plotly Express, Matplotlib, Folium, Streamlit-Folium
- **Database & Storage**: SQLite, Pandas, NumPy
- **Reporting & Exports**: ReportLab (PDF Generation), OpenPyXL (Excel Export)
- **AI Assistant**: Mistral AI Integration (via Groq / Ollama API)

---

## 📜 License

This project is released under the **MIT License**.
