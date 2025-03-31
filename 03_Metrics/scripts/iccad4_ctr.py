from results import Results
from display import Display, MultiDisplay
import numpy as np

# PYXIS - ODOMETRY #
# dis_odom1 = Results('./input/iccad3/odometry/odom1_geodesic-mesa_2025-03-26_21-14-31',
#                     './datasets/iccad3/odometry/odom1.jrl',
#                     './saved_output')
# dis_odom2 = Results('./input/iccad3/odometry/odom2_geodesic-mesa_2025-03-26_21-14-47',
#                     './datasets/iccad3/odometry/odom2.jrl',
#                     './saved_output')
# dis_odom3 = Results('./input/iccad3/odometry/odom3_geodesic-mesa_2025-03-26_21-15-26',
#                     './datasets/iccad3/odometry/odom3.jrl',
#                     './saved_output')
# dis_odom4 = Results('./input/iccad3/odometry/odom4_geodesic-mesa_2025-03-26_21-15-44',
#                     './datasets/iccad3/odometry/odom4.jrl',
#                     './saved_output')
# dis_odom5 = Results('./input/iccad3/odometry/odom5_geodesic-mesa_2025-03-26_21-16-17',
#                     './datasets/iccad3/odometry/odom5.jrl',
#                     './saved_output')

# PYXIS - LC INTRA #
# dis_lc_intra1 = Results('./input/iccad3/lc_intra/lc_intra1_geodesic-mesa_2025-03-26_21-25-02',
#                         './datasets/iccad3/lc_intra/lc_intra1.jrl',
#                         './saved_output')
# dis_lc_intra2 = Results('./input/iccad3/lc_intra/lc_intra2_geodesic-mesa_2025-03-26_21-25-15',
#                         './datasets/iccad3/lc_intra/lc_intra2.jrl',
#                         './saved_output')
# dis_lc_intra3 = Results('./input/iccad3/lc_intra/lc_intra3_geodesic-mesa_2025-03-26_21-25-31',
#                         './datasets/iccad3/lc_intra/lc_intra3.jrl',
#                         './saved_output')
# dis_lc_intra4 = Results('./input/iccad3/lc_intra/lc_intra4_geodesic-mesa_2025-03-26_21-25-48',
#                         './datasets/iccad3/lc_intra/lc_intra4.jrl',
#                         './saved_output')
# dis_lc_intra5 = Results('./input/iccad3/lc_intra/lc_intra5_geodesic-mesa_2025-03-26_21-26-01',
#                         './datasets/iccad3/lc_intra/lc_intra5.jrl',
#                         './saved_output')

# PYXIS - LC INTER Indirect #
ctr_lc_indirect1 = Results('./input/iccad_4/lc_indirect/lc_indirect1_centralized_2025-03-31_12-32-33',
                           './datasets/iccad_4/lc_indirect/lc_indirect1.jrl',
                           './saved_output')
ctr_lc_indirect2 = Results('./input/iccad_4/lc_indirect/lc_indirect2_centralized_2025-03-31_12-32-53',
                           './datasets/iccad_4/lc_indirect/lc_indirect2.jrl',
                           './saved_output')
ctr_lc_indirect3 = Results('./input/iccad_4/lc_indirect/lc_indirect3_centralized_2025-03-31_12-33-03',
                           './datasets/iccad_4/lc_indirect/lc_indirect3.jrl',
                           './saved_output')
ctr_lc_indirect4 = Results('./input/iccad_4/lc_indirect/lc_indirect4_centralized_2025-03-31_12-33-13',
                           './datasets/iccad_4/lc_indirect/lc_indirect4.jrl',
                           './saved_output')
ctr_lc_indirect5 = Results('./input/iccad_4/lc_indirect/lc_indirect5_centralized_2025-03-31_12-33-24',
                           './datasets/iccad_4/lc_indirect/lc_indirect5.jrl',
                           './saved_output')

# PYXIS - LC INTER Direct Pose #
# dis_lc_dir_pose10 = Results('./input/iccad3/lc_direct/pose/lc_dir_pose10_geodesic-mesa_2025-03-26_21-30-09',
#                             './datasets/iccad3/lc_direct/pose/lc_dir_pose10.jrl',
#                             './saved_output')
# dis_lc_dir_pose20 = Results('./input/iccad3/lc_direct/pose/lc_dir_pose20_geodesic-mesa_2025-03-26_21-30-22',
#                             './datasets/iccad3/lc_direct/pose/lc_dir_pose20.jrl',
#                             './saved_output')
# dis_lc_dir_pose30 = Results('./input/iccad3/lc_direct/pose/lc_dir_pose30_geodesic-mesa_2025-03-26_21-30-46',
#                             './datasets/iccad3/lc_direct/pose/lc_dir_pose30.jrl',
#                             './saved_output')
# dis_lc_dir_pose40 = Results('./input/iccad3/lc_direct/pose/lc_dir_pose40_geodesic-mesa_2025-03-26_21-31-14',
#                             './datasets/iccad3/lc_direct/pose/lc_dir_pose40.jrl',
#                             './saved_output')
# dis_lc_dir_pose50 = Results('./input/iccad3/lc_direct/pose/lc_dir_pose50_geodesic-mesa_2025-03-26_21-31-27',
#                             './datasets/iccad3/lc_direct/pose/lc_dir_pose50.jrl',
#                             './saved_output')

# PYXIS - LC INTER Direct Range #
# dis_lc_dir_range10 = Results('./input/iccad3/lc_direct/range/lc_dir_range10_geodesic-mesa_2025-03-26_21-33-03',
#                              './datasets/iccad3/lc_direct/range/lc_dir_range10.jrl',
#                              './saved_output')
# dis_lc_dir_range20 = Results('./input/iccad3/lc_direct/range/lc_dir_range20_geodesic-mesa_2025-03-26_21-33-36',
#                              './datasets/iccad3/lc_direct/range/lc_dir_range20.jrl',
#                              './saved_output')
# dis_lc_dir_range30 = Results('./input/iccad3/lc_direct/range/lc_dir_range30_geodesic-mesa_2025-03-26_21-33-51',
#                              './datasets/iccad3/lc_direct/range/lc_dir_range30.jrl',
#                              './saved_output')
# dis_lc_dir_range40 = Results('./input/iccad3/lc_direct/range/lc_dir_range40_geodesic-mesa_2025-03-26_21-34-08',
#                              './datasets/iccad3/lc_direct/range/lc_dir_range40.jrl',
#                              './saved_output')
# dis_lc_dir_range50 = Results('./input/iccad3/lc_direct/range/lc_dir_range50_geodesic-mesa_2025-03-26_21-34-23',
#                              './datasets/iccad3/lc_direct/range/lc_dir_range50.jrl',
#                              './saved_output')

# PYXIS - LANDMARKS #
# dis_lks_20 = Results('./input/iccad3/landmarks/lks_20_geodesic-mesa_2025-03-26_21-01-26',
#                      './datasets/iccad3/landmarks/lks_20.jrl',
#                      './saved_output')
# dis_lks_40 = Results('./input/iccad3/landmarks/lks_40_geodesic-mesa_2025-03-26_21-01-46',
#                      './datasets/iccad3/landmarks/lks_40.jrl',
#                      './saved_output')
# dis_lks_60 = Results('./input/iccad3/landmarks/lks_60_geodesic-mesa_2025-03-26_21-36-39',
#                      './datasets/iccad3/landmarks/lks_60.jrl',
#                      './saved_output')
# dis_lks_80 = Results('./input/iccad3/landmarks/lks_80_geodesic-mesa_2025-03-26_21-36-54',
#                      './datasets/iccad3/landmarks/lks_80.jrl',
#                      './saved_output')
# dis_lks_100 = Results('./input/iccad3/landmarks/lks_100_geodesic-mesa_2025-03-26_21-37-22',
#                       './datasets/iccad3/landmarks/lks_100.jrl',
#                       './saved_output')

# PYXIS - No Landmarks #
# dis_default = Results('./input/iccad3/default_geodesic-mesa_2025-03-24_21-36-39',
#                       './datasets/iccad3/default.jrl',
#                       './saved_output')
# dis_nolk = Results('./input/iccad3/no_lk_geodesic-mesa_2025-03-24_21-37-15',
#                    './datasets/iccad3/no_lk.jrl',
#                    './saved_output')

# Independent #

# Centralized #
mdsp = MultiDisplay()

# mdsp.add_results('dis_odom1', dis_odom1)
# mdsp.add_results('dis_odom2', dis_odom2)
# mdsp.add_results('dis_odom3', dis_odom3)
# mdsp.add_results('dis_odom4', dis_odom4)
# mdsp.add_results('dis_odom5', dis_odom5)

# mdsp.add_results('dis_lc_intra1', dis_lc_intra1)
# mdsp.add_results('dis_lc_intra2', dis_lc_intra2)
# mdsp.add_results('dis_lc_intra3', dis_lc_intra3)
# mdsp.add_results('dis_lc_intra4', dis_lc_intra4)
# mdsp.add_results('dis_lc_intra5', dis_lc_intra5)

mdsp.add_results('ctr_lc_indirect1', ctr_lc_indirect1)
mdsp.add_results('ctr_lc_indirect2', ctr_lc_indirect2)
mdsp.add_results('ctr_lc_indirect3', ctr_lc_indirect3)
mdsp.add_results('ctr_lc_indirect4', ctr_lc_indirect4)
mdsp.add_results('ctr_lc_indirect5', ctr_lc_indirect5)

# mdsp.add_results('dis_lc_dir_pose10', dis_lc_dir_pose10)
# mdsp.add_results('dis_lc_dir_pose20', dis_lc_dir_pose20)
# mdsp.add_results('dis_lc_dir_pose30', dis_lc_dir_pose30)
# mdsp.add_results('dis_lc_dir_pose40', dis_lc_dir_pose40)
# mdsp.add_results('dis_lc_dir_pose50', dis_lc_dir_pose50)

# mdsp.add_results('dis_lc_dir_range10', dis_lc_dir_range10)
# mdsp.add_results('dis_lc_dir_range20', dis_lc_dir_range20)
# mdsp.add_results('dis_lc_dir_range30', dis_lc_dir_range30)
# mdsp.add_results('dis_lc_dir_range40', dis_lc_dir_range40)
# mdsp.add_results('dis_lc_dir_range50', dis_lc_dir_range50)

# mdsp.add_results('dis_lc_dir_pose10', dis_lc_dir_pose10)
# mdsp.add_results('dis_lc_dir_range10', dis_lc_dir_range10)
# mdsp.add_results('dis_lc_dir_pose20', dis_lc_dir_pose20)
# mdsp.add_results('dis_lc_dir_range20', dis_lc_dir_range20)
# mdsp.add_results('dis_lc_dir_pose30', dis_lc_dir_pose30)
# mdsp.add_results('dis_lc_dir_range30', dis_lc_dir_range30)
# mdsp.add_results('dis_lc_dir_pose40', dis_lc_dir_pose40)
# mdsp.add_results('dis_lc_dir_range40', dis_lc_dir_range40)
# mdsp.add_results('dis_lc_dir_pose50', dis_lc_dir_pose50)
# mdsp.add_results('dis_lc_dir_range50', dis_lc_dir_range50)

# mdsp.add_results('dis_lks_20', dis_lks_20)
# mdsp.add_results('dis_lks_40', dis_lks_40)
# mdsp.add_results('dis_lks_60', dis_lks_60)
# mdsp.add_results('dis_lks_80', dis_lks_80)
# mdsp.add_results('dis_lks_100', dis_lks_100)

# mdsp.add_results('dis_default1', dis_default1)
# mdsp.add_results('dis_default2', dis_default2)
# mdsp.add_results('dis_nolk1', dis_nolk1)
# mdsp.add_results('dis_nolk2', dis_nolk2)
# mdsp.add_results('dis_nolk3', dis_nolk3)
# mdsp.add_results('dis_nolk4', dis_nolk4)
# mdsp.add_results('dis_nolk5', dis_nolk5)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

mdsp.boxplot('transformation_ape')
mdsp.boxplot('point_distance_ape')
mdsp.boxplot('rot_angle_deg_ape')