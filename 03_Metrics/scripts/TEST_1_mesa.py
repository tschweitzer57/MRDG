from results import Results
from display import Display, MultiDisplay
import numpy as np

##########################################################################################################
###             Landmarks - Odom                                                                       ###
##########################################################################################################
# mesa_def_a1_o = Results('./input/TEST_1_mesa/landmarks_odom/default_a1_o_geodesic-mesa_2025-04-11_12-49-01',
#                        './datasets/TEST_1/landmarks_odom/default_a1.jrl',
#                        './saved_output')
# mesa_def_a2_o = Results('./input/TEST_1_mesa/landmarks_odom/default_a2_o_geodesic-mesa_2025-04-11_12-49-28',
#                        './datasets/TEST_1/landmarks_odom/default_a2.jrl',
#                        './saved_output')
# mesa_def_a3_o = Results('./input/TEST_1_mesa/landmarks_odom/default_a3_o_geodesic-mesa_2025-04-11_12-50-05',
#                        './datasets/TEST_1/landmarks_odom/default_a3.jrl',
#                        './saved_output')
# mesa_def_e1_o = Results('./input/TEST_1_mesa/landmarks_odom/default_e1_o_geodesic-mesa_2025-04-11_12-50-40',
#                        './datasets/TEST_1/landmarks_odom/default_e1.jrl',
#                        './saved_output')
# mesa_def_e2_o = Results('./input/TEST_1_mesa/landmarks_odom/default_e2_o_geodesic-mesa_2025-04-11_12-51-13',
#                        './datasets/TEST_1/landmarks_odom/default_e2.jrl',
#                        './saved_output')
# mesa_def_e3_o = Results('./input/TEST_1_mesa/landmarks_odom/default_e3_o_geodesic-mesa_2025-04-11_12-53-12',
#                        './datasets/TEST_1/landmarks_odom/default_e3.jrl',
#                        './saved_output')
# mesa_no_lk1_o = Results('./input/TEST_1_mesa/landmarks_odom/no_lk1_o_geodesic-mesa_2025-04-11_12-53-59',
#                        './datasets/TEST_1/landmarks_odom/no_lk1.jrl',
#                        './saved_output')
# mesa_no_lk2_o = Results('./input/TEST_1_mesa/landmarks_odom/no_lk2_o_geodesic-mesa_2025-04-11_12-54-18',
#                        './datasets/TEST_1/landmarks_odom/no_lk2.jrl',
#                        './saved_output')
# mesa_no_lk3_o = Results('./input/TEST_1_mesa/landmarks_odom/no_lk3_o_geodesic-mesa_2025-04-11_12-54-30',
#                        './datasets/TEST_1/landmarks_odom/no_lk3.jrl',
#                        './saved_output')

##########################################################################################################
###             Landmarks - Noisy                                                                      ###
##########################################################################################################
# mesa_def_a1_n = Results('./input/TEST_1_mesa/landmarks_noisy/default_a1_n_geodesic-mesa_2025-04-11_12-36-24',
#                        './datasets/TEST_1/landmarks_noisy/default_a1.jrl',
#                        './saved_output',
#                        iteration=246)
# mesa_def_a2_n = Results('./input/TEST_1_mesa/landmarks_noisy/default_a2_n_geodesic-mesa_2025-04-11_12-37-37',
#                        './datasets/TEST_1/landmarks_noisy/default_a2.jrl',
#                        './saved_output',
#                        iteration=246)
# mesa_def_a3_n = Results('./input/TEST_1_mesa/landmarks_noisy/default_a3_n_geodesic-mesa_2025-04-11_12-38-44',
#                        './datasets/TEST_1/landmarks_noisy/default_a3.jrl',
#                        './saved_output',
#                        iteration=246)
# mesa_def_e1_n = Results('./input/TEST_1_mesa/landmarks_noisy/default_e1_n_geodesic-mesa_2025-04-11_12-40-10',
#                        './datasets/TEST_1/landmarks_noisy/default_e1.jrl',
#                        './saved_output',
#                        iteration=246)
# mesa_def_e2_n = Results('./input/TEST_1_mesa/landmarks_noisy/default_e2_n_geodesic-mesa_2025-04-11_12-41-13',
#                        './datasets/TEST_1/landmarks_noisy/default_e2.jrl',
#                        './saved_output',
#                        iteration=246)
# mesa_def_e3_n = Results('./input/TEST_1_mesa/landmarks_noisy/default_e3_n_geodesic-mesa_2025-04-11_12-42-16',
#                        './datasets/TEST_1/landmarks_noisy/default_e3.jrl',
#                        './saved_output',
#                        iteration=246)
# mesa_no_lk1_n = Results('./input/TEST_1_mesa/landmarks_noisy/no_lk1_n_geodesic-mesa_2025-04-11_12-43-27',
#                        './datasets/TEST_1/landmarks_noisy/no_lk1.jrl',
#                        './saved_output',
#                        iteration=246)
# mesa_no_lk2_n = Results('./input/TEST_1_mesa/landmarks_noisy/no_lk2_n_geodesic-mesa_2025-04-11_12-44-33',
#                        './datasets/TEST_1/landmarks_noisy/no_lk2.jrl',
#                        './saved_output',
#                        iteration=246)
# mesa_no_lk3_n = Results('./input/TEST_1_mesa/landmarks_noisy/no_lk3_n1_geodesic-mesa_2025-04-11_12-45-44',
#                        './datasets/TEST_1/landmarks_noisy/no_lk3.jrl',
#                        './saved_output',
#                        iteration=246)

##########################################################################################################
###             Landmarks - E/A - Odom                                                                 ###
##########################################################################################################
# mesa_lk_a1_o = Results('./input/TEST_1_mesa/lk_ea_odom/lk_a1_o_geodesic-mesa_2025-04-11_13-04-35',
#                       './datasets/TEST_1/lk_ea_odom/lk_a1.jrl',
#                       './saved_output',
#                       iteration=246)
# mesa_lk_a2_o = Results('./input/TEST_1_mesa/lk_ea_odom/lk_a2_o_geodesic-mesa_2025-04-11_13-07-20',
#                       './datasets/TEST_1/lk_ea_odom/lk_a2.jrl',
#                       './saved_output')
# mesa_lk_a3_o = Results('./input/TEST_1_mesa/lk_ea_odom/lk_a3_o_geodesic-mesa_2025-04-11_13-07-49',
#                       './datasets/TEST_1/lk_ea_odom/lk_a3.jrl',
#                       './saved_output')
# mesa_lk_e1_o = Results('./input/TEST_1_mesa/lk_ea_odom/lk_e1_o_geodesic-mesa_2025-04-11_13-04-11',
#                       './datasets/TEST_1/lk_ea_odom/lk_e1.jrl',
#                       './saved_output')
# mesa_lk_e2_o = Results('./input/TEST_1_mesa/lk_ea_odom/lk_e2_o_geodesic-mesa_2025-04-11_13-03-41',
#                       './datasets/TEST_1/lk_ea_odom/lk_e2.jrl',
#                       './saved_output')
# mesa_lk_e3_o = Results('./input/TEST_1_mesa/lk_ea_odom/lk_e3_o_geodesic-mesa_2025-04-11_13-03-16',
#                       './datasets/TEST_1/lk_ea_odom/lk_e3.jrl',
#                       './saved_output')

##########################################################################################################
###             Landmarks - E/A - Noisy                                                                ###
##########################################################################################################
# mesa_lk_a1_n = Results('./input/TEST_1_mesa/lk_ea_noisy/lk_a1_n_geodesic-mesa_2025-04-11_12-55-59',
#                       './datasets/TEST_1/lk_ea_noisy/lk_a1.jrl',
#                       './saved_output',
#                       iteration=252)
# mesa_lk_a2_n = Results('./input/TEST_1_mesa/lk_ea_noisy/lk_a2_n_geodesic-mesa_2025-04-11_12-57-06',
#                       './datasets/TEST_1/lk_ea_noisy/lk_a2.jrl',
#                       './saved_output',
#                       iteration=252)
# mesa_lk_a3_n = Results('./input/TEST_1_mesa/lk_ea_noisy/lk_a3_n_geodesic-mesa_2025-04-11_12-58-13',
#                       './datasets/TEST_1/lk_ea_noisy/lk_a3.jrl',
#                       './saved_output',
#                       iteration=252)
# mesa_lk_e1_n = Results('./input/TEST_1_mesa/lk_ea_noisy/lk_e1_n_geodesic-mesa_2025-04-11_12-59-22',
#                       './datasets/TEST_1/lk_ea_noisy/lk_e1.jrl',
#                       './saved_output',
#                       iteration=252)
# mesa_lk_e2_n = Results('./input/TEST_1_mesa/lk_ea_noisy/lk_e2_n_geodesic-mesa_2025-04-11_13-00-43',
#                       './datasets/TEST_1/lk_ea_noisy/lk_e2.jrl',
#                       './saved_output',
#                       iteration=252)
# mesa_lk_e3_n = Results('./input/TEST_1_mesa/lk_ea_noisy/lk_e3_n_geodesic-mesa_2025-04-11_13-01-44',
#                       './datasets/TEST_1/lk_ea_noisy/lk_e3.jrl',
#                       './saved_output',
#                       iteration=252)

##########################################################################################################
###             Ouliers - Odom                                                                         ###
##########################################################################################################
# mesa_def1_o = Results('./input/TEST_1_mesa/outliers_odom/default1_o_geodesic-mesa_2025-04-11_13-20-48',
#                      './datasets/TEST_1/outliers_odom/default1.jrl',
#                      './saved_output',
#                      iteration=12)
# mesa_def2_o = Results('./input/TEST_1_mesa/outliers_odom/default2_o_geodesic-mesa_2025-04-11_13-23-40',
#                      './datasets/TEST_1/outliers_odom/default2.jrl',
#                      './saved_output',
#                      iteration=12)
# mesa_def3_o = Results('./input/TEST_1_mesa/outliers_odom/default3_o_geodesic-mesa_2025-04-11_13-24-08',
#                      './datasets/TEST_1/outliers_odom/default3.jrl',
#                      './saved_output',
#                      iteration=12)
# mesa_out1_o = Results('./input/TEST_1_mesa/outliers_odom/outliers1_o_geodesic-mesa_2025-04-11_13-28-01',
#                      './datasets/TEST_1/outliers_odom/outliers1.jrl',
#                      './saved_output',
#                      iteration=12)
# mesa_out2_o = Results('./input/TEST_1_mesa/outliers_odom/outliers2_o_geodesic-mesa_2025-04-11_13-29-02',
#                      './datasets/TEST_1/outliers_odom/outliers2.jrl',
#                      './saved_output',
#                      iteration=12)
# mesa_out3_o = Results('./input/TEST_1_mesa/outliers_odom/outliers3_o_geodesic-mesa_2025-04-11_13-31-46',
#                      './datasets/TEST_1/outliers_odom/outliers3.jrl',
#                      './saved_output',
#                      iteration=12)

##########################################################################################################
###             Outliers - Noisy                                                                       ###
##########################################################################################################
mesa_def1_n = Results('./input/TEST_1_mesa/outliers_noisy/default1_n_geodesic-mesa_2025-04-11_13-10-35',
                     './datasets/TEST_1/outliers_noisy/default1.jrl',
                     './saved_output',
                     iteration=174)
mesa_def2_n = Results('./input/TEST_1_mesa/outliers_noisy/default2_n_geodesic-mesa_2025-04-11_13-12-25',
                     './datasets/TEST_1/outliers_noisy/default2.jrl',
                     './saved_output',
                     iteration=174)
mesa_def3_n = Results('./input/TEST_1_mesa/outliers_noisy/default3_n_geodesic-mesa_2025-04-11_13-13-31',
                     './datasets/TEST_1/outliers_noisy/default3.jrl',
                     './saved_output',
                     iteration=174)
mesa_out1_n = Results('./input/TEST_1_mesa/outliers_noisy/outliers1_n_geodesic-mesa_2025-04-11_13-14-54',
                     './datasets/TEST_1/outliers_noisy/outliers1.jrl',
                     './saved_output',
                     iteration=174)
mesa_out2_n = Results('./input/TEST_1_mesa/outliers_noisy/outliers2_n_geodesic-mesa_2025-04-11_13-16-59',
                     './datasets/TEST_1/outliers_noisy/outliers2.jrl',
                     './saved_output',
                     iteration=174)
mesa_out3_n = Results('./input/TEST_1_mesa/outliers_noisy/outliers3_n_geodesic-mesa_2025-04-11_13-18-37',
                     './datasets/TEST_1/outliers_noisy/outliers3.jrl',
                     './saved_output',
                     iteration=174)

mdsp = MultiDisplay()

################################################
###        Landmarks - Odom                  ###
################################################
# mdsp.add_results('mesa_def_a1_o', mesa_def_a1_o)
# mdsp.add_results('mesa_def_a2_o', mesa_def_a2_o)
# mdsp.add_results('mesa_def_a3_o', mesa_def_a3_o)

# mdsp.add_results('mesa_def_e1_o', mesa_def_e1_o)
# mdsp.add_results('mesa_def_e2_o', mesa_def_e2_o)
# mdsp.add_results('mesa_def_e3_o', mesa_def_e3_o)

# mdsp.add_results('mesa_no_lk1_o', mesa_no_lk1_o)
# mdsp.add_results('mesa_no_lk2_o', mesa_no_lk2_o)
# mdsp.add_results('mesa_no_lk3_o', mesa_no_lk3_o)

################################################
###        Landmarks - Noisy                 ###
################################################
# mdsp.add_results('mesa_def_a1_n', mesa_def_a1_n)
# mdsp.add_results('mesa_def_a2_n', mesa_def_a2_n)
# mdsp.add_results('mesa_def_a3_n', mesa_def_a3_n)

# mdsp.add_results('mesa_def_e1_n', mesa_def_e1_n)
# mdsp.add_results('mesa_def_e2_n', mesa_def_e2_n)
# mdsp.add_results('mesa_def_e3_n', mesa_def_e3_n)

# mdsp.add_results('mesa_no_lk1_n', mesa_no_lk1_n)
# mdsp.add_results('mesa_no_lk2_n', mesa_no_lk2_n)
# mdsp.add_results('mesa_no_lk3_n', mesa_no_lk3_n)

################################################
###        Landmarks - E/A - Odom            ###
################################################
# mdsp.add_results('mesa_lk_a1_o', mesa_lk_a1_o)
# mdsp.add_results('mesa_lk_a2_o', mesa_lk_a2_o)
# mdsp.add_results('mesa_lk_a3_o', mesa_lk_a3_o)

# mdsp.add_results('mesa_lk_e1_o', mesa_lk_e1_o)
# mdsp.add_results('mesa_lk_e2_o', mesa_lk_e2_o)
# mdsp.add_results('mesa_lk_e3_o', mesa_lk_e3_o)

################################################
###        Landmarks - E/A - Noisy           ###
################################################
# mdsp.add_results('mesa_lk_a1_n', mesa_lk_a1_n)
# mdsp.add_results('mesa_lk_a2_n', mesa_lk_a2_n)
# mdsp.add_results('mesa_lk_a3_n', mesa_lk_a3_n)

# mdsp.add_results('mesa_lk_e1_n', mesa_lk_e1_n)
# mdsp.add_results('mesa_lk_e2_n', mesa_lk_e2_n)
# mdsp.add_results('mesa_lk_e3_n', mesa_lk_e3_n)

################################################
###        Ouliers - Odom                    ###
################################################
# mdsp.add_results('mesa_def1_o', mesa_def1_o)
# mdsp.add_results('mesa_def2_o', mesa_def2_o)
# mdsp.add_results('mesa_def3_o', mesa_def3_o)

# mdsp.add_results('mesa_out1_o', mesa_out1_o)
# mdsp.add_results('mesa_out2_o', mesa_out2_o)
# mdsp.add_results('mesa_out3_o', mesa_out3_o)

################################################
###        Outliers - Noisy                  ###
################################################
mdsp.add_results('mesa_def1_n', mesa_def1_n)
mdsp.add_results('mesa_def2_n', mesa_def2_n)
mdsp.add_results('mesa_def3_n', mesa_def3_n)

mdsp.add_results('mesa_out1_n', mesa_out1_n)
mdsp.add_results('mesa_out2_n', mesa_out2_n)
mdsp.add_results('mesa_out3_n', mesa_out3_n)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

mdsp.boxplot('transformation_ape')
mdsp.boxplot('point_distance_ape')
mdsp.boxplot('rot_angle_deg_ape')