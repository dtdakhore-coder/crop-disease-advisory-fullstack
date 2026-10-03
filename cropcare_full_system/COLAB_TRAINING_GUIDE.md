# 🚀 Step-by-Step: Train on Full 38-Class Dataset in Google Colab (Free GPU)

Follow these exact steps in Google Colab to train the full 38-class crop model in ~10-15 minutes using a free GPU.

---

### Step 1: Open Google Colab and Enable GPU
1. Go to **[colab.research.google.com](https://colab.research.google.com)** $\rightarrow$ **New Notebook**.
2. Click **Runtime** $\rightarrow$ **Change runtime type** $\rightarrow$ Select **T4 GPU** $\rightarrow$ Click **Save**.

---

### Step 2: Download Dataset & Code (Cell 1)
Copy and paste this into the first cell in Colab and click **Run (▶)**:

```python
# 1. Download the Full PlantVillage 38-Class Dataset
!wget -O plantvillage.zip "https://github.com/spMohanty/PlantVillage-Dataset/raw/master/raw/color.zip" || \
 curl -L -o plantvillage.zip "https://data.mendeley.com/public-files/datasets/tywbtsjrjv/files/d5652a28-c1d8-4b76-97f3-72fb80f94efc/file_downloaded"

!unzip -q plantvillage.zip -d dataset/
print("✅ Dataset unzipped successfully!")
```

*(Alternatively, if you use Kaggle datasets):*
```python
!pip install kaggle
# Upload your kaggle.json or download via:
!kaggle datasets download -d emmarex/plantdisease -p ./dataset --unzip
```

---

### Step 3: Run the 38-Class Training Script (Cell 2)
Copy and paste this in the next cell and run it:

```python
import tensorflow as tf
import os, json
from tensorflow.keras import layers, models

IMG_SIZE = (224, 224)
BATCH_SIZE = 32

# Path to the unzipped images folder
DATA_DIR = "dataset/color" if os.path.exists("dataset/color") else "dataset"

print("Loading dataset from:", DATA_DIR)
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR, validation_split=0.2, subset="training", seed=42,
    image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode="categorical"
)
val_ds = tf.keras.utils.image_dataset_from_directory(
    DATA_DIR, validation_split=0.2, subset="validation", seed=42,
    image_size=IMG_SIZE, batch_size=BATCH_SIZE, label_mode="categorical"
)

class_names = train_ds.class_names
num_classes = len(class_names)
print(f"\nDiscovered {num_classes} classes!")

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# Model architecture with GPU Data Augmentation & MobileNetV2
data_aug = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.15),
    layers.RandomZoom(0.15),
    layers.RandomContrast(0.15),
])

base = tf.keras.applications.MobileNetV2(
    input_shape=IMG_SIZE + (3,), include_top=False, weights="imagenet"
)
base.trainable = False

inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
x = data_aug(inputs)
x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
x = base(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.BatchNormalization()(x)
x = layers.Dropout(0.3)(x)
x = layers.Dense(256, activation="relu")(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(num_classes, activation="softmax")(x)

model = tf.keras.Model(inputs, outputs)

# Phase 1: Feature Extraction
model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
              loss="categorical_crossentropy", metrics=["accuracy"])
print("\n--- Training Head (4 Epochs) ---")
model.fit(train_ds, validation_data=val_ds, epochs=4)

# Phase 2: Fine-Tuning
base.trainable = True
for layer in base.layers[:-40]:
    layer.trainable = False

model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
              loss="categorical_crossentropy", metrics=["accuracy"])
print("\n--- Fine-Tuning Top Layers (8 Epochs) ---")
model.fit(train_ds, validation_data=val_ds, epochs=8)

# Save Outputs
os.makedirs("model_output", exist_ok=True)
model.save("model_output/crop_disease_model.h5")
with open("model_output/labels.json", "w") as f:
    json.dump(class_names, f, indent=2)

loss, acc = model.evaluate(val_ds)
print(f"\n🎉 Validation Accuracy: {acc*100:.2f}%")
```

---

### Step 4: Download the Model to Your Computer (Cell 3)
Run this cell in Colab to automatically download both files:

```python
from google.colab import files
files.download("model_output/crop_disease_model.h5")
files.download("model_output/labels.json")
```

Once downloaded, simply place them into your `crop-disease-advisory-fullstack/backend/model/` folder! Your backend and website will instantly support **all 38 crop disease classes**!
