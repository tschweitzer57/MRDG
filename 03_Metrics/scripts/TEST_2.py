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
# Initialization : 02
# dataset_folder = 'datasets/TEST_2/landmarks_02'
# results_folder = 'input/TEST_2_ctr/landmarks_02'
# solver = 'ctr'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 04
# dataset_folder = 'datasets/TEST_2/landmarks_04'
# results_folder = 'input/TEST_2_ctr/landmarks_04'
# solver = 'ctr'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 06
# dataset_folder = 'datasets/TEST_2/landmarks_06'
# results_folder = 'input/TEST_2_ctr/landmarks_06'
# solver = 'ctr'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 08
# dataset_folder = 'datasets/TEST_2/landmarks_08'
# results_folder = 'input/TEST_2_ctr/landmarks_08'
# solver = 'ctr'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 10
# dataset_folder = 'datasets/TEST_2/landmarks_10'
# results_folder = 'input/TEST_2_ctr/landmarks_10'
# solver = 'ctr'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

#####################################################
###           Landmarks - Noisy - MESA            ###
#####################################################
# Initialization : 02
# dataset_folder = 'datasets/TEST_2/landmarks_02'
# results_folder = 'input/TEST_2_mesa/landmarks_02'
# solver = 'mesa'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 04
# dataset_folder = 'datasets/TEST_2/landmarks_04'
# results_folder = 'input/TEST_2_mesa/landmarks_04'
# solver = 'mesa'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 06
# dataset_folder = 'datasets/TEST_2/landmarks_06'
# results_folder = 'input/TEST_2_mesa/landmarks_06'
# solver = 'mesa'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 08
# dataset_folder = 'datasets/TEST_2/landmarks_08'
# results_folder = 'input/TEST_2_mesa/landmarks_08'
# solver = 'mesa'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 10
# dataset_folder = 'datasets/TEST_2/landmarks_10'
# results_folder = 'input/TEST_2_mesa/landmarks_10'
# solver = 'mesa'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

#####################################################
###           Landmarks - Noisy - Pyxis           ###
#####################################################
# Initialization : 02
# dataset_folder = 'datasets/TEST_2/landmarks_02'
# results_folder = 'input/TEST_2_pyxis/landmarks_02'
# solver = 'pyxis'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 04
# dataset_folder = 'datasets/TEST_2/landmarks_04'
# results_folder = 'input/TEST_2_pyxis/landmarks_04'
# solver = 'pyxis'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 06
# dataset_folder = 'datasets/TEST_2/landmarks_06'
# results_folder = 'input/TEST_2_pyxis/landmarks_06'
# solver = 'pyxis'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 08
dataset_folder = 'datasets/TEST_2/landmarks_08'
results_folder = 'input/TEST_2_pyxis/landmarks_08'
solver = 'pyxis'
paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

# Initialization : 10
# dataset_folder = 'datasets/TEST_2/landmarks_10'
# results_folder = 'input/TEST_2_pyxis/landmarks_10'
# solver = 'pyxis'
# paths_ctr = get_data_paths(solver, results_folder, dataset_folder)

output_folder = 'saved_output'
data = {}

# Compute errors for all datasets/results couple
computed_paths = paths_ctr
for key in computed_paths.keys():
    print(key, computed_paths[key][1])
    data[key] = Results(computed_paths[key][1], computed_paths[key][0], output_folder, iteration=36)

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