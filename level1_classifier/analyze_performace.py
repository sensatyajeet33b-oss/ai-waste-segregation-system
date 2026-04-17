import tensorflow as tf

model = tf.keras.models.load_model("model/dry_wet_model.keras")

test_path = "C:/Users/KIIT0001/.cache/kagglehub/datasets/sapal6/waste-classification-data-v2/versions/1/DATASET_BINARY/TEST"

test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    test_path,
    image_size=(160, 160),  # Must match training size
    batch_size=32,
    shuffle=False
)

import numpy as np

y_true = np.concatenate([y for x, y in test_ds])

y_pred_probs = model.predict(test_ds)
y_pred = (y_pred_probs > 0.5).astype("int32").flatten()

from sklearn.metrics import classification_report

class_names = test_ds.class_names

print(classification_report(
    y_true,
    y_pred,
    target_names=class_names
))

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_true, y_pred)
print(cm)


import matplotlib.pyplot as plt
import seaborn as sns

plt.figure()
sns.heatmap(cm,
            annot=True,
            fmt="d",
            xticklabels=class_names,
            yticklabels=class_names)

plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()

from sklearn.metrics import accuracy_score

print("Accuracy:", accuracy_score(y_true, y_pred))
print("Average prediction confidence:", np.mean(y_pred_probs))


from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# Flatten predictions
y_pred_probs = y_pred_probs.flatten()

# Compute ROC
fpr, tpr, thresholds = roc_curve(y_true, y_pred_probs)
roc_auc = auc(fpr, tpr)

# Plot
plt.figure()
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.3f})")
plt.plot([0, 1], [0, 1], linestyle='--')  # random guess line

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Waste Classifier")
plt.legend()

plt.show()