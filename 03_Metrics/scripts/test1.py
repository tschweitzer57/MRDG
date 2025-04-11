from results import Results
from display import Display, MultiDisplay
import numpy as np

# PYXIS - LK Odometry #
ctr_def_a1_o = Results('./input/TEST_1_ctr/landmarks_odom/default_a1_o_centralized_2025-04-10_21-54-57',
                       './datasets/TEST_1/landmarks_odom/default_a1.jrl',
                       './saved_output')
ctr_def_a2_o = Results('./input/TEST_1_ctr/landmarks_odom/default_a2_o_centralized_2025-04-10_21-55-00',
                       './datasets/TEST_1/landmarks_odom/default_a2.jrl',
                       './saved_output')
ctr_def_a3_o = Results('./input/TEST_1_ctr/landmarks_odom/default_a3_o_centralized_2025-04-10_21-55-05',
                       './datasets/TEST_1/landmarks_odom/default_a3.jrl',
                       './saved_output')
ctr_def_e1_o = Results('./input/TEST_1_ctr/landmarks_odom/default_e1_o_centralized_2025-04-10_21-55-06',
                       './datasets/TEST_1/landmarks_odom/default_e1.jrl',
                       './saved_output')
ctr_def_e2_o = Results('./input/TEST_1_ctr/landmarks_odom/default_e2_o_centralized_2025-04-10_21-55-08',
                       './datasets/TEST_1/landmarks_odom/default_e2.jrl',
                       './saved_output')
ctr_def_e3_o = Results('./input/TEST_1_ctr/landmarks_odom/default_e3_o_centralized_2025-04-10_21-55-09',
                       './datasets/TEST_1/landmarks_odom/default_e3.jrl',
                       './saved_output')
ctr_no_lk1_o = Results('./input/TEST_1_ctr/landmarks_odom/no_lk1_o_centralized_2025-04-10_21-55-11',
                       './datasets/TEST_1/landmarks_odom/no_lk1.jrl',
                       './saved_output')
ctr_no_lk2_o = Results('./input/TEST_1_ctr/landmarks_odom/no_lk2_o_centralized_2025-04-10_21-55-13',
                       './datasets/TEST_1/landmarks_odom/no_lk2.jrl',
                       './saved_output')
ctr_no_lk3_o = Results('./input/TEST_1_ctr/landmarks_odom/no_lk3_o_centralized_2025-04-10_21-55-15',
                       './datasets/TEST_1/landmarks_odom/no_lk3.jrl',
                       './saved_output')

# PYXIS - LK Odometry #
ctr_def_a1_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_a1_n_centralized_2025-04-10_21-54-27',
                       './datasets/TEST_1/landmarks_noisy/default_a1.jrl',
                       './saved_output')
ctr_def_a2_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_a2_n_centralized_2025-04-10_21-54-49',
                       './datasets/TEST_1/landmarks_noisy/default_a2.jrl',
                       './saved_output')
ctr_def_a3_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_a3_n_centralized_2025-04-10_21-54-50',
                       './datasets/TEST_1/landmarks_noisy/default_a3.jrl',
                       './saved_output')
ctr_def_e1_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_e1_n_centralized_2025-04-10_21-54-51',
                       './datasets/TEST_1/landmarks_noisy/default_e1.jrl',
                       './saved_output')
ctr_def_e2_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_e2_n_centralized_2025-04-10_21-54-53',
                       './datasets/TEST_1/landmarks_noisy/default_e2.jrl',
                       './saved_output')
ctr_def_e3_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_e3_n_centralized_2025-04-10_21-54-53',
                       './datasets/TEST_1/landmarks_noisy/default_e3.jrl',
                       './saved_output')
ctr_no_lk1_n = Results('./input/TEST_1_ctr/landmarks_noisy/no_lk1_n_centralized_2025-04-10_21-54-54',
                       './datasets/TEST_1/landmarks_noisy/no_lk1.jrl',
                       './saved_output')
ctr_no_lk2_n = Results('./input/TEST_1_ctr/landmarks_noisy/no_lk2_n_centralized_2025-04-10_21-54-55',
                       './datasets/TEST_1/landmarks_noisy/no_lk2.jrl',
                       './saved_output')
ctr_no_lk3_n = Results('./input/TEST_1_ctr/landmarks_noisy/no_lk3_n1_centralized_2025-04-10_21-54-56',
                       './datasets/TEST_1/landmarks_noisy/no_lk3.jrl',
                       './saved_output')

mdsp = MultiDisplay()

# mdsp.add_results('ctr_def_a1_o', ctr_def_a1_o)
# mdsp.add_results('ctr_def_a2_o', ctr_def_a2_o)
# mdsp.add_results('ctr_def_a3_o', ctr_def_a3_o)

# mdsp.add_results('ctr_def_e1_o', ctr_def_e1_o)
# mdsp.add_results('ctr_def_e2_o', ctr_def_e2_o)
# mdsp.add_results('ctr_def_e3_o', ctr_def_e3_o)

# mdsp.add_results('ctr_no_lk1_o', ctr_no_lk1_o)
# mdsp.add_results('ctr_no_lk2_o', ctr_no_lk2_o)
# mdsp.add_results('ctr_no_lk3_o', ctr_no_lk3_o)

mdsp.add_results('ctr_def_a1_n', ctr_def_a1_n)
mdsp.add_results('ctr_def_a2_n', ctr_def_a2_n)
mdsp.add_results('ctr_def_a3_n', ctr_def_a3_n)

mdsp.add_results('ctr_def_e1_n', ctr_def_e1_n)
mdsp.add_results('ctr_def_e2_n', ctr_def_e2_n)
mdsp.add_results('ctr_def_e3_n', ctr_def_e3_n)

mdsp.add_results('ctr_no_lk1_n', ctr_no_lk1_n)
mdsp.add_results('ctr_no_lk2_n', ctr_no_lk2_n)
mdsp.add_results('ctr_no_lk3_n', ctr_no_lk3_n)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

mdsp.boxplot('transformation_ape')
mdsp.boxplot('point_distance_ape')
mdsp.boxplot('rot_angle_deg_ape')