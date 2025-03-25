from results import Results
from display import Display, MultiDisplay
import numpy as np



# PYXIS - ODOMETRY #
# dis_odom1 = Results('./input/iccad2/odometry/odom1_geodesic-mesa_2025-03-24_18-19-25',
#                     './datasets/iccad2/odometry/odom1.jrl',
#                     './saved_output')
# dis_odom2 = Results('./input/iccad2/odometry/odom2_geodesic-mesa_2025-03-24_18-19-40',
#                     './datasets/iccad2/odometry/odom2.jrl',
#                     './saved_output')
# dis_odom3 = Results('./input/iccad2/odometry/odom3_geodesic-mesa_2025-03-24_18-19-51',
#                     './datasets/iccad2/odometry/odom3.jrl',
#                     './saved_output')
# dis_odom4 = Results('./input/iccad2/odometry/odom4_geodesic-mesa_2025-03-24_18-20-07',
#                     './datasets/iccad2/odometry/odom4.jrl',
#                     './saved_output')
# dis_odom5 = Results('./input/iccad2/odometry/odom5_geodesic-mesa_2025-03-24_18-21-26',
#                     './datasets/iccad2/odometry/odom5.jrl',
#                     './saved_output')

# PYXIS - LC INTRA #
# dis_lc_intra1 = Results('./input/iccad2/lc_intra/lc_intra1_geodesic-mesa_2025-03-24_18-13-07',
#                         './datasets/iccad2/lc_intra/lc_intra1.jrl',
#                         './saved_output')
# dis_lc_intra2 = Results('./input/iccad2/lc_intra/lc_intra2_geodesic-mesa_2025-03-24_18-13-29',
#                         './datasets/iccad2/lc_intra/lc_intra2.jrl',
#                         './saved_output')
# dis_lc_intra3 = Results('./input/iccad2/lc_intra/lc_intra3_geodesic-mesa_2025-03-24_18-14-28',
#                         './datasets/iccad2/lc_intra/lc_intra3.jrl',
#                         './saved_output')
# dis_lc_intra4 = Results('./input/iccad2/lc_intra/lc_intra4_geodesic-mesa_2025-03-24_18-14-45',
#                         './datasets/iccad2/lc_intra/lc_intra4.jrl',
#                         './saved_output')
# dis_lc_intra5 = Results('./input/iccad2/lc_intra/lc_intra5_geodesic-mesa_2025-03-24_18-15-00',
#                         './datasets/iccad2/lc_intra/lc_intra5.jrl',
#                         './saved_output')

# PYXIS - LC INTER Indirect #
# dis_lc_indirect1 = Results('./input/iccad2/lc_indirect/lc_indirect1_geodesic-mesa_2025-03-24_18-10-29',
#                            './datasets/iccad2/lc_indirect/lc_indirect1.jrl',
#                            './saved_output')
# dis_lc_indirect2 = Results('./input/iccad2/lc_indirect/lc_indirect2_geodesic-mesa_2025-03-24_18-10-45',
#                            './datasets/iccad2/lc_indirect/lc_indirect2.jrl',
#                            './saved_output')
# dis_lc_indirect3 = Results('./input/iccad2/lc_indirect/lc_indirect3_geodesic-mesa_2025-03-24_18-11-37',
#                            './datasets/iccad2/lc_indirect/lc_indirect3.jrl',
#                            './saved_output')
# dis_lc_indirect4 = Results('./input/iccad2/lc_indirect/lc_indirect4_geodesic-mesa_2025-03-24_18-11-56',
#                            './datasets/iccad2/lc_indirect/lc_indirect4.jrl',
#                            './saved_output')
# dis_lc_indirect5 = Results('./input/iccad2/lc_indirect/lc_indirect5_geodesic-mesa_2025-03-24_18-12-21',
#                            './datasets/iccad2/lc_indirect/lc_indirect5.jrl',
#                            './saved_output')

# PYXIS - LC INTER Direct Pose #
# dis_lc_dir_pose10 = Results('./input/iccad2/lc_direct/pose/lc_dir_pose10_geodesic-mesa_2025-03-24_18-02-11',
#                             './datasets/iccad2/lc_direct/pose/lc_dir_pose10.jrl',
#                             './saved_output')
# dis_lc_dir_pose20 = Results('./input/iccad2/lc_direct/pose/lc_dir_pose20_geodesic-mesa_2025-03-24_18-02-26',
#                             './datasets/iccad2/lc_direct/pose/lc_dir_pose20.jrl',
#                             './saved_output')
# dis_lc_dir_pose30 = Results('./input/iccad2/lc_direct/pose/lc_dir_pose30_geodesic-mesa_2025-03-24_18-03-03',
#                             './datasets/iccad2/lc_direct/pose/lc_dir_pose30.jrl',
#                             './saved_output')
# dis_lc_dir_pose40 = Results('./input/iccad2/lc_direct/pose/lc_dir_pose40_geodesic-mesa_2025-03-24_18-03-17',
#                             './datasets/iccad2/lc_direct/pose/lc_dir_pose40.jrl',
#                             './saved_output')
# dis_lc_dir_pose50 = Results('./input/iccad2/lc_direct/pose/lc_dir_pose50_geodesic-mesa_2025-03-24_18-03-29',
#                             './datasets/iccad2/lc_direct/pose/lc_dir_pose50.jrl',
#                             './saved_output')

# PYXIS - LC INTER Direct Range #
# dis_lc_dir_range10 = Results('./input/iccad2/lc_direct/range/lc_dir_range10_geodesic-mesa_2025-03-24_18-05-54',
#                              './datasets/iccad2/lc_direct/range/lc_dir_range10.jrl',
#                              './saved_output')
# dis_lc_dir_range20 = Results('./input/iccad2/lc_direct/range/lc_dir_range20_geodesic-mesa_2025-03-24_18-06-30',
#                              './datasets/iccad2/lc_direct/range/lc_dir_range20.jrl',
#                              './saved_output')
# dis_lc_dir_range30 = Results('./input/iccad2/lc_direct/range/lc_dir_range30_geodesic-mesa_2025-03-24_18-06-53',
#                              './datasets/iccad2/lc_direct/range/lc_dir_range30.jrl',
#                              './saved_output')
# dis_lc_dir_range40 = Results('./input/iccad2/lc_direct/range/lc_dir_range40_geodesic-mesa_2025-03-24_18-07-14',
#                              './datasets/iccad2/lc_direct/range/lc_dir_range40.jrl',
#                              './saved_output')
# dis_lc_dir_range50 = Results('./input/iccad2/lc_direct/range/lc_dir_range50_geodesic-mesa_2025-03-24_18-07-31',
#                              './datasets/iccad2/lc_direct/range/lc_dir_range50.jrl',
#                              './saved_output')

# PYXIS - LANDMARKS #
# dis_lks_20 = Results('./input/iccad2/landmarks/lks_20_geodesic-mesa_2025-03-24_17-53-40',
#                      './datasets/iccad2/landmarks/lks_20.jrl',
#                      './saved_output')
# dis_lks_40 = Results('./input/iccad2/landmarks/lks_40_geodesic-mesa_2025-03-24_17-54-01',
#                      './datasets/iccad2/landmarks/lks_40.jrl',
#                      './saved_output')
# dis_lks_60 = Results('./input/iccad2/landmarks/lks_60_geodesic-mesa_2025-03-24_17-54-18',
#                      './datasets/iccad2/landmarks/lks_60.jrl',
#                      './saved_output')
# dis_lks_80 = Results('./input/iccad2/landmarks/lks_80_geodesic-mesa_2025-03-24_17-55-48',
#                      './datasets/iccad2/landmarks/lks_80.jrl',
#                      './saved_output')
# dis_lks_100 = Results('./input/iccad2/landmarks/lks_100_geodesic-mesa_2025-03-24_17-56-06',
#                       './datasets/iccad2/landmarks/lks_100.jrl',
#                       './saved_output')

# PYXIS - No Landmarks #
dis_default1 = Results('./input/iccad2/default_geodesic-mesa_2025-03-24_21-36-39',
                       './datasets/iccad2/default.jrl',
                       './saved_output')
dis_default2 = Results('./input/iccad2/default_geodesic-mesa_2025-03-24_21-36-50',
                       './datasets/iccad2/default.jrl',
                       './saved_output')
dis_nolk1 = Results('./input/iccad2/no_lk_geodesic-mesa_2025-03-24_21-37-15',
                    './datasets/iccad2/no_lk.jrl',
                    './saved_output')
dis_nolk2 = Results('./input/iccad2/no_lk_geodesic-mesa_2025-03-24_21-37-21',
                    './datasets/iccad2/no_lk.jrl',
                    './saved_output')
dis_nolk3 = Results('./input/iccad2/no_lk_geodesic-mesa_2025-03-24_21-38-50',
                    './datasets/iccad2/no_lk.jrl',
                    './saved_output')
dis_nolk4 = Results('./input/iccad2/no_lk_geodesic-mesa_2025-03-24_21-38-58',
                    './datasets/iccad2/no_lk.jrl',
                    './saved_output')
dis_nolk5 = Results('./input/iccad2/no_lk_geodesic-mesa_2025-03-24_21-39-03',
                    './datasets/iccad2/no_lk.jrl',
                    './saved_output')

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

# mdsp.add_results('dis_lc_indirect1', dis_lc_indirect1)
# mdsp.add_results('dis_lc_indirect2', dis_lc_indirect2)
# mdsp.add_results('dis_lc_indirect3', dis_lc_indirect3)
# mdsp.add_results('dis_lc_indirect4', dis_lc_indirect4)
# mdsp.add_results('dis_lc_indirect5', dis_lc_indirect5)

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

# mdsp.add_results('dis_lks_20', dis_lks_20)
# mdsp.add_results('dis_lks_40', dis_lks_40)
# mdsp.add_results('dis_lks_60', dis_lks_60)
# mdsp.add_results('dis_lks_80', dis_lks_80)
# mdsp.add_results('dis_lks_100', dis_lks_100)

mdsp.add_results('dis_default1', dis_default1)
mdsp.add_results('dis_default2', dis_default2)
mdsp.add_results('dis_nolk1', dis_nolk1)
mdsp.add_results('dis_nolk2', dis_nolk2)
mdsp.add_results('dis_nolk3', dis_nolk3)
mdsp.add_results('dis_nolk4', dis_nolk4)
mdsp.add_results('dis_nolk5', dis_nolk5)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

# mdsp.boxplot('transformation_ape')
# mdsp.boxplot('point_distance_ape')
# mdsp.boxplot('rot_angle_deg_ape')