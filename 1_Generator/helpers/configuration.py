import json
import numpy as np
import os
import glob

def get_config_paths(config_folders):
    """Return all JSON config file paths from the given folder list."""
    if isinstance(config_folders, str):
        config_folders = [config_folders]

    file_paths = []

    for config_folder in config_folders:
        if not os.path.isdir(config_folder):
            continue

        # Add JSON files directly in the current folder
        file_paths.extend(glob.glob(os.path.join(config_folder, '*.json')))

        # Add JSON files inside each subfolder of the current folder
        for entry in os.listdir(config_folder):
            entry_path = os.path.join(config_folder, entry)
            if os.path.isdir(entry_path):
                file_paths.extend(glob.glob(os.path.join(entry_path, '*.json')))

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

# # Example usage
# config_folder = './configs/TEST_1'  # Replace with the path to your folder
# get_folder_paths(config_folder)
# # Example usage
# folder_path = './configs/TEST_1'  # Replace with the path to your folder
# get_jrl_file_paths(folder_path)
# Example usage
# config_folder = './configs/TEST_1'  # Replace with the path to your folder
# file_paths = get_config_paths(config_folder)
# print(file_paths[0])
# file_name = os.path.basename(file_paths[0])
# print(file_name)
# folder_path = os.path.dirname(file_paths[0])
# folder_name = os.path.basename(folder_path)
# print(folder_path)
# print(folder_name)

def generate_complete_config_file():
    output_path="/home/workspace/configs/default.json"
    default_config = {
        "name": "default_complete_dataset",
        "output_dir": "/home/workspace/output",
        "dataset-options": {
            "repeats": 1,
            "initialization_type": "noisy_gt"
        },
        "trajectory":{
            "seed": 67,
            "robots": 10,
            "poses": 250,
            "traj_probs": [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05],
            "x_lim": [-40, 40],
            "y_lim": [-40, 40],
            "z_lim": [-40, 40]
        },
        "landmarks": {
            "seed": 57,
            "number": 30,
            "pack": "all",
            "detection_prob": 0.4,
            "detection_num": 50
        },
        "intra-loop-closure": {
            "number": 20,
            "frequency": 50,
            "index": 20
        },
        "inter-indirect-loop-closure": {
            "number": 20,
            "frequency": 50,
            "index": 20
        },
        "inter-direct-loop-closure": {
            "pose": {
                "number": 20,
                "frequency": 50
            },
            "range": {
                "number": 20,
                "frequency": 50
            }
        },
        "sigmas": {
            "initialization": [0.3, 0.3, 0.3, 0.15, 0.15, 0.15],

            "prior": [0.05, 0.05, 0.05, 0.1, 0.1, 0.1],
            "robot_zero_prior": [0.05, 0.05, 0.05, 0.1, 0.1, 0.1],

            "odom": [0.05, 0.05, 0.05, 0.03, 0.03, 0.03],

            "lc_intra": [0.10, 0.10, 0.10, 0.04, 0.04, 0.04],
            "lc_inter_indirect": [0.25, 0.25, 0.25, 0.08, 0.08, 0.08],
            "lc_inter_direct_pose": [0.20, 0.20, 0.20, 0.06, 0.06, 0.06],
            "lc_inter_direct_range": 0.10,
            "landmarks": [0.03, 0.03, 0.15]
        },
        "outliers": {
            "perceptual_aliasing":10,
            "robot_failure":1,
            "robot_loss":1
        }
    }

    with open(output_path, "w") as f:
        json.dump(default_config, f, indent=4)
    print(f"Default config file generated at {output_path}")

class DatasetConfiguration():
    def __init__(self, json_file_path):
        json_data = self.read_json_file(json_file_path)

        self.raw_dict = json_data

        self.output_dir = json_data.get('output_dir')
        self.name = json_data.get('name')
        
        # Dataset-options
        self.dataset_opts = json_data.get('dataset-options')

        # Trajectory
        self.trajectory = json_data.get('trajectory')

        # Landmarks
        self.landmarks = json_data.get('landmarks')

        # Intra loop closure
        self.lc_intra = json_data.get('intra-loop-closure')

        # Indirect inter loop closure
        self.lc_inter_indirect = json_data.get('inter-indirect-loop-closure')

        # Direct inter loop closure
        self.lc_inter_direct = json_data.get('inter-direct-loop-closure')

        # Sigmas
        self.sigmas = json_data.get('sigmas')

        # Outliers
        self.outliers = json_data.get('outliers')
     
    def __str__(self):
        output  = f"----------------------------------\n"
        output += f"-----  Dataset Parameters :  -----\n"
        output += f"----------------------------------\n\n"
        output += f"Dataset name : {self.name}\n"
        output += f"Output directory : {self.output_dir}\n"
        output += f"\n"

        output += self.__json_section_str(self.dataset_opts, "Dataset-options")
        output += self.__json_section_str(self.trajectory, "Trajectory")
        output += self.__json_section_str(self.landmarks, "Landmarks")
        output += self.__json_section_str(self.lc_intra, "Loop closure - Intra")
        output += self.__json_section_str(self.lc_inter_indirect, "Loop closure - Inter - Indirect")
        output += self.__json_section_str(self.lc_inter_direct, "Loop closure - Inter - Direct")
        output += self.__json_section_str(self.sigmas, "Sigmas")
        output += self.__json_section_str(self.outliers, "Outliers")

        return output
    
    def read_json_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from the file '{file_path}'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def __title_str(self, title):
        output = f"{title} :"
        output += "\n" + "-" * len(output) + "\n"
        return output
    
    def __json_section_str(self, section_data, section_name):
        if section_data is not None:
            output = self.__title_str(section_name)
            for item in section_data.items():
                output += f"{item[0]}: {item[1]}\n"
            output += f"\n"
        else:
            output = ""

        return output

if __name__ == '__main__':
    # Dataset Parameters
    # generate_default_config_file()
    file_path = '/home/workspace/configs/default.json'
    Params = DatasetConfiguration(file_path)
    print(Params)