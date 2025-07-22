import json
import numpy as np

def generate_default_config_file():
    output_path="/home/workspace/configs/default.json"
    default_config = {
        "output_dir": "/home/workspace/output",
        "name": "default_dataset",
        "dataset-options": {
            "repeats": 1,
            "number_poses": 250,
            "number_robots": 4,
            "initialization_type": "noisy_gt",
            "trajectory_seed": 43
        },
        "limits": {
            "x": [-30, 30],
            "y": [-30, 30],
            "z": [-30, 30]
        },
        "odometry": {
            "odom_probs": [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        },
        "intra-loop-closure": {
            "frequency": 50,
            "index": 20
        },
        "inter-indirect-loop-closure": {
            "frequency": 50,
            "index": 20
        },
        "inter-direct-loop-closure": {
            "pose": {
                "frequency": 50
            },
            "range": {
                "frequency": 50
            }
        },
        "landmarks": {
            "number": 30,
            "seed": 57,
            "pack": "all",
            "probability": 0.4
        },
        "sigmas": {
            "initialization": [0.2, 0.2, 0.2, 1, 1, 1],
            "prior": [0.0175, 0.0175, 0.0175, 0.01, 0.01, 0.01],
            "robot_zero_prior": [0.0175, 0.0175, 0.0175, 0.01, 0.01, 0.01],

            "odom": [0.175, 0.175, 0.175, 0.05, 0.05, 0.05],

            "lc_intra": [0.175, 0.175, 0.175, 0.05, 0.05, 0.05],
            "lc_inter_indirect": [0.175, 0.175, 0.175, 0.05, 0.05, 0.05],
            "lc_inter_direct_pose": [0.175, 0.175, 0.175, 0.05, 0.05, 0.05],
            "lc_inter_direct_range": 0.10,
            "landmarks": [0.05, 0.05, 0.1]
        },
        "outliers": {
            "rate": 0.0
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

        # Limits
        self.limits = json_data.get('limits')
        
        # Odometry
        self.odometry = json_data.get('odometry')

        # Intra loop closure
        self.lc_intra = json_data.get('intra-loop-closure')

        # Indirect inter loop closure
        self.lc_inter_indirect = json_data.get('inter-indirect-loop-closure')

        # Direct inter loop closure
        self.lc_inter_direct = json_data.get('inter-direct-loop-closure')

        # Landmarks
        self.landmarks = json_data.get('landmarks')

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

        output += self.__json_section_str(self.limits, "Limits")
        output += self.__json_section_str(self.dataset_opts, "Dataset-options")
        output += self.__json_section_str(self.landmarks, "Landmarks")
        output += self.__json_section_str(self.odometry, "Odometry")
        output += self.__json_section_str(self.lc_intra, "Loop closure - Intra")
        output += self.__json_section_str(self.lc_inter_indirect, "Loop closure - Inter - Indirect")
        output += self.__json_section_str(self.lc_inter_direct, "Loop closure - Inter - Direct")
        output += self.__json_section_str(self.sigmas, "Sigmas")

        # if self.limits is not None:
        #     output += self.__title_str("Limits")
        #     for item in self.limits.items():
        #         output += f"{item[0]}: {item[1]}\n"
        #     output += f"\n"

        # if self.dataset_opts is not None:
        #     output += self.__title_str("Dataset-options")
        #     for item in self.dataset_opts.items():
        #         output += f"{item[0]}: {item[1]}\n"
        #     output += f"\n"

        # if self.landmarks is not None:
        #     output += self.__title_str("Landmarks")
        #     for item in self.landmarks.items():
        #         output += f"{item[0]}: {item[1]}\n"
        #     output += f"\n"
        
        # if self.odometry is not None:
        #     output += self.__title_str("Odometry")
        #     for item in self.odometry.items():
        #         output += f"{item[0]}: {item[1]}\n"
        #     output += f"\n"

        # if self.lc_intra is not None:
        #     output += self.__title_str("Loop closure - Intra")
        #     for item in self.lc_intra.items():
        #         output += f"{item[0]}: {item[1]}\n"
        #     output += f"\n"

        # if self.lc_inter_indirect is not None:
        #     output += self.__title_str("Loop closure - Inter - Indirect")
        #     for item in self.lc_inter_indirect.items():
        #         output += f"{item[0]}: {item[1]}\n"
        #     output += f"\n"

        # if self.lc_inter_direct is not None:
        #     output += self.__title_str("Loop closure - Inter - Direct")
        #     for item in self.lc_inter_direct.items():
        #         output += f"{item[0]}: {item[1]}\n"
        #     output += f"\n"

        # if self.sigmas is not None:
        #     output += self.__title_str("Sigmas")
        #     for item in self.sigmas.items():
        #         output += f"{item[0]}: {item[1]}\n"
        #     output += f"\n"

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
    generate_default_config_file()
    file_path = '/home/workspace/configs/default.json'
    Params = DatasetConfiguration(file_path)
    print(Params)