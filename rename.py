import os

# Use this file/function to rename data
def rename_files_in_directory(root_dir):
    S = set()
    i = 0
    for subdir, dirs, files in os.walk(root_dir):
        for i, file in enumerate(files):
            if file.endswith(('.jpg', '.png', '.jpeg', '.JPG', '.gif')):  
                
                S.add(subdir.split('\\')[2])
                print(i)
                i += 1

                
                # # Generate new file name based on directory name and index
                # directory_name = os.path.basename(subdir)
                # new_file_name = f"{directory_name}_{i+1:03d}{os.path.splitext(file)[1]}"
                
                # # Full file paths
                # old_file_path = os.path.join(subdir, file)
                # new_file_path = os.path.join(subdir, new_file_name)
                
                # # Rename the file
                # os.rename(old_file_path, new_file_path)
                # print(f'Renamed: {old_file_path} -> {new_file_path}')
    print(S)

# Define the root directory you want to process
root_directory = '.\\images'
rename_files_in_directory(root_directory)
