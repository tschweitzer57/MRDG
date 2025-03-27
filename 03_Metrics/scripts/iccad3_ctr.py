from results import Results
from display import Display, MultiDisplay
import numpy as np



# CENTRALIZED - ODOMETRY #
# ctr_odom1 = Results('./input/iccad3_others/odometry/odom1_centralized_2025-03-26_20-45-02',
#                     './datasets/iccad3/odometry/odom1.jrl',
#                     './saved_output')
# ctr_odom2 = Results('./input/iccad3_others/odometry/odom2_centralized_2025-03-26_20-45-07',
#                     './datasets/iccad3/odometry/odom2.jrl',
#                     './saved_output')
# ctr_odom3 = Results('./input/iccad3_others/odometry/odom3_centralized_2025-03-26_20-45-13',
#                     './datasets/iccad3/odometry/odom3.jrl',
#                     './saved_output')
# ctr_odom4 = Results('./input/iccad3_others/odometry/odom4_centralized_2025-03-26_20-45-19',
#                     './datasets/iccad3/odometry/odom4.jrl',
#                     './saved_output')
# ctr_odom5 = Results('./input/iccad3_others/odometry/odom5_centralized_2025-03-26_20-45-24',
#                     './datasets/iccad3/odometry/odom5.jrl',
#                     './saved_output')

# CENTRALIZED - LC INTRA #
ctr_lc_intra1 = Results('./input/iccad3_others/lc_intra/lc_intra1_centralized_2025-03-26_20-43-38',
                        './datasets/iccad3/lc_intra/lc_intra1.jrl',
                        './saved_output')
ctr_lc_intra2 = Results('./input/iccad3_others/lc_intra/lc_intra2_centralized_2025-03-26_20-43-44',
                        './datasets/iccad3/lc_intra/lc_intra2.jrl',
                        './saved_output')
ctr_lc_intra3 = Results('./input/iccad3_others/lc_intra/lc_intra3_centralized_2025-03-26_20-43-54',
                        './datasets/iccad3/lc_intra/lc_intra3.jrl',
                        './saved_output')
ctr_lc_intra4 = Results('./input/iccad3_others/lc_intra/lc_intra4_centralized_2025-03-26_20-44-01',
                        './datasets/iccad3/lc_intra/lc_intra4.jrl',
                        './saved_output')
ctr_lc_intra5 = Results('./input/iccad3_others/lc_intra/lc_intra5_centralized_2025-03-26_20-44-07',
                        './datasets/iccad3/lc_intra/lc_intra5.jrl',
                        './saved_output')

# CENTRALIZED - LC INTER Indirect #
# ctr_lc_indirect1 = Results('./input/iccad3_others/lc_indirect/lc_indirect1_centralized_2025-03-24_17-15-57',
#                            './datasets/iccad3/lc_indirect/lc_indirect1.jrl',
#                            './saved_output')
# ctr_lc_indirect2 = Results('./input/iccad3_others/lc_indirect/lc_indirect2_centralized_2025-03-24_17-16-05',
#                            './datasets/iccad3/lc_indirect/lc_indirect2.jrl',
#                            './saved_output')
# ctr_lc_indirect3 = Results('./input/iccad3_others/lc_indirect/lc_indirect3_centralized_2025-03-24_17-16-13',
#                            './datasets/iccad3/lc_indirect/lc_indirect3.jrl',
#                            './saved_output')
# ctr_lc_indirect4 = Results('./input/iccad3_others/lc_indirect/lc_indirect4_centralized_2025-03-24_17-16-18',
#                            './datasets/iccad3/lc_indirect/lc_indirect4.jrl',
#                            './saved_output')
# ctr_lc_indirect5 = Results('./input/iccad3_others/lc_indirect/lc_indirect5_centralized_2025-03-24_17-16-24',
#                            './datasets/iccad3/lc_indirect/lc_indirect5.jrl',
#                            './saved_output')

# CENTRALIZED - LC INTER Direct Pose #
# ctr_lc_dir_pose10 = Results('./input/iccad3/lc_direct/pose/lc_dir_pose10_geodesic-mesa_2025-03-24_18-02-11',
#                             './datasets/iccad3/lc_direct/pose/lc_dir_pose10.jrl',
#                             './saved_output')
# ctr_lc_dir_pose20 = Results('./input/iccad3/lc_direct/pose/lc_dir_pose20_geodesic-mesa_2025-03-24_18-02-26',
#                             './datasets/iccad3/lc_direct/pose/lc_dir_pose20.jrl',
#                             './saved_output')
# ctr_lc_dir_pose30 = Results('./input/iccad3/lc_direct/pose/lc_dir_pose30_geodesic-mesa_2025-03-24_18-03-03',
#                             './datasets/iccad3/lc_direct/pose/lc_dir_pose30.jrl',
#                             './saved_output')
# ctr_lc_dir_pose40 = Results('./input/iccad3/lc_direct/pose/lc_dir_pose40_geodesic-mesa_2025-03-24_18-03-17',
#                             './datasets/iccad3/lc_direct/pose/lc_dir_pose40.jrl',
#                             './saved_output')
# ctr_lc_dir_pose50 = Results('./input/iccad3/lc_direct/pose/lc_dir_pose50_geodesic-mesa_2025-03-24_18-03-29',
#                             './datasets/iccad3/lc_direct/pose/lc_dir_pose50.jrl',
#                             './saved_output')

# CENTRALIZED - LC INTER Direct Range #
# ctr_lc_dir_range10 = Results('./input/iccad3/lc_direct/range/lc_dir_range10_geodesic-mesa_2025-03-24_18-05-54',
#                              './datasets/iccad3/lc_direct/range/lc_dir_range10.jrl',
#                              './saved_output')
# ctr_lc_dir_range20 = Results('./input/iccad3/lc_direct/range/lc_dir_range20_geodesic-mesa_2025-03-24_18-06-30',
#                              './datasets/iccad3/lc_direct/range/lc_dir_range20.jrl',
#                              './saved_output')
# ctr_lc_dir_range30 = Results('./input/iccad3/lc_direct/range/lc_dir_range30_geodesic-mesa_2025-03-24_18-06-53',
#                              './datasets/iccad3/lc_direct/range/lc_dir_range30.jrl',
#                              './saved_output')
# ctr_lc_dir_range40 = Results('./input/iccad3/lc_direct/range/lc_dir_range40_geodesic-mesa_2025-03-24_18-07-14',
#                              './datasets/iccad3/lc_direct/range/lc_dir_range40.jrl',
#                              './saved_output')
# ctr_lc_dir_range50 = Results('./input/iccad3/lc_direct/range/lc_dir_range50_geodesic-mesa_2025-03-24_18-07-31',
#                              './datasets/iccad3/lc_direct/range/lc_dir_range50.jrl',
#                              './saved_output')

# CENTRALIZED - LANDMARKS #
# ctr_lks_20 = Results('./input/iccad3/landmarks/lks_20_geodesic-mesa_2025-03-24_17-53-40',
#                      './datasets/iccad3/landmarks/lks_20.jrl',
#                      './saved_output')
# ctr_lks_40 = Results('./input/iccad3/landmarks/lks_40_geodesic-mesa_2025-03-24_17-54-01',
#                      './datasets/iccad3/landmarks/lks_40.jrl',
#                      './saved_output')
# ctr_lks_60 = Results('./input/iccad3/landmarks/lks_60_geodesic-mesa_2025-03-24_17-54-18',
#                      './datasets/iccad3/landmarks/lks_60.jrl',
#                      './saved_output')
# ctr_lks_80 = Results('./input/iccad3/landmarks/lks_80_geodesic-mesa_2025-03-24_17-55-48',
#                      './datasets/iccad3/landmarks/lks_80.jrl',
#                      './saved_output')
# ctr_lks_100 = Results('./input/iccad3/landmarks/lks_100_geodesic-mesa_2025-03-24_17-56-06',
#                       './datasets/iccad3/landmarks/lks_100.jrl',
#                       './saved_output')

# CENTRALIZED - No Landmarks #
# ctr_default1 = Results('./input/iccad3/default_geodesic-mesa_2025-03-24_21-36-39',
#                        './datasets/iccad3/default.jrl',
#                        './saved_output')
# ctr_default2 = Results('./input/iccad3/default_geodesic-mesa_2025-03-24_21-36-50',
#                        './datasets/iccad3/default.jrl',
#                        './saved_output')
# ctr_nolk1 = Results('./input/iccad3/no_lk_geodesic-mesa_2025-03-24_21-37-15',
#                     './datasets/iccad3/no_lk.jrl',
#                     './saved_output')
# ctr_nolk2 = Results('./input/iccad3/no_lk_geodesic-mesa_2025-03-24_21-37-21',
#                     './datasets/iccad3/no_lk.jrl',
#                     './saved_output')
# ctr_nolk3 = Results('./input/iccad3/no_lk_geodesic-mesa_2025-03-24_21-38-50',
#                     './datasets/iccad3/no_lk.jrl',
#                     './saved_output')
# ctr_nolk4 = Results('./input/iccad3/no_lk_geodesic-mesa_2025-03-24_21-38-58',
#                     './datasets/iccad3/no_lk.jrl',
#                     './saved_output')
# ctr_nolk5 = Results('./input/iccad3/no_lk_geodesic-mesa_2025-03-24_21-39-03',
#                     './datasets/iccad3/no_lk.jrl',
#                     './saved_output')

# Independent #

# Centralized #
mdsp = MultiDisplay()

# mdsp.add_results('ctr_odom1', ctr_odom1)
# mdsp.add_results('ctr_odom2', ctr_odom2)
# mdsp.add_results('ctr_odom3', ctr_odom3)
# mdsp.add_results('ctr_odom4', ctr_odom4)
# mdsp.add_results('ctr_odom5', ctr_odom5)

mdsp.add_results('ctr_lc_intra1', ctr_lc_intra1)
mdsp.add_results('ctr_lc_intra2', ctr_lc_intra2)
mdsp.add_results('ctr_lc_intra3', ctr_lc_intra3)
mdsp.add_results('ctr_lc_intra4', ctr_lc_intra4)
mdsp.add_results('ctr_lc_intra5', ctr_lc_intra5)

# mdsp.add_results('ctr_lc_indirect1', ctr_lc_indirect1)
# mdsp.add_results('ctr_lc_indirect2', ctr_lc_indirect2)
# mdsp.add_results('ctr_lc_indirect3', ctr_lc_indirect3)
# mdsp.add_results('ctr_lc_indirect4', ctr_lc_indirect4)
# mdsp.add_results('ctr_lc_indirect5', ctr_lc_indirect5)

# mdsp.add_results('ctr_lc_dir_pose10', ctr_lc_dir_pose10)
# mdsp.add_results('ctr_lc_dir_pose20', ctr_lc_dir_pose20)
# mdsp.add_results('ctr_lc_dir_pose30', ctr_lc_dir_pose30)
# mdsp.add_results('ctr_lc_dir_pose40', ctr_lc_dir_pose40)
# mdsp.add_results('ctr_lc_dir_pose50', ctr_lc_dir_pose50)

# mdsp.add_results('ctr_lc_dir_range10', ctr_lc_dir_range10)
# mdsp.add_results('ctr_lc_dir_range20', ctr_lc_dir_range20)
# mdsp.add_results('ctr_lc_dir_range30', ctr_lc_dir_range30)
# mdsp.add_results('ctr_lc_dir_range40', ctr_lc_dir_range40)
# mdsp.add_results('ctr_lc_dir_range50', ctr_lc_dir_range50)

# mdsp.add_results('ctr_lks_20', ctr_lks_20)
# mdsp.add_results('ctr_lks_40', ctr_lks_40)
# mdsp.add_results('ctr_lks_60', ctr_lks_60)
# mdsp.add_results('ctr_lks_80', ctr_lks_80)
# mdsp.add_results('ctr_lks_100', ctr_lks_100)

# mdsp.add_results('ctr_default1', ctr_default1)
# mdsp.add_results('ctr_default2', ctr_default2)
# mdsp.add_results('ctr_nolk1', ctr_nolk1)
# mdsp.add_results('ctr_nolk2', ctr_nolk2)
# mdsp.add_results('ctr_nolk3', ctr_nolk3)
# mdsp.add_results('ctr_nolk4', ctr_nolk4)
# mdsp.add_results('ctr_nolk5', ctr_nolk5)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

# mdsp.boxplot('transformation_ape')
# mdsp.boxplot('point_distance_ape')
# mdsp.boxplot('rot_angle_deg_ape')