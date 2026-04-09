import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from joblib import dump
from features import extract_features

DATASET_DIR = os.path.join(os.path.dirname(__file__), "face_shape_dataset")


X = []
y = []

print("Extracting features from dataset...")

for shape in os.listdir(DATASET_DIR):
    folder = os.path.join(DATASET_DIR, shape)
    if not os.path.isdir(folder):
        continue

    for img_name in os.listdir(folder):
        img_path = os.path.join(folder, img_name)
        features = extract_features(img_path)

        if features:
            X.append(features)
            y.append(shape)

X = np.array(X)
y = np.array(y)

print("Total samples:", len(X))

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=300, random_state=42)
model.fit(X_train, y_train)

# Test accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy * 100, "%")

# Save model
dump(model, "face_shape_model.pkl")
print("✅ Model saved as face_shape_model.pkl")
