"""
CropCare AI - Flask backend.
Serves the trained model + rule-based advisory knowledge base.

Run:
    pip install -r requirements.txt
    python app.py
Then open website/demo.html in a browser (or host both together).
"""
import json, os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
from PIL import Image
import tensorflow as tf

from knowledge_base import get_advice

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "crop_disease_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "model", "labels.json")

app = Flask(__name__, static_folder="../website", static_url_path="")
CORS(app)  # allow the frontend (file:// or another origin) to call this API

IMG_SIZE = (224, 224)
model = None
gatekeeper_model = None
class_names = []

PLANT_RELATED_WORDS = {
    "leaf", "plant", "tree", "flower", "vegetable", "fruit", "fungus", "mushroom",
    "cabbage", "broccoli", "zucchini", "cucumber", "pot", "greenhouse", "garden",
    "acorn", "ear", "bell_pepper", "cucumber", "head_cabbage", "fig", "pineapple",
    "banana", "pomegranate", "lemon", "orange", "strawberry", "hay", "daisy",
    "sunflower", "cardoon", "artichoke", "poppy", "rose", "grass", "rapeseed"
}

def load_model():
    global model, gatekeeper_model, class_names
    try:
        gatekeeper_model = tf.keras.applications.MobileNetV2(weights="imagenet")
        print("Leaf gatekeeper (ImageNet) loaded successfully.")
    except Exception as e:
        print(f"Could not load gatekeeper: {e}")

    if not os.path.exists(MODEL_PATH):
        print("WARNING: model/crop_disease_model.h5 not found.")
        print("Run train.py first (see README_BACKEND.md). Server runs in SIMULATION mode.")
        return
    model = tf.keras.models.load_model(
        MODEL_PATH,
        custom_objects={
            "preprocess": tf.keras.applications.mobilenet_v2.preprocess_input
        },
        compile=False
    )
    with open(LABELS_PATH) as f:
        class_names = json.load(f)
    print(f"Model loaded: {len(class_names)} classes")

load_model()

NON_PLANT_WORDS = {
    "cat", "dog", "cougar", "tiger", "feline", "tabby", "lion", "cheetah", "leopard",
    "canine", "hound", "terrier", "retriever", "dingo", "car", "vehicle", "wheel",
    "automobile", "person", "human", "face", "suit", "jersey", "phone", "cellular",
    "computer", "screen", "keyboard", "bottle", "cup", "chair", "furniture", "shoe",
    "bird", "horse", "bear", "cattle", "cow", "sheep", "pig", "elephant", "room",
    "building", "window", "desk", "table", "wall", "cloth", "paper", "book"
}

def check_is_plant(arr):
    """Checks if the image is a plant leaf or a non-plant object (cat, car, dog, person, etc.)."""
    if gatekeeper_model is None:
        print("[GATEKEEPER WARNING] Gatekeeper model not loaded, skipping check.")
        return True, "Plant / Leaf", 1.0
    try:
        preds = gatekeeper_model.predict(arr, verbose=0)
        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=5)[0]
        print(f"[GATEKEEPER LOG] Top ImageNet predictions: {[(d[1], round(float(d[2]), 3)) for d in decoded]}")

        top_id, top_label, top_conf = decoded[0]
        readable_label = top_label.replace("_", " ").title()
        top_label_lower = top_label.lower()

        # 1. Direct check: Is top label a known non-plant (animal, vehicle, person)?
        is_known_non_plant = any(w in top_label_lower for w in NON_PLANT_WORDS)
        if is_known_non_plant and top_conf >= 0.08:
            print(f"[GATEKEEPER REJECTED] Non-plant detected: {readable_label} ({top_conf*100:.1f}%)")
            return False, readable_label, round(float(top_conf) * 100, 1)

        # 2. Check if top 3 predictions are dominated by non-plant objects
        non_plant_score = sum(d[2] for d in decoded[:3] if any(w in d[1].lower() for w in NON_PLANT_WORDS))
        if non_plant_score >= 0.15:
            # find most prominent non-plant name
            for d in decoded:
                if any(w in d[1].lower() for w in NON_PLANT_WORDS):
                    readable_label = d[1].replace("_", " ").title()
                    break
            print(f"[GATEKEEPER REJECTED] Non-plant score {non_plant_score*100:.1f}%: {readable_label}")
            return False, readable_label, round(float(non_plant_score) * 100, 1)

        # 3. Botanical check
        is_plant_related = any(w in top_label_lower for w in PLANT_RELATED_WORDS)
        if not is_plant_related and top_conf >= 0.20:
            has_plant = any(any(w in d[1].lower() for w in PLANT_RELATED_WORDS) and d[2] > 0.15 for d in decoded[:3])
            if not has_plant:
                print(f"[GATEKEEPER REJECTED] Unrelated object: {readable_label} ({top_conf*100:.1f}%)")
                return False, readable_label, round(float(top_conf) * 100, 1)

        print(f"[GATEKEEPER PASSED] Verified as plant leaf.")
        return True, "Plant / Leaf", 1.0
    except Exception as e:
        print(f"[GATEKEEPER ERROR] Exception during check: {e}")
        return True, "Plant / Leaf", 1.0

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok", "model_loaded": model is not None,
                    "gatekeeper_loaded": gatekeeper_model is not None,
                    "classes": len(class_names)})

@app.route("/classes")
def classes():
    return jsonify({"classes": class_names})

@app.route("/predict", methods=["POST"])
def predict():
    """Accepts multipart/form-data with field 'image'. Returns crop, disease,
    confidence and full advisory data."""
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    file = request.files["image"]
    try:
        img = Image.open(file.stream).convert("RGB").resize(IMG_SIZE)
    except Exception:
        return jsonify({"error": "Invalid image file"}), 400

    arr = np.asarray(img, dtype=np.float32)[None, ...]
    arr = tf.keras.applications.mobilenet_v2.preprocess_input(arr)

    # 1. Check if image actually contains a plant/leaf
    is_plant, detected_name, gatekeeper_conf = check_is_plant(arr)
    if not is_plant:
        return jsonify({
            "is_plant": False,
            "detected_object": detected_name,
            "confidence": gatekeeper_conf,
            "crop": "Non-Crop Image",
            "disease": f"Not a Leaf ({detected_name} Detected)",
            "desc": f"The uploaded photo appears to contain '{detected_name}' rather than a crop leaf. The disease classifier works exclusively on plant leaves (Tomato, Potato, Bell Pepper).",
            "fertilizer": "Not applicable — no crop leaf detected.",
            "nutrients": "Not applicable.",
            "care": [
                "Take a close-up photo of the crop leaf in clear lighting.",
                "Ensure the leaf covers most of the camera frame.",
                "Avoid animals, people, vehicles, or cluttered backgrounds in the photo."
            ],
            "simulated": False
        })

    if model is None:
        # Simulation fallback (same behavior as frontend demo)
        import random
        if class_names:
            label = random.choice(class_names)
        else:
            fallback = ["Tomato___Early_blight", "Potato___Late_blight",
                        "Rice___Leaf_blast", "Corn_(maize)___Common_rust_",
                        "Tomato___healthy"]
            label = random.choice(fallback)
        advice = get_advice(label)
        return jsonify({"crop": advice["crop"], "disease": advice["disease"],
                        "confidence": round(random.uniform(72, 97), 1),
                        "simulated": True, **advice})

    probs = model.predict(arr, verbose=0)[0]
    top = int(np.argmax(probs))
    label = class_names[top]
    advice = get_advice(label)
    return jsonify({"crop": advice["crop"], "disease": advice["disease"],
                    "confidence": round(float(probs[top]) * 100, 1),
                    "top3": [{"label": class_names[i], "prob": round(float(probs[i])*100, 1)}
                             for i in probs.argsort()[-3:][::-1]],
                    "simulated": False, **advice})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
