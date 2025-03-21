from results import Results
from display import Display
import numpy as np

test = Results('./input/Pyxis/landmarks_80_geodesic-mesa_2025-03-19_15-12-59',
               './datasets/landmarks/landmarks_80.jrl',
               './saved_output')
#test = Results('./input/landmarks_geodesic-mesa_2025-02-27_11-16-52', './saved_output', './datasets/landmarks.jrl')

# Generate results folder
# TODO: add possibility to load data from generated results

print(test.get_errors('all'))
# dsp = Display(test)
# dsp.plot_trajectories_all()
# dsp.boxplot('transformation_ape', './saved_output/peer_80lk.png')
# dsp.boxplot('transformation_ape')
# dsp.plot_trajectories_comp(['gt','est'])

# dsp.plot_trajectories('gt')
# dsp.plot_trajectories_all('gt')
# dsp.plot_trajectories('est')
# dsp.plot_trajectories_all('est')

# dsp_test = Test('./datasets/landmarks_2.jrl')
# dsp_test.plot_trajectories('init')
# dsp_test.plot_trajectories_all('gt')
# dsp_test.boxplot()
# dsp_test.errorbar()
# dsp_test.violin()