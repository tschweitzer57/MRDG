from results import Results
from display import Display, MultiDisplay
import numpy as np

# CENTRALIZED - DEFAULT #
default1 = Results('./input/var_others/default1_centralized_2025-03-27_01-09-58',
                   './datasets/var/default1.jrl',
                   './saved_output')
default2 = Results('./input/var_others/default2_centralized_2025-03-27_01-10-03',
                   './datasets/var/default2.jrl',
                   './saved_output')
default3 = Results('./input/var_others/default3_centralized_2025-03-27_01-10-08',
                   './datasets/var/default3.jrl',
                   './saved_output')
default4 = Results('./input/var_others/default4_centralized_2025-03-27_01-10-13',
                   './datasets/var/default4.jrl',
                   './saved_output')
default5 = Results('./input/var_others/default5_centralized_2025-03-27_01-10-17',
                   './datasets/var/default5.jrl',
                   './saved_output')
default6 = Results('./input/var_others/default6_centralized_2025-03-27_01-10-23',
                   './datasets/var/default6.jrl',
                   './saved_output')
default7 = Results('./input/var_others/default7_centralized_2025-03-27_01-10-32',
                   './datasets/var/default7.jrl',
                   './saved_output')
default8 = Results('./input/var_others/default8_centralized_2025-03-27_01-10-36',
                   './datasets/var/default8.jrl',
                   './saved_output')
default9 = Results('./input/var_others/default9_centralized_2025-03-27_01-10-44',
                   './datasets/var/default9.jrl',
                   './saved_output')
default10 = Results('./input/var_others/default10_centralized_2025-03-27_01-10-49',
                    './datasets/var/default10.jrl',
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

mdsp.add_results('default1', default1)
mdsp.add_results('default2', default2)
mdsp.add_results('default3', default3)
mdsp.add_results('default4', default4)
mdsp.add_results('default5', default5)
mdsp.add_results('default6', default6)
mdsp.add_results('default7', default7)
mdsp.add_results('default8', default8)
mdsp.add_results('default9', default9)
mdsp.add_results('default10', default10)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

# mdsp.boxplot('transformation_ape')
# mdsp.boxplot('point_distance_ape')
# mdsp.boxplot('rot_angle_deg_ape')