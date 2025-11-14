import os
import glob

def get_config_paths(config_folder):
    # List all entries in the parent folder
    entries = os.listdir(config_folder)

    # Filter out the entries that are directories
    folder_paths = [os.path.join(config_folder, entry) for entry in entries if os.path.isdir(os.path.join(config_folder, entry))]

    file_paths = []
    jrl_files = glob.glob(os.path.join(config_folder, '*.json'))
    file_paths += jrl_files

    # Print the path of each folder
    for folder_path in folder_paths:
        jrl_files = glob.glob(os.path.join(folder_path, '*.json'))
        file_paths += jrl_files

    return file_paths

def get_jrl_file_paths(folder_path):
    # Use glob to find all .jrl files in the specified folder
    jrl_files = glob.glob(os.path.join(folder_path, '*.json'))

    # Print the path of each .jrl file
    for file_path in jrl_files:
        print(file_path)

def get_folder_paths(config_folder):
    # List all entries in the parent folder
    entries = os.listdir(parent_folder)

    # Filter out the entries that are directories
    folder_paths = [os.path.join(parent_folder, entry) for entry in entries if os.path.isdir(os.path.join(parent_folder, entry))]

    # Print the path of each folder
    for folder_path in folder_paths:
        print(folder_path)

def get_config_paths(config_folder):
    # List all entries in the parent folder
    entries = os.listdir(config_folder)

    # Filter out the entries that are directories
    folder_paths = [os.path.join(config_folder, entry) for entry in entries if os.path.isdir(os.path.join(config_folder, entry))]

    file_paths = []

    # Print the path of each folder
    for folder_path in folder_paths:
        jrl_files = glob.glob(os.path.join(folder_path, '*.json'))
        file_paths += jrl_files

    return file_paths

# # Example usage
# config_folder = './configs/TEST_1'  # Replace with the path to your folder
# get_folder_paths(config_folder)
# # Example usage
# folder_path = './configs/TEST_1'  # Replace with the path to your folder
# get_jrl_file_paths(folder_path)
# Example usage
config_folder = './configs/TEST_1'  # Replace with the path to your folder
file_paths = get_config_paths(config_folder)
print(file_paths[0])
file_name = os.path.basename(file_paths[0])
print(file_name)
folder_path = os.path.dirname(file_paths[0])
folder_name = os.path.basename(folder_path)
print(folder_path)
print(folder_name)