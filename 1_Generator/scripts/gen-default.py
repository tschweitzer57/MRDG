from generator import DatasetGenerator
from configuration import get_config_paths

if __name__ == "__main__":

    # config_folder = './configs/VLD1'
    # config_paths = get_config_paths(config_folder)

    # for file_path in config_paths:
    #     dataset = DatasetGenerator(file_path)
    #     dataset.generate_dataset()

    file_path = './configs/DEFAULT/default.json'
    dataset = DatasetGenerator(file_path)
    dataset.generate_dataset()