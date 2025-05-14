from flask import Flask, render_template, request, redirect, url_for, session
import os
import uuid
from datetime import datetime
import cv2
import numpy as np
from roboflow import Roboflow
import supervision as sv
from werkzeug.utils import secure_filename
from utils.treatment import get_treatment_plan

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

users = {}
treatment_history = []

# Roboflow setup
rf = Roboflow(api_key="8Ig4ZXFGMdcjm9YWzPsL")
project = rf.workspace().project("apple-plant-disease-detection-p2448-aurbo")
model = project.version(4).model

class_map = {
    0: "Apple_Black_rot",
    1: "Apple_cedar_Apple_rust",
    2: "Apple_healthy",
    3: "Apple_scab"
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(path)
        return path, filename
    return None, None

def calculate_severity_category(score):
    if score >= 66:
        return "Severe"
    elif score >= 33:
        return "Moderate"
    elif score > 0:
        return "Mild"
    else:
        return "None"

def analyze_image(image_path, original_filename):
    result = model.predict(image_path, confidence=40, overlap=30).json()
    image = cv2.imread(image_path)

    detections = sv.Detections.from_inference(result)
    labels = [class_map.get(class_id, 'Unknown') for class_id in detections.class_id]

    annotated_image = sv.BoundingBoxAnnotator().annotate(image.copy(), detections)
    annotated_image = sv.LabelAnnotator().annotate(annotated_image, detections, labels)

    result_filename = f"{uuid.uuid4().hex}_{original_filename}"
    result_path = os.path.join(RESULT_FOLDER, result_filename)
    cv2.imwrite(result_path, annotated_image)

    height, width, _ = image.shape
    image_area = height * width

    total_box_area = 0
    if isinstance(detections.xyxy, np.ndarray) and len(detections.xyxy) > 0:
        for box in detections.xyxy:
            x1, y1, x2, y2 = map(int, box)
            total_box_area += (x2 - x1) * (y2 - y1)

        predicted_class = labels[0] if labels else "Apple_healthy"
        severity_score = round((total_box_area / image_area) * 100, 1)
    else:
        predicted_class = "Apple_healthy"
        severity_score = 0.0

    return predicted_class, result_filename, severity_score

# Integrated Pesticide Recommendation Function
def get_pesticide_recommendation(disease, severity_score):
    recommendation = {
        "message": "No pesticide recommendation available.",
        "strength": "N/A",
        "products": "N/A",
        "frequency": "N/A",
        "safety": "N/A"
    }

    if disease == "Apple_Black_rot":
        if severity_score <= 30:
            recommendation.update({
                "message": "Mild infection detected. Early control advised.",
                "strength": "1.5 ml per liter of water",
                "products": "Captan 50 WP, Ziram 76DF",
                "frequency": "Spray once every 10 days",
                "safety": "Wear gloves and a mask. Avoid spraying during windy conditions. Wash hands after use."
            })
        elif severity_score <= 60:
            recommendation.update({
                "message": "Moderate infection. Start immediate treatment.",
                "strength": "2 ml per liter of water",
                "products": "Thiophanate-methyl, Myclobutanil",
                "frequency": "Spray every 7 days for 2 weeks",
                "safety": "Avoid eye and skin contact. Wash equipment thoroughly after spraying."
            })
        else:
            recommendation.update({
                "message": "Severe infection. Aggressive pesticide plan required.",
                "strength": "2.5–3 ml per liter",
                "products": "Copper-based fungicides, Mancozeb, or Dithane M-45",
                "frequency": "Spray every 5 days for 3 applications",
                "safety": "Use full PPE. Keep children and animals away for 24 hours."
            })

    elif disease == "Apple_cedar_Apple_rust":
        if severity_score <= 30:
            recommendation.update({
                "message": "Low-level rust. Preventative fungicide recommended.",
                "strength": "1–1.5 ml per liter",
                "products": "Myclobutanil, Propiconazole",
                "frequency": "Apply once every 14 days",
                "safety": "Apply during early morning or evening. Wear long sleeves and goggles."
            })
        elif severity_score <= 60:
            recommendation.update({
                "message": "Moderate rust. Begin treatment promptly.",
                "strength": "2 ml per liter",
                "products": "Propiconazole, Mancozeb",
                "frequency": "Apply weekly for 3 weeks",
                "safety": "Avoid inhaling spray mist. Store chemicals in original containers."
            })
        else:
            recommendation.update({
                "message": "High infection rate. Control immediately.",
                "strength": "2.5–3 ml per liter",
                "products": "Trifloxystrobin + Tebuconazole (e.g., Nativo)",
                "frequency": "Apply every 5 days for 3 cycles",
                "safety": "Use full PPE. Do not spray during pollination period."
            })

    elif disease == "Apple_scab":
        if severity_score <= 30:
            recommendation.update({
                "message": "Initial scab signs. Preventive action required.",
                "strength": "1.5 ml per liter",
                "products": "Captan or Mancozeb",
                "frequency": "Apply every 10–14 days",
                "safety": "Ensure foliage is dry before spraying. Wear rubber gloves and mask."
            })
        elif severity_score <= 60:
            recommendation.update({
                "message": "Moderate scab. Apply curative fungicides.",
                "strength": "2 ml per liter",
                "products": "Dodine or Trifloxystrobin",
                "frequency": "Apply weekly for 3–4 weeks",
                "safety": "Avoid contact with eyes. Wash sprayer after use."
            })
        else:
            recommendation.update({
                "message": "Advanced scab detected. Use systemic fungicides.",
                "strength": "3 ml per liter",
                "products": "Difenoconazole, Copper Oxychloride",
                "frequency": "Spray every 4–5 days until symptoms reduce",
                "safety": "Apply with respirator. Do not allow spray to drift into water sources."
            })

    elif disease == "Apple_healthy":
        recommendation.update({
            "message": "Plant is healthy. No pesticide needed.",
            "strength": "None",
            "products": "None",
            "frequency": "Not applicable",
            "safety": "Continue regular inspection and maintain hygiene."
        })

    return recommendation


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if email in users:
            return "Email already registered!"
        users[email] = {'name': name, 'password': password}
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)
        if user and user['password'] == password:
            session['user'] = email
            return redirect(url_for('dashboard'))
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=users[session['user']]['name'])

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('login'))

    if 'image' not in request.files:
        return "No image uploaded."

    file = request.files['image']
    image_path, original_filename = save_image(file)

    if not image_path:
        return "Invalid file."

    disease, result_filename, severity_score = analyze_image(image_path, original_filename)
    severity = calculate_severity_category(severity_score)

    session['disease'] = disease
    session['severity_score'] = severity_score

    treatment_history.append({
        'user': session['user'],
        'image': result_filename,
        'disease': disease,
        'severity_score': severity_score,
        'date': datetime.now().strftime("%Y-%m-%d")
    })

    return render_template('predict.html',
                           image_path=result_filename,
                           disease=disease,
                           severity_score=severity_score,
                           severity=severity,
                           concentration=f"{severity_score:.1f}%",
                           recommendation=[ 
                               "Apply pesticide suited to severity.",
                               "Isolate affected plants.",
                               "Follow up in 5 days."
                           ])

@app.route('/ai_treatment', methods=['GET', 'POST'])
def ai_treatment():
    treatment_result = None

    if request.method == 'POST':
        disease = request.form['disease']
        severity_score = int(request.form['severity'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        soil_type = request.form['soil_type']
        growth_stage = request.form['growth_stage']

        treatment_result = get_treatment_plan(
            disease=disease,
            severity_score=severity_score,
            temperature=temperature,
            humidity=humidity,
            soil_type=soil_type,
            growth_stage=growth_stage,
        )

    return render_template('ai_treatment.html', treatment=treatment_result)

@app.route('/treatment')
def treatment():
    if 'user' not in session:
        return redirect(url_for('login'))

    history = [entry for entry in treatment_history if entry['user'] == session['user']]
    return render_template('treatment.html', history=history)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
