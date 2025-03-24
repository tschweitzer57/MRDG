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
dis_2_20lk = Results('./input/Pyxis/landmarks_2_20_geodesic-mesa_2025-03-19_15-02-56',
                     './datasets/landmarks/landmarks_2_20.jrl',
                     './saved_output')
dis_2_40lk = Results('./input/Pyxis/landmarks_2_40_geodesic-mesa_2025-03-19_15-04-23',
                     './datasets/landmarks/landmarks_2_40.jrl',
                     './saved_output')
dis_2_60lk = Results('./input/Pyxis/landmarks_2_60_geodesic-mesa_2025-03-19_15-05-52',
                     './datasets/landmarks/landmarks_2_60.jrl',
                     './saved_output')
dis_2_80lk = Results('./input/Pyxis/landmarks_2_80_geodesic-mesa_2025-03-19_15-09-47',
                     './datasets/landmarks/landmarks_2_80.jrl',
                     './saved_output')

## CENTRALIZED : ALL ##
cent_80lk = Results('./input/Centralized/landmarks_80_centralized_2025-03-19_16-20-50',
                    './datasets/landmarks/landmarks_80.jrl',
                    './saved_output')
cent_60lk = Results('./input/Centralized/landmarks_60_centralized_2025-03-19_16-20-41',
                    './datasets/landmarks/landmarks_60.jrl',
                    './saved_output')
cent_40lk = Results('./input/Centralized/landmarks_40_centralized_2025-03-19_16-16-25',
                    './datasets/landmarks/landmarks_40.jrl',
                    './saved_output')
cent_20lk = Results('./input/Centralized/landmarks_20_centralized_2025-03-19_16-16-12',
                    './datasets/landmarks/landmarks_20.jrl',
                    './saved_output')

## CENTRALIZED : 2 - 2 ##
cent_2_20lk = Results('./input/Centralized/landmarks_2_20_centralized_2025-03-19_16-21-37',
                      './datasets/landmarks/landmarks_2_20.jrl',
                      './saved_output')
cent_2_40lk = Results('./input/Centralized/landmarks_2_40_centralized_2025-03-19_16-21-27',
                      './datasets/landmarks/landmarks_2_40.jrl',
                      './saved_output')
cent_2_60lk = Results('./input/Centralized/landmarks_2_60_centralized_2025-03-19_16-21-18',
                      './datasets/landmarks/landmarks_2_60.jrl',
                      './saved_output')
cent_2_80lk = Results('./input/Centralized/landmarks_2_80_centralized_2025-03-19_16-21-01',
                      './datasets/landmarks/landmarks_2_80.jrl',
                      './saved_output')



mdsp = MultiDisplay()

# mdsp.add_results('dis_80lk', dis_80lk)
# mdsp.add_results('dis_60lk', dis_60lk)
# mdsp.add_results('dis_40lk', dis_40lk)
# mdsp.add_results('dis_20lk', dis_20lk)

# mdsp.add_results('dis_2_20lk', dis_2_20lk)
# mdsp.add_results('dis_20lk', dis_20lk)
# mdsp.add_results('dis_2_40lk', dis_2_40lk)
# mdsp.add_results('dis_40lk', dis_40lk)
# mdsp.add_results('dis_2_60lk', dis_2_60lk)
# mdsp.add_results('dis_60lk', dis_60lk)
# mdsp.add_results('dis_2_80lk', dis_2_80lk)
# mdsp.add_results('dis_80lk', dis_80lk)

mdsp.add_results('cent_2_20lk', cent_2_20lk)
mdsp.add_results('cent_20lk', cent_20lk)
mdsp.add_results('cent_2_40lk', cent_2_40lk)
mdsp.add_results('cent_40lk', cent_40lk)
mdsp.add_results('cent_2_60lk', cent_2_60lk)
mdsp.add_results('cent_60lk', cent_60lk)
mdsp.add_results('cent_2_80lk', cent_2_80lk)
mdsp.add_results('cent_80lk', cent_80lk)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

mdsp.boxplot('transformation_ape')
mdsp.boxplot('point_distance_ape')
mdsp.boxplot('rot_angle_deg_ape')

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