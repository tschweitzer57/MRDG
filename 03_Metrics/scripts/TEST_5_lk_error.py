from results import Results, Results2
from display import Display, MultiDisplay
import numpy as np

import os
import glob
import sys

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
###           TEST_4 - Pyxis                      ###
#####################################################
dataset_folder = 'datasets/TEST_5'
results_folder = 'input/TEST_5'
output_folder = 'saved_output'

solver = 'pyxis'

results_paths = get_data_paths(solver, results_folder, dataset_folder)
data = {}

for key in results_paths.keys():
    res = Results2(results_paths[key][1], results_paths[key][0], output_folder)
    res.get_gtlk_error(1)
    break


# mdsp = MultiDisplay()

# for key in data.keys():
#     mdsp.add_results(key, data[key])

# mdsp.std_boxplot(output_path='saved_output')

# for key in data.keys():
#     if 'default' in key:
#         name_id = 'default'
#     elif 'noisy' in key:
#         name_id = 'noisy'
#     else:
#         name_id = 'none'
#     for idx, result in enumerate(data[key]):
#         dsp = Display(result)
#         dsp.plot_trajectories_all(data_type='est', ref='gt',name=f'{name_id}: iteration {idx}')