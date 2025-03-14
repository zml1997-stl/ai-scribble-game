document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    let isDrawing = false;

    // Canvas Drawing Logic
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    function startDrawing(e) {
        isDrawing = true;
        draw(e); // Start drawing immediately on click
    }

    function draw(e) {
        if (!isDrawing) return;
        ctx.lineWidth = 2;
        ctx.lineCap = 'round';
        ctx.strokeStyle = '#000';

        const rect = canvas.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        ctx.lineTo(x, y);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(x, y);
    }

    function stopDrawing() {
        isDrawing = false;
        ctx.beginPath();
    }

    // Clear Canvas
    document.getElementById('clearCanvas').addEventListener('click', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });

    // Submit Drawing and Description
    document.getElementById('submitBtn').addEventListener('click', () => {
        const description = document.getElementById('description').value;
        const dataUrl = canvas.toDataURL('image/png'); // Convert canvas to image

        // For now, just show feedback (we’ll connect to backend later)
        const feedback = document.getElementById('feedback');
        feedback.textContent = `Submitted: "${description}"`;
        feedback.classList.remove('d-none');

        // Clear inputs
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        document.getElementById('description').value = '';
    });
});