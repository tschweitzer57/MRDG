import os
from helpers.solvers import distributed_Solver, centralized_Solver, separated_Solver
from helpers.parser import has_comm_edge

# TODO handle solvers options through config file

def get_dataset_paths(directory):
    dataset_paths = {}
    
    for root, dirs, files in os.walk(directory):
        if files:
            file_paths = []
            for file in files:
                if file[-4:] == '.jrl':
                    file_paths.append(os.path.join(root, file))
            dataset_paths[os.path.basename(root)] = file_paths
    return dataset_paths

def set_output_dir(results_path, subfolder, dataset_path):
    dataset_name = os.path.basename(dataset_path)
    name = dataset_name.replace(subfolder + '_', '')
    name = name.replace('.jrl', '')
    return results_path + '/' + subfolder + '/' + name

if __name__ == "__main__":

    dataset_folder = 'output/datasets/syscon25'
    results_output_dir = 'output/results/syscon25'
    dataset_paths = get_dataset_paths(dataset_folder)

    for subfolder in dataset_paths.keys():
        results = results_output_dir + '/' + subfolder
        for path in dataset_paths[subfolder]:
            result_dir = set_output_dir(results_output_dir, subfolder, path)

            # Compute separated
            print('Solving Separated')
            solver_s = separated_Solver(path)
            solver_s.solve()
            solver_s.save_results(result_dir + '/separated')

            if has_comm_edge(path):
                # Compute distributed
                print('Solving distributed')
                solver_d = distributed_Solver(path)
                solver_d.solve()
                solver_d.save_results(result_dir + '/distributed')

            if has_comm_edge(path):
                # Compute centralized
                print('Solving centralized')
                solver_c = centralized_Solver(path)
                solver_c.solve()
                solver_c.save_results(result_dir + '/centralized')
        