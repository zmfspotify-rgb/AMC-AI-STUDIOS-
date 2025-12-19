/**
 * AMC AI Studios - 3D First-Person Theater Environment
 * 
 * Uses Three.js for 3D rendering and first-person controls
 */

class Theater3D {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.npcs = {};
        this.clock = new THREE.Clock();
        
        // Player state
        this.playerPosition = new THREE.Vector3(0, 1.7, 10);  // Eye level
        this.playerRotation = new THREE.Euler(0, 0, 0, 'YXZ');
        this.moveSpeed = 5.0;
        this.lookSpeed = 0.002;
        
        // Movement
        this.keys = {};
        this.mouseMovement = { x: 0, y: 0 };
        this.pointerLocked = false;
        
        this.init();
    }
    
    init() {
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x0a0a0a);
        this.scene.fog = new THREE.Fog(0x0a0a0a, 10, 50);
        
        // Create camera
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.copy(this.playerPosition);
        
        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);
        
        // Build theater environment
        this.buildTheaterEnvironment();
        
        // Setup controls
        this.setupControls();
        
        // Setup lighting
        this.setupLighting();
        
        // Start animation loop
        this.animate();
        
        // Handle resize
        window.addEventListener('resize', () => this.onWindowResize());
    }
    
    buildTheaterEnvironment() {
        // Floor
        const floorGeometry = new THREE.PlaneGeometry(50, 50);
        const floorMaterial = new THREE.MeshStandardMaterial({
            color: 0x2a0a0a,
            roughness: 0.8,
            metalness: 0.2
        });
        const floor = new THREE.Mesh(floorGeometry, floorMaterial);
        floor.rotation.x = -Math.PI / 2;
        floor.receiveShadow = true;
        this.scene.add(floor);
        
        // Walls
        this.buildWalls();
        
        // Lobby
        this.buildLobby();
        
        // Ticket counter
        this.buildTicketCounter();
        
        // Concession stand
        this.buildConcessions();
        
        // Theaters
        this.buildTheater('theater_1', new THREE.Vector3(-15, 0, -10));
        this.buildTheater('theater_2', new THREE.Vector3(0, 0, -10));
        this.buildTheater('theater_3', new THREE.Vector3(15, 0, -10));
        
        // Red carpet (for events)
        this.buildRedCarpet();
        
        // Decorative elements
        this.addDecorativeElements();
    }
    
    buildWalls() {
        const wallMaterial = new THREE.MeshStandardMaterial({
            color: 0x1a0505,
            roughness: 0.9
        });
        
        // Front wall
        const frontWall = new THREE.Mesh(
            new THREE.BoxGeometry(50, 5, 0.2),
            wallMaterial
        );
        frontWall.position.set(0, 2.5, -25);
        frontWall.receiveShadow = true;
        this.scene.add(frontWall);
        
        // Back wall
        const backWall = frontWall.clone();
        backWall.position.z = 25;
        this.scene.add(backWall);
        
        // Left wall
        const leftWall = new THREE.Mesh(
            new THREE.BoxGeometry(0.2, 5, 50),
            wallMaterial
        );
        leftWall.position.set(-25, 2.5, 0);
        this.scene.add(leftWall);
        
        // Right wall
        const rightWall = leftWall.clone();
        rightWall.position.x = 25;
        this.scene.add(rightWall);
    }
    
    buildLobby() {
        // Lobby area with ambient lighting
        const lobbyLight = new THREE.PointLight(0xff6666, 0.5, 20);
        lobbyLight.position.set(0, 4, 15);
        this.scene.add(lobbyLight);
        
        // Posters on walls
        this.addPosterWall(-23, 15);
        this.addPosterWall(23, 15);
    }
    
    buildTicketCounter() {
        // Ticket counter
        const counterGeometry = new THREE.BoxGeometry(8, 1.2, 1.5);
        const counterMaterial = new THREE.MeshStandardMaterial({
            color: 0x8b0000,
            roughness: 0.5,
            metalness: 0.3
        });
        const counter = new THREE.Mesh(counterGeometry, counterMaterial);
        counter.position.set(-10, 0.6, 8);
        counter.castShadow = true;
        this.scene.add(counter);
        
        // Counter screen
        const screenGeometry = new THREE.PlaneGeometry(3, 2);
        const screenMaterial = new THREE.MeshBasicMaterial({ color: 0x4444ff });
        const screen = new THREE.Mesh(screenGeometry, screenMaterial);
        screen.position.set(-10, 2, 7.2);
        this.scene.add(screen);
    }
    
    buildConcessions() {
        // Concession stand
        const standGeometry = new THREE.BoxGeometry(6, 1.2, 2);
        const standMaterial = new THREE.MeshStandardMaterial({
            color: 0xffd700,
            roughness: 0.6,
            metalness: 0.2
        });
        const stand = new THREE.Mesh(standGeometry, standMaterial);
        stand.position.set(10, 0.6, 8);
        stand.castShadow = true;
        this.scene.add(stand);
    }
    
    buildTheater(theaterId, position) {
        // Theater entrance
        const entranceGeometry = new THREE.BoxGeometry(4, 3, 0.2);
        const entranceMaterial = new THREE.MeshStandardMaterial({
            color: 0x000000,
            emissive: 0x220000
        });
        const entrance = new THREE.Mesh(entranceGeometry, entranceMaterial);
        entrance.position.copy(position);
        entrance.userData = { type: 'theater_entrance', theaterId: theaterId };
        this.scene.add(entrance);
        
        // Theater sign
        this.addTheaterSign(theaterId, position);
    }
    
    addTheaterSign(theaterId, position) {
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 512;
        canvas.height = 128;
        
        context.fillStyle = '#000000';
        context.fillRect(0, 0, canvas.width, canvas.height);
        
        context.fillStyle = '#ff0000';
        context.font = 'bold 48px Arial';
        context.textAlign = 'center';
        context.fillText(theaterId.toUpperCase().replace('_', ' '), 256, 80);
        
        const texture = new THREE.CanvasTexture(canvas);
        const signMaterial = new THREE.MeshBasicMaterial({ map: texture });
        const signGeometry = new THREE.PlaneGeometry(4, 1);
        const sign = new THREE.Mesh(signGeometry, signMaterial);
        sign.position.set(position.x, position.y + 2, position.z + 0.1);
        this.scene.add(sign);
    }
    
    buildRedCarpet() {
        // Red carpet for premiere events
        const carpetGeometry = new THREE.PlaneGeometry(3, 15);
        const carpetMaterial = new THREE.MeshStandardMaterial({
            color: 0xcc0000,
            roughness: 0.8
        });
        const carpet = new THREE.Mesh(carpetGeometry, carpetMaterial);
        carpet.rotation.x = -Math.PI / 2;
        carpet.position.set(0, 0.01, 5);
        carpet.visible = false;  // Only visible during events
        carpet.userData = { type: 'red_carpet' };
        this.scene.add(carpet);
    }
    
    addPosterWall(x, z) {
        // Add movie posters to walls
        const posterGeometry = new THREE.PlaneGeometry(2, 3);
        const posterMaterial = new THREE.MeshBasicMaterial({ color: 0x333333 });
        
        for (let i = 0; i < 3; i++) {
            const poster = new THREE.Mesh(posterGeometry, posterMaterial);
            poster.position.set(x, 2, z - i * 5);
            if (x < 0) poster.rotation.y = Math.PI / 2;
            else poster.rotation.y = -Math.PI / 2;
            this.scene.add(poster);
        }
    }
    
    addDecorativeElements() {
        // Add plants, benches, etc.
        // Plants
        for (let i = 0; i < 4; i++) {
            const plant = this.createPlant();
            plant.position.set(
                (i % 2 === 0 ? -1 : 1) * 8,
                0,
                15 - (i * 5)
            );
            this.scene.add(plant);
        }
    }
    
    createPlant() {
        const group = new THREE.Group();
        
        // Pot
        const potGeometry = new THREE.CylinderGeometry(0.3, 0.4, 0.5, 8);
        const potMaterial = new THREE.MeshStandardMaterial({ color: 0x8b4513 });
        const pot = new THREE.Mesh(potGeometry, potMaterial);
        pot.position.y = 0.25;
        group.add(pot);
        
        // Plant
        const leafGeometry = new THREE.SphereGeometry(0.5, 8, 8);
        const leafMaterial = new THREE.MeshStandardMaterial({ color: 0x228b22 });
        const leaves = new THREE.Mesh(leafGeometry, leafMaterial);
        leaves.position.y = 1;
        group.add(leaves);
        
        return group;
    }
    
    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
        this.scene.add(ambientLight);
        
        // Main lobby lights
        const lobbyLight1 = new THREE.PointLight(0xffffff, 0.8, 30);
        lobbyLight1.position.set(0, 4, 10);
        lobbyLight1.castShadow = true;
        this.scene.add(lobbyLight1);
        
        const lobbyLight2 = lobbyLight1.clone();
        lobbyLight2.position.set(-10, 4, 0);
        this.scene.add(lobbyLight2);
        
        const lobbyLight3 = lobbyLight1.clone();
        lobbyLight3.position.set(10, 4, 0);
        this.scene.add(lobbyLight3);
        
        // Dramatic theater entrance lighting
        const theaterLight = new THREE.SpotLight(0xff0000, 0.5, 20, Math.PI / 6);
        theaterLight.position.set(0, 5, -5);
        theaterLight.target.position.set(0, 0, -10);
        this.scene.add(theaterLight);
        this.scene.add(theaterLight.target);
    }
    
    setupControls() {
        // Keyboard controls
        document.addEventListener('keydown', (e) => {
            this.keys[e.code] = true;
        });
        
        document.addEventListener('keyup', (e) => {
            this.keys[e.code] = false;
        });
        
        // Mouse controls (pointer lock)
        this.renderer.domElement.addEventListener('click', () => {
            this.renderer.domElement.requestPointerLock();
        });
        
        document.addEventListener('pointerlockchange', () => {
            this.pointerLocked = document.pointerLockElement === this.renderer.domElement;
        });
        
        document.addEventListener('mousemove', (e) => {
            if (this.pointerLocked) {
                this.mouseMovement.x = e.movementX;
                this.mouseMovement.y = e.movementY;
            }
        });
    }
    
    updatePlayerMovement(delta) {
        if (!this.pointerLocked) return;
        
        const moveVector = new THREE.Vector3();
        
        // Forward/backward
        if (this.keys['KeyW']) moveVector.z -= 1;
        if (this.keys['KeyS']) moveVector.z += 1;
        
        // Left/right
        if (this.keys['KeyA']) moveVector.x -= 1;
        if (this.keys['KeyD']) moveVector.x += 1;
        
        // Normalize and apply speed
        if (moveVector.length() > 0) {
            moveVector.normalize();
            moveVector.multiplyScalar(this.moveSpeed * delta);
            
            // Rotate movement vector based on camera rotation
            moveVector.applyEuler(this.playerRotation);
            
            // Update position
            this.playerPosition.add(moveVector);
            
            // Clamp to bounds
            this.playerPosition.x = THREE.MathUtils.clamp(this.playerPosition.x, -23, 23);
            this.playerPosition.z = THREE.MathUtils.clamp(this.playerPosition.z, -23, 23);
        }
        
        // Mouse look
        this.playerRotation.y -= this.mouseMovement.x * this.lookSpeed;
        this.playerRotation.x -= this.mouseMovement.y * this.lookSpeed;
        this.playerRotation.x = THREE.MathUtils.clamp(this.playerRotation.x, -Math.PI / 2, Math.PI / 2);
        
        // Reset mouse movement
        this.mouseMovement.x = 0;
        this.mouseMovement.y = 0;
        
        // Update camera
        this.camera.position.copy(this.playerPosition);
        this.camera.rotation.copy(this.playerRotation);
    }
    
    addNPC(npcData) {
        // Create NPC representation
        const npcGeometry = new THREE.CapsuleGeometry(0.3, 1.4, 8, 16);
        const npcMaterial = new THREE.MeshStandardMaterial({
            color: Math.random() * 0xffffff,
            roughness: 0.7
        });
        const npc = new THREE.Mesh(npcGeometry, npcMaterial);
        npc.castShadow = true;
        npc.position.set(npcData.position[0], 1, npcData.position[2]);
        npc.userData = { npcId: npcData.id, npcData: npcData };
        
        this.scene.add(npc);
        this.npcs[npcData.id] = npc;
    }
    
    updateNPC(npcData) {
        if (!this.npcs[npcData.id]) {
            this.addNPC(npcData);
            return;
        }
        
        const npc = this.npcs[npcData.id];
        
        // Smoothly interpolate position
        npc.position.x = THREE.MathUtils.lerp(npc.position.x, npcData.position[0], 0.1);
        npc.position.z = THREE.MathUtils.lerp(npc.position.z, npcData.position[2], 0.1);
        
        // Update rotation
        if (npcData.rotation !== undefined) {
            npc.rotation.y = npcData.rotation;
        }
        
        // Update user data
        npc.userData.npcData = npcData;
    }
    
    removeNPC(npcId) {
        if (this.npcs[npcId]) {
            this.scene.remove(this.npcs[npcId]);
            delete this.npcs[npcId];
        }
    }
    
    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        const delta = this.clock.getDelta();
        
        // Update player movement
        this.updatePlayerMovement(delta);
        
        // Render
        this.renderer.render(this.scene, this.camera);
    }
    
    async loadTheaterState() {
        // Fetch theater state from server
        try {
            const response = await fetch('/api/theater/state');
            const data = await response.json();
            
            // Update NPCs
            data.npcs.forEach(npcData => {
                this.updateNPC(npcData);
            });
            
            // Remove NPCs that no longer exist
            Object.keys(this.npcs).forEach(npcId => {
                if (!data.npcs.find(n => n.id === npcId)) {
                    this.removeNPC(npcId);
                }
            });
            
        } catch (error) {
            console.error('Failed to load theater state:', error);
        }
    }
    
    startStateUpdates() {
        // Update theater state every 2 seconds
        setInterval(() => this.loadTheaterState(), 2000);
        this.loadTheaterState();  // Initial load
    }
}

// Initialize when DOM is ready
let theater3D = null;

function initTheater3D() {
    theater3D = new Theater3D('theater-3d-container');
    theater3D.startStateUpdates();
}
