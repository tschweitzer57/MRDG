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

