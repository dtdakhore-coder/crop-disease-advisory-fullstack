"""
CropCare AI - Full 38-Class Dataset Training Script (Colab & Kaggle Ready)
Architecture: MobileNetV2 / EfficientNet with Data Augmentation and Transfer Learning.

How to run on Google Colab (Free GPU):
1. Open Google Colab (https://colab.research.google.com).
2. Set Runtime to T4 GPU (Runtime -> Change runtime type -> T4 GPU).
3. Run the cells to download the 38-class PlantVillage dataset, train, and download model.
"""

import os, json, argparse
import tensorflow as tf
from tensorflow.keras import layers, models

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

def build_data_pipelines(data_dir, seed=42):
    """Loads image dataset with automatic 80/20 train/validation split and prefetching."""
    print(f"Loading dataset from: {data_dir}")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=seed,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical"
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=seed,
        image_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        label_mode="categorical"
    )

    class_names = train_ds.class_names
    print(f"\nDiscovered {len(class_names)} classes:")
    for idx, name in enumerate(class_names):
        print(f"  [{idx:02d}] {name}")

    # Optimize pipeline for fast GPU throughput
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds, class_names

def create_crop_model(num_classes):
    """Constructs MobileNetV2 with Data Augmentation layers and custom classification head."""
    # Data Augmentation pipeline directly on GPU
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.15),
        layers.RandomZoom(0.15),
        layers.RandomContrast(0.15),
    ], name="data_augmentation")

    # Pre-trained MobileNetV2 base
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=IMG_SIZE + (3,),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # Freeze for Phase 1

    inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
    x = data_augmentation(inputs)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(256, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = tf.keras.Model(inputs, outputs, name="CropCare_MobileNetV2")
    return model, base_model

def train(data_dir, epochs=12, output_dir="model"):
    train_ds, val_ds, class_names = build_data_pipelines(data_dir)
    num_classes = len(class_names)

    model, base_model = create_crop_model(num_classes)

    # Callbacks
    os.makedirs(output_dir, exist_ok=True)
    best_model_path = os.path.join(output_dir, "crop_disease_model.h5")

    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor="val_accuracy", patience=4, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=2, min_lr=1e-6)
    ]

    print("\n=======================================================")
    print("PHASE 1: Training Classification Head (Base Model Frozen)")
    print("=======================================================")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    initial_epochs = max(4, epochs // 2)
    model.fit(train_ds, validation_data=val_ds, epochs=initial_epochs, callbacks=callbacks)

    print("\n=======================================================")
    print("PHASE 2: Fine-Tuning Top 40 Layers of MobileNetV2")
    print("=======================================================")
    base_model.trainable = True
    # Freeze all layers except the last 40 layers
    for layer in base_model.layers[:-40]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    total_epochs = initial_epochs + epochs
    model.fit(train_ds, validation_data=val_ds, initial_epoch=initial_epochs, epochs=total_epochs, callbacks=callbacks)

    # Evaluate final accuracy
    val_loss, val_acc = model.evaluate(val_ds)
    print(f"\n🏆 Final Validation Accuracy: {val_acc * 100:.2f}% (Loss: {val_loss:.4f})")

    # Save Model & Labels JSON
    print(f"\nSaving model to {best_model_path}...")
    model.save(best_model_path)

    labels_path = os.path.join(output_dir, "labels.json")
    with open(labels_path, "w") as f:
        json.dump(class_names, f, indent=2)
    print(f"Saved {len(class_names)} class labels to {labels_path}")

    print("\n✅ Training Complete! Download 'crop_disease_model.h5' and 'labels.json'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train CropCare AI on Full 38-Class Dataset")
    parser.add_argument("--data", required=True, help="Path to dataset root folder")
    parser.add_argument("--epochs", type=int, default=10, help="Number of fine-tuning epochs")
    parser.add_argument("--out", default="model", help="Output directory")
    args = parser.parse_args()

    train(args.data, args.epochs, args.out)
