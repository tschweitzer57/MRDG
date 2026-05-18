from parser import DatasetParser
import os

if __name__ == "__main__":

    dataset_path = "./saved_outputs/VLD1/detection_shared.jrl"
    
    parser = DatasetParser(dataset_path)
    parser.summary(file=True)
    parser.plot_trajectories(data_type='gt')