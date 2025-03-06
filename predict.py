import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image

def load_tflite_model(model_path):
    interpreter = tflite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter


def preprocess_image(img_path, target_size=(256, 256)):
    img = Image.open(img_path).convert("RGB")  # Open image and ensure RGB format
    img = img.resize(target_size)  # Resize to target dimensions
    img_array = np.array(img).astype(np.float32) / 255.0  # Convert to float32 and normalize
    img_array = np.expand_dims(img_array, axis=0)  # Expand dimensions for model input
    return img_array

def predict(interpreter, img_array, class_names=("non-shark", "shark")):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    
    prediction = interpreter.get_tensor(output_details[0]['index'])
    predicted_class_index = np.argmax(prediction, axis=1)[0]
    predicted_class = class_names[predicted_class_index]
    confidence = prediction[0][predicted_class_index]
    
    return predicted_class, confidence

model_path = "initial_model.tflite"  # Path to your TensorFlow Lite model
interpreter = load_tflite_model(model_path)

while True:
    image_path = input("Select an image: ")
    img_array = preprocess_image(image_path)
    predicted_class, confidence = predict(interpreter, img_array)
    print(f"Predicted class: {predicted_class} with confidence: {confidence:.2f}")
