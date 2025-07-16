from results import Results, Results2
from display import Display, MultiDisplay
import numpy as np

import os
import glob
import sys

def group(data_paths):
    datasets_group = {}
    for item in data_paths.items():
        print(item)
        dataset = item[0][1]
        solver = item[0][0]

        if dataset not in datasets_group.keys():
            datasets_group[dataset] = []
            datasets_group[dataset].append((solver,item[1]))
        else:
            datasets_group[dataset].append((solver,item[1]))

    return datasets_group

def get_data_paths(solvers, results_folder, dataset_folder):
    # Get all dataset .jrl files paths
    datasets_paths = glob.glob(os.path.join(dataset_folder, '*.jrl'))

    # Get all results paths
    entries = os.listdir(results_folder)
    results_paths = [os.path.join(results_folder, entry) for entry in entries if os.path.isdir(os.path.join(results_folder, entry))]

    # Define output list
    paths = {}
    for solver in solvers:
        for result_path in results_paths:
            for dataset_path in datasets_paths:
                dataset_name = os.path.splitext(os.path.basename(dataset_path))[0]
                if dataset_name in os.path.basename(result_path) and solver in os.path.basename(result_path):
                    paths[(solver , dataset_name)] = (result_path, dataset_path)
    return paths

#####################################################
###           BR_1 - Pyxis                      ###
#####################################################
dataset_folder = './datasets/BR_1'
results_folder = './input/BR_1'
output_folder = 'saved_output'

solvers = ['pyxis', 'mesa', 'mesa-2']

results_paths = get_data_paths(solvers, results_folder, dataset_folder)
data = {}

for dataset_group in group(results_paths).items():
    dataset = dataset_group[0]
    print(f"Dataset: {dataset}")
    solvers = []
    errors = {}
    errors['gt'] = []
    errors['consensus'] = []

    for data in dataset_group[1]:
        print(f"Solver: {data[0]}")
        solvers.append(data[0])
        res = Results2(data[1][0], data[1][1], output_folder)
        errors['consensus'].append(res.get_consensuslk_error(1))
        errors['gt'].append(res.get_gtlk_error(1))

    dsp = Display2()
    dsp.plot_consensuslk_error(errors['consensus'],solvers,'Consensus de l\'essaim')

#     print(results_paths[key][0], results_paths[key][1])
    
    # res1 = Results(results_paths[key][0], results_paths[key][1], output_folder)
    # res = Results2(results_paths[key][0], results_paths[key][1], output_folder)
    # err = res.get_consensuslk_error(1)
    # dsp = Display(res1)
    # dsp.plot_consensuslk_error([err],['Val'],'Consensus de l\'essaim')
    # err = res.get_gtlk_error(1)
    # dsp.plot_gtlk_error(err)