# TrafficIQ

## AI-Powered Smart Traffic Monitoring and Intelligent Traffic Management System

**Version:** 1.0

**Status:** Final Design Specification

**Project Type:** End-to-End Artificial Intelligence System

**Target Platform:** Streamlit Community Cloud

**Primary Language:** Python 3.11+

---

# 1. Project Overview

## 1.1 Introduction

TrafficIQ is an AI-powered intelligent traffic monitoring and analytics platform capable of automatically analyzing traffic videos using Computer Vision and Machine Learning.

Unlike traditional traffic monitoring systems that simply detect vehicles, TrafficIQ performs complete traffic intelligence by combining:

* Object Detection
* Vehicle Tracking
* Traffic Signal Recognition
* Feature Engineering
* Machine Learning
* Time-Series Forecasting
* Interactive Geographic Visualization
* AI-powered Traffic Assistant

The system is designed to process uploaded traffic videos or live webcam streams, extract meaningful traffic information, generate structured datasets, predict traffic conditions, recommend signal timings, estimate emissions, visualize analytics on an interactive map, and answer traffic-related questions using an AI assistant.

The project emphasizes modularity, reproducibility, scalability, and production-oriented software engineering practices.

---

# 2. Project Objectives

The project has the following primary objectives:

### Computer Vision

Detect traffic objects from videos.

Detect:

* Cars
* Motorcycles
* Trucks
* Buses
* Auto Rickshaws
* Bicycles
* Pedestrians
* Traffic Lights
* Traffic Signs

---

### Traffic Analysis

Generate meaningful traffic statistics including

* Vehicle Count
* Vehicle Distribution
* Queue Length
* Average Speed
* Waiting Time
* Road Occupancy
* Heavy Vehicle Ratio

---

### Traffic Intelligence

Predict

* Traffic Density
* Congestion Level
* Signal Timing
* Future Traffic Conditions
* Vehicle Emissions

---

### Visualization

Provide an interactive dashboard displaying

* Live processed video
* Vehicle statistics
* Graphs
* Interactive map
* Predictions
* Recommendations

---

### Artificial Intelligence Assistant

Provide an AI assistant capable of explaining

* Traffic conditions
* Congestion causes
* Predicted trends
* Signal recommendations
* Emission statistics

---

# 3. Project Philosophy

TrafficIQ follows one fundamental principle.

> **Computer Vision should run only once.**

The video should never be repeatedly processed by multiple independent models.

Instead,

Computer Vision generates structured information once.

All Machine Learning models learn only from structured data.

This architecture significantly improves

* speed
* modularity
* maintainability
* explainability
* deployment

---

# 4. System Workflow

```
Video
    │
    ▼
Frame Extraction
    │
    ▼
YOLO Object Detection
    │
    ▼
ByteTrack Tracking
    │
    ▼
HSV Traffic Signal Detection
    │
    ▼
Feature Generation
    │
    ▼
feature_dataset.csv
    │
    ├────────► Traffic Density Model
    │
    ├────────► Congestion Prediction
    │
    ├────────► Signal Optimization
    │
    ├────────► Traffic Forecasting
    │
    └────────► Emission Estimation
                    │
                    ▼
            Streamlit Dashboard
                    │
                    ▼
             AI Traffic Assistant
```

---

# 5. Complete Technology Stack

## Programming Language

Python 3.11+

---

## Deep Learning

PyTorch

Ultralytics YOLOv11

TorchVision

---

## Machine Learning

scikit-learn

XGBoost

LightGBM

CatBoost (optional benchmarking)

Joblib

---

## Computer Vision

OpenCV

NumPy

Pillow

ByteTrack

HSV Color Segmentation

---

## Data Processing

Pandas

NumPy

Polars (optional)

---

## Visualization

Plotly

Matplotlib

Altair

---

## Dashboard

Streamlit

---

## Backend

FastAPI

Uvicorn

Pydantic

---

## Database

SQLite

SQLAlchemy

---

## Interactive Maps

OpenStreetMap

Leaflet

Folium

---

## AI Assistant

OpenAI API (configurable)

Prompt Engineering

Context-based Responses

---

## Deployment

GitHub

Streamlit Community Cloud

---

# 6. Project Folder Structure

```
TrafficIQ/

│
├── README.md
├── Project.md
├── requirements.txt
├── config.py
├── .gitignore
├── LICENSE
│
├── notebooks/
│
├── datasets/
│
├── models/
│
├── src/
│
├── app/
│
├── database/
│
├── outputs/
│
├── reports/
│
├── logs/
│
├── configs/
│
├── tests/
│
└── deployment/
```

---

# 7. Detailed Folder Structure

## notebooks/

Contains complete model development.

```
notebooks/

01_dataset_preparation.ipynb

02_preprocessing.ipynb

03_yolo_training.ipynb

04_vehicle_tracking.ipynb

05_feature_generation.ipynb

06_traffic_density.ipynb

07_congestion_prediction.ipynb

08_signal_optimization.ipynb

09_traffic_forecasting.ipynb

10_emission_estimation.ipynb

11_model_evaluation.ipynb

12_streamlit_testing.ipynb
```

Every notebook must

* save outputs
* save trained models
* save plots
* save metrics
* never overwrite previous experiments

---

## datasets/

```
datasets/

raw/

processed/

external/

generated/

training/

testing/

validation/
```

---

### raw/

Contains

Original videos

Original images

Original datasets

Nothing should ever be modified here.

---

### processed/

Contains

Cleaned datasets

Generated datasets

Feature CSVs

Tracking outputs

---

### external/

Contains downloaded datasets

Example

BDD100K

IDD

---

### generated/

Contains datasets generated by the pipeline.

Example

```
feature_dataset.csv

detections.csv

tracking.csv

statistics.csv
```

---

# 8. Models Folder

```
models/

yolo/

traffic_density/

congestion/

signal/

forecast/

emission/

metadata/
```

---

## YOLO

```
models/yolo/

best.pt

last.pt

training_metrics.json

training_history.csv

confusion_matrix.png

results.png

model_info.json
```

---

## Traffic Density

```
models/traffic_density/

best_model.joblib

scaler.joblib

encoder.joblib

metrics.json

feature_importance.csv

training_history.csv
```

---

## Congestion

```
models/congestion/

best_model.joblib

scaler.joblib

encoder.joblib

metrics.json

classification_report.txt
```

---

## Signal Optimization

```
models/signal/

best_model.joblib

metrics.json

feature_importance.csv
```

---

## Forecast

```
models/forecast/

best_model.keras

scaler.joblib

history.csv

metrics.json
```

---

## Emission

```
models/emission/

best_model.joblib

scaler.joblib

metrics.json
```

---

# 9. Source Code Structure

```
src/

detection/

tracking/

signal_detection/

feature_engineering/

density/

congestion/

signal_optimizer/

forecasting/

emission/

database/

assistant/

utils/
```

Each folder must be completely independent.

No notebook should contain reusable business logic.

Every reusable component belongs inside **src/**.

---

# 10. Application Structure

```
app/

Home.py

pages/

components/

assets/

api/

styles/
```

---

## Home.py

Responsible for

* Upload Video
* Webcam
* Project Overview
* Processing Status

---

## Pages

```
Dashboard

Map

Predictions

Analytics

AI Assistant

Settings
```

---

# 11. Configuration Management

Every configurable value must be stored outside the code.

Example

```
configs/

app.yaml

model.yaml

database.yaml

paths.yaml

thresholds.yaml
```

Hardcoded paths are strictly prohibited.

Every module must read paths from configuration files.

---

# 12. Coding Standards

The implementation generated from this specification **must follow these mandatory rules**:

### No hardcoded absolute paths

❌

```
C:\Users\Mihir\Desktop\Dataset
```

✔

```
DATASET_PATH = config.DATASET_PATH
```

---

### No notebook-specific imports

Every reusable function belongs inside

```
src/
```

---

### Every notebook must be executable independently

A notebook must never rely on variables created in another notebook.

Each notebook should load the required datasets, models, or configuration files explicitly.

---

### Every trained model must be saved

Training a model without saving it is prohibited.

Every notebook that trains a model must save:

* Trained weights
* Configuration
* Metrics
* Evaluation plots
* Metadata

---

### Every experiment must be reproducible

Random seeds should be fixed wherever applicable.

Configuration values should be externalized.

Dependencies should be version-pinned in `requirements.txt`.

---

---

# 13. Dataset Strategy

## 13.1 Philosophy

TrafficIQ is **not** designed around finding one perfect dataset.

Instead, the project builds its **own structured dataset** from traffic videos.

The architecture follows:

```text
Traffic Videos
        │
        ▼
YOLO Object Detection
        │
        ▼
Vehicle Tracking
        │
        ▼
Traffic Light Detection
        │
        ▼
Feature Engineering
        │
        ▼
Generated Dataset
(feature_dataset.csv)
        │
        ▼
Machine Learning Models
```

This allows every ML model to be trained using the same standardized feature set.

---

# 14. Dataset Sources

## Object Detection Dataset

YOLO will be trained from scratch using

Primary Dataset

```
BDD100K
```

Fine-tuning Dataset

```
Indian Driving Dataset (IDD)
```

Purpose

* Indian traffic adaptation
* Auto Rickshaw detection
* Better dense traffic detection

---

## Video Dataset

Traffic videos are used only for inference and feature generation.

Videos should contain

* Intersections
* Highways
* Urban roads
* Day
* Evening
* Night
* Rain
* Heavy traffic
* Light traffic

Videos are stored inside

```
datasets/raw/videos/
```

---

# 15. Computer Vision Pipeline

Only **one deep learning model** is trained.

```
YOLOv11
```

Everything else uses deterministic algorithms.

Complete pipeline

```text
Video

↓

Frame Extraction

↓

YOLO

↓

ByteTrack

↓

HSV Signal Detection

↓

Feature Generation
```

---

# 16. Notebook 01

## Dataset Preparation

Notebook

```
01_dataset_preparation.ipynb
```

Purpose

Prepare

* images
* labels
* YAML
* train
* validation
* test

Outputs

```
datasets/training/

datasets/validation/

datasets/testing/

dataset.yaml
```

No models are trained.

---

# 17. Notebook 02

## Data Preprocessing

Purpose

Image preprocessing

Tasks

* Remove corrupt images
* Verify labels
* Resize verification
* Dataset statistics
* Class distribution
* Dataset visualization

Outputs

```
reports/dataset_statistics.csv

reports/class_distribution.csv

reports/sample_images/

reports/dataset_report.md
```

---

# 18. Notebook 03

# YOLOv11 Training

Purpose

Train Object Detection model.

Input

```
datasets/training

dataset.yaml
```

Output

```
models/yolo/

best.pt

last.pt

results.png

training_metrics.json

training_history.csv

confusion_matrix.png

model_info.json
```

---

## Detected Classes

YOLO must detect

```
Car

Motorcycle

Truck

Bus

Auto Rickshaw

Bicycle

Pedestrian

Traffic Light

Traffic Sign
```

No additional classes should be added unless explicitly approved.

---

## YOLO Output

Every frame returns

```
Bounding Box

Confidence

Class

Center X

Center Y

Width

Height
```

---

# 19. Notebook 04

# Vehicle Tracking

Purpose

Track every detected object.

Algorithm

```
ByteTrack
```

No training required.

---

## Inputs

```
YOLO detections
```

---

## Outputs

For every detected vehicle

```
Vehicle ID

Frame Number

X

Y

Speed

Direction

Movement Status

Track History
```

---

Output CSV

```
tracking.csv
```

---

Example

| Frame | Vehicle_ID | Class | Speed | Direction |
| ----- | ---------- | ----- | ----- | --------- |
| 120   | 7          | Car   | 31.2  | North     |

---

Saved inside

```
datasets/generated/
```

---

# 20. Traffic Signal Recognition

No AI model is trained.

Pipeline

```text
YOLO

↓

Traffic Light Bounding Box

↓

Crop

↓

HSV

↓

Color Detection
```

---

Purpose

Determine

```
Red

Yellow

Green
```

---

Output

```
signal_states.csv
```

Example

| Frame | Signal |
| ----- | ------ |
| 120   | Red    |
| 121   | Red    |
| 122   | Green  |

---

# 21. HSV Detection

Algorithm

```
RGB

↓

HSV

↓

Red Mask

↓

Yellow Mask

↓

Green Mask

↓

Largest Pixel Count

↓

Signal State
```

Advantages

* no training

* no dataset

* lightweight

* reproducible

---

# 22. Notebook 05

# Feature Engineering

This notebook is the **most important notebook** in the project.

Everything after this notebook depends on it.

---

Inputs

```
YOLO Output

tracking.csv

signal_states.csv
```

---

Output

```
feature_dataset.csv
```

---

# 23. Feature Engineering Pipeline

```text
YOLO Objects

+

Tracking Information

+

Signal State

↓

Statistics

↓

Feature Engineering

↓

feature_dataset.csv
```

---

# 24. Feature List

The generated dataset should contain the following features.

## Time

```
Timestamp

Frame Number

Video Name
```

---

## Vehicle Counts

```
Car Count

Bike Count

Truck Count

Bus Count

Auto Count

Bicycle Count

Pedestrian Count

Total Vehicle Count
```

---

## Signal Information

```
Signal State
```

Possible values

```
Red

Yellow

Green
```

---

## Traffic Features

```
Average Speed

Maximum Speed

Minimum Speed

Median Speed

Queue Length

Waiting Time

Road Occupancy

Moving Vehicles

Stopped Vehicles

Heavy Vehicle Ratio

Traffic Flow Rate

Vehicle Density Estimate
```

---

## Environmental Features

```
Time of Day

Day/Night

Weather (optional)

Road Type (optional)
```

---

# 25. Feature Dataset Example

| Timestamp | Cars | Bike | Truck | Bus | Auto | Pedestrian | Avg Speed | Queue | Waiting | Signal | Occupancy |
| --------- | ---- | ---- | ----- | --- | ---- | ---------- | --------- | ----- | ------- | ------ | --------- |
| 09:30:01  | 32   | 21   | 3     | 2   | 9    | 14         | 28.3      | 11    | 7.4     | Green  | 61        |

---

# 26. Feature Dataset Storage

Generated dataset

```
datasets/generated/

feature_dataset.csv
```

---

Additional generated files

```
feature_statistics.csv

feature_summary.json

correlation_matrix.csv
```

---

# 27. Feature Engineering Outputs

The notebook must generate

```
feature_dataset.csv

feature_statistics.csv

feature_summary.json

missing_values.csv

correlation_matrix.csv

feature_distribution/

plots/
```

---

# 28. Data Validation

The notebook must validate

Missing Values

Duplicate Rows

Invalid Speeds

Negative Counts

Invalid Queue Length

Invalid Signal Labels

Outliers

Invalid Frame Numbers

---

Validation report

```
reports/feature_validation.md
```

---

# 29. Machine Learning Input Contract

Every downstream model **must only read**

```
feature_dataset.csv
```

No model is allowed to

* reopen videos

* rerun YOLO

* rerun tracking

* rerun HSV

This keeps the project modular.

---

# 30. Saved Data Flow

```text
Video

↓

YOLO

↓

detections.csv

↓

ByteTrack

↓

tracking.csv

↓

HSV

↓

signal_states.csv

↓

Feature Engineering

↓

feature_dataset.csv

↓

Machine Learning
```

---

# 31. Generated Files

After Notebook 05 completes, the following files must exist.

```
datasets/generated/

detections.csv

tracking.csv

signal_states.csv

feature_dataset.csv

feature_statistics.csv

feature_summary.json

correlation_matrix.csv
```

---

# 32. Rules for Notebook 05

The notebook **must not**

❌ Train ML models

❌ Predict congestion

❌ Predict density

❌ Predict emissions

❌ Predict signals

Its only responsibility is

```
Generate feature_dataset.csv
```

Every subsequent notebook depends exclusively on this dataset.

---
---

# 33. Machine Learning Pipeline

After `feature_dataset.csv` has been generated, the Computer Vision stage is complete.

Every Machine Learning model in TrafficIQ **must use only the generated feature dataset**.

The original videos must **never** be processed again.

---

# Complete ML Pipeline

```text
feature_dataset.csv
          │
          ▼
 ┌────────────────────┐
 │ Traffic Density    │
 └────────────────────┘
          │
          ▼
 ┌────────────────────┐
 │ Congestion Model   │
 └────────────────────┘
          │
          ▼
 ┌────────────────────┐
 │ Signal Optimizer   │
 └────────────────────┘
          │
          ▼
 ┌────────────────────┐
 │ Traffic Forecast   │
 └────────────────────┘
          │
          ▼
 ┌────────────────────┐
 │ Emission Model     │
 └────────────────────┘
```

---

# 34. Notebook 06

# Traffic Density Prediction

Notebook

```
06_traffic_density.ipynb
```

---

## Objective

Predict the current traffic density.

The model learns from traffic features generated from the Computer Vision pipeline.

---

## Input Dataset

```
datasets/generated/

feature_dataset.csv
```

---

## Input Features

The model may use

```
Car Count

Bike Count

Truck Count

Bus Count

Auto Count

Pedestrian Count

Average Speed

Maximum Speed

Minimum Speed

Queue Length

Waiting Time

Road Occupancy

Heavy Vehicle Ratio

Traffic Flow Rate

Signal State

Time of Day
```

---

## Target

Traffic Density

Recommended representation

```
Continuous Percentage

0–100%
```

Example

```
12%

38%

61%

93%
```

Regression is preferred over classification because the dashboard can later categorize the values if needed.

---

## Candidate Models

Train and compare

```
Random Forest Regressor

XGBoost Regressor

LightGBM Regressor
```

---

## Model Selection

The notebook must automatically choose the best model using

Primary Metric

```
R² Score
```

Secondary Metrics

```
MAE

RMSE

MAPE
```

---

## Saved Outputs

```
models/traffic_density/

best_model.joblib

scaler.joblib

feature_columns.json

metrics.json

feature_importance.csv

training_history.csv
```

---

## Notebook Outputs

```
Prediction Distribution

Residual Plot

Feature Importance

Metrics Table

Cross Validation Scores
```

---

# 35. Notebook 07

# Congestion Prediction

Notebook

```
07_congestion_prediction.ipynb
```

---

## Objective

Predict traffic congestion.

---

## Inputs

```
feature_dataset.csv
```

---

## Input Features

```
Vehicle Counts

Average Speed

Queue Length

Road Occupancy

Heavy Vehicle Ratio

Traffic Density Prediction

Signal State

Time of Day
```

---

## Target

```
Low

Moderate

High

Critical
```

---

## Candidate Models

```
Random Forest

XGBoost

LightGBM
```

---

## Evaluation Metrics

```
Accuracy

Precision

Recall

F1 Score

ROC AUC (if applicable)
```

---

## Saved Outputs

```
models/congestion/

best_model.joblib

label_encoder.joblib

metrics.json

classification_report.txt

confusion_matrix.png

feature_importance.csv
```

---

# 36. Notebook 08

# Signal Timing Optimization

Notebook

```
08_signal_optimization.ipynb
```

---

## Objective

Recommend the optimal green signal duration.

---

## Important Design Decision

This notebook **does not detect the current signal state**.

Current signal state already comes from

```
YOLO

↓

HSV
```

This notebook predicts

```
Recommended Green Duration
```

---

## Inputs

```
feature_dataset.csv
```

---

## Features

```
Traffic Density

Congestion Level

Vehicle Counts

Queue Length

Average Speed

Heavy Vehicle Ratio

Signal State
```

---

## Target

```
Green Time (seconds)
```

Example

```
18

25

41

63
```

---

## Candidate Models

```
Random Forest Regressor

XGBoost Regressor

LightGBM Regressor
```

---

## Output

Dashboard displays

```
Current Signal

↓

Red

↓

Recommended Green Time

↓

47 seconds
```

---

## Saved Outputs

```
models/signal/

best_model.joblib

metrics.json

feature_importance.csv
```

---

# 37. Notebook 09

# Traffic Forecasting

Notebook

```
09_traffic_forecasting.ipynb
```

---

## Objective

Predict future traffic conditions.

---

## Inputs

Historical feature dataset.

Time-series sequences generated from

```
feature_dataset.csv
```

---

## Features

```
Historical Density

Historical Vehicle Count

Historical Queue Length

Historical Speed

Historical Occupancy
```

---

## Targets

Predict

```
Traffic after

5 minutes

15 minutes

30 minutes
```

---

## Candidate Models

```
LSTM

GRU
```

---

## Evaluation

```
MAE

RMSE

MAPE
```

---

## Saved Outputs

```
models/forecast/

best_model.keras

history.csv

metrics.json

sequence_config.json

scaler.joblib
```

---

# 38. Notebook 10

# Emission Estimation

Notebook

```
10_emission_estimation.ipynb
```

---

## Objective

Estimate emissions based on detected traffic.

---

## Inputs

```
feature_dataset.csv
```

---

## Features

```
Car Count

Bike Count

Truck Count

Bus Count

Average Speed

Waiting Time

Queue Length

Road Occupancy

Traffic Density
```

---

## Targets

Estimate

```
CO₂

NOx

PM2.5

Fuel Consumption
```

---

## Candidate Models

```
Random Forest

XGBoost

LightGBM
```

---

## Output

Dashboard

```
Emission Level

↓

Moderate

↓

CO₂

315 kg/hour

↓

Fuel Consumption

92 L/hour
```

---

## Saved Outputs

```
models/emission/

best_model.joblib

metrics.json

feature_importance.csv

scaler.joblib
```

---

# 39. Notebook 11

# Model Evaluation

Notebook

```
11_model_evaluation.ipynb
```

---

## Purpose

Evaluate every trained model.

Generate

```
Performance Comparison

Model Rankings

Prediction Samples

Error Analysis

Cross Validation

Inference Speed

Memory Usage
```

---

## Output

```
reports/model_comparison.csv

reports/model_summary.md

reports/final_metrics.json

reports/evaluation_plots/
```

---

# 40. Saved Model Architecture

Every model must be stored independently.

```
models/

traffic_density/

congestion/

signal/

forecast/

emission/
```

No notebook should overwrite another notebook's outputs.

---

# 41. Model Metadata

Every trained model must save

```
Model Name

Training Date

Training Dataset

Features Used

Target Variable

Metrics

Library Version

Random Seed
```

Stored as

```
model_info.json
```

---

# 42. Model Loading

No notebook may retrain models during inference.

Inference modules must

```
Load Model

↓

Load Scaler

↓

Predict

↓

Return Results
```

---

# 43. Feature Consistency

Every inference module must verify

```
Feature Count

Feature Names

Feature Order

Data Types
```

If mismatch occurs

Raise an exception.

Never silently continue.

---

# 44. Prediction Pipeline

```
feature_dataset.csv
        │
        ▼
Traffic Density
        │
        ▼
Congestion Prediction
        │
        ▼
Signal Optimization
        │
        ▼
Traffic Forecast
        │
        ▼
Emission Estimation
```

---

# 45. Output JSON Contract

Every prediction module should return a standardized dictionary/object.

Example:

```json
{
  "model_name": "traffic_density",
  "prediction": 71.3,
  "confidence": 0.94,
  "timestamp": "2026-07-29T10:45:00",
  "processing_time_ms": 18
}
```

This standard makes integration with FastAPI and Streamlit much simpler.

---

# 46. Model Storage Rules

Every trained notebook must save:

### Model

```
best_model.joblib
```

### Scaler

```
scaler.joblib
```

### Encoder (if applicable)

```
encoder.joblib
```

### Metadata

```
model_info.json
```

### Metrics

```
metrics.json
```

### Feature List

```
feature_columns.json
```

### Feature Importance

```
feature_importance.csv
```

---

# 47. Model Selection Rules

Each notebook must:

* Train all candidate models.
* Compare them using the defined evaluation metrics.
* Select the best-performing model automatically.
* Save **only the best model** as the production model.
* Save comparison results for all candidate models.

This ensures the deployment always uses the strongest model while preserving benchmarking results.

---

# 48. ML Development Rules

Every ML notebook **must**:

* Use train/validation/test splits.
* Set a fixed random seed.
* Avoid data leakage.
* Save preprocessing objects (scalers, encoders).
* Save evaluation plots.
* Never hardcode feature lists.
* Load feature names dynamically from the generated dataset.
* Be runnable independently without relying on previous notebook variables.

---

---

# 49. Software Architecture

TrafficIQ follows a **layered modular architecture**.

Each layer has a single responsibility.

```text
                        User
                          │
                          ▼
                  Streamlit Frontend
                          │
                    REST API Calls
                          │
                          ▼
                    FastAPI Backend
                          │
        ┌─────────────────┼──────────────────┐
        ▼                 ▼                  ▼
 Computer Vision      ML Inference      AI Assistant
        │                 │                  │
        └─────────────────┼──────────────────┘
                          ▼
                    SQLite Database
```

Each layer must be completely independent.

---

# 50. Why Streamlit + FastAPI?

The application **must not** place all code inside Streamlit.

Instead

```text
Streamlit

↓

Requests

↓

FastAPI

↓

Models
```

Advantages

* Models load only once
* Faster inference
* Cleaner code
* Easier debugging
* Easier deployment
* Easier future mobile integration

---

# 51. Application Workflow

## Video Upload Mode

```text
User Uploads Video

↓

Video Validation

↓

Video Saved

↓

Processing Starts

↓

Frame Extraction

↓

YOLO Detection

↓

ByteTrack

↓

HSV Detection

↓

Feature Generation

↓

ML Predictions

↓

Database Save

↓

Dashboard
```

---

## Webcam Mode

```text
Webcam

↓

Capture Frames

↓

Temporary Video Buffer

↓

Process Buffer

↓

Generate Features

↓

Predictions

↓

Dashboard
```

Webcam processing should follow the same pipeline as uploaded videos.

---

# 52. Streamlit Structure

```text
app/

Home.py

pages/

components/

assets/

styles/

utils/
```

---

## Home.py

Responsibilities

* Project introduction
* Upload video
* Webcam input
* Processing progress
* Processing status
* Navigation

No prediction logic should exist here.

---

# 53. Pages Structure

```text
pages/

01_Dashboard.py

02_Map.py

03_Analytics.py

04_Predictions.py

05_AI_Assistant.py

06_System_Status.py
```

---

## Dashboard

Displays

* Uploaded video
* Processed video
* Current traffic statistics
* Traffic density
* Congestion level
* Signal recommendation
* Emissions

---

## Analytics

Displays

* Vehicle distribution
* Speed distribution
* Queue analysis
* Traffic trends
* Density history

---

## Predictions

Displays

* Density prediction
* Congestion prediction
* Signal recommendation
* Forecast
* Emission estimation

---

## AI Assistant

Displays

Chat interface.

The assistant receives

* Predictions
* Statistics
* Database results

It **must not** receive raw videos.

---

# 54. FastAPI Structure

```text
src/api/

main.py

routes/

schemas/

services/

middleware/
```

---

## Routes

```text
upload.py

predict.py

dashboard.py

assistant.py

map.py
```

---

# 55. REST Endpoints

## Upload

```text
POST

/upload
```

Input

Video

Output

Processing ID

---

## Process

```text
POST

/process
```

Starts complete pipeline.

---

## Prediction

```text
GET

/predictions
```

Returns

```json
{
 "density": 72.4,
 "congestion": "High",
 "recommended_green_time": 46,
 "forecast": "Traffic expected to decrease in 15 minutes",
 "emission_level": "Moderate"
}
```

---

## Dashboard

```text
GET

/dashboard
```

Returns

Current dashboard statistics.

---

## Assistant

```text
POST

/chat
```

Receives

User Question

Returns

LLM Response

---

# 56. SQLite Database

Database

```text
database/

trafficiq.db
```

---

Tables

```text
videos

processing_sessions

detections

tracking

features

predictions

system_logs
```

---

# 57. Database Schema

## videos

| Column      | Type     |
| ----------- | -------- |
| id          | INTEGER  |
| filename    | TEXT     |
| upload_time | DATETIME |
| duration    | REAL     |
| fps         | INTEGER  |
| resolution  | TEXT     |

---

## processing_sessions

| Column      | Type     |
| ----------- | -------- |
| id          | INTEGER  |
| video_id    | INTEGER  |
| status      | TEXT     |
| start_time  | DATETIME |
| finish_time | DATETIME |

---

## detections

Stores

YOLO outputs

---

## tracking

Stores

ByteTrack outputs

---

## features

Stores

Generated feature dataset.

---

## predictions

Stores

All ML predictions.

---

# 58. OpenStreetMap Integration

TrafficIQ must use

```text
OpenStreetMap

+

Leaflet

+

Folium
```

No paid APIs.

No API keys.

No billing.

---

## Purpose

The map is used for visualization only.

It should display

* Traffic location
* Density color
* Congestion marker
* Prediction popup

---

Example

```text
Ahmedabad Junction

🟢 Low

🟡 Moderate

🔴 High

⚫ Critical
```

---

# 59. Map Workflow

```text
Prediction

↓

Coordinates

↓

Folium

↓

Interactive Map

↓

Dashboard
```

---

## Marker Information

Popup

```text
Intersection Name

Vehicle Count

Density

Congestion

Average Speed

Signal State

Recommended Green Time
```

---

# 60. AI Traffic Assistant

Purpose

Explain predictions.

Not generate them.

---

Input

```text
Predictions

+

Statistics

+

User Question
```

---

Example

User

```text
Why is congestion high?
```

Assistant

```text
Congestion is currently high because

Vehicle Count increased by 42%

Average Speed dropped below 18 km/h

Queue Length exceeded 20 vehicles

Current signal is Red

Heavy Vehicle Ratio increased
```

---

The assistant **must never**

* read videos
* run YOLO
* rerun predictions

It only explains existing outputs.

---

# 61. Logging

All modules must generate logs.

```text
logs/

application.log

processing.log

training.log

errors.log
```

---

Every log entry should contain

```text
Timestamp

Module

Status

Execution Time

Message
```

---

# 62. Error Handling

Every module must use

```text
try

↓

except

↓

logging

↓

Raise Meaningful Error
```

Never use

```python
except:
    pass
```

---

# 63. Progress Tracking

During processing

The user should see

```text
Video Upload

██████████

Frame Extraction

████████

YOLO Detection

██████

Tracking

██████

Feature Generation

█████

Predictions

████

Dashboard Ready
```

---

# 64. Configuration Files

```text
configs/

paths.yaml

database.yaml

model.yaml

api.yaml

streamlit.yaml
```

No paths

No thresholds

No ports

should be hardcoded.

---

# 65. Local Run Workflow

```text
Clone Repository

↓

Install Requirements

↓

Run FastAPI

↓

Run Streamlit

↓

Upload Video

↓

Processing

↓

Dashboard
```

---

Commands

```bash
pip install -r requirements.txt

uvicorn src.api.main:app --reload

streamlit run app/Home.py
```

---

# 66. Deployment Workflow

Target

```text
Streamlit Community Cloud
```

---

Deployment Steps

```text
Push to GitHub

↓

Connect Repository

↓

Install Requirements

↓

Load Models

↓

Launch Streamlit
```

---

Important Rule

Deployment **must not retrain models**.

Only

Load

↓

Predict

↓

Display

---

# 67. Module Communication

```text
YOLO

↓

Tracking

↓

HSV

↓

Feature Engineering

↓

ML Models

↓

SQLite

↓

FastAPI

↓

Streamlit

↓

User
```

Every module should communicate through saved files, structured objects, or API responses—not shared notebook variables.

---

# 68. Security

Although authentication is intentionally omitted for this version, the application should still:

* Validate uploaded file types.
* Reject unsupported formats.
* Limit upload size.
* Sanitize filenames.
* Prevent accidental overwriting of existing outputs.
* Avoid exposing internal file paths or stack traces to the user.

---

# 69. Performance Expectations

Target processing goals (subject to hardware):

* Video loading: < 2 seconds
* Frame extraction: Real-time or faster than real-time
* YOLO inference: GPU preferred, CPU supported
* Feature generation: Streaming or batch
* Dashboard loading: < 3 seconds after processing completes

These are engineering targets, not strict guarantees.

---

---

# 70. Complete Project Directory Structure

The final project repository should follow the structure below. This organization ensures modularity, maintainability, and ease of collaboration.

```text
TrafficIQ/
│
├── README.md
├── Project.md
├── requirements.txt
├── LICENSE
├── .gitignore
├── config.py
│
├── configs/
│   ├── api.yaml
│   ├── app.yaml
│   ├── database.yaml
│   ├── model.yaml
│   ├── paths.yaml
│   ├── thresholds.yaml
│   └── streamlit.yaml
│
├── datasets/
│   ├── raw/
│   │   ├── videos/
│   │   ├── images/
│   │   └── labels/
│   │
│   ├── processed/
│   ├── generated/
│   ├── training/
│   ├── validation/
│   ├── testing/
│   └── external/
│
├── notebooks/
│   ├── 01_dataset_preparation.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_yolo_training.ipynb
│   ├── 04_vehicle_tracking.ipynb
│   ├── 05_feature_generation.ipynb
│   ├── 06_traffic_density.ipynb
│   ├── 07_congestion_prediction.ipynb
│   ├── 08_signal_optimization.ipynb
│   ├── 09_traffic_forecasting.ipynb
│   ├── 10_emission_estimation.ipynb
│   ├── 11_model_evaluation.ipynb
│   └── 12_streamlit_testing.ipynb
│
├── src/
├── app/
├── database/
├── models/
├── outputs/
├── reports/
├── logs/
├── tests/
└── deployment/
```

---

# 71. Responsibility of Every Folder

## configs/

Stores all configurable values.

Contains

* Model parameters
* Thresholds
* File paths
* Database configuration
* API configuration

---

## datasets/

Stores every dataset used by the project.

Never modify the raw datasets.

Generated datasets should always be stored separately.

---

## notebooks/

Responsible only for

* experimentation
* model training
* evaluation

No reusable business logic should remain inside notebooks.

---

## src/

Contains reusable Python modules.

Every notebook should import from here.

This is the heart of the project.

---

## app/

Contains the complete Streamlit application.

No training code belongs here.

Only

* model loading
* inference
* visualization
* user interaction

---

## models/

Contains every trained model.

No temporary files.

Only production-ready models.

---

## reports/

Contains

* graphs
* evaluation reports
* comparison reports
* markdown summaries
* confusion matrices

---

## logs/

Stores application logs.

Should rotate automatically when files become too large.

---

## outputs/

Stores

* processed videos
* processed images
* prediction outputs
* temporary visualization files

---

## tests/

Contains automated testing scripts.

---

# 72. Notebook Dependency Graph

The notebooks must be executed in the following order.

```text
01 Dataset Preparation
          │
          ▼
02 Preprocessing
          │
          ▼
03 YOLO Training
          │
          ▼
04 Vehicle Tracking
          │
          ▼
05 Feature Engineering
          │
          ▼
06 Density Prediction
          │
          ▼
07 Congestion Prediction
          │
          ▼
08 Signal Optimization
          │
          ▼
09 Traffic Forecasting
          │
          ▼
10 Emission Estimation
          │
          ▼
11 Model Evaluation
          │
          ▼
12 Streamlit Testing
```

Skipping notebooks is not recommended unless their outputs already exist.

---

# 73. Saved Artifacts

After completing the project, the repository should contain the following important artifacts.

## Models

```text
best.pt

traffic_density.joblib

congestion.joblib

signal.joblib

forecast.keras

emission.joblib
```

---

## Datasets

```text
detections.csv

tracking.csv

signal_states.csv

feature_dataset.csv
```

---

## Reports

```text
evaluation_report.md

dataset_report.md

model_comparison.csv

final_metrics.json
```

---

## Database

```text
trafficiq.db
```

---

# 74. Testing Strategy

Every module should be tested independently before integration.

---

## Unit Testing

Verify

* helper functions
* utility functions
* preprocessing functions
* feature engineering

---

## Integration Testing

Verify

```text
YOLO

↓

Tracking

↓

HSV

↓

Feature Generation
```

works correctly.

---

## End-to-End Testing

Verify

```text
Upload Video

↓

Processing

↓

Predictions

↓

Dashboard
```

without failures.

---

## Performance Testing

Measure

* Processing time
* GPU utilization
* CPU utilization
* Memory usage
* Inference speed

---

# 75. Coding Standards

The project must follow the following conventions.

---

## Naming

Variables

```python
vehicle_count
```

Functions

```python
calculate_density()
```

Classes

```python
TrafficPredictor
```

Constants

```python
MAX_QUEUE_LENGTH
```

---

## Documentation

Every public function should contain

* description
* parameters
* return values
* exceptions

using standard Python docstrings.

---

## Comments

Only explain

* complex algorithms
* important assumptions
* optimization decisions

Avoid obvious comments.

---

## Imports

Use absolute imports.

Avoid circular dependencies.

Group imports into

1. Standard library
2. Third-party libraries
3. Local modules

---

# 76. Development Rules

The following rules are mandatory.

### Rule 1

Never retrain models during inference.

---

### Rule 2

Always load saved models.

---

### Rule 3

Never hardcode file paths.

---

### Rule 4

Never duplicate code.

---

### Rule 5

Every module must be reusable.

---

### Rule 6

Every notebook must run independently.

---

### Rule 7

Every model must save metadata.

---

### Rule 8

Every experiment must be reproducible.

---

### Rule 9

Handle all expected exceptions gracefully.

---

### Rule 10

Log every important processing step.

---

# 77. LLM Implementation Rules

This document is intended to guide another LLM in implementing the project.

The implementation agent should follow these principles:

1. Never invent missing datasets.
2. Never fabricate prediction values.
3. Prefer deterministic algorithms when possible.
4. Use production-ready coding practices.
5. Keep modules loosely coupled.
6. Follow the defined folder structure.
7. Preserve compatibility across operating systems.
8. Write clean, documented, maintainable code.
9. Validate all inputs before processing.
10. Reuse existing modules instead of rewriting logic.

---

# 78. Future Improvements

Potential future enhancements include:

### Computer Vision

* Multi-camera support
* Drone traffic analysis
* Accident detection
* Lane detection
* Illegal parking detection
* Wrong-way driving detection
* Emergency vehicle prioritization

---

### Machine Learning

* Reinforcement learning for adaptive traffic signals
* Graph Neural Networks for road network modeling
* Federated learning across cities
* Online learning for continuous model updates

---

### Dashboard

* Real-time alerts
* Historical analytics
* Custom dashboards
* Mobile-responsive interface

---

### AI Assistant

* Voice interaction
* Multilingual support
* Natural language report generation
* Automatic traffic incident summaries

---

### Deployment

* Docker containerization
* Kubernetes orchestration
* Cloud GPU inference
* Distributed processing

---

# 79. Project Deliverables

The completed project should include:

### Source Code

* Complete Python implementation
* Modular package structure
* Streamlit application
* FastAPI backend

---

### Models

* Trained YOLO model
* All trained ML models
* Saved preprocessing objects
* Metadata files

---

### Datasets

* Generated feature dataset
* Detection outputs
* Tracking outputs
* Signal state outputs

---

### Documentation

* README.md
* Project.md
* Installation guide
* User guide
* API documentation
* Model documentation

---

### Reports

* Dataset analysis
* Model evaluation
* Performance comparison
* Final project report

---

# 80. Success Criteria

The project will be considered complete when it satisfies the following:

* Uploads and validates videos successfully.
* Processes videos through YOLO, ByteTrack, and HSV pipelines.
* Generates all intermediate datasets correctly.
* Trains and saves all planned ML models.
* Produces consistent predictions from saved models.
* Displays results in a functional Streamlit dashboard.
* Stores processing information in SQLite.
* Provides AI-generated explanations based on prediction outputs.
* Maintains a modular, reproducible, and documented codebase.

---

# 81. Final Implementation Checklist

Before deployment, verify:

### Data

* [ ] Dataset prepared
* [ ] Dataset validated
* [ ] Feature dataset generated

---

### Computer Vision

* [ ] YOLO trained
* [ ] Tracking implemented
* [ ] HSV signal detection verified

---

### Machine Learning

* [ ] Density model trained
* [ ] Congestion model trained
* [ ] Signal optimization model trained
* [ ] Forecasting model trained
* [ ] Emission model trained

---

### Backend

* [ ] FastAPI operational
* [ ] Endpoints tested
* [ ] Models loaded successfully

---

### Frontend

* [ ] Streamlit pages complete
* [ ] Interactive charts functional
* [ ] Map visualization operational
* [ ] AI Assistant integrated

---

### Deployment

* [ ] Requirements verified
* [ ] Configuration files validated
* [ ] Repository cleaned
* [ ] Documentation completed
* [ ] Models included
* [ ] Final testing passed

---

# 82. Conclusion

TrafficIQ is designed as a comprehensive, end-to-end intelligent traffic analytics platform that combines modern computer vision, machine learning, software engineering, and interactive visualization into a single modular system.

The architecture intentionally separates **perception**, **feature engineering**, **prediction**, **backend services**, and **user interface** to ensure scalability, maintainability, and reproducibility. By relying on a single vision model (YOLOv11) for perception and building all downstream intelligence from structured features, the system minimizes redundant computation while providing a flexible foundation for future enhancements.

This document serves as the authoritative engineering specification for the implementation of TrafficIQ. Any future development, maintenance, or extension of the project should adhere to the architectural principles, module responsibilities, coding standards, and workflow definitions established here to preserve consistency and software quality.

---

# Document Information

**Project Name:** TrafficIQ – AI-Powered Smart Traffic Monitoring and Intelligent Traffic Management System

**Version:** 1.0

**Document Type:** Complete Engineering Specification (Project.md)

**Status:** Final

**Language:** Python 3.11+

**Primary Frameworks:** YOLOv11, ByteTrack, OpenCV, Streamlit, FastAPI, SQLite, Scikit-learn, XGBoost, LightGBM, PyTorch

**Target Deployment:** Streamlit Community Cloud

**Primary Objective:** Develop a modular, production-oriented AI traffic intelligence platform capable of transforming raw traffic videos into actionable insights, predictions, and decision support.
