from datetime import date
import gtsam

from copy import copy
from string import ascii_letters
from itertools import combinations

from generator import DatasetGenerator
from configuration import get_config_paths

if __name__ == "__main__":

    config_folder = './configs/BR_1'
    output_dir = './saved_outputs/BR_1'
    
    file_paths = get_config_paths(config_folder)

    for config_file_path in file_paths:
        print("Generating dataset for config:", config_file_path)
        # dataset = DatasetGenerator(config_file_path)
        # dataset.generate_dataset(output_dir)