from results import Results
from display import Display, MultiDisplay
import numpy as np

# PYXIS - ODOMETRY #
# ctr_odom1 = Results('./input/iccad_4_ctr/odometry/odom1_centralized_2025-04-02_09-18-37',
#                     './datasets/iccad_4/odometry/odom1.jrl',
#                     './saved_output')
# ctr_odom2 = Results('./input/iccad_4_ctr/odometry/odom2_centralized_2025-04-02_09-18-42',
#                     './datasets/iccad_4/odometry/odom2.jrl',
#                     './saved_output')
# ctr_odom3 = Results('./input/iccad_4_ctr/odometry/odom3_centralized_2025-04-02_09-18-47',
#                     './datasets/iccad_4/odometry/odom3.jrl',
#                     './saved_output')
# ctr_odom4 = Results('./input/iccad_4_ctr/odometry/odom4_centralized_2025-04-02_09-18-53',
#                     './datasets/iccad_4/odometry/odom4.jrl',
#                     './saved_output')
# ctr_odom5 = Results('./input/iccad_4_ctr/odometry/odom5_centralized_2025-04-02_09-19-01',
#                     './datasets/iccad_4/odometry/odom5.jrl',
#                     './saved_output')

# PYXIS - LC INTRA #
# ctr_lc_intra1 = Results('./input/iccad_4_ctr/lc_intra/lc_intra1_centralized_2025-04-02_09-03-23',
#                         './datasets/iccad_4/lc_intra/lc_intra1.jrl',
#                         './saved_output')
# ctr_lc_intra2 = Results('./input/iccad_4_ctr/lc_intra/lc_intra2_centralized_2025-04-02_09-03-39',
#                         './datasets/iccad_4/lc_intra/lc_intra2.jrl',
#                         './saved_output')
# ctr_lc_intra3 = Results('./input/iccad_4_ctr/lc_intra/lc_intra3_centralized_2025-04-02_09-03-45',
#                         './datasets/iccad_4/lc_intra/lc_intra3.jrl',
#                         './saved_output')
# ctr_lc_intra4 = Results('./input/iccad_4_ctr/lc_intra/lc_intra4_centralized_2025-04-02_09-03-53',
#                         './datasets/iccad_4/lc_intra/lc_intra4.jrl',
#                         './saved_output')
# ctr_lc_intra5 = Results('./input/iccad_4_ctr/lc_intra/lc_intra5_centralized_2025-04-02_09-03-59',
#                         './datasets/iccad_4/lc_intra/lc_intra5.jrl',
#                         './saved_output')

# PYXIS - LC INTER Indirect #
# ctr_lc_indirect1 = Results('./input/iccad_4_ctr/lc_indirect/lc_indirect1_centralized_2025-03-31_12-32-33',
#                            './datasets/iccad_4/lc_indirect/lc_indirect1.jrl',
#                            './saved_output')
# ctr_lc_indirect2 = Results('./input/iccad_4_ctr/lc_indirect/lc_indirect2_centralized_2025-03-31_12-32-53',
#                            './datasets/iccad_4/lc_indirect/lc_indirect2.jrl',
#                            './saved_output')
# ctr_lc_indirect3 = Results('./input/iccad_4_ctr/lc_indirect/lc_indirect3_centralized_2025-03-31_12-33-03',
#                            './datasets/iccad_4/lc_indirect/lc_indirect3.jrl',
#                            './saved_output')
# ctr_lc_indirect4 = Results('./input/iccad_4_ctr/lc_indirect/lc_indirect4_centralized_2025-03-31_12-33-13',
#                            './datasets/iccad_4/lc_indirect/lc_indirect4.jrl',
#                            './saved_output')
# ctr_lc_indirect5 = Results('./input/iccad_4_ctr/lc_indirect/lc_indirect5_centralized_2025-03-31_12-33-24',
#                            './datasets/iccad_4/lc_indirect/lc_indirect5.jrl',
#                            './saved_output')

# PYXIS - LC INTER Direct Pose #
# ctr_lc_dir_pose10 = Results('./input/iccad_4_ctr/lc_direct/pose/lc_dir_pose10_centralized_2025-04-02_09-06-13',
#                             './datasets/iccad_4/lc_direct/pose/lc_dir_pose10.jrl',
#                             './saved_output')
# ctr_lc_dir_pose20 = Results('./input/iccad_4_ctr/lc_direct/pose/lc_dir_pose20_centralized_2025-04-02_09-06-19',
#                             './datasets/iccad_4/lc_direct/pose/lc_dir_pose20.jrl',
#                             './saved_output')
# ctr_lc_dir_pose30 = Results('./input/iccad_4_ctr/lc_direct/pose/lc_dir_pose30_centralized_2025-04-02_09-06-24',
#                             './datasets/iccad_4/lc_direct/pose/lc_dir_pose30.jrl',
#                             './saved_output')
# ctr_lc_dir_pose40 = Results('./input/iccad_4_ctr/lc_direct/pose/lc_dir_pose40_centralized_2025-04-02_09-06-31',
#                             './datasets/iccad_4/lc_direct/pose/lc_dir_pose40.jrl',
#                             './saved_output')
# ctr_lc_dir_pose50 = Results('./input/iccad_4_ctr/lc_direct/pose/lc_dir_pose50_centralized_2025-04-02_09-06-38',
#                             './datasets/iccad_4/lc_direct/pose/lc_dir_pose50.jrl',
#                             './saved_output')

# PYXIS - LC INTER Direct Range #
# ctr_lc_dir_range10 = Results('./input/iccad_4_ctr/lc_direct/range/lc_dir_range10_centralized_2025-04-02_09-07-21',
#                              './datasets/iccad_4/lc_direct/range/lc_dir_range10.jrl',
#                              './saved_output')
# ctr_lc_dir_range20 = Results('./input/iccad_4_ctr/lc_direct/range/lc_dir_range20_centralized_2025-04-02_09-07-27',
#                              './datasets/iccad_4/lc_direct/range/lc_dir_range20.jrl',
#                              './saved_output')
# ctr_lc_dir_range30 = Results('./input/iccad_4_ctr/lc_direct/range/lc_dir_range30_centralized_2025-04-02_09-07-34',
#                              './datasets/iccad_4/lc_direct/range/lc_dir_range30.jrl',
#                              './saved_output')
# ctr_lc_dir_range40 = Results('./input/iccad_4_ctr/lc_direct/range/lc_dir_range40_centralized_2025-04-02_09-07-39',
#                              './datasets/iccad_4/lc_direct/range/lc_dir_range40.jrl',
#                              './saved_output')
# ctr_lc_dir_range50 = Results('./input/iccad_4_ctr/lc_direct/range/lc_dir_range50_centralized_2025-04-02_09-07-44',
#                              './datasets/iccad_4/lc_direct/range/lc_dir_range50.jrl',
#                              './saved_output')

# PYXIS - LANDMARKS ALL #
# ctr_lksa_20 = Results('./input/iccad_4_ctr/lks_all/lks_20_centralized_2025-04-02_09-15-47',
#                       './datasets/iccad_4/lks_all/lks_20.jrl',
#                       './saved_output')
# ctr_lksa_40 = Results('./input/iccad_4_ctr/lks_all/lks_40_centralized_2025-04-02_09-15-54',
#                       './datasets/iccad_4/lks_all/lks_40.jrl',
#                       './saved_output')
# ctr_lksa_60 = Results('./input/iccad_4_ctr/lks_all/lks_60_centralized_2025-04-02_09-16-00',
#                       './datasets/iccad_4/lks_all/lks_60.jrl',
#                       './saved_output')
# ctr_lksa_80 = Results('./input/iccad_4_ctr/lks_all/lks_80_centralized_2025-04-02_09-16-05',
#                       './datasets/iccad_4/lks_all/lks_80.jrl',
#                       './saved_output')
# ctr_lksa_100 = Results('./input/iccad_4_ctr/lks_all/lks_100_centralized_2025-04-02_09-16-12',
#                        './datasets/iccad_4/lks_all/lks_100.jrl',
#                        './saved_output')

# PYXIS - LANDMARKS EDGES #
# ctr_lkse_20 = Results('./input/iccad_4_ctr/lks_edges/lks_20_centralized_2025-04-02_09-17-07',
#                       './datasets/iccad_4/lks_edges/lks_20.jrl',
#                       './saved_output')
# ctr_lkse_40 = Results('./input/iccad_4_ctr/lks_edges/lks_40_centralized_2025-04-02_09-17-01',
#                       './datasets/iccad_4/lks_edges/lks_40.jrl',
#                       './saved_output')
# ctr_lkse_60 = Results('./input/iccad_4_ctr/lks_edges/lks_60_centralized_2025-04-02_09-16-53',
#                       './datasets/iccad_4/lks_edges/lks_60.jrl',
#                       './saved_output')
# ctr_lkse_80 = Results('./input/iccad_4_ctr/lks_edges/lks_80_centralized_2025-04-02_09-16-46',
#                       './datasets/iccad_4/lks_edges/lks_80.jrl',
#                       './saved_output')
# ctr_lkse_100 = Results('./input/iccad_4_ctr/lks_edges/lks_100_centralized_2025-04-02_09-16-38',
#                        './datasets/iccad_4/lks_edges/lks_100.jrl',
#                        './saved_output')



# PYXIS - No Landmarks #
ctr_default = Results('./input/iccad_4_ctr/default_centralized_2025-04-02_09-22-11',
                      './datasets/iccad_4/default.jrl',
                      './saved_output')
ctr_nolandmarks = Results('./input/iccad_4_ctr/no_lk_centralized_2025-04-02_09-22-02',
                          './datasets/iccad_4/no_lk.jrl',
                          './saved_output')


mdsp = MultiDisplay()

# mdsp.add_results('ctr_odom1', ctr_odom1)
# mdsp.add_results('ctr_odom2', ctr_odom2)
# mdsp.add_results('ctr_odom3', ctr_odom3)
# mdsp.add_results('ctr_odom4', ctr_odom4)
# mdsp.add_results('ctr_odom5', ctr_odom5)

# mdsp.add_results('ctr_lc_intra1', ctr_lc_intra1)
# mdsp.add_results('ctr_lc_intra2', ctr_lc_intra2)
# mdsp.add_results('ctr_lc_intra3', ctr_lc_intra3)
# mdsp.add_results('ctr_lc_intra4', ctr_lc_intra4)
# mdsp.add_results('ctr_lc_intra5', ctr_lc_intra5)

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

# mdsp.add_results('ctr_lc_dir_pose10', ctr_lc_dir_pose10)
# mdsp.add_results('ctr_lc_dir_range10', ctr_lc_dir_range10)
# mdsp.add_results('ctr_lc_dir_pose20', ctr_lc_dir_pose20)
# mdsp.add_results('ctr_lc_dir_range20', ctr_lc_dir_range20)
# mdsp.add_results('ctr_lc_dir_pose30', ctr_lc_dir_pose30)
# mdsp.add_results('ctr_lc_dir_range30', ctr_lc_dir_range30)
# mdsp.add_results('ctr_lc_dir_pose40', ctr_lc_dir_pose40)
# mdsp.add_results('ctr_lc_dir_range40', ctr_lc_dir_range40)
# mdsp.add_results('ctr_lc_dir_pose50', ctr_lc_dir_pose50)
# mdsp.add_results('ctr_lc_dir_range50', ctr_lc_dir_range50)

# mdsp.add_results('ctr_lksa_20', ctr_lksa_20)
# mdsp.add_results('ctr_lksa_40', ctr_lksa_40)
# mdsp.add_results('ctr_lksa_60', ctr_lksa_60)
# mdsp.add_results('ctr_lksa_80', ctr_lksa_80)
# mdsp.add_results('ctr_lksa_100', ctr_lksa_100)

# mdsp.add_results('ctr_lkse_20', ctr_lkse_20)
# mdsp.add_results('ctr_lkse_40', ctr_lkse_40)
# mdsp.add_results('ctr_lkse_60', ctr_lkse_60)
# mdsp.add_results('ctr_lkse_80', ctr_lkse_80)
# mdsp.add_results('ctr_lkse_100', ctr_lkse_100)

# mdsp.add_results('ctr_lkse_20', ctr_lkse_20)
# mdsp.add_results('ctr_lksa_20', ctr_lksa_20)
# mdsp.add_results('ctr_lkse_40', ctr_lkse_40)
# mdsp.add_results('ctr_lksa_40', ctr_lksa_40)
# mdsp.add_results('ctr_lkse_60', ctr_lkse_60)
# mdsp.add_results('ctr_lksa_60', ctr_lksa_60)
# mdsp.add_results('ctr_lkse_80', ctr_lkse_80)
# mdsp.add_results('ctr_lksa_80', ctr_lksa_80)
# mdsp.add_results('ctr_lkse_100', ctr_lkse_100)
# mdsp.add_results('ctr_lksa_100', ctr_lksa_100)

mdsp.add_results('ctr_default', ctr_default)
mdsp.add_results('ctr_nolandmarks', ctr_nolandmarks)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

mdsp.boxplot('transformation_ape')
mdsp.boxplot('point_distance_ape')
mdsp.boxplot('rot_angle_deg_ape')