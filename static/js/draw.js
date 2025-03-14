// Initialize canvas and context
const canvas = document.getElementById('drawingCanvas');
const ctx = canvas.getContext('2d');
let drawing = false;

// Set up canvas properties
ctx.lineWidth = 2;
ctx.lineCap = 'round';
ctx.strokeStyle = '#000000';

// Mouse/touch event handlers
function startDrawing(e) {
    drawing = true;
    draw(e);
}

function stopDrawing() {
    drawing = false;
    ctx.beginPath();
}

function draw(e) {
    if (!drawing) return;

    const rect = canvas.getBoundingClientRect();
    let x, y;

    // Handle touch events for mobile
    if (e.type.startsWith('touch')) {
        e.preventDefault();
        const touch = e.touches[0];
        x = touch.clientX - rect.left;
        y = touch.clientY - rect.top;
    } else {
        x = e.clientX - rect.left;
        y = e.clientY - rect.top;
    }

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
}

// Event listeners for desktop
canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseleave', stopDrawing);

// Event listeners for mobile
canvas.addEventListener('touchstart', startDrawing);
canvas.addEventListener('touchend', stopDrawing);
canvas.addEventListener('touchmove', draw);

// Clear canvas function
function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

// Submit drawing data with form
document.querySelector('form').addEventListener('submit', (e) => {
    const drawingData = canvas.toDataURL('image/png');
    document.getElementById('drawingData').value = drawingData;
});

// Optional: Add a clear button (uncomment to include)
// const clearButton = document.createElement('button');
// clearButton.textContent = 'Clear Canvas';
// clearButton.className = 'btn btn-secondary btn-small mt-2';
// clearButton.onclick = clearCanvas;
// canvas.parentNode.insertBefore(clearButton, canvas.nextSibling);