import os
import glob

def get_jrl_file_paths(folder_path):
    # Use glob to find all .jrl files in the specified folder
    jrl_files = glob.glob(os.path.join(folder_path, '*.json'))

    print(type(jrl_files))

    # Print the path of each .jrl file
    for file_path in jrl_files:
        print(file_path)

# Example usage
folder_path = './configs/TEST_1'  # Replace with the path to your folder
get_jrl_file_paths(folder_path)

def get_folder_paths(parent_folder):
    # List all entries in the parent folder
    entries = os.listdir(parent_folder)

    # Filter out the entries that are directories
    folder_paths = [os.path.join(parent_folder, entry) for entry in entries if os.path.isdir(os.path.join(parent_folder, entry))]

    # Print the path of each folder
    for folder_path in folder_paths:
        print(folder_path)

# Example usage
parent_folder = './configs/TEST_1'  # Replace with the path to your folder
get_folder_paths(parent_folder)
