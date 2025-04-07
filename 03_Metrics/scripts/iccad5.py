from results import Results
from display import Display, MultiDisplay
import numpy as np

# PYXIS - LANDMARKS #
ctr_def_noisy = Results('./input/iccad_5_ctr/default_noisy_gt_centralized_2025-04-07_12-13-42',
                        './datasets/iccad_5/default_noisy_gt.jrl',
                        './saved_output')
ctr_def_noisy_e = Results('./input/iccad_5_ctr/default_noisy_gt_e_centralized_2025-04-07_12-15-19',
                          './datasets/iccad_5/default_noisy_gt_e.jrl',
                          './saved_output')
ctr_def_odom = Results('./input/iccad_5_ctr/default_odom_centralized_2025-04-07_12-14-53',
                       './datasets/iccad_5/default_odom.jrl',
                       './saved_output')
ctr_def_odom_e = Results('./input/iccad_5_ctr/default_odom_e_centralized_2025-04-07_12-15-03',
                         './datasets/iccad_5/default_odom_e.jrl',
                         './saved_output')
ctr_no_lk_noisy = Results('./input/iccad_5_ctr/no_lk_noisy_gt_centralized_2025-04-07_12-14-15',
                          './datasets/iccad_5/no_lk_noisy_gt.jrl',
                          './saved_output')
ctr_no_lk_odom = Results('./input/iccad_5_ctr/no_lk_odom_centralized_2025-04-07_12-13-58',
                         './datasets/iccad_5/no_lk_odom.jrl',
                         './saved_output')

mdsp = MultiDisplay()

mdsp.add_results('ctr_no_lk_odom', ctr_no_lk_odom)
mdsp.add_results('ctr_def_odom', ctr_def_odom)
mdsp.add_results('ctr_def_odom_e', ctr_def_odom_e)
# mdsp.add_results('ctr_no_lk_noisy', ctr_no_lk_noisy)
# mdsp.add_results('ctr_def_noisy', ctr_def_noisy)
# mdsp.add_results('ctr_def_noisy_e', ctr_def_noisy_e)


mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

mdsp.boxplot('transformation_ape')
mdsp.boxplot('point_distance_ape')
mdsp.boxplot('rot_angle_deg_ape')