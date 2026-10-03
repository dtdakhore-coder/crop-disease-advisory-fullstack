"""
CropCare AI - Flask backend
Serves the trained crop-disease model, plant-image gatekeeper,
and rule-based advisory knowledge base.
"""

import json
import os
import random

import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from knowledge_base import get_advice


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "crop_disease_model.h5"
)

LABELS_PATH = os.path.join(
    BASE_DIR,
    "model",
    "labels.json"
)

WEBSITE_DIR = os.path.join(
    BASE_DIR,
    "website"
)


# ============================================================
# FLASK APP
# ============================================================

app = Flask(
    __name__,
    static_folder=WEBSITE_DIR,
    static_url_path=""
)

CORS(app)


# ============================================================
# SETTINGS
# ============================================================

IMG_SIZE = (224, 224)

model = None
gatekeeper_model = None
class_names = []


# ============================================================
# PLANT / LEAF WORDS
# ============================================================

PLANT_RELATED_WORDS = {
    "leaf",
    "plant",
    "tree",
    "flower",
    "vegetable",
    "fruit",
    "fungus",
    "mushroom",
    "cabbage",
    "broccoli",
    "zucchini",
    "cucumber",
    "pot",
    "greenhouse",
    "garden",
    "acorn",
    "ear",
    "bell_pepper",
    "head_cabbage",
    "fig",
    "pineapple",
    "banana",
    "pomegranate",
    "lemon",
    "orange",
    "strawberry",
    "hay",
    "daisy",
    "sunflower",
    "cardoon",
    "artichoke",
    "poppy",
    "rose",
    "grass",
    "rapeseed",
    "corn",
    "maize",
    "potato",
    "tomato"
}


# ============================================================
# NON-PLANT WORDS
# ============================================================

NON_PLANT_WORDS = {
    "cat",
    "dog",
    "cougar",
    "tiger",
    "feline",
    "tabby",
    "lion",
    "cheetah",
    "leopard",
    "canine",
    "hound",
    "terrier",
    "retriever",
    "dingo",
    "car",
    "vehicle",
    "wheel",
    "automobile",
    "person",
    "human",
    "face",
    "suit",
    "jersey",
    "phone",
    "cellular",
    "computer",
    "screen",
    "keyboard",
    "bottle",
    "cup",
    "chair",
    "furniture",
    "shoe",
    "bird",
    "horse",
    "bear",
    "cattle",
    "cow",
    "sheep",
    "pig",
    "elephant",
    "room",
    "building",
    "window",
    "desk",
    "table",
    "wall",
    "cloth",
    "paper",
    "book"
}


# ============================================================
# LOAD MODELS
# ============================================================

def load_model():

    global model
    global gatekeeper_model
    global class_names

    # --------------------------------------------------------
    # Load ImageNet gatekeeper
    # --------------------------------------------------------

    try:

        gatekeeper_model = tf.keras.applications.MobileNetV2(
            weights="imagenet"
        )

        print("Leaf gatekeeper loaded successfully.")

    except Exception as e:

        print("WARNING: Gatekeeper could not be loaded.")
        print("Gatekeeper error:", e)

        gatekeeper_model = None


    # --------------------------------------------------------
    # Load crop disease model
    # --------------------------------------------------------

    if not os.path.exists(MODEL_PATH):

        print("WARNING: Crop disease model not found:")
        print(MODEL_PATH)
        print("Running in simulation mode.")

        return


    if not os.path.exists(LABELS_PATH):

        print("WARNING: labels.json not found:")
        print(LABELS_PATH)
        print("Running in simulation mode.")

        return


    try:

        model = tf.keras.models.load_model(
            MODEL_PATH,
            compile=False
        )

        with open(
            LABELS_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            class_names = json.load(f)


        print(
            f"Crop disease model loaded successfully: "
            f"{len(class_names)} classes"
        )


    except Exception as e:

        print("ERROR loading crop disease model:")
        print(e)

        model = None


# ============================================================
# GATEKEEPER
# ============================================================

def check_is_plant(arr):

    """
    Checks whether the uploaded image appears to be
    a plant/leaf rather than an unrelated object.
    """

    # If gatekeeper cannot load, do not crash the application.
    if gatekeeper_model is None:

        print(
            "[GATEKEEPER] Model unavailable. "
            "Allowing image to continue."
        )

        return True, "Plant / Leaf", 100.0


    try:

        predictions = gatekeeper_model.predict(
            arr,
            verbose=0
        )


        decoded = tf.keras.applications.mobilenet_v2.decode_predictions(
            predictions,
            top=5
        )[0]


        print(
            "[GATEKEEPER] Predictions:",
            [
                (
                    item[1],
                    round(float(item[2]), 3)
                )
                for item in decoded
            ]
        )


        # ----------------------------------------------------
        # Top prediction
        # ----------------------------------------------------

        top_id = decoded[0][0]
        top_label = decoded[0][1]
        top_conf = float(decoded[0][2])

        readable_label = top_label.replace(
            "_",
            " "
        ).title()

        top_label_lower = top_label.lower()


        # ----------------------------------------------------
        # Check obvious non-plant objects
        # ----------------------------------------------------

        if any(
            word in top_label_lower
            for word in NON_PLANT_WORDS
        ):

            if top_conf >= 0.08:

                print(
                    "[GATEKEEPER] NON-PLANT:",
                    readable_label
                )

                return (
                    False,
                    readable_label,
                    round(top_conf * 100, 1)
                )


        # ----------------------------------------------------
        # Calculate non-plant score from top 3
        # ----------------------------------------------------

        non_plant_score = 0.0

        for item in decoded[:3]:

            label = item[1].lower()
            confidence = float(item[2])

            if any(
                word in label
                for word in NON_PLANT_WORDS
            ):

                non_plant_score += confidence


        if non_plant_score >= 0.15:

            detected = readable_label

            for item in decoded:

                label = item[1].lower()

                if any(
                    word in label
                    for word in NON_PLANT_WORDS
                ):

                    detected = item[1].replace(
                        "_",
                        " "
                    ).title()

                    break


            print(
                "[GATEKEEPER] NON-PLANT SCORE:",
                detected
            )

            return (
                False,
                detected,
                round(non_plant_score * 100, 1)
            )


        # ----------------------------------------------------
        # Check plant-related predictions
        # ----------------------------------------------------

        top_is_plant = any(
            word in top_label_lower
            for word in PLANT_RELATED_WORDS
        )


        if not top_is_plant and top_conf >= 0.20:

            plant_found = False

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

                    plant_found = True
                    break


            if not plant_found:

                print(
                    "[GATEKEEPER] UNRELATED OBJECT:",
                    readable_label
                )

                return (
                    False,
                    readable_label,
                    round(top_conf * 100, 1)
                )


        print("[GATEKEEPER] PLANT / LEAF PASSED")

        return (
            True,
            "Plant / Leaf",
            100.0
        )


    except Exception as e:

        print(
            "[GATEKEEPER ERROR]:",
            e
        )

        # Never crash the backend because of gatekeeper.
        return (
            True,
            "Plant / Leaf",
            100.0
        )


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return send_from_directory(
        WEBSITE_DIR,
        "index.html"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "gatekeeper_loaded": gatekeeper_model is not None,
        "classes": len(class_names)
    })


# ============================================================
# CLASSES
# ============================================================

@app.route("/classes")
def classes():

    return jsonify({
        "classes": class_names
    })


# ============================================================
# PREDICTION
# ============================================================

@app.route(
    "/predict",
    methods=["POST"]
)
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


    # --------------------------------------------------------
    # Read image
    # --------------------------------------------------------

    try:

        img = Image.open(
            file.stream
        ).convert("RGB")

        img = img.resize(
            IMG_SIZE
        )

    except Exception:

        return jsonify({
            "error": "Invalid image file"
        }), 400


    # --------------------------------------------------------
    # Convert image to NumPy
    # --------------------------------------------------------

    arr = np.asarray(
        img,
        dtype=np.float32
    )

    arr = np.expand_dims(
        arr,
        axis=0
    )


    # --------------------------------------------------------
    # MobileNetV2 preprocessing
    # --------------------------------------------------------

    arr = tf.keras.applications.mobilenet_v2.preprocess_input(
        arr
    )


    # ========================================================
    # STEP 1 - GATEKEEPER
    # ========================================================

    is_plant, detected_name, gatekeeper_conf = check_is_plant(
        arr
    )


    if not is_plant:

        return jsonify({

            "is_plant": False,

            "detected_object": detected_name,

            "confidence": gatekeeper_conf,

            "crop": "Non-Crop Image",

            "disease": (
                f"Not a Leaf "
                f"({detected_name} Detected)"
            ),

            "desc": (
                f"The uploaded photo appears to contain "
                f"'{detected_name}' instead of a crop leaf. "
                f"Please upload a clear photo of a plant leaf."
            ),

            "fertilizer": (
                "Not applicable — no crop leaf detected."
            ),

            "nutrients": (
                "Not applicable."
            ),

            "care": [

                "Take a close-up photo of the crop leaf.",

                "Make sure the leaf is clearly visible.",

                "Use good lighting.",

                "Avoid animals, people, vehicles, "
                "and unrelated objects in the image."

            ],

            "simulated": False

        })


    # ========================================================
    # STEP 2 - CROP DISEASE MODEL
    # ========================================================

    if model is None:

        if class_names:

            label = random.choice(
                class_names
            )

        else:

            fallback = [

                "Tomato___Early_blight",

                "Potato___Late_blight",

                "Tomato___healthy",

                "Corn_(maize)___Common_rust_"

            ]

            label = random.choice(
                fallback
            )


        advice = get_advice(
            label
        )


        return jsonify({

            "is_plant": True,

            "crop": advice["crop"],

            "disease": advice["disease"],

            "confidence": round(
                random.uniform(72, 97),
                1
            ),

            "simulated": True,

            **advice

        })


    # ========================================================
    # REAL MODEL PREDICTION
    # ========================================================

    try:

        probabilities = model.predict(
            arr,
            verbose=0
        )[0]


        top_index = int(
            np.argmax(probabilities)
        )


        # Safety check
        if top_index >= len(class_names):

            return jsonify({
                "error": (
                    "Model output does not match "
                    "labels.json"
                )
            }), 500


        label = class_names[
            top_index
        ]


        advice = get_advice(
            label
        )


        # ----------------------------------------------------
        # Top 3 predictions
        # ----------------------------------------------------

        top_indices = probabilities.argsort()[-3:][::-1]


        top3 = []


        for index in top_indices:

            index = int(index)

            if index < len(class_names):

                top3.append({

                    "label": class_names[index],

                    "prob": round(
                        float(
                            probabilities[index]
                        ) * 100,
                        1
                    )

                })


        # ----------------------------------------------------
        # Final response
        # ----------------------------------------------------

        return jsonify({

            "is_plant": True,

            "crop": advice["crop"],

            "disease": advice["disease"],

            "confidence": round(
                float(
                    probabilities[top_index]
                ) * 100,
                1
            ),

            "top3": top3,

            "simulated": False,

            **advice

        })


    except Exception as e:

        print(
            "Prediction error:",
            e
        )

        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    load_model()

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
