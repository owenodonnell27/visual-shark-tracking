import os

def rename_files(root_dir):
    for subdir, dirs, files in os.walk(root_dir):
        for i, file in enumerate(files):
            if file.endswith(('.jpg', '.png')):  # Add other file extensions if needed
                # Create new file name based on directory structure and index
                new_file_name = f"{os.path.basename(subdir)}_{i+1:03d}{os.path.splitext(file)[1]}"
                
                # Form full file paths
                old_file_path = os.path.join(subdir, file)
                new_file_path = os.path.join(subdir, new_file_name)
                
                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f'Renamed: {old_file_path} -> {new_file_path}')

# Define the root directory of your dataset
root_directory = 'path_to_your_dataset'
rename_files(root_directory)
