from flask import Flask, render_template, request, redirect, url_for, jsonify, flash , Response, send_from_directory
from flask_pymongo import PyMongo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from bson import ObjectId
import bcrypt
import cv2
import mediapipe as mp
from fer import FER
import numpy as np
import certifi

# Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # change to strong secret key

# MongoDB config
app.config["MONGO_URI"] = "mongodb+srv://kapalasuryacharan1:R.2qyTRpHgaA9_B@cluster0.ozoe4sw.mongodb.net/mydatabase?retryWrites=true&w=majority"
mongo = PyMongo(app, tlsCAFile=certifi.where())

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ---- User class ----
class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc["_id"])
        self.username = user_doc["username"]

@login_manager.user_loader
def load_user(user_id):
    user_doc = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_doc) if user_doc else None

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets', filename)


# ---- Mediapipe + FER setup ----
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.6)

emotion_detector = FER(mtcnn=True)
cap = cv2.VideoCapture(0)
camera_on = True


# ---- Hand Gesture Classification ----
def classify_hand_landmarks(hand_landmarks):
    tips = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky
    fingers = []

    # Handedness check
    hand_label = "Right" if hand_landmarks.landmark[17].x < hand_landmarks.landmark[5].x else "Left"

    # Thumb
    if hand_label == "Right":
        fingers.append(1 if hand_landmarks.landmark[tips[0]].x > hand_landmarks.landmark[tips[0] - 1].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x else 0)

    # Other fingers
    for id in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tips[id]].y < hand_landmarks.landmark[tips[id] - 2].y else 0)

    total_fingers = sum(fingers)

    if total_fingers == 0:
        return "Fist ✊"
    elif total_fingers == 5:
        return "Open Palm 🖐"
    elif fingers == [0,1,0,0,0]:
        return "1 Finger ☝️"
    elif fingers == [0,1,1,0,0]:
        return "2 Fingers ✌️"
    elif fingers == [0,1,1,1,0]:
        return "3 Fingers"
    elif fingers == [0,1,1,1,1]:
        return "4 Fingers"
    elif fingers == [1,0,0,0,0]:
        wrist_y = hand_landmarks.landmark[0].y
        thumb_y = hand_landmarks.landmark[tips[0]].y
        return "Thumbs Up 👍" if thumb_y < wrist_y else "Thumbs Down 👎"
    return f"{total_fingers} Fingers"


# ---- Frame Generator ----
def generate_frames(mode="gestures"):
    global camera_on, cap
    while True:
        if not camera_on:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            continue

        if not cap.isOpened():
            cap = cv2.VideoCapture(0)

        success, frame = cap.read()
        if not success:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if mode == "gestures":
            results = hands.process(rgb)
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
                    gesture = classify_hand_landmarks(handLms)
                    h, w, _ = frame.shape
                    cx = int(handLms.landmark[0].x * w)
                    cy = int(handLms.landmark[0].y * h)
                    cv2.putText(frame, gesture, (cx, cy - 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        elif mode == "facial":
            result = emotion_detector.detect_emotions(rgb)
            if result:
                for face in result:
                    (x, y, w, h) = face["box"]
                    emotions = face["emotions"]
                    top_emotion = max(emotions, key=emotions.get)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{top_emotion.capitalize()}",
                                (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                1, (0, 255, 0), 2)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# ---- Auth Routes ----
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print("REGISTER ATTEMPT:", username)  # <-- Debug print

        if mongo.db.users.find_one({"username": username}):
            flash("Username already exists!", "danger")
            return redirect(url_for("register"))

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        mongo.db.users.insert_one({"username": username, "password": hashed_pw})
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_doc = mongo.db.users.find_one({"username": username})
        if user_doc and bcrypt.checkpw(password.encode("utf-8"), user_doc["password"]):
            login_user(User(user_doc))
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid credentials", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))


# ---- App Routes ----
@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("index.html", username=current_user.username)
    return render_template("login.html")

@app.route("/facial")
@login_required
def facial_page():
    return render_template("facial.html")

@app.route("/gestures")
@login_required
def gestures_page():
    return render_template("gestures.html")

@app.route("/video_feed/<mode>")
@login_required
def video_feed(mode):
    return jsonify({"error": "Invalid mode"}) if mode not in ["gestures", "facial"] else Response(
        generate_frames(mode), mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route("/camera_on")
@login_required
def turn_camera_on():
    global camera_on, cap
    camera_on = True
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    return jsonify({"status": "Camera ON"})

@app.route("/camera_off")
@login_required
def turn_camera_off():
    global camera_on, cap
    camera_on = False
    if cap.isOpened():
        cap.release()
    return jsonify({"status": "Camera OFF"})


if __name__ == "__main__":
    app.run(debug=True)
