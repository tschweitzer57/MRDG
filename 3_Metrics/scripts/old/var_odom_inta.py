from results import Results
from display import Display, MultiDisplay
import numpy as np

# CENTRALIZED - DEFAULT #
# intra31 = Results('./input/var_intra_others/lc_intra3_centralized_2025-03-27_05-38-32',
#                   './datasets/var_intra/lc_intra31.jrl',
#                   './saved_output')
# intra32 = Results('./input/var_intra_others/lc_intra3_centralized_2025-03-27_05-38-39',
#                   './datasets/var_intra/lc_intra32.jrl',
#                   './saved_output')
# intra33 = Results('./input/var_intra_others/lc_intra3_centralized_2025-03-27_05-38-45',
#                   './datasets/var_intra/lc_intra33.jrl',
#                   './saved_output')
# intra34 = Results('./input/var_intra_others/lc_intra3_centralized_2025-03-27_05-38-52',
#                   './datasets/var_intra/lc_intra34.jrl',
#                   './saved_output')
# intra35 = Results('./input/var_intra_others/lc_intra3_centralized_2025-03-27_05-38-57',
#                   './datasets/var_intra/lc_intra35.jrl',
#                   './saved_output')
# intra36 = Results('./input/var_intra_others/lc_intra3_centralized_2025-03-27_05-39-05',
#                   './datasets/var_intra/lc_intra36.jrl',
#                   './saved_output')
# intra37 = Results('./input/var_intra_others/lc_intra3_centralized_2025-03-27_05-39-11',
#                   './datasets/var_intra/lc_intra37.jrl',
#                   './saved_output')
# intra38 = Results('./input/var_intra_others/lc_intra3_centralized_2025-03-27_05-39-17',
#                   './datasets/var_intra/lc_intra38.jrl',
#                   './saved_output')
# intra39 = Results('./input/var_intra_others/lc_intra3_centralized_2025-03-27_05-39-24',
#                   './datasets/var_intra/lc_intra39.jrl',
#                   './saved_output')

odom1 = Results('./input/var_odom_others/odom1_centralized_2025-03-27_05-42-44',
                './datasets/var_odom/odom1.jrl',
                './saved_output')
odom2 = Results('./input/var_odom_others/odom1_centralized_2025-03-27_05-42-48',
                './datasets/var_odom/odom2.jrl',
                './saved_output')
odom3 = Results('./input/var_odom_others/odom1_centralized_2025-03-27_05-42-51',
                './datasets/var_odom/odom3.jrl',
                './saved_output')
odom4 = Results('./input/var_odom_others/odom1_centralized_2025-03-27_05-42-54',
                './datasets/var_odom/odom4.jrl',
                './saved_output')
odom5 = Results('./input/var_odom_others/odom1_centralized_2025-03-27_05-42-58',
                './datasets/var_odom/odom5.jrl',
                './saved_output')
odom6 = Results('./input/var_odom_others/odom1_centralized_2025-03-27_05-43-02',
                './datasets/var_odom/odom6.jrl',
                './saved_output')
odom7 = Results('./input/var_odom_others/odom1_centralized_2025-03-27_05-43-05',
                './datasets/var_odom/odom7.jrl',
                './saved_output')
odom8 = Results('./input/var_odom_others/odom1_centralized_2025-03-27_05-43-09',
                './datasets/var_odom/odom8.jrl',
                './saved_output')
odom9 = Results('./input/var_odom_others/odom1_centralized_2025-03-27_05-43-13',
                './datasets/var_odom/odom9.jrl',
                './saved_output')









# PYXIS - DEFAULT #
# default1 = Results('./input/var_others/default1_centralized_2025-03-27_01-09-58',
#                    './datasets/var/default1.jrl',
#                    './saved_output')
# default2 = Results('./input/var_others/default2_centralized_2025-03-27_01-10-03',
#                    './datasets/var/default2.jrl',
#                    './saved_output')
# default3 = Results('./input/var_others/default3_centralized_2025-03-27_01-10-08',
#                    './datasets/var/default3.jrl',
#                    './saved_output')
# default4 = Results('./input/var_others/default4_centralized_2025-03-27_01-10-13',
#                    './datasets/var/default4.jrl',
#                    './saved_output')
# default5 = Results('./input/var_others/default5_centralized_2025-03-27_01-10-17',
#                    './datasets/var/default5.jrl',
#                    './saved_output')
# default6 = Results('./input/var_others/default6_centralized_2025-03-27_01-10-23',
#                    './datasets/var/default6.jrl',
#                    './saved_output')
# default7 = Results('./input/var_others/default7_centralized_2025-03-27_01-10-32',
#                    './datasets/var/default7.jrl',
#                    './saved_output')
# default8 = Results('./input/var_others/default8_centralized_2025-03-27_01-10-36',
#                    './datasets/var/default8.jrl',
#                    './saved_output')
# default9 = Results('./input/var_others/default9_centralized_2025-03-27_01-10-44',
#                    './datasets/var/default9.jrl',
#                    './saved_output')
# default10 = Results('./input/var_others/default10_centralized_2025-03-27_01-10-49',
#                     './datasets/var/default10.jrl',
#                     './saved_output')

mdsp = MultiDisplay()

# mdsp.add_results('ctr_odom1', ctr_odom1)
# mdsp.add_results('ctr_odom2', ctr_odom2)
# mdsp.add_results('ctr_odom3', ctr_odom3)
# mdsp.add_results('ctr_odom4', ctr_odom4)
# mdsp.add_results('ctr_odom5', ctr_odom5)

# mdsp.add_results('intra31', intra31)
# mdsp.add_results('intra32', intra32)
# mdsp.add_results('intra33', intra33)
# mdsp.add_results('intra34', intra34)
# mdsp.add_results('intra35', intra35)
# mdsp.add_results('intra36', intra36)
# mdsp.add_results('intra37', intra37)
# mdsp.add_results('intra38', intra38)
# mdsp.add_results('intra39', intra39)

mdsp.add_results('odom1', odom1)
mdsp.add_results('odom2', odom2)
mdsp.add_results('odom3', odom3)
mdsp.add_results('odom4', odom4)
mdsp.add_results('odom5', odom5)
mdsp.add_results('odom6', odom6)
mdsp.add_results('odom7', odom7)
mdsp.add_results('odom8', odom8)
mdsp.add_results('odom9', odom9)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

# mdsp.boxplot('transformation_ape')
# mdsp.boxplot('point_distance_ape')
# mdsp.boxplot('rot_angle_deg_ape')