import os
from helpers.solvers2 import distributed_Solver, centralized_Solver, separated_Solver
# from helpers.parser import has_comm_edge

# TODO handle solvers options through config file

# def get_dataset_paths(directory):
#     dataset_paths = {}
    
#     for root, dirs, files in os.walk(directory):
#         if files:
#             file_paths = []
#             for file in files:
#                 if file[-4:] == '.jrl':
#                     file_paths.append(os.path.join(root, file))
#             dataset_paths[os.path.basename(root)] = file_paths
#     return dataset_paths

# def set_output_dir(results_path, subfolder, dataset_path):
#     dataset_name = os.path.basename(dataset_path)
#     name = dataset_name.replace(subfolder + '_', '')
#     name = name.replace('.jrl', '')
#     return results_path + '/' + subfolder + '/' + name

if __name__ == "__main__":
    
    dataset_folder = 'landmarks'
    dataset_file = 'landmarks'
    
    input_folder = './output_debug'
    output_folder = './output_debug/results'
    input_path = os.path.join(input_folder, dataset_folder, dataset_file + ".jrl")
    output_path = os.path.join(output_folder, dataset_folder, dataset_file)

    solver_c = centralized_Solver(input_path)
    solver_c.solve()
    solver_c.save_results(output_path)
    print('computed centralized')

    solver_s = separated_Solver(input_path)
    solver_s.solve()
    solver_s.save_results(output_path)
    separated_Solver
    print('computed separated')