"""
Training script - MobileNetV2 transfer learning for crop disease classification.
Run on Google Colab (free GPU) or any machine with the PlantVillage dataset.

Expected dataset layout (one folder per class, class names like 'Tomato___Early_blight'):
    dataset/
        Tomato___Early_blight/  *.JPG
        Tomato___Late_blight/   *.JPG
        Potato___healthy/       *.JPG
        ...

Usage:
    python train.py --data /path/to/dataset --epochs 10 --out model
"""
import argparse, json, os
import tensorflow as tf
from tensorflow.keras import layers, models

IMG_SIZE = (224, 224)
BATCH = 32

def build_datasets(data_dir, seed=42):
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir, validation_split=0.2, subset="training", seed=seed,
        image_size=IMG_SIZE, batch_size=BATCH, label_mode="categorical")
    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir, validation_split=0.2, subset="validation", seed=seed,
        image_size=IMG_SIZE, batch_size=BATCH, label_mode="categorical")
    class_names = train_ds.class_names
    train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
    val_ds = val_ds.prefetch(tf.data.AUTOTUNE)
    return train_ds, val_ds, class_names

def build_model(num_classes):
    base = tf.keras.applications.MobileNetV2(
        input_shape=IMG_SIZE + (3,), include_top=False, weights="imagenet")
    base.trainable = False  # freeze base first (feature extractor)
    model = models.Sequential([
        layers.Input(shape=IMG_SIZE + (3,)),
        tf.keras.applications.mobilenet_v2.preprocess_input,
        base,
        layers.GlobalAveragePooling2D(),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="categorical_crossentropy",
                  metrics=["accuracy"])
    return model, base

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True, help="Path to dataset folder")
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--out", default="model")
    args = ap.parse_args()

    train_ds, val_ds, class_names = build_datasets(args.data)
    print(f"Classes ({len(class_names)}):", class_names)

    model, base = build_model(len(class_names))

    print("\n--- Phase 1: training head (base frozen) ---")
    model.fit(train_ds, validation_data=val_ds, epochs=max(3, args.epochs // 2))

    print("\n--- Phase 2: fine-tuning last 30 layers of MobileNetV2 ---")
    base.trainable = True
    for layer in base.layers[:-30]:
        layer.trainable = False
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
                  loss="categorical_crossentropy", metrics=["accuracy"])
    model.fit(train_ds, validation_data=val_ds, epochs=args.epochs)

    os.makedirs(args.out, exist_ok=True)
    model.save(os.path.join(args.out, "crop_disease_model.h5"))
    with open(os.path.join(args.out, "labels.json"), "w") as f:
        json.dump(class_names, f, indent=2)

    # Also export TensorFlow.js for browser-only deployment (optional)
    try:
        import subprocess
        subprocess.run(["tensorflowjs_converter", "--input_format=keras",
                        os.path.join(args.out, "crop_disease_model.h5"),
                        os.path.join(args.out, "tfjs_model")], check=True)
        print("TensorFlow.js model exported to tfjs_model/")
    except Exception as e:
        print("TF.js export skipped:", e)

    loss, acc = model.evaluate(val_ds)
    print(f"\nFinal validation accuracy: {acc*100:.2f}%")

if __name__ == "__main__":
    main()
