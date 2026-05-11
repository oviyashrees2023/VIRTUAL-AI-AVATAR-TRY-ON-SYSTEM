# AI Virtual Avatar Try-On System

## Project Overview

The AI Virtual Avatar Try-On System is an intelligent 3D virtual avatar generation and fashion try-on platform developed using Artificial Intelligence, Machine Learning, Flask, Three.js, Blender, and MakeHuman.

The system captures or uploads a user image, detects the facial structure using Machine Learning techniques, generates a suitable 3D avatar model, and allows users to virtually try hairstyles, eyebrows, and dresses in real time.

This project combines:

* Computer Vision
* Machine Learning
* 3D Graphics
* Web Technologies
* Human Modeling
* Virtual Fashion Rendering

---

# Features

## AI Face Shape Detection

* Detects user face shape from uploaded image
* Uses MediaPipe facial landmarks
* Extracts facial geometric ratios
* Predicts face shape using Random Forest Classifier

Supported face shapes:

* Oval
* Round
* Square
* Heart
* Diamond
* Triangle
* Rectangle

---

## 3D Avatar Generation

* Automatically selects avatar based on:

  * Gender
  * Face Shape
* Uses OBJ + MTL based 3D models
* Supports texture rendering
* Built using Three.js

---

## Virtual Fashion Try-On

Users can:

* Wear dresses
* Apply hairstyles
* Rotate avatar manually
* Zoom and inspect avatar

Supported assets:

* OBJ Models
* MTL Materials
* PNG/JPG textures

---

## Interactive 3D Viewer

Features:

* Real-time rendering
* Mouse rotation
* Zoom support
* OrbitControls integration
* Dynamic lighting
* Responsive UI

---

## Avatar Image Export

* Users can download avatar image
* PNG export support
* Renderer configured with preserveDrawingBuffer

---

# Technologies Used

| Category           | Technology            |
| ------------------ | --------------------- |
| Frontend           | HTML, CSS, JavaScript |
| 3D Rendering       | Three.js              |
| Backend            | Flask                 |
| Machine Learning   | Scikit-learn          |
| Computer Vision    | OpenCV                |
| Landmark Detection | MediaPipe             |
| 3D Modeling        | Blender               |
| Human Modeling     | MakeHuman             |
| ML Model Storage   | Joblib                |
| Version Control    | Git & GitHub          |

---

# System Architecture

```text
User Image
     ↓
Frontend Upload Interface
     ↓
Flask Backend API
     ↓
MediaPipe Landmark Extraction
     ↓
Feature Extraction
     ↓
Random Forest Face Shape Prediction
     ↓
Avatar Selection Engine
     ↓
Three.js 3D Rendering
     ↓
Virtual Try-On System
     ↓
Final Avatar Visualization
```

---

# Folder Structure

```text
VIRTUAL_AVATAR_SYSTEM/
│
├── backend/
│   ├── app.py
│   ├── features.py
│   ├── ml_face_shape.py
│   ├── train_model.py
│   ├── utils.py
│   ├── face_shape_model.pkl
│   ├── uploads/
│   └── face_shape_dataset/
│
├── frontend/
│   ├── index.html
│   ├── main.html
│   ├── capture.html
│   ├── avatar.html
│   └── js/
│       ├── api.js
│       └── avatar.js
│
├── models/
│   ├── male/
│   └── female/
│
├── dresses/
│   ├── male/
│   └── female/
│
├── hairstyles/
│   ├── male/
│   └── female/
│
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Dataset Information

The face shape dataset was collected from publicly available facial image datasets and categorized manually into different face shape classes.

## Dataset Distribution

| Face Shape | Samples |
| ---------- | ------- |
| Oval       | 797     |
| Round      | 789     |
| Square     | 799     |
| Heart      | 798     |
| Diamond    | 260     |
| Triangle   | 250     |
| Rectangle  | 900     |
| Total      | 4,593   |

---

# Train-Test Split

| Face Shape | Train | Test |
| ---------- | ----- | ---- |
| Oval       | 638   | 159  |
| Round      | 631   | 158  |
| Square     | 639   | 160  |
| Heart      | 638   | 160  |
| Diamond    | 208   | 52   |
| Triangle   | 200   | 50   |
| Rectangle  | 720   | 180  |
| Total      | 3,674 | 919  |

---

# Machine Learning Model

## Random Forest Classifier

The project uses Random Forest Classification for face shape prediction.

### Why Random Forest?

* High accuracy on structured facial ratio data
* Handles non-linear relationships
* Reduces overfitting
* Works well with small and medium datasets
* Stable predictions
* Good multi-class classification performance
* Handles imbalanced datasets better than many classifiers

---

# Feature Extraction

The system extracts:

* Face height
* Face width
* Jaw width
* Forehead width

Generated feature ratios:

```python
face_height / face_width
jaw_width / face_width
forehead_width / face_width
```

These ratios are used as input features for the Random Forest model.

---

# Face Landmark Detection

MediaPipe Face Mesh is used to extract 468 facial landmarks.

Important landmarks:

| Landmark | Purpose        |
| -------- | -------------- |
| 10       | Forehead       |
| 152      | Chin           |
| 234      | Left cheek     |
| 454      | Right cheek    |
| 172      | Left jaw       |
| 397      | Right jaw      |
| 127      | Left forehead  |
| 356      | Right forehead |

---

# Classifier Comparison

| Classifier          | Accuracy  | Speed     | Overfitting | Suitable              |
| ------------------- | --------- | --------- | ----------- | --------------------- |
| Random Forest       | High      | Fast      | Low         | Yes                   |
| SVM                 | High      | Medium    | Medium      | Moderate              |
| KNN                 | Medium    | Slow      | High        | No                    |
| Decision Tree       | Medium    | Fast      | Very High   | No                    |
| Logistic Regression | Medium    | Very Fast | Low         | No                    |
| CNN                 | Very High | Slow      | Medium      | Requires Huge Dataset |
| Naive Bayes         | Low       | Very Fast | Low         | No                    |

---

# 3D Modeling Workflow

## MakeHuman

Used for:

* Human avatar creation
* Body generation
* Gender-specific modeling

---

## Blender

Used for:

* OBJ export
* Dress fitting
* Hair alignment
* Texture fixing
* Shrinkwrap modifier
* Scaling and transformations

---

# Blender Workflow

## Removing Body and Keeping Dress Only

1. Import MakeHuman avatar into Blender
2. Select clothing object
3. Apply Shrinkwrap modifier
4. Separate clothing mesh
5. Delete body mesh
6. Export dress as OBJ + MTL

---

# Texture System

Textures are loaded using MTL files.

Example:

```mtl
map_Kd textures/uniformDiffuse.png
map_Bump textures/uniformNormal.png
```

Supported maps:

| Map      | Purpose         |
| -------- | --------------- |
| map_Kd   | Diffuse texture |
| map_Bump | Normal map      |
| map_d    | Transparency    |
| map_Ns   | Roughness       |
| map_refl | Metallic        |

---

# Backend API Endpoints

## Upload Image

```http
POST /upload
```

Uploads user image.

---

## Analyze Face

```http
POST /analyze-face
```

Predicts face shape.

---

## Get Avatar

```http
POST /get-avatar
```

Returns suitable avatar model.

---

## Get Dresses

```http
POST /get-dresses
```

Returns available dresses.

---

## Get Hairstyles

```http
POST /get-hairstyles
```

Returns hairstyles.

---

# Frontend Workflow

## main.html

Landing page.

## index.html

Gender selection.

## capture.html

Image upload and capture.

## avatar.html

3D avatar visualization.

---

# How to Run the Project

## Step 1 — Clone Repository

```bash
git clone https://github.com/oviyashrees2023/VIRTUAL-AI-AVATAR-TRY-ON-SYSTEM.git
```

---

## Step 2 — Open Project

```bash
cd VIRTUAL-AI-AVATAR-TRY-ON-SYSTEM
```

---

## Step 3 — Create Virtual Environment

```bash
python -m venv venv
```

---

## Step 4 — Activate Environment

### Windows

```bash
venv\Scripts\activate
```

---

## Step 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 6 — Run Flask Backend

```bash
cd backend
python app.py
```

---

## Step 7 — Run Frontend

Open:

```text
frontend/main.html
```

using Live Server.

---

# requirements.txt

```text
flask
flask-cors
opencv-python
mediapipe
numpy
scikit-learn
joblib
```

---

# Performance Metrics

| Metric      | Value |
| ----------- | ----- |
| Accuracy    | 92%   |
| Precision   | 91%   |
| Recall      | 90%   |
| F1 Score    | 90%   |
| Specificity | 93%   |

---

# Hyperparameters

| Parameter    | Value |
| ------------ | ----- |
| n_estimators | 100   |
| max_depth    | 10    |
| criterion    | gini  |
| random_state | 42    |

---

# Advantages

* Real-time avatar generation
* AI-based face shape detection
* Interactive virtual try-on
* Lightweight architecture
* High rendering quality
* Easy scalability
* User-friendly interface

---

# Limitations

* Requires proper lighting for image detection
* Limited hairstyle dataset
* No real-time animation yet
* Some high-poly OBJ files require optimization

---

# Future Enhancements

* AI outfit recommendation
* AR virtual try-on
* Real-time body tracking
* Full-body avatar generation
* Animation support
* Voice interaction
* Skin tone matching
* Cloth physics simulation
* GAN-based avatar realism

---

# GitHub Notes

## Files Included

* Python source code
* Frontend code
* OBJ models
* MTL files
* Textures
* ML model

## Files Excluded

* Blender source files (.blend)
* Temporary uploads
* Virtual environment
* Cache files

Reason:

Large Blender source files were excluded to reduce repository size and improve deployment efficiency.

---

# Pages

## Main Page

<img width="2559" height="1424" alt="image" src="https://github.com/user-attachments/assets/6b564f66-4dac-4b91-b2a5-2976b172a7d2" />


<img width="2559" height="1418" alt="image" src="https://github.com/user-attachments/assets/25914e4e-5f3d-40e9-b48d-f63e3f0a910c" />


## Gender Selection


<img width="2558" height="1429" alt="Screenshot 2026-05-11 151604" src="https://github.com/user-attachments/assets/ace8edc9-bfc1-47a7-a780-bfca46c6b04c" />



## Face Detection


<img width="2559" height="1416" alt="Screenshot 2026-05-11 151653" src="https://github.com/user-attachments/assets/f5083a8d-d51e-463d-8d67-520d6649fd10" />

<img width="2559" height="1427" alt="image" src="https://github.com/user-attachments/assets/c855065c-b694-4c2b-bbf4-56aee684f16a" />



## Avatar Generation


<img width="2559" height="1417" alt="Screenshot 2026-05-11 151746" src="https://github.com/user-attachments/assets/68b7ffa4-f116-4562-bde1-c84a1321c3ce" />


## Virtual Try-On

<img width="2559" height="1412" alt="Screenshot 2026-05-11 151842" src="https://github.com/user-attachments/assets/c42473a7-e8d1-4016-9636-0429d3bbc3c1" />


---

# Conclusion

The AI Virtual Avatar Try-On System successfully integrates Machine Learning, Computer Vision, and 3D rendering technologies to create an intelligent and interactive virtual fashion platform.

The system demonstrates effective face shape prediction using Random Forest Classification and enables users to visualize personalized 3D avatars with hairstyles, and dresses in real time.

The project provides a scalable foundation for future AI-powered virtual fashion applications, AR-based try-on systems, and intelligent avatar generation platforms.

---

# Author

## OVIYA SHREE S

Integrated M.Tech Software Engineering
VIT Vellore

---

# License

This project is developed for academic and research purposes.
