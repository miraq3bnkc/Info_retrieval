import os

folder_path = 'docs'
items = os.listdir(folder_path)

# Count the number of files
num_files = len(items)

print(f'The folder "{folder_path}" contains {num_files} files.')