import cv2
import mediapipe as mp
import numpy as np

mp_face_mesh = mp.solutions.face_mesh

def extract_features(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None

    h, w, _ = image.shape

    with mp_face_mesh.FaceMesh(static_image_mode=True) as face_mesh:
        results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.multi_face_landmarks:
            return None

        lm = results.multi_face_landmarks[0].landmark

        def point(i):
            return np.array([lm[i].x * w, lm[i].y * h])

        # Key landmarks
        forehead = point(10)
        chin = point(152)
        left_cheek = point(234)
        right_cheek = point(454)
        left_jaw = point(172)
        right_jaw = point(397)
        left_forehead = point(127)
        right_forehead = point(356)

        face_height = np.linalg.norm(forehead - chin)
        face_width = np.linalg.norm(left_cheek - right_cheek)
        jaw_width = np.linalg.norm(left_jaw - right_jaw)
        forehead_width = np.linalg.norm(left_forehead - right_forehead)

        # Features (ratios)
        return [
            face_height / face_width,
            jaw_width / face_width,
            forehead_width / face_width
        ]
