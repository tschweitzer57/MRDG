from metrics import Results
from display import Display, Test

# test = Results('./input/landmarks_2_geodesic-mesa_2025-03-01_01-21-08', './saved_output', './datasets/landmarks_2.jrl')

# Generate results folder
# TODO: add possibility to load data from generated results

# test.compute_all_results()
# dsp = Display(test)
dsp_test = Test('./datasets/landmarks_2.jrl')
# dsp_test.plot_trajectories('init')
# dsp_test.plot_trajectories_all('gt')
dsp_test.boxplot()
dsp_test.errorbar()
dsp_test.violin()