#Convert Your Model to TensorFlow Lite (TFLite) Format:

import tensorflow as tf

# Load model
model = tf.keras.models.load_model("model.h5")

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model
with open("model.tflite", "wb") as f:
    f.write(tflite_model)

#Load and Run the Model Using Python: 
import numpy as np
import tflite_runtime.interpreter as tflite

# Load the TFLite model
interpreter = tflite.Interpreter(model_path="model_edgetpu.tflite")
interpreter.allocate_tensors()

# Get input and output tensors
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Prepare input data (modify as per your model)
input_data = np.array([[...]], dtype=np.float32)

# Run inference
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

# Get results
output_data = interpreter.get_tensor(output_details[0]['index'])
print("Inference result:", output_data)


##Connecting ML Model to a Camera 
#Install OpenCV:
#sudo apt install python3-opencv

import cv2
from pycoral.adapters.detect import get_objects
from pycoral.utils.edgetpu import make_interpreter

# Load model
interpreter = make_interpreter("mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite")
interpreter.allocate_tensors()

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Run inference
    cv2.imshow("Live Feed", frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()