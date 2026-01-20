const video = document.getElementById('video');
const expressionEl = document.getElementById('expression');
const cameraBtn = document.getElementById('cameraBtn');
const cameraStatus = document.getElementById('cameraStatus');

let stream = null;
let intervalId = null;

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.style.display = 'block';
        cameraStatus.textContent = 'Camera: On';
        cameraBtn.textContent = 'Stop Camera';

        intervalId = setInterval(() => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);

            const dataUrl = canvas.toDataURL('image/jpeg');

            fetch('/analyze_frame', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ image: dataUrl, mode: "facial" })
            })
            .then(res => res.json())
            .then(data => {
                expressionEl.textContent = data.expression;
            })
            .catch(err => console.error("API error:", err));
        }, 200);
    } catch (err) {
        console.error("Webcam error:", err);
    }
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    if (intervalId) {
        clearInterval(intervalId);
        intervalId = null;
    }
    video.style.display = 'none';
    cameraStatus.textContent = 'Camera: Off';
    cameraBtn.textContent = 'Start Camera';
    expressionEl.textContent = '-';
}

cameraBtn.addEventListener('click', () => {
    if (stream) {
        stopCamera();
    } else {
        startCamera();
    }
});
