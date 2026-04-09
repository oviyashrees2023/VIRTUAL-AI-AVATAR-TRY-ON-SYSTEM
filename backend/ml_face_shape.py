from joblib import load
from features import extract_features
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "face_shape_model.pkl")

model = load(MODEL_PATH)

def detect_face_shape_ml(image_path):
    features = extract_features(image_path)
    if features is None:
        return "oval"

    pred = model.predict([features])[0]
    return str(pred).lower().strip()
