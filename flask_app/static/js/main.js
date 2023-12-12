import * as THREE from './node_modules/three';
import { OrbitControls } from 'https://unpkg.com/three@0.126.1/examples/jsm/controls/OrbitControls.js'

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
// var;variable global
// let;variable acces only in blocks
// const;variable read only


// const renderer = new THREE.WebGLRenderer();

// document.body.appendChild(renderer.domElement);

const canvas = document.getElementById('myCanvas');
const renderer = new THREE.WebGLRenderer({ canvas:canvas });
renderer.setSize(window.innerWidth, window.innerHeight);

// Add a directional light to the scene
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(0, 1, 1).normalize();
scene.add(directionalLight);

// create a sphere
const sphere = new THREE.SphereGeometry(5, 64, 64);
const mesh = new THREE.MeshBasicMaterial({
  map: new THREE.TextureLoader().load('./img/earthworld1.png')
});
const model = new THREE.Mesh(sphere, mesh);
scene.add(model);

camera.position.z = 20;

function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();

const sizes={
  
}


// controls
const controls = new OrbitControls(camera,canvas);
controls.enableDamping = true;
controls.enablePan=false;
controls.enableZoom = false;
controls.autoRotate = true;
controls.autoRotateSpeed = 2;


window.addEventListener("resize",()=>{
  window.innerWidth=window.innerWidth
  window.innerHeight=window.innerHeight
  // update camera
  camera.updateProjectionMatrix();
  camera.aspect=window.innerWidth/window.innerHeight;
  renderer.setSize(window.innerWidth,window.innerHeight);
})

const loop = () =>{
  controls.update();
  renderer.render(scene,camera);
  window.requestAnimationFrame(loop);
}
loop();
