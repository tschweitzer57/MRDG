from generator import DatasetGenerator
from configuration import get_config_paths

#===================================================
# Here define configuration folder to use
#===================================================
CONFIG_FOLDERS = ["./configs/LK_OUT_FM",
                  "./configs/LK_OUT_B",
                  "configs/LK_1"
                  ]

if __name__ == "__main__":
    
    config_paths = get_config_paths(CONFIG_FOLDERS)

    for file_path in config_paths:
        dataset = DatasetGenerator(file_path)
        dataset.generate_dataset()