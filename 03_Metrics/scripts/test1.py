from results import Results
from display import Display, MultiDisplay
import numpy as np

##########################################################################################################
###             Landmarks - Odom                                                                       ###
##########################################################################################################
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

##########################################################################################################
###             Landmarks - Noisy                                                                      ###
##########################################################################################################
# ctr_def_a1_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_a1_n_centralized_2025-04-10_21-54-27',
#                        './datasets/TEST_1/landmarks_noisy/default_a1.jrl',
#                        './saved_output')
# ctr_def_a2_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_a2_n_centralized_2025-04-10_21-54-49',
#                        './datasets/TEST_1/landmarks_noisy/default_a2.jrl',
#                        './saved_output')
# ctr_def_a3_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_a3_n_centralized_2025-04-10_21-54-50',
#                        './datasets/TEST_1/landmarks_noisy/default_a3.jrl',
#                        './saved_output')
# ctr_def_e1_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_e1_n_centralized_2025-04-10_21-54-51',
#                        './datasets/TEST_1/landmarks_noisy/default_e1.jrl',
#                        './saved_output')
# ctr_def_e2_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_e2_n_centralized_2025-04-10_21-54-53',
#                        './datasets/TEST_1/landmarks_noisy/default_e2.jrl',
#                        './saved_output')
# ctr_def_e3_n = Results('./input/TEST_1_ctr/landmarks_noisy/default_e3_n_centralized_2025-04-10_21-54-53',
#                        './datasets/TEST_1/landmarks_noisy/default_e3.jrl',
#                        './saved_output')
# ctr_no_lk1_n = Results('./input/TEST_1_ctr/landmarks_noisy/no_lk1_n_centralized_2025-04-10_21-54-54',
#                        './datasets/TEST_1/landmarks_noisy/no_lk1.jrl',
#                        './saved_output')
# ctr_no_lk2_n = Results('./input/TEST_1_ctr/landmarks_noisy/no_lk2_n_centralized_2025-04-10_21-54-55',
#                        './datasets/TEST_1/landmarks_noisy/no_lk2.jrl',
#                        './saved_output')
# ctr_no_lk3_n = Results('./input/TEST_1_ctr/landmarks_noisy/no_lk3_n1_centralized_2025-04-10_21-54-56',
#                        './datasets/TEST_1/landmarks_noisy/no_lk3.jrl',
#                        './saved_output')

##########################################################################################################
###             Landmarks - E/A - Noisy                                                                ###
##########################################################################################################
# ctr_lk_a1_n = Results('./input/TEST_1_ctr/lk_ea_noisy/lk_a1_n_centralized_2025-04-10_21-55-18',
#                       './datasets/TEST_1/lk_ea_noisy/lk_a1.jrl',
#                       './saved_output')
# ctr_lk_a2_n = Results('./input/TEST_1_ctr/lk_ea_noisy/lk_a2_n_centralized_2025-04-10_21-55-18',
#                       './datasets/TEST_1/lk_ea_noisy/lk_a2.jrl',
#                       './saved_output')
# ctr_lk_a3_n = Results('./input/TEST_1_ctr/lk_ea_noisy/lk_a3_n_centralized_2025-04-10_21-55-19',
#                       './datasets/TEST_1/lk_ea_noisy/lk_a3.jrl',
#                       './saved_output')
# ctr_lk_e1_n = Results('./input/TEST_1_ctr/lk_ea_noisy/lk_e1_n_centralized_2025-04-10_21-55-20',
#                       './datasets/TEST_1/lk_ea_noisy/lk_e1.jrl',
#                       './saved_output')
# ctr_lk_e2_n = Results('./input/TEST_1_ctr/lk_ea_noisy/lk_e2_n_centralized_2025-04-10_21-55-21',
#                       './datasets/TEST_1/lk_ea_noisy/lk_e2.jrl',
#                       './saved_output')
# ctr_lk_e3_n = Results('./input/TEST_1_ctr/lk_ea_noisy/lk_e3_n_centralized_2025-04-10_21-55-22',
#                       './datasets/TEST_1/lk_ea_noisy/lk_e3.jrl',
#                       './saved_output')

##########################################################################################################
###             Landmarks - E/A - Odom                                                                 ###
##########################################################################################################
# ctr_lk_a1_o = Results('./input/TEST_1_ctr/lk_ea_odom/lk_a1_o_centralized_2025-04-10_21-55-23',
#                       './datasets/TEST_1/lk_ea_odom/lk_a1.jrl',
#                       './saved_output')
# ctr_lk_a1_o = Results('./input/TEST_1_ctr/lk_ea_odom/lk_a2_o_centralized_2025-04-10_21-55-24',
#                       './datasets/TEST_1/lk_ea_odom/lk_a2.jrl',
#                       './saved_output')
# ctr_lk_a1_o = Results('./input/TEST_1_ctr/lk_ea_odom/lk_a3_o_centralized_2025-04-10_21-55-26',
#                       './datasets/TEST_1/lk_ea_odom/lk_a3.jrl',
#                       './saved_output')
# ctr_lk_a1_o = Results('./input/TEST_1_ctr/lk_ea_odom/lk_e1_o_centralized_2025-04-10_21-55-28',
#                       './datasets/TEST_1/lk_ea_odom/lk_e1.jrl',
#                       './saved_output')
# ctr_lk_a1_o = Results('./input/TEST_1_ctr/lk_ea_odom/lk_e2_o_centralized_2025-04-10_21-55-29',
#                       './datasets/TEST_1/lk_ea_odom/lk_e2.jrl',
#                       './saved_output')
# ctr_lk_a1_o = Results('./input/TEST_1_ctr/lk_ea_odom/lk_e3_o_centralized_2025-04-10_21-55-33',
#                       './datasets/TEST_1/lk_ea_odom/lk_e3.jrl',
#                       './saved_output')

##########################################################################################################
###             Outliers - Noisy                                                                       ###
##########################################################################################################
# ctr_def1_n = Results('./input/TEST_1_ctr/outliers_noisy/default1_n_centralized_2025-04-10_21-55-35',
#                      './datasets/TEST_1/outliers_noisy/default1.jrl',
#                      './saved_output')
# ctr_def2_n = Results('./input/TEST_1_ctr/outliers_noisy/default2_n_centralized_2025-04-10_21-55-39',
#                      './datasets/TEST_1/outliers_noisy/default2.jrl',
#                      './saved_output')
# ctr_def3_n = Results('./input/TEST_1_ctr/outliers_noisy/default3_n_centralized_2025-04-10_21-55-40',
#                      './datasets/TEST_1/outliers_noisy/default3.jrl',
#                      './saved_output')
# ctr_out1_n = Results('./input/TEST_1_ctr/outliers_noisy/outliers1_n_centralized_2025-04-10_21-55-43',
#                      './datasets/TEST_1/outliers_noisy/outliers1.jrl',
#                      './saved_output')
# ctr_out2_n = Results('./input/TEST_1_ctr/outliers_noisy/outliers2_n_centralized_2025-04-10_21-55-47',
#                      './datasets/TEST_1/outliers_noisy/outliers2.jrl',
#                      './saved_output')
# ctr_out3_n = Results('./input/TEST_1_ctr/outliers_noisy/outliers3_n_centralized_2025-04-10_21-55-50',
#                      './datasets/TEST_1/outliers_noisy/outliers3.jrl',
#                      './saved_output')

##########################################################################################################
###             Ouliers - Odom                                                                         ###
##########################################################################################################
# ctr_def1_o = Results('./input/TEST_1_ctr/outliers_odom/default1_o_centralized_2025-04-10_21-55-52',
#                      './datasets/TEST_1/outliers_odom/default1.jrl',
#                      './saved_output')
# ctr_def2_o = Results('./input/TEST_1_ctr/outliers_odom/default2_o_centralized_2025-04-10_21-55-54',
#                      './datasets/TEST_1/outliers_odom/default2.jrl',
#                      './saved_output')
# ctr_def3_o = Results('./input/TEST_1_ctr/outliers_odom/default3_o_centralized_2025-04-10_21-55-56',
#                      './datasets/TEST_1/outliers_odom/default3.jrl',
#                      './saved_output')
# ctr_out1_o = Results('./input/TEST_1_ctr/outliers_odom/outliers1_o_centralized_2025-04-10_21-55-58',
#                      './datasets/TEST_1/outliers_odom/outliers1.jrl',
#                      './saved_output')
# ctr_out2_o = Results('./input/TEST_1_ctr/outliers_odom/outliers2_o_centralized_2025-04-10_21-56-01',
#                      './datasets/TEST_1/outliers_odom/outliers2.jrl',
#                      './saved_output')
# ctr_out3_o = Results('./input/TEST_1_ctr/outliers_odom/outliers3_o_centralized_2025-04-10_21-56-05',
#                      './datasets/TEST_1/outliers_odom/outliers3.jrl',
#                      './saved_output')

mdsp = MultiDisplay()

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
###        Landmarks - E/A - Noisy           ###
################################################
# mdsp.add_results('ctr_lk_a1_n', ctr_lk_a1_n)
# mdsp.add_results('ctr_lk_a2_n', ctr_lk_a2_n)
# mdsp.add_results('ctr_lk_a3_n', ctr_lk_a3_n)

# mdsp.add_results('ctr_lk_e1_n', ctr_lk_e1_n)
# mdsp.add_results('ctr_lk_e2_n', ctr_lk_e2_n)
# mdsp.add_results('ctr_lk_e3_n', ctr_lk_e3_n)

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
###        Outliers - Noisy                  ###
################################################
# mdsp.add_results('ctr_def1_n', ctr_def1_n)
# mdsp.add_results('ctr_def1_n', ctr_def1_n)
# mdsp.add_results('ctr_def1_n', ctr_def1_n)

# mdsp.add_results('ctr_out1_n', ctr_out1_n)
# mdsp.add_results('ctr_out2_n', ctr_out2_n)
# mdsp.add_results('ctr_out3_n', ctr_out3_n)

################################################
###        Ouliers - Odom                    ###
################################################
# mdsp.add_results('ctr_def1_o', ctr_def1_o)
# mdsp.add_results('ctr_def1_o', ctr_def1_o)
# mdsp.add_results('ctr_def1_o', ctr_def1_o)

# mdsp.add_results('ctr_out1_o', ctr_out1_o)
# mdsp.add_results('ctr_out2_o', ctr_out2_o)
# mdsp.add_results('ctr_out3_o', ctr_out3_o)

mdsp.boxplot('transformation_rpe')
mdsp.boxplot('point_distance_rpe')
mdsp.boxplot('rot_angle_deg_rpe')

mdsp.boxplot('transformation_ape')
mdsp.boxplot('point_distance_ape')
mdsp.boxplot('rot_angle_deg_ape')