from results import Results
from display import Display, MultiDisplay
import numpy as np


## DISTRIBUTED : ALL ##
dis_80lk = Results('./input/Pyxis/landmarks_80_geodesic-mesa_2025-03-19_15-12-59',
                   './datasets/landmarks/landmarks_80.jrl',
                   './saved_output')
dis_60lk = Results('./input/Pyxis/landmarks_60_geodesic-mesa_2025-03-19_15-17-21',
                   './datasets/landmarks/landmarks_60.jrl',
                   './saved_output')
dis_40lk = Results('./input/Pyxis/landmarks_40_geodesic-mesa_2025-03-19_15-19-29',
                   './datasets/landmarks/landmarks_40.jrl',
                   './saved_output')
dis_20lk = Results('./input/Pyxis/landmarks_20_geodesic-mesa_2025-03-19_15-27-16',
                   './datasets/landmarks/landmarks_20.jrl',
                   './saved_output')

## DISTRIBUTED : 2 - 2 ##

mdsp = MultiDisplay()
mdsp.add_results('dis_80lk', dis_80lk)
mdsp.add_results('dis_60lk', dis_60lk)
mdsp.add_results('dis_40lk', dis_40lk)
mdsp.add_results('dis_20lk', dis_20lk)

mdsp.boxplot()

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