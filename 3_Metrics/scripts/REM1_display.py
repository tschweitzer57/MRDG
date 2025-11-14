from results import Results, Results2
from display import Display, Display2, MultiDisplay
from loader import Loader
import numpy as np

#####################################################
###               Results display                 ###
#####################################################
dataset_folder = './datasets/REM_1'
results_folder = './input/REM_1'
solvers = ['mesa']

output_folder = 'saved_output'
display_folder = 'display_output'

data = Loader(solvers, results_folder, dataset_folder)

for result_line in data:
    res = Results2(result_line.result_path, result_line.dataset_path, output_folder)

#     dataset = dataset_group[0]

#     for paths in dataset_group[1]:
#         print(paths)
        # res = Results2(data[1][0], data[1][1], output_folder)
    
#     solvers = []
#     errors = {}
#     errors['consensus'] = []
#     dsp = Display2(display_folder)

#     for data in dataset_group[1]:
#         print(f"Solver: {data[0]}")
#         solvers.append(data[0])
#         res = Results2(data[1][0], data[1][1], output_folder)
#         errors['consensus'].append(res.get_consensuslk_error(1))
#         dsp.plot_gtlk_error(res.get_gtlk_error(1), f'Swarm Errors on landmark 1 ({dataset} - {data[0]})')

#     dsp.plot_consensuslk_error(errors['consensus'],solvers, f'Swarm Consensus on landmark 1 ({dataset})')