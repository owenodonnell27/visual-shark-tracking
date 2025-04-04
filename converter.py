import tensorflow as tf

import os

tflite_model_path = "./board_code/models/initial_model.h5"
if os.path.exists(tflite_model_path):
    print("TFLite model successfully created:", tflite_model_path)
else:
    print("TFLite model was NOT created.")

# Load the model from the .h5 file
model = tf.keras.models.load_model('./board_code/models/initial_model.h5')

# Create a TFLiteConverter object from the model
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Convert the model to TensorFlow Lite format
tflite_model = converter.convert()

# Save the TensorFlow Lite model to a file
with open('initial_model.tflite', 'wb') as f:
    f.write(tflite_model)
