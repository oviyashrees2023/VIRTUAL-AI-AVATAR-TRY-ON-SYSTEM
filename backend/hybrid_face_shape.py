from face_analysis import detect_face_shape_geometry

from ml_face_shape import detect_face_shape_ml


def hybrid_face_shape(image_path):
    geo_shape = detect_face_shape_geometry(image_path)
    ml_shape, confidence = detect_face_shape_ml(image_path)

    print("Geometry:", geo_shape)
    print("ML:", ml_shape, "Confidence:", confidence)

    # 🔥 Decision Logic
    if ml_shape is not None and confidence > 0.65:
        return ml_shape

    if ml_shape == geo_shape:
        return geo_shape

    # fallback to geometry (more stable)
    return geo_shape
