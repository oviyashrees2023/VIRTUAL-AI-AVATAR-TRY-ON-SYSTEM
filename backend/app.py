from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os, json

from ml_face_shape import detect_face_shape_ml



app = Flask(__name__)
CORS(app)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODELS_DIR = os.path.join(ROOT_DIR, "models")
DRESSES_DIR = os.path.join(ROOT_DIR, "dresses")
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
HAIRSTYLES_DIR = os.path.join(ROOT_DIR, "hairstyles")
EYEBROWS_DIR = os.path.join(ROOT_DIR, "eyebrows")


os.makedirs(UPLOAD_DIR, exist_ok=True)


# =========================
# UPLOAD IMAGE
# =========================
@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(save_path)

    return jsonify({"image_path": save_path.replace("\\", "/")})

# =========================
# ANALYZE FACE
# =========================
@app.route("/analyze-face", methods=["POST"])
def analyze_face():
    data = request.json
    image_path = data.get("image_path")

    raw_shape = detect_face_shape_ml(image_path)
    face_shape = normalize_face_shape(raw_shape)

    print("ML FACE SHAPE:", raw_shape)
    print("NORMALIZED:", face_shape)

    return jsonify({"face_shape": face_shape})




def normalize_face_shape(shape):
    shape = shape.lower().strip()

    mapping = {
        "round": "round",
        "oval": "oval",
        "square": "square",
        "long": "rectangle",
        "triangle": "triangle",
        "heart": "heart",
        "diamond": "diamond"
    }

    return mapping.get(shape, "oval")
# =========================

# GET AVATAR MODEL
# =========================
@app.route("/get-avatar", methods=["POST"])
def get_avatar():
    data = request.json
    gender = data["gender"]
    face_shape = normalize_face_shape(data["face_shape"])


    folder = os.path.join(MODELS_DIR, gender, face_shape)
    info_file = os.path.join(folder, "info.json")

    if not os.path.exists(info_file):
        return jsonify({"error": "Model not found"}), 404

    with open(info_file) as f:
        info = json.load(f)

    obj_url = f"http://127.0.0.1:5000/models/{gender}/{face_shape}/{info['model_file']}"
    mtl_url = f"http://127.0.0.1:5000/models/{gender}/{face_shape}/{info['mtl_file']}"

    return jsonify({"obj": obj_url, "mtl": mtl_url})

# =========================
# GET DRESSES
# =========================
@app.route("/get-dresses", methods=["POST"])
def get_dresses():
    data = request.json
    gender = data["gender"]

    gender_dir = os.path.join(DRESSES_DIR, gender)
    dresses = []

    if not os.path.exists(gender_dir):
        return jsonify({"dresses": []})

    for category in os.listdir(gender_dir):
        folder = os.path.join(gender_dir, category)
        info_file = os.path.join(folder, "info.json")

        if not os.path.exists(info_file):
            continue

        with open(info_file) as f:
            info = json.load(f)

        obj_url = f"http://127.0.0.1:5000/dresses/{gender}/{category}/{info['model_file']}"
        mtl_url = f"http://127.0.0.1:5000/dresses/{gender}/{category}/{info['mtl_file']}"

        dresses.append({
            "category": category,
            "obj": obj_url,
            "mtl": mtl_url
        })

    return jsonify({"dresses": dresses})

@app.route("/get-hairstyles", methods=["POST"])
def get_hairstyles():
    data = request.json
    gender = data["gender"]

    gender_dir = os.path.join(HAIRSTYLES_DIR, gender)
    hairstyles = []

    if not os.path.exists(gender_dir):
        return jsonify({"hairstyles": []})

    for category in os.listdir(gender_dir):
        folder = os.path.join(gender_dir, category)
        info_file = os.path.join(folder, "info.json")

        if not os.path.exists(info_file):
            continue

        with open(info_file) as f:
            info = json.load(f)

        obj_url = f"http://127.0.0.1:5000/hairstyles/{gender}/{category}/{info['model_file']}"
        mtl_url = f"http://127.0.0.1:5000/hairstyles/{gender}/{category}/{info['mtl_file']}"

        hairstyles.append({
            "category": category,
            "obj": obj_url,
            "mtl": mtl_url
        })

    return jsonify({"hairstyles": hairstyles})


@app.route("/get-eyebrows", methods=["POST"])
def get_eyebrows():
    data = request.json
    gender = data["gender"]

    gender_dir = os.path.join(EYEBROWS_DIR, gender)
    eyebrows = []

    if not os.path.exists(gender_dir):
        return jsonify({"eyebrows": []})

    for category in os.listdir(gender_dir):
        folder = os.path.join(gender_dir, category)
        info_file = os.path.join(folder, "info.json")

        if not os.path.exists(info_file):
            continue

        with open(info_file) as f:
            info = json.load(f)

        obj_url = f"http://127.0.0.1:5000/eyebrows/{gender}/{category}/{info['model_file']}"
        mtl_url = f"http://127.0.0.1:5000/eyebrows/{gender}/{category}/{info['mtl_file']}"

        eyebrows.append({
            "category": category,
            "obj": obj_url,
            "mtl": mtl_url
        })

    return jsonify({"eyebrows": eyebrows})



# =========================
# SERVE FILES
# =========================
@app.route("/models/<path:path>")
def serve_models(path):
    return send_from_directory(MODELS_DIR, path)

@app.route("/dresses/<path:path>")
def serve_dresses(path):
    return send_from_directory(DRESSES_DIR, path)

@app.route("/hairstyles/<path:path>")
def serve_hairstyles(path):
    return send_from_directory(HAIRSTYLES_DIR, path)

@app.route("/eyebrows/<path:path>")
def serve_eyebrows(path):
    return send_from_directory(EYEBROWS_DIR, path)
                                                                                                    


# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    app.run(debug=True)
