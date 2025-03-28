# Imports
import os
import shutil

directory_list = ['images/train', 'images/test', 'images/val']

# Iterate through each directory
for dir in directory_list:

    # Creating a directories for 'shark' and 'no_shark'
    shark_dir = os.path.join(dir, "shark")
    no_shark_dir = os.path.join(dir, "no_shark")

    # Create destination folders if they don't exist
    os.makedirs(shark_dir, exist_ok=True)
    os.makedirs(no_shark_dir, exist_ok=True)

    # Iterate through files in the train directory
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            if "shark" in filename.lower() or "hammerhead" in filename.lower():
                shutil.move(file_path, os.path.join(shark_dir, filename))
            else:
                shutil.move(file_path, os.path.join(no_shark_dir, filename))

    print("Images have been organized into 'shark' and 'no_shark' folders.")

print("All dataset splits have been processed!")
