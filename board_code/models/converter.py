import tensorflow as tf

# Load the model from the .h5 file
model = tf.keras.models.load_model('./initial_model.h5')

# Create a TFLiteConverter object from the model
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Convert the model to TensorFlow Lite format
tflite_model = converter.convert()

# Save the TensorFlow Lite model to a file
with open('initial_weights.tflite', 'wb') as f:
    f.write(tflite_model)
