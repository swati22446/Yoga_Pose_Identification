import os
import io
import base64
import numpy as np
from flask import Flask, request, render_template, redirect, url_for
from tensorflow.keras.models import load_model
from PIL import Image

app = Flask(__name__)

# ── Configuration ──────────────────────────────────────────────────────────────
MODEL_PATH   = os.path.join(os.path.dirname(__file__), 'xcep_yoga_best.keras')
IMG_SIZE     = (299, 299)
ALLOWED_EXT  = {'png', 'jpg', 'jpeg', 'webp'}

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024   # 10 MB

# ── Class labels (must match training order) ───────────────────────────────────
CLASS_LABELS = ['Downdog', 'Goddess', 'Plank', 'Tree', 'Warrior2']

# ── Pose info ──────────────────────────────────────────────────────────────────
POSE_INFO = {
    'Downdog': {
        'display': 'Downward Dog',
        'emoji': '🐕',
        'description': (
            "Downward-Facing Dog (Adho Mukha Svanasana) is one of yoga's most iconic poses, "
            "forming a full-body stretch in an inverted V-shape. "
            "It deeply lengthens the hamstrings, calves, and spine while building strength in the arms and shoulders. "
            "Regular practice decompresses the vertebrae, improves circulation to the brain, and relieves tension headaches. "
            "It is commonly used as a transitional and resting pose in Vinyasa and Ashtanga flows."
        ),
        'benefits': ['Relieves back pain', 'Improves circulation', 'Stretches hamstrings & calves'],
    },
    'Goddess': {
        'display': 'Goddess Pose',
        'emoji': '👸',
        'description': (
            "Goddess Pose (Utkata Konasana) is a powerful wide-legged squat that radiates strength and stability. "
            "With feet turned out and arms raised, the pose simultaneously opens the hips and engages the entire lower body. "
            "It targets the quadriceps, glutes, inner thighs, and core, building functional strength and endurance. "
            "The pose also stimulates the sacral chakra, encouraging creativity and emotional balance. "
            "It is a staple in sequences focused on grounding energy and lower-body conditioning."
        ),
        'benefits': ['Tones inner thighs', 'Opens hip flexors', 'Builds core strength'],
    },
    'Plank': {
        'display': 'Plank Pose',
        'emoji': '💪',
        'description': (
            "Plank Pose (Phalakasana) is a foundational pose that develops total-body strength and mental endurance. "
            "The body is held in a straight line from head to heels, requiring engagement of the core, arms, and legs together. "
            "It is particularly effective for strengthening the transverse abdominis and preventing lower-back injury. "
            "Holding the plank also improves spinal alignment and builds the focus needed for advanced arm balances. "
            "It serves as the launchpad for transitions like Chaturanga and Side Plank in dynamic flows."
        ),
        'benefits': ['Strengthens core', 'Improves posture', 'Tones arms & shoulders'],
    },
    'Tree': {
        'display': 'Tree Pose',
        'emoji': '🌳',
        'description': (
            "Tree Pose (Vrksasana) is a classical balancing posture that cultivates stillness and mental clarity. "
            "Standing on one leg with the other foot pressed to the inner thigh or calf, you embody the rootedness of a tree. "
            "The pose strengthens the ankles, knees, and standing-leg muscles while stretching the groin and inner thigh. "
            "It trains proprioception — the body's awareness of its position in space — which benefits all physical activities. "
            "Consistent practice sharpens concentration and fosters the mind-body connection at the heart of yoga."
        ),
        'benefits': ['Improves balance', 'Strengthens ankles', 'Enhances concentration'],
    },
    'Warrior2': {
        'display': 'Warrior II',
        'emoji': '⚔️',
        'description': (
            "Warrior II (Virabhadrasana II) is a dynamic standing pose that embodies power, focus, and determination. "
            "With legs spread wide, the front knee bent to 90 degrees, and arms extended parallel to the floor, it opens the entire body. "
            "It builds significant stamina and strength in the quadriceps, hamstrings, and glutes while opening the hips and chest. "
            "The steady drishti (gaze) over the front fingertips develops mental fortitude and unwavering focus. "
            "Warrior II is a cornerstone of Hatha and Vinyasa sequences and is accessible yet deeply challenging for all levels."
        ),
        'benefits': ['Strengthens legs', 'Opens hips & chest', 'Builds endurance'],
    },
}

# ── Load model safely ──────────────────────────────────────────────────────────
model = None

def get_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found at: {MODEL_PATH}. "
                "Place 'xcep_yoga_best.keras' in the Flask/ folder."
            )
        print("Loading model…")
        model = load_model(MODEL_PATH)
        print("Model loaded successfully.")
    return model

# ── Helpers ────────────────────────────────────────────────────────────────────
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def preprocess_and_predict(img_bytes):
    img   = Image.open(io.BytesIO(img_bytes)).convert('RGB').resize(IMG_SIZE)
    arr   = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)
    preds = get_model().predict(arr, verbose=0)[0]

    top   = int(np.argmax(preds))
    label = CLASS_LABELS[top]
    conf  = round(float(preds[top]) * 100, 2)

    # All classes sorted descending — list of (display_name, pct) tuples for Jinja
    all_preds = sorted(
        [(CLASS_LABELS[i], round(float(p) * 100, 2)) for i, p in enumerate(preds)],
        key=lambda x: x[1], reverse=True
    )
    return label, conf, all_preds

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/input')
def input_page():
    return render_template('input.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Validate upload
    if 'file' not in request.files:
        return render_template('input.html', error='No file uploaded.')

    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return render_template('input.html', error='Invalid file. Please use PNG, JPG, or WEBP.')

    try:
        img_bytes            = file.read()
        label, conf, all_preds = preprocess_and_predict(img_bytes)
    except FileNotFoundError as e:
        return render_template('input.html', error=str(e))
    except Exception as e:
        return render_template('input.html', error=f'Prediction failed: {str(e)}')

    # Encode image as base64 for embedding directly in output.html
    ext     = file.filename.rsplit('.', 1)[1].lower()
    img_b64 = base64.b64encode(img_bytes).decode('utf-8')

    info = POSE_INFO.get(label, {
        'display': label.title(), 'emoji': '🧘',
        'description': '', 'benefits': []
    })

    return render_template(
        'output.html',
        display=info['display'],
        emoji=info['emoji'],
        description=info['description'],
        benefits=info['benefits'],
        confidence=conf,
        all_preds=all_preds,   # list of (name, pct) tuples
        img_b64=img_b64,
        img_ext=ext,
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"\n✅  Server → http://127.0.0.1:{port}\n")
    app.run(debug=True, host='0.0.0.0', port=port)