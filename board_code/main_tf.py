import sys
import os
import time
from queue import Queue
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

def load_model(model_path, weights_path):
    model = tf.keras.models.load_model(model_path)
    model.load_weights(weights_path) 
    return model

def preprocess_image(img_path, target_size=(256, 256)):
    img = load_img(img_path, target_size=target_size) 
    img_array = img_to_array(img) 
    img_array = np.expand_dims(img_array, axis=0) 
    img_array /= 255.0 
    return img_array


def predict(model, img_array, class_names=('non-shark', 'shark')):
    prediction = model.predict(img_array) 

    predicted_class_index = np.argmax(prediction, axis=1)[0] 
    predicted_class = class_names[predicted_class_index]  

    confidence = prediction[0][predicted_class_index] 
    return predicted_class, confidence


def print_table(data):
    headers = ['Name', 'Accuracy', 'F1 Score', 'Battery']
    attributes = ['name', 'accuracy', 'f1', 'battery']

    col_widths = [max(len(str(item[attr])) for item in data + [dict(zip(attributes, headers))]) for attr in attributes]
    total_width = sum(col_widths) + len(col_widths) * 3 - 1  # Adjust total width

    print('-' * total_width)

    header_row = ' | '.join(f'{headers[i]:<{col_widths[i]}}' for i in range(4))
    print(header_row)

    print('-' * total_width)

    for obj in data:
        row = ' | '.join(f'{str(obj[attr]):<{col_widths[i]}}' for i, attr in enumerate(attributes))
        print(row)

    print('-' * total_width)


if __name__ == '__main__':

    model_data = [
        {'name': 'initial_model', 'accuracy': 0.80, 'f1': 0.89, 'battery': 'battery usage'},
        {'name': 'dummy_model', 'accuracy': 100, 'f1': 'Perfect', 'battery': 'None'}
    ]

    if '--table' in sys.argv:
        print_table(model_data)
        sys.exit()

    model_path = weights_path = './models/' + sys.argv[1]
    image_path = './' 

    model_path += '.h5'
    weights_path += '_weights.h5'
    model = load_model(model_path, weights_path)

    image_queue = Queue()

    while True:
        image_names = os.listdir('./new_images')
        for image in image_names:
            image_queue.put(image)

            old_path = './new_images/' + image
            new_path = './queued_images/' + image
            os.rename(old_path, new_path)

        time.sleep(1)

        if not image_queue.empty():
            current_image = image_queue.get()
            img_array = preprocess_image('./queued_images/' + current_image)
            predicted_class, confidence = predict(model, img_array)
            print(f'Predicted class: {predicted_class} with confidence: {confidence:.2f}')

            old_path = './queued_images/' + current_image
            new_path = './old_images/' + current_image
            os.rename(old_path, new_path)
