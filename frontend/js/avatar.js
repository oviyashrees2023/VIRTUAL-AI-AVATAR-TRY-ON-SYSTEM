let scene, camera, renderer,controls;

let avatarModel = null;
let currentDress = null;

const gender = localStorage.getItem("gender");
const faceShape = localStorage.getItem("face_shape");

// store real center of avatar
let avatarCenter = new THREE.Vector3(0, 1, 0);

// ===============================
// SHOW FACE SHAPE TEXT
// ===============================
window.addEventListener("load", () => {
  const banner = document.getElementById("faceShapeBanner");

  if (!banner) return;

  if (!faceShape) {
    banner.innerText = "Face shape not detected";
    banner.style.color = "#64748b";
    return;
  }

  banner.innerText = `Your face shape is ${faceShape.toUpperCase()}`;

  if (gender === "female") {
    banner.style.color = "#e77c9a";
  } else {
    banner.style.color = "#5eaee7";
  }
});

init();
loadAvatar();
loadDresses();
loadHairstyles();
// loadEyebrows() removed — #eyebrow-list no longer in HTML, was crashing entire script


// ===============================
// INIT THREE JS
// ===============================
function init() {
  scene = new THREE.Scene();
  scene.background = new THREE.Color(0xf8f4f0); // light background

  const container = document.querySelector(".avatar-view");
  const width = container.clientWidth;
  const height = container.clientHeight;

  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
  camera.position.set(0, 1.5, 4);

  renderer = new THREE.WebGLRenderer({
  antialias: true,
  preserveDrawingBuffer: true  // 🔥 REQUIRED for image download
});
  renderer.setSize(width, height);
  renderer.setPixelRatio(window.devicePixelRatio);

  document.getElementById("canvas-container").appendChild(renderer.domElement);

  

  controls = new THREE.OrbitControls(camera, renderer.domElement);

// smooth interaction
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// IMPORTANT: lock unwanted movements
controls.enablePan = false;   // ❌ no dragging scene sideways
controls.enableZoom = true;  // ✅ allow zoom
controls.minDistance = 2;    // zoom in limit
controls.maxDistance = 6;    // zoom out limit

// restrict vertical rotation (prevents weird top view)
controls.minPolarAngle = Math.PI / 2.2;
controls.maxPolarAngle = Math.PI / 2;

  const light1 = new THREE.DirectionalLight(0xffffff, 0.8);
  light1.position.set(2, 4, 2);
  scene.add(light1);

  const light2 = new THREE.DirectionalLight(0xffffff, 0.6);
  light2.position.set(-2, 3, -2);
  scene.add(light2);

  const ambient = new THREE.AmbientLight(0xffffff, 0.6);
  scene.add(ambient);

  animate();
}

// ===============================
// ANIMATE — no auto-rotation
// ===============================
let angle = 0;
let radius = 4;

function animate() {
  requestAnimationFrame(animate);
  if (controls) controls.update(); 
  renderer.render(scene, camera);
}

// ===============================
// CENTER MODEL + FLOOR FIX
// ===============================
function centerModel(model) {
  const box = new THREE.Box3().setFromObject(model);

  const center = new THREE.Vector3();
  box.getCenter(center);

  model.position.sub(center);

  // lift model so feet touches ground
  model.position.y -= box.min.y;
}

// ===============================
// UPDATE AVATAR CENTER
// ===============================
function updateAvatarCenter(model) {
  const box = new THREE.Box3().setFromObject(model);
  box.getCenter(avatarCenter);
}

// ===============================
// AUTO CAMERA FIT
// ===============================
function fitCameraToModel(model) {
  const box = new THREE.Box3().setFromObject(model);
  const size = box.getSize(new THREE.Vector3());
  box.getCenter(avatarCenter);

  const maxDim = Math.max(size.x, size.y, size.z);
  radius = maxDim * 1.3;

  camera.lookAt(avatarCenter);
}

// ===============================
// LOAD AVATAR
// ===============================
async function loadAvatar() {
  const data = await getAvatar(gender, faceShape);

  const mtlLoader = new THREE.MTLLoader();
  mtlLoader.load(data.mtl, (materials) => {
    materials.preload();

    const objLoader = new THREE.OBJLoader();
    objLoader.setMaterials(materials);

    objLoader.load(data.obj, (obj) => {
      avatarModel = obj;

      // SCALE MODEL
      const box = new THREE.Box3().setFromObject(avatarModel);
      const size = new THREE.Vector3();
      box.getSize(size);

      const scaleFactor = 2.2 / size.y;
      avatarModel.scale.setScalar(scaleFactor);

      centerModel(avatarModel);
      updateAvatarCenter(avatarModel);

      scene.add(avatarModel);

      fitCameraToModel(avatarModel);

      console.log("Avatar Loaded Successfully");

    });
  });
}

// ===============================
// LOAD DRESSES LIST
// ===============================
async function loadDresses() {
  const data = await getDresses(gender);
  const panel = document.getElementById("dress-list");

  panel.innerHTML = "";

  data.dresses.forEach((d) => {
    const btn = document.createElement("div");
    btn.className = "dress-item";
    btn.innerText = d.category;

    btn.onclick = () => wearDress(d.obj, d.mtl);

    panel.appendChild(btn);
  });
}

async function loadHairstyles() {
  const data = await getHairstyles(gender);
  const panel = document.getElementById("hair-list");

  panel.innerHTML = "";

  data.hairstyles.forEach((h) => {
    const btn = document.createElement("div");
    btn.className = "hair-item";
    btn.innerText = h.category;

    btn.onclick = () => wearHair(h.obj, h.mtl);

    panel.appendChild(btn);
  });
}



let currentHair = null;

function wearHair(objUrl, mtlUrl) {
  if (!avatarModel) return;

  if (currentHair) {
    avatarModel.remove(currentHair);
    currentHair = null;
  }

  const mtlLoader = new THREE.MTLLoader();
  mtlLoader.load(mtlUrl, (materials) => {
    materials.preload();

    const objLoader = new THREE.OBJLoader();
    objLoader.setMaterials(materials);

    objLoader.load(objUrl, (hairObj) => {
      currentHair = hairObj;

      hairObj.position.set(0, 0, 0);
      hairObj.rotation.set(0, 0, 0);
      hairObj.scale.set(1, 1, 1);

      avatarModel.add(hairObj);

      console.log("Hairstyle applied!");
    });
  });
}



// ===============================
// WEAR DRESS (ATTACH TO AVATAR)
// ===============================
function wearDress(objUrl, mtlUrl) {
  if (!avatarModel) return;

  if (currentDress) {
    avatarModel.remove(currentDress);
    currentDress = null;
  }

  const basePath = mtlUrl.substring(0, mtlUrl.lastIndexOf("/") + 1);

const mtlLoader = new THREE.MTLLoader();
mtlLoader.setResourcePath(basePath);   // 🔥 REQUIRED
mtlLoader.setPath(basePath);

mtlLoader.load(mtlUrl.split("/").pop(), (materials) => {
  materials.preload();

  const objLoader = new THREE.OBJLoader();
  objLoader.setMaterials(materials);
  objLoader.setPath(basePath);

  objLoader.load(objUrl.split("/").pop(), (dressObj) => {
      currentDress = dressObj;

      dressObj.position.set(0, 0, 0);
      dressObj.rotation.set(0, 0, 0);
      dressObj.scale.set(1, 1, 1);

      avatarModel.add(dressObj);

      // update center again after adding dress
      updateAvatarCenter(avatarModel);
      fitCameraToModel(avatarModel);

      console.log("Dress Added Successfully");
    });
  });
  
}

// ===============================
// RESIZE FIX
// ===============================
function resizeRenderer() {
  const container = document.querySelector(".avatar-view");
  const width = container.clientWidth;
  const height = container.clientHeight;

  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  renderer.setSize(width, height);
}

window.addEventListener("resize", resizeRenderer);
setTimeout(resizeRenderer, 500);

// ===============================
// BUTTON CLICK EFFECT
// ===============================
document.addEventListener("click", (e) => {
  if (e.target.classList.contains("dress-item")) {
    e.target.style.animation = "pop 0.3s ease";
    setTimeout(() => (e.target.style.animation = ""), 300);
  }
});

function downloadAvatarImage() {
  renderer.render(scene, camera); // ensure latest frame

  const canvas = renderer.domElement;

  const link = document.createElement("a");
  link.href = canvas.toDataURL("image/png");
  link.download = "avatar.png";
  link.click();
}

document.getElementById("downloadBtn").addEventListener("click", downloadAvatarImage);