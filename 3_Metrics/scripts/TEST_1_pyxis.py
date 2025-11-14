from results import Results
from display import Display, MultiDisplay
import numpy as np

init_opt = True

##########################################################################################################
###             Landmarks - Odom                                                                       ###
##########################################################################################################
# ctr_def_a1_o = Results('./input/TEST_1_pyxis/landmarks_odom/default_a1_o_geodesic-mesa_2025-04-11_08-34-29',
#                        './datasets/TEST_1/landmarks_odom/default_a1.jrl',
#                        './saved_output',
#                        iteration=12)
# ctr_def_a2_o = Results('./input/TEST_1_pyxis/landmarks_odom/default_a2_o_geodesic-mesa_2025-04-11_08-34-50',
#                        './datasets/TEST_1/landmarks_odom/default_a2.jrl',
#                        './saved_output',
#                        iteration=12)
# ctr_def_a3_o = Results('./input/TEST_1_pyxis/landmarks_odom/default_a3_o_geodesic-mesa_2025-04-11_08-35-35',
#                        './datasets/TEST_1/landmarks_odom/default_a3.jrl',
#                        './saved_output',
#                        iteration=12)
# ctr_def_e1_o = Results('./input/TEST_1_pyxis/landmarks_odom/default_e1_o_geodesic-mesa_2025-04-11_08-35-55',
#                        './datasets/TEST_1/landmarks_odom/default_e1.jrl',
#                        './saved_output',
#                        iteration=12)
# ctr_def_e2_o = Results('./input/TEST_1_pyxis/landmarks_odom/default_e2_o_geodesic-mesa_2025-04-11_08-36-15',
#                        './datasets/TEST_1/landmarks_odom/default_e2.jrl',
#                        './saved_output',
#                        iteration=12)
# ctr_def_e3_o = Results('./input/TEST_1_pyxis/landmarks_odom/default_e3_o_geodesic-mesa_2025-04-11_08-38-03',
#                        './datasets/TEST_1/landmarks_odom/default_e3.jrl',
#                        './saved_output',
#                        iteration=12)
# ctr_no_lk1_o = Results('./input/TEST_1_pyxis/landmarks_odom/no_lk1_o_geodesic-mesa_2025-04-11_08-41-07',
#                        './datasets/TEST_1/landmarks_odom/no_lk1.jrl',
#                        './saved_output',
#                        iteration=12)
# ctr_no_lk2_o = Results('./input/TEST_1_pyxis/landmarks_odom/no_lk2_o_geodesic-mesa_2025-04-11_08-41-16',
#                        './datasets/TEST_1/landmarks_odom/no_lk2.jrl',
#                        './saved_output',
#                        iteration=12)
# ctr_no_lk3_o = Results('./input/TEST_1_pyxis/landmarks_odom/no_lk3_o_geodesic-mesa_2025-04-11_08-41-27',
#                        './datasets/TEST_1/landmarks_odom/no_lk3.jrl',
#                        './saved_output',
#                        iteration=12)

##########################################################################################################
###             Landmarks - Noisy                                                                      ###
##########################################################################################################
ctr_def_a1_n = Results('./input/TEST_1_pyxis/landmarks_noisy/default_a1_n_geodesic-mesa_2025-04-11_08-12-05',
                       './datasets/TEST_1/landmarks_noisy/default_a1.jrl',
                       './saved_output',
                       iteration=996,
                       init=init_opt)
ctr_def_a2_n = Results('./input/TEST_1_pyxis/landmarks_noisy/default_a2_n_geodesic-mesa_2025-04-11_08-19-33',
                       './datasets/TEST_1/landmarks_noisy/default_a2.jrl',
                       './saved_output',
                       iteration=996,
                       init=init_opt)
ctr_def_a3_n = Results('./input/TEST_1_pyxis/landmarks_noisy/default_a3_n_geodesic-mesa_2025-04-11_08-21-11',
                       './datasets/TEST_1/landmarks_noisy/default_a3.jrl',
                       './saved_output',
                       iteration=996,
                       init=init_opt)
ctr_def_e1_n = Results('./input/TEST_1_pyxis/landmarks_noisy/default_e1_n_geodesic-mesa_2025-04-11_08-23-41',
                       './datasets/TEST_1/landmarks_noisy/default_e1.jrl',
                       './saved_output',
                       iteration=996,
                       init=init_opt)
ctr_def_e2_n = Results('./input/TEST_1_pyxis/landmarks_noisy/default_e2_n_geodesic-mesa_2025-04-11_08-25-03',
                       './datasets/TEST_1/landmarks_noisy/default_e2.jrl',
                       './saved_output',
                       iteration=996,
                       init=init_opt)
ctr_def_e3_n = Results('./input/TEST_1_pyxis/landmarks_noisy/default_e3_n_geodesic-mesa_2025-04-11_08-26-25',
                       './datasets/TEST_1/landmarks_noisy/default_e3.jrl',
                       './saved_output',
                       iteration=996,
                       init=init_opt)
ctr_no_lk1_n = Results('./input/TEST_1_pyxis/landmarks_noisy/no_lk1_n_geodesic-mesa_2025-04-11_08-28-03',
                       './datasets/TEST_1/landmarks_noisy/no_lk1.jrl',
                       './saved_output',
                       iteration=996,
                       init=init_opt)
ctr_no_lk2_n = Results('./input/TEST_1_pyxis/landmarks_noisy/no_lk2_n_geodesic-mesa_2025-04-11_08-30-23',
                       './datasets/TEST_1/landmarks_noisy/no_lk2.jrl',
                       './saved_output',
                       iteration=996,
                       init=init_opt)
ctr_no_lk3_n = Results('./input/TEST_1_pyxis/landmarks_noisy/no_lk3_n_geodesic-mesa_2025-04-11_08-31-37',
                       './datasets/TEST_1/landmarks_noisy/no_lk3.jrl',
                       './saved_output',
                       iteration=432,
                       init=init_opt)

##########################################################################################################
###             Landmarks - E/A - Odom                                                                 ###
##########################################################################################################
# ctr_lk_a1_o = Results('./input/TEST_1_pyxis/lk_ea_odom/lk_a1_o_geodesic-mesa_2025-04-11_11-21-35',
#                       './datasets/TEST_1/lk_ea_odom/lk_a1.jrl',
#                       './saved_output',
#                       iteration=30)
# ctr_lk_a2_o = Results('./input/TEST_1_pyxis/lk_ea_odom/lk_a2_o_geodesic-mesa_2025-04-11_11-24-18',
#                       './datasets/TEST_1/lk_ea_odom/lk_a2.jrl',
#                       './saved_output',
#                       iteration=30)
# ctr_lk_a3_o = Results('./input/TEST_1_pyxis/lk_ea_odom/lk_a3_o_geodesic-mesa_2025-04-11_11-25-40',
#                       './datasets/TEST_1/lk_ea_odom/lk_a3.jrl',
#                       './saved_output',
#                       iteration=30)
# ctr_lk_e1_o = Results('./input/TEST_1_pyxis/lk_ea_odom/lk_e1_o_geodesic-mesa_2025-04-11_11-26-57',
#                       './datasets/TEST_1/lk_ea_odom/lk_e1.jrl',
#                       './saved_output',
#                       iteration=30)
# ctr_lk_e2_o = Results('./input/TEST_1_pyxis/lk_ea_odom/lk_e2_o_geodesic-mesa_2025-04-11_11-27-49',
#                       './datasets/TEST_1/lk_ea_odom/lk_e2.jrl',
#                       './saved_output',
#                       iteration=30)
# ctr_lk_e3_o = Results('./input/TEST_1_pyxis/lk_ea_odom/lk_e3_o_geodesic-mesa_2025-04-11_11-28-36',
#                       './datasets/TEST_1/lk_ea_odom/lk_e3.jrl',
#                       './saved_output',
#                       iteration=30)

##########################################################################################################
###             Landmarks - E/A - Noisy                                                                ###
##########################################################################################################
# ctr_lk_a1_n = Results('./input/TEST_1_pyxis/lk_ea_noisy/lk_a1_n_geodesic-mesa_2025-04-11_11-12-33',
#                       './datasets/TEST_1/lk_ea_noisy/lk_a1.jrl',
#                       './saved_output',
#                       iteration=252)
# ctr_lk_a2_n = Results('./input/TEST_1_pyxis/lk_ea_noisy/lk_a2_n_geodesic-mesa_2025-04-11_11-13-47',
#                       './datasets/TEST_1/lk_ea_noisy/lk_a2.jrl',
#                       './saved_output',
#                       iteration=252)
# ctr_lk_a3_n = Results('./input/TEST_1_pyxis/lk_ea_noisy/lk_a3_n_geodesic-mesa_2025-04-11_11-15-03',
#                       './datasets/TEST_1/lk_ea_noisy/lk_a3.jrl',
#                       './saved_output',
#                       iteration=252)
# ctr_lk_e1_n = Results('./input/TEST_1_pyxis/lk_ea_noisy/lk_e1_n_geodesic-mesa_2025-04-11_11-16-20',
#                       './datasets/TEST_1/lk_ea_noisy/lk_e1.jrl',
#                       './saved_output',
#                       iteration=252)
# ctr_lk_e2_n = Results('./input/TEST_1_pyxis/lk_ea_noisy/lk_e2_n_geodesic-mesa_2025-04-11_11-17-26',
#                       './datasets/TEST_1/lk_ea_noisy/lk_e2.jrl',
#                       './saved_output',
#                       iteration=252)
# ctr_lk_e3_n = Results('./input/TEST_1_pyxis/lk_ea_noisy/lk_e3_n_geodesic-mesa_2025-04-11_11-18-36',
#                       './datasets/TEST_1/lk_ea_noisy/lk_e3.jrl',
#                       './saved_output',
#                       iteration=252)

##########################################################################################################
###             Ouliers - Odom                                                                         ###
##########################################################################################################
# ctr_def1_o = Results('./input/TEST_1_pyxis/outliers_odom/default1_o_geodesic-mesa_2025-04-11_11-51-01',
#                      './datasets/TEST_1/outliers_odom/default1.jrl',
#                      './saved_output',
#                      iteration=252)
# ctr_def2_o = Results('./input/TEST_1_pyxis/outliers_odom/default2_o_geodesic-mesa_2025-04-11_11-53-43',
#                      './datasets/TEST_1/outliers_odom/default2.jrl',
#                      './saved_output')
# ctr_def3_o = Results('./input/TEST_1_pyxis/outliers_odom/default3_o_geodesic-mesa_2025-04-11_11-54-08',
#                      './datasets/TEST_1/outliers_odom/default3.jrl',
#                      './saved_output',
#                      iteration=312)
# ctr_out1_o = Results('./input/TEST_1_pyxis/outliers_odom/outliers1_o_geodesic-mesa_2025-04-11_11-57-23',
#                      './datasets/TEST_1/outliers_odom/outliers1.jrl',
#                      './saved_output')
# ctr_out2_o = Results('./input/TEST_1_pyxis/outliers_odom/outliers2_o_geodesic-mesa_2025-04-11_11-58-06',
#                      './datasets/TEST_1/outliers_odom/outliers2.jrl',
#                      './saved_output')
# ctr_out3_o = Results('./input/TEST_1_pyxis/outliers_odom/outliers3_o_geodesic-mesa_2025-04-11_11-59-49',
#                      './datasets/TEST_1/outliers_odom/outliers3.jrl',
#                      './saved_output')

##########################################################################################################
###             Outliers - Noisy                                                                       ###
##########################################################################################################
# ctr_def1_n = Results('./input/TEST_1_pyxis/outliers_noisy/default1_n_geodesic-mesa_2025-04-11_11-39-04',
#                      './datasets/TEST_1/outliers_noisy/default1.jrl',
#                      './saved_output',
#                      iteration=252,
#                      init=init_opt)
# ctr_def2_n = Results('./input/TEST_1_pyxis/outliers_noisy/default2_n_geodesic-mesa_2025-04-11_11-40-37',
#                      './datasets/TEST_1/outliers_noisy/default2.jrl',
#                      './saved_output',
#                      iteration=252,
#                      init=init_opt)
# ctr_def3_n = Results('./input/TEST_1_pyxis/outliers_noisy/default3_n_geodesic-mesa_2025-04-11_11-43-20',
#                      './datasets/TEST_1/outliers_noisy/default3.jrl',
#                      './saved_output',
#                      iteration=252,
#                      init=init_opt)
# ctr_out1_n = Results('./input/TEST_1_pyxis/outliers_noisy/outliers1_n_geodesic-mesa_2025-04-11_11-45-40',
#                      './datasets/TEST_1/outliers_noisy/outliers1.jrl',
#                      './saved_output',
#                      iteration=252,
#                      init=init_opt)
# ctr_out2_n = Results('./input/TEST_1_pyxis/outliers_noisy/outliers2_n_geodesic-mesa_2025-04-11_11-47-12',
#                      './datasets/TEST_1/outliers_noisy/outliers2.jrl',
#                      './saved_output',
#                      iteration=252,
#                      init=init_opt)
# ctr_out3_n = Results('./input/TEST_1_pyxis/outliers_noisy/outliers3_n_geodesic-mesa_2025-04-11_11-48-56',
#                      './datasets/TEST_1/outliers_noisy/outliers3.jrl',
#                      './saved_output',
#                      iteration=252,
#                      init=init_opt)

mdsp = MultiDisplay()

################################################
###        Landmarks - Odom                  ###
################################################
# mdsp.add_results('ctr_def_a1_o', ctr_def_a1_o)
# mdsp.add_results('ctr_def_a2_o', ctr_def_a2_o)
# mdsp.add_results('ctr_def_a3_o', ctr_def_a3_o)

# mdsp.add_results('ctr_def_e1_o', ctr_def_e1_o)
# mdsp.add_results('ctr_def_e2_o', ctr_def_e2_o)
# mdsp.add_results('ctr_def_e3_o', ctr_def_e3_o)

# mdsp.add_results('ctr_no_lk1_o', ctr_no_lk1_o)
# mdsp.add_results('ctr_no_lk2_o', ctr_no_lk2_o)
# mdsp.add_results('ctr_no_lk3_o', ctr_no_lk3_o)

################################################
###        Landmarks - Noisy                 ###
################################################
mdsp.add_results('ctr_def_a1_n', ctr_def_a1_n)
mdsp.add_results('ctr_def_a2_n', ctr_def_a2_n)
mdsp.add_results('ctr_def_a3_n', ctr_def_a3_n)

mdsp.add_results('ctr_def_e1_n', ctr_def_e1_n)
mdsp.add_results('ctr_def_e2_n', ctr_def_e2_n)
mdsp.add_results('ctr_def_e3_n', ctr_def_e3_n)

mdsp.add_results('ctr_no_lk1_n', ctr_no_lk1_n)
mdsp.add_results('ctr_no_lk2_n', ctr_no_lk2_n)
mdsp.add_results('ctr_no_lk3_n', ctr_no_lk3_n)

################################################
###        Landmarks - E/A - Odom            ###
################################################
# mdsp.add_results('ctr_lk_a1_o', ctr_lk_a1_o)
# mdsp.add_results('ctr_lk_a2_o', ctr_lk_a2_o)
# mdsp.add_results('ctr_lk_a3_o', ctr_lk_a3_o)

# mdsp.add_results('ctr_lk_e1_o', ctr_lk_e1_o)
# mdsp.add_results('ctr_lk_e2_o', ctr_lk_e2_o)
# mdsp.add_results('ctr_lk_e3_o', ctr_lk_e3_o)

################################################
###        Landmarks - E/A - Noisy           ###
################################################
# mdsp.add_results('ctr_lk_a1_n', ctr_lk_a1_n)
# mdsp.add_results('ctr_lk_a2_n', ctr_lk_a2_n)
# mdsp.add_results('ctr_lk_a3_n', ctr_lk_a3_n)

# mdsp.add_results('ctr_lk_e1_n', ctr_lk_e1_n)
# mdsp.add_results('ctr_lk_e2_n', ctr_lk_e2_n)
# mdsp.add_results('ctr_lk_e3_n', ctr_lk_e3_n)

################################################
###        Ouliers - Odom                    ###
################################################
# mdsp.add_results('ctr_def1_o', ctr_def1_o)
# mdsp.add_results('ctr_def2_o', ctr_def2_o)
# mdsp.add_results('ctr_def3_o', ctr_def3_o)

# mdsp.add_results('ctr_out1_o', ctr_out1_o)
# mdsp.add_results('ctr_out2_o', ctr_out2_o)
# mdsp.add_results('ctr_out3_o', ctr_out3_o)

################################################
###        Outliers - Noisy                  ###
################################################
# mdsp.add_results('ctr_def1_n', ctr_def1_n)
# mdsp.add_results('ctr_def2_n', ctr_def2_n)
# mdsp.add_results('ctr_def3_n', ctr_def3_n)

# mdsp.add_results('ctr_out1_n', ctr_out1_n)
# mdsp.add_results('ctr_out2_n', ctr_out2_n)
# mdsp.add_results('ctr_out3_n', ctr_out3_n)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

mdsp.boxplot('transformation_ape')
mdsp.boxplot('point_distance_ape')
mdsp.boxplot('rot_angle_deg_ape')