import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

def load_model(model_path, weights_path):
    model = tf.keras.models.load_model(model_path)
    model.load_weights(weights_path) 
    return model

def preprocess_image(img_path, target_size=(256, 256)):
    img = image.load_img(img_path, target_size=target_size) 
    img_array = image.img_to_array(img) 
    img_array = np.expand_dims(img_array, axis=0) 
    img_array /= 255.0 
    return img_array


def predict(model, img_array, class_names=("non-shark", "shark")):
    prediction = model.predict(img_array) 

    predicted_class_index = np.argmax(prediction, axis=1)[0] 
    predicted_class = class_names[predicted_class_index]  

    confidence = prediction[0][predicted_class_index] 
    return predicted_class, confidence

model_path = "./initial_model.h5" 
weights_path = "./initial_weights.h5" 
image_path = "./images/test/great_white_shark.0.jpg"

model = load_model(model_path, weights_path)
img_array = preprocess_image(image_path)
predicted_class, confidence = predict(model, img_array)

print(f"Predicted class: {predicted_class} with confidence: {confidence:.2f}")
