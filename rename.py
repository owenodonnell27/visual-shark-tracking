import os

# Use this file/function to rename data
def rename_files_in_directory(root_dir):
    S = set()
    for subdir, dirs, files in os.walk(root_dir):

        split_subdir = subdir.split('\\')
        n = 0

        for i, file in enumerate(files):
            if split_subdir[2] not in ('train', 'test', 'val', 'old_train') and file.endswith('.jpg'):  
                print(subdir)
                if(split_subdir[4] == 'val'):
    
                    animal = ''
                    if split_subdir[5] == 'animal dolphin':
                        animal = 'dolphin'
                    elif split_subdir[5] == 'animal sea_turtle':
                        animal = 'sea_turtle'
                    elif split_subdir[5] == 'animal whale':
                        animal = 'whale'
                    elif split_subdir[5] == 'animal harbor_seal':
                        animal = 'seal'
                    else:
                        animal = split_subdir[5]
                    S.add(animal)

                    new_file_name = animal + '.' + str(n) + '.jpg'
                    n += 1

                    # Full file paths
                    old_file_path = os.path.join(subdir, file)
                    new_file_path = os.path.join('./images/val/', new_file_name)
                    
                    # Rename the file
                    os.rename(old_file_path, new_file_path)
                    print(f'Renamed: {old_file_path} -> {new_file_path}')

    print(S)
# Define the root directory you want to process
root_directory = '.\\images'
rename_files_in_directory(root_directory)
