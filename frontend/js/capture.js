async function processImage() {
  const fileInput = document.getElementById("photoInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please upload an image!");
    return;
  }

  const uploadResult = await uploadImage(file);
  const imagePath = uploadResult.image_path;

  const faceResult = await analyzeFace(imagePath);
  const faceShape = faceResult.face_shape;

  const gender = localStorage.getItem("gender");

  const avatar = await getAvatar(gender, faceShape);

  localStorage.setItem("face_shape", faceShape);
  localStorage.setItem("avatar_obj", avatar.obj);
  localStorage.setItem("avatar_mtl", avatar.mtl);

  window.location.href = "avatar.html";
}
