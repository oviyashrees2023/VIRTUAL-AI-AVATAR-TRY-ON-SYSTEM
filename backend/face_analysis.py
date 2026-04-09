import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh


def distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def detect_face_shape_geometry(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return "oval"

    h, w, _ = img.shape

    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        if not result.multi_face_landmarks:
            return "oval"

        landmarks = result.multi_face_landmarks[0].landmark

        def get_point(idx):
            return int(landmarks[idx].x * w), int(landmarks[idx].y * h)

        left_cheek = get_point(234)
        right_cheek = get_point(454)
        chin = get_point(152)
        forehead = get_point(10)
        jaw_left = get_point(172)
        jaw_right = get_point(397)
        forehead_left = get_point(127)
        forehead_right = get_point(356)

        face_width = distance(left_cheek, right_cheek)
        face_height = distance(forehead, chin)
        jaw_width = distance(jaw_left, jaw_right)
        forehead_width = distance(forehead_left, forehead_right)
        cheekbone_width = face_width

        height_width_ratio = face_height / face_width
        jaw_cheek_ratio = jaw_width / cheekbone_width
        forehead_cheek_ratio = forehead_width / cheekbone_width

        if height_width_ratio > 1.45 and jaw_cheek_ratio < 0.95:
            return "oval"
        if height_width_ratio < 1.25 and jaw_cheek_ratio > 0.95:
            return "round"
        if abs(jaw_width - cheekbone_width) < 0.05 * cheekbone_width:
            return "square"
        if height_width_ratio > 1.6:
            return "rectangle"
        if jaw_cheek_ratio > 1.05:
            return "triangle"
        if forehead_cheek_ratio > 1.05:
            return "heart"

        return "diamond"
