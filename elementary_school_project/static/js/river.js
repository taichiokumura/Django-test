const baseImage = document.getElementById('baseImage');
const overlayImage = document.getElementById('overlayImage');
let initialDistance = null;
let initialScale = 1;
let currentScale = 1;
let initialAngle = 0;
let currentAngle = 0;

function handleTouchStart(event, image) {
    if (event.touches.length === 2 && image === baseImage) {
        const touch1 = event.touches[0];
        const touch2 = event.touches[1];
        initialDistance = Math.hypot(touch2.clientX - touch1.clientX, touch2.clientY - touch1.clientY);
        initialScale = currentScale;

        const centerX = (touch1.clientX + touch2.clientX) / 2;
        const centerY = (touch1.clientY + touch2.clientY) / 2;
        const dx = touch1.clientX - centerX;
        const dy = touch1.clientY - centerY;
        initialAngle = Math.atan2(dy, dx);
    } else if (event.touches.length === 1) {
        const touch = event.touches[0];
        const rect = baseImage.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const x = touch.clientX - centerX;
        const y = touch.clientY - centerY;

        overlayImage.style.transform = `translate(${x}px, ${y}px)`;
        }
    }

    function handleTouchMove(event, image) {
        event.preventDefault();
        if (event.touches.length === 2 && image === baseImage) {
            const touch1 = event.touches[0];
            const touch2 = event.touches[1];
            const distance = Math.hypot(touch2.clientX - touch1.clientX, touch2.clientY - touch1.clientY);
            const scale = distance / initialDistance;
            currentScale = initialScale * scale;

            const centerX = (touch1.clientX + touch2.clientX) / 2;
            const centerY = (touch1.clientY + touch2.clientY) / 2;
            const dx = touch1.clientX - centerX;
            const dy = touch1.clientY - centerY;
            const angle = Math.atan2(dy, dx);
            currentAngle = angle - initialAngle;

            image.style.transform = `scale(${currentScale}) rotate(${currentAngle}rad)`;
        }
    }

    function handleTouchEnd(event, image) {
        if (event.touches.length < 2) {
            initialDistance = null;
        }
    }

    function handleTouchPosition(event, image) {
        const touch = event.touches[0];
        const rect = image.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        const x = (touch.clientX - centerX) / currentScale;
        const y = (touch.clientY - centerY) / currentScale;
        const rotatedX = x * Math.cos(-currentAngle) - y * Math.sin(-currentAngle);
        const rotatedY = x * Math.sin(-currentAngle) + y * Math.cos(-currentAngle);

        console.log(`Touched at (x: ${rotatedX.toFixed(2)}, y: ${rotatedY.toFixed(2)})`);

        const coordinatesDisplay = document.createElement('div');
        coordinatesDisplay.style.position = 'absolute';
        coordinatesDisplay.style.top = `${touch.clientY}px`;
        coordinatesDisplay.style.left = `${touch.clientX}px`;
        coordinatesDisplay.textContent = `(x: ${rotatedX.toFixed(2)}, y: ${rotatedY.toFixed(2)})`;
        document.body.appendChild(coordinatesDisplay);

        setTimeout(() => {
            coordinatesDisplay.remove();
        }, 2000);
    }

    baseImage.addEventListener('touchstart', (event) => handleTouchStart(event, baseImage));
    baseImage.addEventListener('touchmove', (event) => handleTouchMove(event, baseImage));
    baseImage.addEventListener('touchend', (event) => handleTouchEnd(event, baseImage));
    baseImage.addEventListener('touchcancel', (event) => handleTouchEnd(event, baseImage));
    baseImage.addEventListener('touchstart', (event) => handleTouchPosition(event, baseImage));

    overlayImage.addEventListener('touchstart', (event) => handleTouchStart(event, overlayImage));
    overlayImage.addEventListener('touchstart', (event) => handleTouchPosition(event, overlayImage));