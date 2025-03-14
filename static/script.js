document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('drawingCanvas');
    const ctx = canvas.getContext('2d');
    let isDrawing = false;

    // Canvas Drawing Logic (unchanged)
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);

    function startDrawing(e) {
        isDrawing = true;
        draw(e);
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

    // Clear Canvas (unchanged)
    document.getElementById('clearCanvas').addEventListener('click', () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    });

    // Submit Drawing and Description
    document.getElementById('submitBtn').addEventListener('click', () => {
        const description = document.getElementById('description').value;
        const dataUrl = canvas.toDataURL('image/png'); // Convert canvas to base64 image

        // Send to Flask backend
        fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                drawing: dataUrl,
                description: description,
            }),
        })
        .then(response => response.json())
        .then(data => {
            const feedback = document.getElementById('feedback');
            feedback.textContent = data.message;
            feedback.classList.remove('d-none');
            if (data.success) {
                feedback.classList.remove('alert-info');
                feedback.classList.add('alert-success');
            } else {
                feedback.classList.remove('alert-info');
                feedback.classList.add('alert-danger');
            }

            // Clear inputs
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            document.getElementById('description').value = '';
        })
        .catch(error => {
            console.error('Error:', error);
            const feedback = document.getElementById('feedback');
            feedback.textContent = 'Error submitting your drawing!';
            feedback.classList.remove('d-none');
            feedback.classList.add('alert-danger');
        });
    });
});