from parser import DatasetParser
import os

if __name__ == "__main__":

    dataset_folder = "./saved_outputs/BR_1"
    dataset_name = 'default_4'
    output_path = os.path.join(dataset_folder, dataset_name + "_parsed.txt")
    dataset_path = os.path.join(dataset_folder, dataset_name + ".jrl")
    
    parser = DatasetParser(dataset_path)
    # parser.summary(file=True, filepath=output_path)
    parser.summary(file=True)
    # parser.plot_trajectories(data_type='init')