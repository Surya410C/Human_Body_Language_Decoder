const video = document.getElementById('video');
const gestureEl = document.getElementById('gesture');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; })
    .catch(err => console.error("Webcam error:", err));

setInterval(() => {
    if (video.videoWidth === 0) return; // wait until video is ready

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    const dataUrl = canvas.toDataURL('image/jpeg');

    fetch('/analyze_frame', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataUrl, mode: "gestures" })
    })
    .then(res => res.json())
    .then(data => {
        gestureEl.textContent = data.gesture || "Error";
    })
    .catch(err => console.error("API error:", err));
}, 1000);
