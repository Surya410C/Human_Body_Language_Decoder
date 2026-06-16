# 🤖 Body Language Decoder

A real-time **Body Language Detection** web application that uses computer vision to recognize **hand gestures** and **facial expressions** through a live webcam feed. Built with Flask, MediaPipe, OpenCV, and FER — with user authentication powered by MongoDB.

---

## 🚀 Features

- 🖐 **Hand Gesture Recognition** — Detects gestures like Fist, Open Palm, Thumbs Up/Down, 1–4 Fingers using MediaPipe
- 😊 **Facial Emotion Detection** — Identifies emotions (happy, sad, angry, surprised, etc.) in real-time using the FER library with MTCNN
- 🎥 **Live Webcam Streaming** — Camera toggle (on/off) with real-time video feed streamed via Flask
- 🔐 **User Authentication** — Secure Register/Login/Logout system using Flask-Login and bcrypt password hashing
- 🗄️ **MongoDB Integration** — User data stored and managed with Flask-PyMongo and MongoDB Atlas
- 🎨 **Animated UI** — Smooth scroll-triggered animations, hero section with video background, responsive design

---

## 🗂️ Project Structure

```
Body Language Detection/
│
├── app.py                     # Main Flask application (routes, gesture & emotion logic)
│
├── templates/
│   ├── index.html             # Home / landing page
│   ├── facial.html            # Facial emotion detection page
│   ├── gestures.html          # Hand gesture recognition page
│   ├── login.html             # Login page
│   └── register.html          # Register page
│
├── static/
│   ├── index.css              # Main stylesheet with animations
│   ├── login.css              # Login page styles
│   ├── register.css           # Register page styles
│   ├── facial.js              # Frontend: webcam capture → facial API
│   └── gestures.js            # Frontend: webcam capture → gesture API
│
├── assets/
│   └── shooting_star.mp4      # Background video for hero section
│
└── requirements.txt           # Python dependencies
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Computer Vision | OpenCV, MediaPipe |
| Emotion Detection | FER (Facial Expression Recognition) with MTCNN |
| Authentication | Flask-Login, bcrypt |
| Database | MongoDB Atlas via Flask-PyMongo |
| Frontend | HTML, CSS, Vanilla JavaScript |
| Video Streaming | Flask `Response` with MJPEG |

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/body-language-detection.git
cd body-language-detection
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install flask flask-pymongo flask-login bcrypt opencv-python mediapipe fer numpy certifi pymongo
```

### 4. Configure MongoDB

In `app.py`, update the MongoDB URI with your own MongoDB Atlas connection string:

```python
app.config["MONGO_URI"] = "your-mongodb-atlas-connection-string"
```

### 5. Set a secure secret key

```python
app.secret_key = "your-strong-secret-key"
```

---

## ▶️ Run the Application

```bash
python app.py
```

Then open your browser and go to:

```
http://127.0.0.1:5000
```

---

## 🔐 Authentication Flow

```
Register → Login → Home Dashboard → Choose Mode
                                        ↓              ↓
                               Facial Detection   Gesture Detection
```

All detection pages are protected and require login. Users are stored securely in MongoDB with bcrypt-hashed passwords.

---

## 🖐 Supported Gestures

| Gesture | Description |
|---|---|
| ✊ Fist | All fingers closed |
| 🖐 Open Palm | All 5 fingers open |
| ☝️ 1 Finger | Index finger only |
| ✌️ 2 Fingers | Index + middle finger |
| 3 / 4 Fingers | Three or four fingers extended |
| 👍 Thumbs Up | Thumb raised upward |
| 👎 Thumbs Down | Thumb pointing downward |

---

## 😊 Detected Emotions

The FER library with MTCNN backend detects the following facial emotions in real-time:

`Happy` · `Sad` · `Angry` · `Surprised` · `Fearful` · `Disgusted` · `Neutral`

---

## 📡 API Routes

| Route | Method | Description |
|---|---|---|
| `/` | GET | Home / landing page |
| `/register` | GET, POST | User registration |
| `/login` | GET, POST | User login |
| `/logout` | GET | User logout |
| `/facial` | GET | Facial detection page (login required) |
| `/gestures` | GET | Gesture detection page (login required) |
| `/video_feed/<mode>` | GET | Live video stream (`facial` or `gestures`) |
| `/camera_on` | GET | Turn camera on |
| `/camera_off` | GET | Turn camera off |

---

## 📦 Requirements

```
flask
flask-pymongo
flask-login
bcrypt
pymongo
opencv-python
mediapipe
fer
numpy
```

Install all with:

```bash
pip install -r requirements.txt
```

> **Note:** `mediapipe` requires Python 3.8–3.11. Make sure your Python version is compatible.

---

## 📌 Notes

- A webcam is required for real-time detection.
- The `.venv/` folder is included in the zip but should be excluded from GitHub. Add it to `.gitignore`.
- MongoDB Atlas credentials in `app.py` should be moved to environment variables before deploying publicly.

---

## 🔒 .gitignore Recommendation

Add this to your `.gitignore` before pushing to GitHub:

```
.venv/
__pycache__/
*.pyc
.env
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements

- [MediaPipe by Google](https://mediapipe.dev/)
- [FER — Facial Expression Recognition](https://github.com/justinshenk/fer)
- [OpenCV](https://opencv.org/)
- [Flask](https://flask.palletsprojects.com/)
- [MongoDB Atlas](https://www.mongodb.com/atlas)
