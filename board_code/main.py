import numpy as np
import tflite_runtime.interpreter as tflite
from PIL import Image
import sys
import time
import datetime
import serial
import os
import coral_fswebcam
import coral_uart
import random


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
    
    # Sleep for a little to delay the start on boot
    # time.sleep(10)

    # Calling this function with: python3 main.py <model name (no file extension)>

    model_data = [
        {'name': 'initial_model', 'accuracy': 0.80, 'f1': 0.89, 'battery': 'battery usage'},
        {'name': 'dummy_model', 'accuracy': 100, 'f1': '1.0', 'battery': 'None'}
    ]

    if '--table' in sys.argv:
        print_table(model_data)
        sys.exit()

    model_path = '/home/mendel/shark/models/' + sys.argv[1] + '.tflite'
    model = load_tflite_model(model_path)

    ser = serial.Serial('/dev/ttymxc2', 9600)
    timer = time.time()
    while True:
        
        time.sleep(5)
        coral_fswebcam.capture()

        img_array = preprocess_image('/home/mendel/shark/camera_image.jpg')
        predicted_class, confidence = predict(model, img_array)
        print(f'Predicted class: {predicted_class} with confidence: {confidence:.2f}')

        if (predicted_class == 'shark'):
            output = f'shark: {predicted_class} {datetime.datetime.now(datetime.timezone.utc)}\0'
            ser.write(output.encode('utf-8'))
        elif (timer - time.time() > 300):
            ser.write(b'health: Still alive')
            timer = time.time()
      
    ser.close()
