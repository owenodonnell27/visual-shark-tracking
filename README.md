# Visual Shark Tracking

UConn and OWL Integration's Senior Design Project

# Model Training

Due to the large size of the .m5 and .tflite files, GitHub will not allow them to be pushed to a remote repository. So in order to get the .tflite file to upload to a coral board, you must first train the model using one of the Jupyter Notebooks and then use converter.py to convert the .h5 file you get from model training to a .tflite file.

Images used in training are stored in the images zip file. Depending on what model you are training you may need to restructure the organization of the images. If using shark.ipynb remove images from the shark and no shark folders and move them into their parent folder. For example, for the training images, move all images in the shark and no shark folders into the train folders. shark_detection_with_transfer_learning.ipynb uses the image organization as is.

Once you have your model trained, in converter.py in the tools folder, replace MODEL FILE NAME HERE with your models name to get a .tflite model and move the .tflite file into the models folder in the board_code folder.

# Connecting to the Coral Board and Using SCP

In order to use scp to copy files to the coral board follow the follownig steps. First, connect the coral board to power and then connect the board to your computer. Next, open a commmand prompt and type mdt devices. This command will give the ip address of your coral board which will be needed later to save it. Finally, use the command: mdt shell. This will give acces to the board's shell.

Next check if there is an .ssh directory already on the board. If so remove it and any files inside the directory. Next create a new .ssh directory with the command: mkdir -p ~/.ssh and then change its permisions with the command: chmod 700 ~/.ssh. Next create a key on your computer. Use the command cat keyname.pub to list the public key and then copy. In the coral board use the command: vim authorized_keys to create the authorized_keys file with vim and then paste the public key here using right click with a mouse or tap the track pad with two fingers. This will copy the key to the file. Then press the i key to go to INSERT mode and have there be a new line after the key. After than hit escape and the :wq to exit the file. Finally use the command: chmod 600 ~/.ssh/authorized_keys. This will change the permissions of the newly created file. To copy a file use the command scp filename mendel@board_ipaddr:path where path is where you want the file to be stored.

When done with the coral board remove the authorized_keys folder from your board if you are not the only one using the board. This is becaues the coral board only allows one key on the board at a time so if you and another person are both using the board only one person will be able to access the board if the key is left on it.

# Coral Board

While in the coral board's shell, create a directory of your choosing. Before being able to upload files to a coral board using scp, you must upload an ssh key to the board. Once you have the key added, use scp to copy all models in the models folder, coral_fswebcam.py, coral_uart.py, and main.py to your newly created directory.

Make sure you have the camera plugged in and then run main.py.

CMDs to use on program running on boot:

How to edit the file that runs main.py on boot: sudo vim /etc/systemd/system/myscript.service
To stop: sudo systemctl stop myscript.service
Check status: systemctl status myscript.service
To see live output: sudo journalctl -fu myscript.service
