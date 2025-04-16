from results import Results
from display import Display, MultiDisplay
import numpy as np

import os
import glob

def get_data_paths(solver, results_folder, dataset_folder):
    # Get all dataset .jrl files paths
    datasets_paths = glob.glob(os.path.join(dataset_folder, '*.jrl'))

    # Get all results paths
    entries = os.listdir(results_folder)
    results_paths = [os.path.join(results_folder, entry) for entry in entries if os.path.isdir(os.path.join(results_folder, entry))]

    # Define output list
    paths = {}

    for result_path in results_paths:
        for dataset_path in datasets_paths:
            dataset_name = os.path.splitext(os.path.basename(dataset_path))[0]
            if dataset_name in os.path.basename(result_path):
                paths[solver +'_'+ dataset_name] = (dataset_path,result_path)

    return paths

#####################################################
###           Landmarks - Noisy - CTR             ###
#####################################################
dataset_folder = 'datasets/TEST_1/landmarks_noisy'
results_folder = 'input/TEST_1_ctr/landmarks_noisy'
solver = 'ctr'
paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

#####################################################
###           Landmarks - Noisy - MESA            ###
#####################################################
dataset_folder = 'datasets/TEST_1/landmarks_noisy'
results_folder = 'input/TEST_1_mesa/landmarks_noisy'
solver = 'mesa'
paths_mesa = get_data_paths(solver, results_folder, dataset_folder)

#####################################################
###           Landmarks - Noisy - PYXIS           ###
#####################################################
dataset_folder = 'input/TEST_1_pyxis/landmarks_noisy'
results_folder = 'input/TEST_1_ctr/landmarks_noisy'
solver = 'pyxis'
paths_pyxis = get_data_paths(solver, results_folder, dataset_folder)

output_folder = 'saved_output'
data = {}

# Compute errors for all datasets/results couple
for key in paths_mesa.keys():
    if not 'no_lk' in key:
        print(key, paths_mesa[key][1])
        data[key] = Results(paths_mesa[key][1], paths_mesa[key][0], output_folder)

for key in paths_pyxis.keys():
    if not 'no_lk' in key:
        print(key, paths_pyxis[key][1])
        data[key] = Results(paths_pyxis[key][1], paths_pyxis[key][0], output_folder)

mdsp = MultiDisplay()

for key in data.keys():
    mdsp.add_results(key, data[key])

mdsp.std_boxplot(output_path='saved_output')
# mdsp.boxplot('transformation_rpe')
# mdsp.boxplot('point_distance_rpe')
# mdsp.boxplot('rot_angle_deg_rpe')

# mdsp.boxplot('transformation_ape')
# mdsp.boxplot('point_distance_ape')
# mdsp.boxplot('rot_angle_deg_ape')



