const BASE_URL = "http://127.0.0.1:5000";

async function uploadImage(file) {
  const formData = new FormData();
  formData.append("image", file);

  const res = await fetch(`${BASE_URL}/upload`, {
    method: "POST",
    body: formData
  });

  return await res.json();
}

async function analyzeFace(imagePath) {
  const res = await fetch(`${BASE_URL}/analyze-face`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ image_path: imagePath })
  });

  return await res.json();
}

async function getAvatar(gender, faceShape) {
  const res = await fetch(`${BASE_URL}/get-avatar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gender: gender, face_shape: faceShape })
  });

  return await res.json();
}

async function getDresses(gender) {
  const res = await fetch(`${BASE_URL}/get-dresses`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gender: gender })
  });

  return await res.json();
}

async function getHairstyles(gender) {
  const res = await fetch("http://127.0.0.1:5000/get-hairstyles", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gender })
  });

  return await res.json();
}

async function getEyebrows(gender) {
  const res = await fetch("http://127.0.0.1:5000/get-eyebrows", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ gender })
  });

  return await res.json();
}

