"""
CropCare AI - Flask backend
"""

import json
import os
import random

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
from PIL import Image
import tensorflow as tf

from knowledge_base import get_advice


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "crop_disease_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "model", "labels.json")
WEBSITE_DIR = os.path.join(BASE_DIR, "website")

app = Flask(
    __name__,
    static_folder=WEBSITE_DIR,
    static_url_path=""
)

CORS(app)

IMG_SIZE = (224, 224)

model = None
gatekeeper_model = None
class_names = []


PLANT_RELATED_WORDS = {
    "leaf", "plant", "tree", "flower", "vegetable", "fruit",
    "fungus", "mushroom", "cabbage", "broccoli", "zucchini",
    "cucumber", "pot", "greenhouse", "garden", "acorn", "ear",
    "bell_pepper", "head_cabbage", "fig", "pineapple", "banana",
    "pomegranate", "lemon", "orange", "strawberry", "hay",
    "daisy", "sunflower", "cardoon", "artichoke", "poppy",
    "rose", "grass", "rapeseed"
}


NON_PLANT_WORDS = {
    "cat", "dog", "cougar", "tiger", "feline", "tabby", "lion",
    "cheetah", "leopard", "canine", "hound", "terrier", "retriever",
    "dingo", "car", "vehicle", "wheel", "automobile", "person",
    "human", "face", "suit", "jersey", "phone", "cellular",
    "computer", "screen", "keyboard", "bottle", "cup", "chair",
    "furniture", "shoe", "bird", "horse", "bear", "cattle",
    "cow", "sheep", "pig", "elephant", "room", "building",
    "window", "desk", "table", "wall", "cloth", "paper", "book"
}


def load_model():
    global model, gatekeeper_model, class_names

    # Load MobileNetV2 gatekeeper
    try:
        gatekeeper_model = tf.keras.applications.MobileNetV2(
            weights="imagenet"
        )
        print("Leaf gatekeeper loaded successfully.")
    except Exception as e:
        print("Gatekeeper could not be loaded:", e)
        gatekeeper_model = None

    # Load crop disease model
    if not os.path.exists(MODEL_PATH):
        print("WARNING: Model file not found:")
        print(MODEL_PATH)
        return

    if not os.path.exists(LABELS_PATH):
        print("WARNING: labels.json not found:")
        print(LABELS_PATH)
        return

    try:
        model = tf.keras.models.load_model(
            MODEL_PATH,
            compile=False
        )

        with open(LABELS_PATH, "r", encoding="utf-8") as f:
            class_names = json.load(f)

        print("Crop disease model loaded successfully.")
        print("Classes:", len(class_names))

    except Exception as e:
        print("Could not load crop disease model:", e)
        model = None


def check_is_plant(arr):
    if gatekeeper_model is None:
        return True, "Plant / Leaf", 100.0

    try:
        preds = gatekeeper_model.predict(arr, verbose=0)

        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(
            preds,
            top=5
        )[0]

        print(
            "[GATEKEEPER]",
            [
                (d[1], round(float(d[2]), 3))
                for d in decoded
            ]
        )

        top_label = decoded[0][1]
        top_conf = float(decoded[0][2])

        readable_label = top_label.replace("_", " ").title()
        top_label_lower = top_label.lower()

        # Check obvious non-plant objects
        if any(word in top_label_lower for word in NON_PLANT_WORDS):
            if top_conf >= 0.08:
                return (
                    False,
                    readable_label,
                    round(top_conf * 100, 1)
                )

        # Check top 3 predictions
        non_plant_score = 0.0

        for item in decoded[:3]:
            label = item[1].lower()
            confidence = float(item[2])

            if any(word in label for word in NON_PLANT_WORDS):
                non_plant_score += confidence

        if non_plant_score >= 0.15:
            for item in decoded:
                label = item[1].lower()

                if any(word in label for word in NON_PLANT_WORDS):
                    readable_label = item[1].replace(
                        "_", " "
                    ).title()
                    break

            return (
                False,
                readable_label,
                round(non_plant_score * 100, 1)
            )

        # Botanical check
        is_plant_related = any(
            word in top_label_lower
            for word in PLANT_RELATED_WORDS
        )

        if not is_plant_related and top_conf >= 0.20:

            has_plant = False

            for item in decoded[:3]:
                label = item[1].lower()
                confidence = float(item[2])

                if (
                    any(
                        word in label
                        for word in PLANT_RELATED_WORDS
                    )
                    and confidence > 0.15
                ):
                    has_plant = True
                    break

            if not has_plant:
                return (
                    False,
                    readable_label,
                    round(top_conf * 100, 1)
                )

        return True, "Plant / Leaf", 100.0

    except Exception as e:
        print("Gatekeeper error:", e)

        # Do not block the application if gatekeeper fails
        return True, "Plant / Leaf", 100.0


load_model()


@app.route("/")
def home():
    return send_from_directory(
        WEBSITE_DIR,
        "index.html"
    )


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "gatekeeper_loaded": gatekeeper_model is not None,
        "classes": len(class_names)
    })


@app.route("/classes")
def classes():
    return jsonify({
        "classes": class_names
    })


@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:
        return jsonify({
            "error": "No image uploaded"
        }), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({
            "error": "No image selected"
        }), 400

    try:
        img = Image.open(file.stream).convert("RGB")
        img = img.resize(IMG_SIZE)

    except Exception:
        return jsonify({
            "error": "Invalid image file"
        }), 400

    arr = np.asarray(
        img,
        dtype=np.float32
    )

    arr = np.expand_dims(arr, axis=0)

    arr = tf.keras.applications.mobilenet_v2.preprocess_input(
        arr
    )

    # Check whether image contains a plant
    is_plant, detected_name, gatekeeper_conf = check_is_plant(arr)

    if not is_plant:

        return jsonify({
            "is_plant": False,
            "detected_object": detected_name,
            "confidence": gatekeeper_conf,
            "crop": "Non-Crop Image",
            "disease": f"Not a Leaf ({detected_name} Detected)",
            "desc": (
                "The uploaded photo appears to contain "
                f"'{detected_name}' instead of a crop leaf."
            ),
            "fertilizer": (
                "Not applicable — no crop leaf detected."
            ),
            "nutrients": "Not applicable.",
            "care": [
                "Take a close-up photo of the crop leaf.",
                "Make sure the leaf is clearly visible.",
                "Use good lighting.",
                "Avoid animals, people and objects "
                "in the background."
            ],
            "simulated": False
        })

    # If trained model is not available
    if model is None:

        if class_names:
            label = random.choice(class_names)
        else:
            fallback = [
                "Tomato___Early_blight",
                "Potato___Late_blight",
                "Tomato___healthy",
                "Corn_(maize)___Common_rust_"
            ]

            label = random.choice(fallback)

        advice = get_advice(label)

        return jsonify({
            "crop": advice["crop"],
            "disease": advice["disease"],
            "confidence": round(
                random.uniform(72, 97),
                1
            ),
            "simulated": True,
            **advice
        })

    # Run disease prediction
    try:

        probs = model.predict(
            arr,
            verbose=0
        )[0]

        top = int(np.argmax(probs))

        if top >= len(class_names):
            return jsonify({
                "error": "Model classes do not match labels.json"
            }), 500

        label = class_names[top]

        advice = get_advice(label)

        top_indices = probs.argsort()[-3:][::-1]

        top3 = []

        for i in top_indices:
            if i < len(class_names):
                top3.append({
                    "label": class_names[i],
                    "prob": round(
                        float(probs[i]) * 100,
                        1
                    )
                })

        return jsonify({
            "is_plant": True,
            "crop": advice["crop"],
            "disease": advice["disease"],
            "confidence": round(
                float(probs[top]) * 100,
                1
            ),
            "top3": top3,
            "simulated": False,
            **advice
        })

    except Exception as e:

        print("Prediction error:", e)

        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
