// Hero 3D Scene — Developer Command Center using Three.js
(function() {
  const canvas = document.getElementById('hero-canvas');
  if (!canvas || typeof THREE === 'undefined') return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const isMobile = window.innerWidth < 768;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: !isMobile, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, isMobile ? 1.5 : 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.set(0, 0, 18);

  // Lights
  const ambient = new THREE.AmbientLight(0x9333ea, 0.4);
  scene.add(ambient);
  const pointLight1 = new THREE.PointLight(0x8b5cf6, 2, 50);
  pointLight1.position.set(10, 10, 10);
  scene.add(pointLight1);
  const pointLight2 = new THREE.PointLight(0x06b6d4, 1, 40);
  pointLight2.position.set(-10, -5, 5);
  scene.add(pointLight2);

  const objects = [];
  const particleCount = isMobile ? 400 : 900;

  // Digital grid floor
  const gridHelper = new THREE.GridHelper(60, 30, 0x3b1a6b, 0x1a0a30);
  gridHelper.position.y = -8;
  scene.add(gridHelper);

  // Central core — icosahedron "developer core"
  const coreGeo = new THREE.IcosahedronGeometry(1.8, 1);
  const coreMat = new THREE.MeshPhongMaterial({
    color: 0x7c3aed,
    emissive: 0x4c1d95,
    wireframe: true,
    transparent: true,
    opacity: 0.7,
  });
  const core = new THREE.Mesh(coreGeo, coreMat);
  core.position.set(6, 0, -4);
  scene.add(core);
  objects.push({ mesh: core, rotX: 0.004, rotY: 0.007 });

  // Inner solid core
  const innerCore = new THREE.Mesh(
    new THREE.IcosahedronGeometry(1.2, 2),
    new THREE.MeshPhongMaterial({ color: 0x5b21b6, emissive: 0x3b0764, transparent: true, opacity: 0.5 })
  );
  core.add(innerCore);
  objects.push({ mesh: innerCore, rotX: -0.006, rotY: 0.003 });

  // Floating data nodes (tetrahedra)
  const nodePositions = [
    [3, 3, -2], [-3, 2.5, -3], [8, 2, -5],
    [5, -3, -2], [-1, -3, -4], [8, -2, -6],
    [-4, 0, -6], [10, 0, -3],
  ];
  nodePositions.forEach((pos, i) => {
    const size = 0.3 + Math.random() * 0.4;
    const geo = i % 3 === 0
      ? new THREE.TetrahedronGeometry(size)
      : i % 3 === 1
        ? new THREE.OctahedronGeometry(size)
        : new THREE.BoxGeometry(size, size, size);
    const hue = i % 2 === 0 ? 0x8b5cf6 : 0x06b6d4;
    const mat = new THREE.MeshPhongMaterial({
      color: hue,
      emissive: hue,
      emissiveIntensity: 0.3,
      transparent: true,
      opacity: 0.6 + Math.random() * 0.3,
      wireframe: Math.random() > 0.5,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.set(...pos);
    scene.add(mesh);
    objects.push({ mesh, rotX: (Math.random() - 0.5) * 0.02, rotY: (Math.random() - 0.5) * 0.02, float: Math.random() * Math.PI * 2, floatSpeed: 0.008 + Math.random() * 0.006 });
  });

  // Orbiting rings around core
  const ringGeo = new THREE.TorusGeometry(3, 0.04, 8, 60);
  const ringMat = new THREE.MeshBasicMaterial({ color: 0x7c3aed, transparent: true, opacity: 0.35 });
  const ring1 = new THREE.Mesh(ringGeo, ringMat);
  ring1.rotation.x = Math.PI / 3;
  core.add(ring1);

  const ring2 = new THREE.Mesh(
    new THREE.TorusGeometry(4, 0.03, 8, 60),
    new THREE.MeshBasicMaterial({ color: 0x06b6d4, transparent: true, opacity: 0.2 })
  );
  ring2.rotation.x = Math.PI / 5;
  ring2.rotation.z = Math.PI / 4;
  core.add(ring2);

  // Particles
  const positions = new Float32Array(particleCount * 3);
  for (let i = 0; i < particleCount; i++) {
    positions[i * 3] = (Math.random() - 0.5) * 50;
    positions[i * 3 + 1] = (Math.random() - 0.5) * 40;
    positions[i * 3 + 2] = (Math.random() - 0.5) * 30 - 5;
  }
  const particleGeo = new THREE.BufferGeometry();
  particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  const particleMat = new THREE.PointsMaterial({
    size: 0.06,
    color: 0x8b5cf6,
    transparent: true,
    opacity: 0.5,
  });
  const particles = new THREE.Points(particleGeo, particleMat);
  scene.add(particles);

  // Code panel geometry — flat rectangles floating in space
  const panelData = [
    { pos: [-5, 2, -8], w: 3.5, h: 2.5 },
    { pos: [6, 3.5, -10], w: 2.8, h: 1.8 },
    { pos: [-4, -3, -7], w: 2, h: 1.5 },
  ];
  panelData.forEach(({ pos, w, h }) => {
    const panelGeo = new THREE.PlaneGeometry(w, h);
    const panelMat = new THREE.MeshBasicMaterial({
      color: 0x1a0a30,
      transparent: true,
      opacity: 0.35,
      side: THREE.DoubleSide,
    });
    const panel = new THREE.Mesh(panelGeo, panelMat);
    panel.position.set(...pos);
    panel.rotation.y = (Math.random() - 0.5) * 0.6;

    // Border lines
    const edges = new THREE.EdgesGeometry(panelGeo);
    const lineMat = new THREE.LineBasicMaterial({ color: 0x5b21b6, transparent: true, opacity: 0.5 });
    const lines = new THREE.LineSegments(edges, lineMat);
    panel.add(lines);

    scene.add(panel);
    objects.push({ mesh: panel, rotY: (Math.random() - 0.5) * 0.003, float: Math.random() * Math.PI * 2, floatSpeed: 0.005 });
  });

  // Mouse parallax
  let mouseX = 0, mouseY = 0;
  document.addEventListener('mousemove', e => {
    mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  // Resize
  function onResize() {
    const w = window.innerWidth, h = window.innerHeight;
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
  }
  window.addEventListener('resize', onResize);

  // Hero section observer — pause when off screen
  let visible = true;
  const heroEl = document.getElementById('home');
  if (heroEl) {
    const heroObs = new IntersectionObserver(entries => { visible = entries[0].isIntersecting; }, { threshold: 0.05 });
    heroObs.observe(heroEl);
  }

  let clock = new THREE.Clock();
  let animId;

  function animate() {
    animId = requestAnimationFrame(animate);
    if (!visible) return;

    const t = clock.getElapsedTime();

    // Parallax camera
    camera.position.x += (mouseX * 1.5 - camera.position.x) * 0.04;
    camera.position.y += (-mouseY * 1 - camera.position.y) * 0.04;
    camera.lookAt(scene.position);

    // Animate objects
    objects.forEach(obj => {
      if (obj.rotX) obj.mesh.rotation.x += obj.rotX;
      if (obj.rotY) obj.mesh.rotation.y += obj.rotY;
      if (obj.float !== undefined) {
        obj.mesh.position.y += Math.sin(t * obj.floatSpeed + obj.float) * 0.003;
      }
    });

    // Rotate particle field slowly
    particles.rotation.y = t * 0.02;

    // Pulse core glow
    pointLight1.intensity = 1.5 + Math.sin(t * 2) * 0.5;

    renderer.render(scene, camera);
  }

  animate();

  // Cleanup on page unload
  window.addEventListener('unload', () => {
    cancelAnimationFrame(animId);
    renderer.dispose();
    particleGeo.dispose();
    particleMat.dispose();
    coreGeo.dispose();
    coreMat.dispose();
  });
})();
