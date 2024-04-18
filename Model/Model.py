import pandas as pd
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, BatchNormalization
import random
import keras
import tensorflow as tf
from tensorflow.keras import regularizers
import os
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_validation_curves(history, title='Model Performance'):
    """
    This function plots the training and validation accuracy and loss.

    Args:
    history: TensorFlow Keras history object from the fit method.
    title (str): Title of the graph.
    """
    # Extracting the history for accuracy and loss
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(1, len(acc) + 1)

    # Plotting training and validation accuracy
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, acc, label='Training Accuracy')
    plt.plot(epochs, val_acc, label='Validation Accuracy')
    plt.title(title + ' - Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()

    # Plotting training and validation loss
    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, label='Training Loss')
    plt.plot(epochs, val_loss, label='Validation Loss')
    plt.title(title + ' - Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()

    plt.tight_layout()
    plt.show()
def load_and_process_data(directory):
    features_list = []
    labels_list = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory, file_name)
            df = pd.read_csv(file_path)
            current_features = []
            current_label = None
            for _, row in df.iterrows():
                features = row[['AccelX', 'AccelY', 'AccelZ']].tolist()
                current_features.append(features)
                if row['Sep'] == 1:
                    if current_label is None:  # Fallback if no label is provided before 'Sep'
                        current_label = row['Label']
                    features_list.append(current_features)
                    labels_list.append(current_label)
                    current_features = []
                    current_label = row['Label']  # Update the label for the next sequence
            # Add the last set of features if it hasn't been added yet
            if current_features:
                features_list.append(current_features)
                labels_list.append(current_label)
    return labels_list, features_list

def prepare_data(directory):
    label, features = load_and_process_data(directory)
    padded_features = pad_sequences(features, padding='post', dtype='float32')
    print(len(label))
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(label)
    categorical_labels = to_categorical(encoded_labels)
    return padded_features, categorical_labels, label_encoder.classes_

# Define the directory path where your CSV files are stored
directory_path = r'C:\Users\Fernando\Downloads\Newfinalproject\Model\Data'

# Prepare data
X, y, class_names = prepare_data(directory_path)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape= (99,3)),
    tf.keras.layers.LSTM(32, return_sequences=True),
    tf.keras.layers.LSTM(16, return_sequences = False),
    tf.keras.layers.BatchNormalization(axis=-1,momentum=0.99,epsilon=0.001),
    tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=regularizers.l1_l2(l1=0.01, l2=0.02)),
    tf.keras.layers.Dropout(rate=0.2, noise_shape=None, seed=None),
    tf.keras.layers.Dense(8, activation='softmax'),

])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=225, validation_split=0.2, batch_size=32)

test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f'Test accuracy: {test_accuracy}')
model.save('LSTM_model.keras')

y_pred = model.predict(X_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)
# Computing the confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)

# Plotting the confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()
plot_validation_curves(history)
