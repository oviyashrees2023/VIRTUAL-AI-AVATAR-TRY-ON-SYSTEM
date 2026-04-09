import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_json(path):
    with open(path, "r") as f:
        return json.load(f)

# ===========================
# AVATAR LOADER
# ===========================

def get_avatar(gender, face_shape):
    folder = os.path.join(BASE_DIR, "models", gender, face_shape)

    info_path = os.path.join(folder, "info.json")
    if not os.path.exists(info_path):
        return None

    info = read_json(info_path)

    obj_path = os.path.join(folder, info["model_file"])
    mtl_path = os.path.join(folder, info["mtl_file"])
    texture_path = os.path.join(folder, info["texture_folder"])

    return {
        "gender": gender,
        "face_shape": face_shape,
        "obj": f"http://127.0.0.1:5000/models/{gender}/{face_shape}/{info['model_file']}",
        "mtl": f"http://127.0.0.1:5000/models/{gender}/{face_shape}/{info['mtl_file']}",
        "textures": texture_path.replace("\\", "/")
    }

# ===========================
# DRESS LOADER
# ===========================

def get_dresses(gender, face_shape=None):
    base = os.path.join(BASE_DIR, "dresses", gender)
    dresses = []

    if not os.path.exists(base):
        return dresses

    for category in os.listdir(base):
        folder = os.path.join(base, category)
        info_path = os.path.join(folder, "info.json")

        if not os.path.exists(info_path):
            continue

        info = read_json(info_path)

        # Filter by face shape if provided
        if face_shape and face_shape not in info.get("compatible_face_shapes", []):
            continue

        obj_path = os.path.join(folder, info["model_file"])
        mtl_path = os.path.join(folder, info["mtl_file"])
        texture_path = os.path.join(folder, info["texture_folder"])

        dresses.append({
            "category": category,
            "obj": f"http://127.0.0.1:5000/dresses/{gender}/{category}/{info['model_file']}",
            "mtl": f"http://127.0.0.1:5000/dresses/{gender}/{category}/{info['mtl_file']}",
            "textures": texture_path.replace("\\", "/")
        })

    return dresses
