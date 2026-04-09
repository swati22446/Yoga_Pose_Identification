# 🧘 Yoga Pose Classifier

AI-powered yoga pose detection using **Xception Transfer Learning** + **Flask** web application.

## Project Structure

```
YOGA POSE/
├── Dataset/                        ← Download dataset here (see below)
├── Flask/
│   ├── static/
│   │   ├── assets/                 ← Any images/icons
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   ├── templates/
│   │   ├── index.html              ← Landing page
│   │   ├── input.html              ← Upload page
│   │   └── output.html             ← Results page
│   ├── app.py                      ← Flask backend
│   ├── link.txt                    ← Dataset & resource links
│   ├── uploaded_image.png          ← Auto-saved on prediction
│   └── xcep_yoga.h5                ← Trained model (add after training)
└── Training/
    └── Xception.ipynb              ← Google Colab training notebook
```

## Detected Poses

| Pose | Class |
|------|-------|
| 🐕 Downward Dog | `downdog` |
| 👸 Goddess | `goddess` |
| 💪 Plank | `plank` |
| 🌳 Tree | `tree` |
| ⚔️ Warrior II | `warrior2` |

---

## Step 1 — Get the Dataset

Download from Kaggle: https://www.kaggle.com/datasets/ujjwalchowdhury/yoga-pose-classification

Place in `Dataset/` folder. Structure should be:
```
Dataset/
├── train/
│   ├── downdog/
│   ├── goddess/
│   ├── plank/
│   ├── tree/
│   └── warrior2/
└── test/
    ├── downdog/
    └── ...
```

---

## Step 2 — Train the Model (Google Colab)

1. Open `Training/Xception.ipynb` in [Google Colab](https://colab.research.google.com)
2. Enable GPU: Runtime → Change runtime type → T4 GPU
3. Upload your `kaggle.json` API token when prompted
4. Run all cells
5. Download `xcep_yoga.h5` from your Google Drive
6. Place it in the `Flask/` folder

---

## Step 3 — Run the Flask App

```bash
cd Flask

# Install dependencies
pip install flask tensorflow numpy pillow

# Run
python app.py
```

Open: **http://localhost:5000**

---

## How It Works

```
User uploads image (input.html)
        ↓
Flask saves it as uploaded_image.png
        ↓
Xception model predicts (299×299 input)
        ↓
Results shown on output.html
(pose name, confidence %, all class probabilities, benefits)
```

## Model Architecture

```
Input (299×299×3)
    → Xception Base (ImageNet, frozen → fine-tuned)
    → GlobalAveragePooling2D
    → BatchNorm → Dense(512) → Dropout(0.4)
    → Dense(256) → Dropout(0.3)
    → Dense(5, Softmax)
```
