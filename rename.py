import os

# Use this file/function to rename data
def rename_files_in_directory(root_dir):

    for subdir, dirs, files in os.walk(root_dir):
        for i, file in enumerate(files):
            if file.endswith(('.jpg')):  
                
                new_file_name = file + '.jpg'

                # Full file paths
                old_file_path = os.path.join(subdir, file)
                new_file_path = os.path.join(subdir, new_file_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} -> {new_file_path}')

# Define the root directory you want to process
# root_directory = '.\\images'
# rename_files_in_directory(root_directory)
