import os
import glob
import re
import sys

class DatasetGroup():
    def __init__(self, solver, dataset, result_path, dataset_path):
        self.solver = solver
        self.dataset = dataset
        self.result_path = result_path
        self.dataset_path = dataset_path

class Loader():
    def __init__(self, solvers, results_folder, dataset_folder):

        self.data_groups = self.__groupData(solvers, results_folder, dataset_folder)
        self.index = 0
        
    # def __init__(self, results_path, dataset_path, export_path, iteration='final', init=False):
    #     self.Results = Results(results_path, dataset_path, export_path, iteration, init)
    #     self.Data = Data(self.Results)

    def dataset(self, dataset_name):
        return [data for data in self.data_groups if data.dataset == dataset_name]

    def solver(self, solver_name):
        return [data for data in self.data_groups if data.solver == solver_name]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.data_groups):
            value = self.data_groups[self.index]
            self.index += 1
            return value
        else:
            raise StopIteration

    def __groupData(self, solvers, results_folder, dataset_folder):
        # get all data paths
        # Get all dataset .jrl files paths
        datasets_paths = glob.glob(os.path.join(dataset_folder, '*.jrl'))

        # Get all results paths
        entries = os.listdir(results_folder)
        results_paths = [os.path.join(results_folder, entry) for entry in entries if os.path.isdir(os.path.join(results_folder, entry))]

        dataGroups = []
        for solver in solvers:
            for result_path in results_paths:
                for dataset_path in datasets_paths:
                    dataset_name = os.path.splitext(os.path.basename(dataset_path))[0]
                    basename = os.path.basename(result_path)
                    dataset_match = re.search(r'(?<![a-zA-Z0-9])' + re.escape(dataset_name) + r'(?![a-zA-Z0-9])', basename)
                    solver_match = re.search(r'(?<![a-zA-Z0-9])' + re.escape(solver) + r'(?![a-zA-Z0-9])', basename)
                    if dataset_match and solver_match:
                        dataGroups.append(DatasetGroup(solver, dataset_name, result_path, dataset_path))
        return dataGroups
    
    # def group(data_paths):
    #     datasets_group = {}
    #     for item in data_paths.items():
    #         print(item)
    #         dataset = item[0][1]
    #         solver = item[0][0]

    #         if dataset not in datasets_group.keys():
    #             datasets_group[dataset] = []
    #             datasets_group[dataset].append((solver,item[1]))
    #         else:
    #             datasets_group[dataset].append((solver,item[1]))

    #     return datasets_group
        

if __name__ == "__main__":
    dataset_folder = './datasets/REM_1'
    results_folder = './input/REM_1'
    solvers = ['mesa']
    # output_folder = 'saved_output'
    # display_folder = 'display_output'

    data = Loader(solvers, results_folder, dataset_folder)
    for data_group in data.solver('mesa'):
        print(len(data.solver('mesa')))
        print(data_group.solver)
        print(data_group.dataset)
        print(data_group.result_path)
        print(data_group.dataset_path)

    for data_group in data.dataset('mesa_landmarks'):
        print(data_group.solver)
        print(data_group.dataset)
        print(data_group.result_path)
        print(data_group.dataset_path)