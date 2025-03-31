from parser import DatasetParser
import os

if __name__ == "__main__":

    dataset_folder = "./saved_outputs/iccad_4/lc_indirect"
    dataset_name = 'lc_indirect5'
    output_path = os.path.join(dataset_folder, dataset_name + "_parsed.txt")
    dataset_path = os.path.join(dataset_folder, dataset_name + ".jrl")
    
    parser = DatasetParser(dataset_path)
    parser.print(file=True, filepath=output_path)