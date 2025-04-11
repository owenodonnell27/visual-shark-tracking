# Visual Shark Tracking

UConn and OWL Integration's Senior Design Project

# Model Training

Due to the large size of the .m5 and .tflite files, GitHub will not allow them to be pushed to a remote repository. So in order to get the .tflite file to upload to a coral board, you must first train the model using one of the Jupyter Notebooks and then use converter.py to convert the .h5 file you get from model training to a .tflite file.

Images used in training are stored in the images zip file. Depending on what model you are training you may need to restructure the organization of the images. If using shark.ipynb remove images from the shark and no shark folders and move them into their parent folder. For example, for the training images, move all images in the shark and no shark folders into the train folders. shark_detection_with_transfer_learning.ipynb uses the image organization as is.

Once you have your model trained, in converter.py in the tools folder, replace MODEL FILE NAME HERE with your models name to get a .tflite model and move the .tflite file into the models folder in the board_code folder.

# Coral Board

While in the coral board's shell, create a directory of your choosing. Before being able to upload files to a coral board using scp, you must upload an ssh key to the board. Once you have the key added, use scp to copy all models in the models folder, coral_fswebcam.py, coral_uart.py, and main.py to your newly created directory.

Make sure you have the camera plugged in and then run main.py.
