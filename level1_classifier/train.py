# import tensorflow as tf
# import numpy as np
# import os

# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# from tensorflow.keras.applications import MobileNetV2
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
# from tensorflow.keras.models import Model
# from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
# from sklearn.utils.class_weight import compute_class_weight

# # ==============================
# # 1️⃣ Configuration
# # ==============================

# IMG_SIZE = 224
# BATCH_SIZE = 32
# EPOCHS = 20

# train_dir = "DATASET/TRAIN"
# test_dir = "DATASET/TEST"
# model_save_path = "model/waste_model_v2.keras"

# # Create model directory if not exists
# os.makedirs("model", exist_ok=True)

# # ==============================
# # 2️⃣ Data Generators
# # ==============================

# train_datagen = ImageDataGenerator(
#     preprocessing_function=preprocess_input,
#     rotation_range=30,
#     zoom_range=0.2,
#     horizontal_flip=True,
#     width_shift_range=0.2,
#     height_shift_range=0.2,
#     shear_range=0.1,
#     fill_mode='nearest'
# )

# test_datagen = ImageDataGenerator(
#     preprocessing_function=preprocess_input
# )

# train_data = train_datagen.flow_from_directory(
#     train_dir,
#     target_size=(IMG_SIZE, IMG_SIZE),
#     batch_size=BATCH_SIZE,
#     class_mode='binary',
#     shuffle=True
# )

# test_data = test_datagen.flow_from_directory(
#     test_dir,
#     target_size=(IMG_SIZE, IMG_SIZE),
#     batch_size=BATCH_SIZE,
#     class_mode='binary',
#     shuffle=False
# )

# # ==============================
# # 3️⃣ Handle Class Imbalance
# # ==============================

# cls_train = train_data.classes

# class_weights = compute_class_weight(
#     class_weight='balanced',
#     classes=np.unique(cls_train),
#     y=cls_train
# )

# class_weights_dict = dict(enumerate(class_weights))

# print(f"\n⚖️ Calculated Class Weights: {class_weights_dict}\n")

# # ==============================
# # 4️⃣ Build MobileNetV2 Model
# # ==============================

# base_model = MobileNetV2(
#     input_shape=(IMG_SIZE, IMG_SIZE, 3),
#     include_top=False,
#     weights='imagenet'
# )

# # Fine-tuning strategy
# base_model.trainable = True

# # Freeze first 100 layers
# for layer in base_model.layers[:100]:
#     layer.trainable = False

# # Custom head
# x = base_model.output
# x = GlobalAveragePooling2D()(x)
# x = Dense(256, activation='relu')(x)
# x = BatchNormalization()(x)
# x = Dropout(0.4)(x)
# outputs = Dense(1, activation='sigmoid')(x)

# model = Model(inputs=base_model.input, outputs=outputs)

# # ==============================
# # 5️⃣ Compile Model
# # ==============================

# model.compile(
#     optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
#     loss=tf.keras.losses.BinaryCrossentropy(label_smoothing=0.1),  # reduces overconfidence
#     metrics=['accuracy']
# )

# model.summary()

# # ==============================
# # 6️⃣ Callbacks
# # ==============================

# callbacks = [
#     EarlyStopping(
#         monitor='val_loss',
#         patience=4,
#         restore_best_weights=True
#     ),
#     ReduceLROnPlateau(
#         monitor='val_loss',
#         factor=0.2,
#         patience=2,
#         min_lr=1e-6
#     ),
#     ModelCheckpoint(
#         model_save_path,
#         monitor='val_loss',
#         save_best_only=True
#     )
# ]

# # ==============================
# # 7️⃣ Train
# # ==============================

# print("\n🚀 Starting Training...\n")

# history = model.fit(
#     train_data,
#     epochs=EPOCHS,
#     validation_data=test_data,
#     callbacks=callbacks,
#     class_weight=class_weights_dict
# )

# # ==============================
# # 8️⃣ Save Final Model
# # ==============================

# model.save(model_save_path)

# print(f"\n✅ Training complete! Model saved at: {model_save_path}")

import kagglehub
import os
import shutil
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# ==============================
# Download Dataset
# ==============================

path = kagglehub.dataset_download("sapal6/waste-classification-data-v2")
print("Dataset path:", path)

original_path = os.path.join(path, "DATASET")
binary_path = os.path.join(path, "DATASET_BINARY")

for split in ["TRAIN", "TEST"]:
    os.makedirs(os.path.join(binary_path, split, "Dry"), exist_ok=True)
    os.makedirs(os.path.join(binary_path, split, "Wet"), exist_ok=True)

    # O → Wet
    organic_folder = os.path.join(original_path, split, "O")
    for file in os.listdir(organic_folder):
        shutil.copy(
            os.path.join(organic_folder, file),
            os.path.join(binary_path, split, "Wet", file)
        )

    # N + R → Dry
    for cls in ["N", "R"]:
        folder = os.path.join(original_path, split, cls)
        for file in os.listdir(folder):
            shutil.copy(
                os.path.join(folder, file),
                os.path.join(binary_path, split, "Dry", file)
            )

print("Binary dataset created successfully!")

# ==============================
# Load Dataset
# ==============================

IMG_SIZE = 160
BATCH_SIZE = 16

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    os.path.join(binary_path, "TRAIN"),
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    os.path.join(binary_path, "TEST"),
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.shuffle(1000).prefetch(AUTOTUNE)
test_ds = test_ds.prefetch(AUTOTUNE)

# ==============================
# Build Model
# ==============================

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights='imagenet'
)

base_model.trainable = False

model = keras.Sequential([
    layers.Rescaling(1./255),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(1, activation='sigmoid')
])

model.compile(
    optimizer=keras.optimizers.Adam(learning_rate=0.0001),
    loss='binary_crossentropy',
    metrics=['accuracy']
)

early_stop = keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=3,
    restore_best_weights=True
)

history = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=20,
    callbacks=[early_stop]
)

loss, acc = model.evaluate(test_ds)
print("Test Accuracy:", acc)

# IMPORTANT: Save using TF 2.15
model.save("dry_wet_model.keras")