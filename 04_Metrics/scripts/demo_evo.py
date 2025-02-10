# Main modules
from evo.core import metrics
from evo.core.units import Unit

# additional modules
from evo.tools import log
log.configure_logging(verbose=False, debug=False, silent=False)

import pprint
import numpy as np

from evo.tools import plot
import matplotlib.pyplot as plt

# temporarily override some package settings
from evo.tools.settings import SETTINGS
SETTINGS.plot_usetex = False
plot.apply_settings(SETTINGS)

# Required to match timestamps
from evo.core import sync

# To load files
from evo.tools import file_interface

import os
from os.path import basename, dirname, split
from collections import defaultdict
import copy

# import evo.core.trajectory as traj
# from evo.tools import file_interface
# from evo.core.metrics import PoseRelation, calculate_trajectory_error


# TODO from path get data
# TODO from data compute errors and display paths





# # Compute Absolute Trajectory Error
# alignment = traj.align_trajectories(est_traj, gt_traj)
# ate = calculate_trajectory_error(alignment, PoseRelation.translation_part)
# print("ATE:", ate)

def get_dataset_paths(directory):
    dataset_paths = defaultdict(lambda: defaultdict(lambda: defaultdict((lambda: defaultdict(lambda: defaultdict(list))))))
    
    for root, dirs, files in os.walk(directory):
        if files:
            # TODO convertir files en liste de robots avec gt et est
            # dir_solver = split(root)[1]
            # dir_parameterSet = split(split(root)[0])[1]
            # dir_testParameter = split(split(split(root)[0])[0])[1]
            # dataset_paths[dir_testParameter][dir_parameterSet][dir_solver] = files
            dirs = root.split('/')

            for file in files:
                file_name, ext = os.path.splitext(file)
                if ext == '.txt':
                    file_name = file_name.split('_')
                    dataset_paths[dirs[-3]][dirs[-2]][dirs[-1]][file_name[1]][file_name[-1]] = os.path.join(root, file)
    return dataset_paths

def stack_results(files):
    for file in files:
        print(0)
    return 0

def compute_rpe():
    print('not implemented')

def compute_ape():
    print('not implemented')

if __name__ == "__main__":
    # Load ground truth and estimated trajectory
    # gt_traj = file_interface.read_tum_trajectory_file("test_evo/stamped_groundtruth.txt")
    # est_traj = file_interface.read_tum_trajectory_file("test_evo/stamped_traj_estimate.txt")
    #results = get_dataset_paths(directory)
    
    directory = 'output_debug/results/landmarks/landmarks'
    
    solvers = ['c','s']
    robots = ['a','b','c','d']
    solver = solvers[0]
    robot = robots[0]
    est_file = os.path.join(directory, 'results' + solver + '_' + robot + "_landmarks_estimates.txt")
    ref_file = os.path.join(directory, 'results' + solver + '_' + robot + "_landmarks_groundtruth.txt")
    
    traj_ref = file_interface.read_tum_trajectory_file(ref_file)
    traj_est = file_interface.read_tum_trajectory_file(est_file)

    # Matching timestamps
    max_diff = 0.01
    traj_ref, traj_est = sync.associate_trajectories(traj_ref, traj_est, max_diff)

    # Align trajectory
    if False:
        traj_est_aligned = copy.deepcopy(traj_est)
        traj_est_aligned.align(traj_ref, correct_scale=False, correct_only_scale=False)

    # Set computed error
    pose_relation = metrics.PoseRelation.translation_part
    # pose_relation = metrics.PoseRelation.full_transformation
    # pose_relation = metrics.PoseRelation.rotation_part
    # pose_relation = metrics.PoseRelation.rotation_angle_deg
    # pose_relation = metrics.PoseRelation.point_distance

    # Set RPE
        # normal mode (compute for nb:delta of frames / meters:delta elapsed)
    delta = 10
    delta_unit = Unit.frames 

        # all pairs mode
    all_pairs = False  # activate

    # Set APE
    use_aligned_trajectories = False
    
    # Data preparation
    if use_aligned_trajectories:
        data = (traj_ref, traj_est_aligned) 
    else:
        data = (traj_ref, traj_est)

    # Run APE
    ape_metric = metrics.APE(pose_relation)
    ape_metric.process_data(data)

    # Run RPE
    rpe_metric = metrics.RPE(pose_relation=pose_relation, delta=delta, delta_unit=delta_unit, all_pairs=all_pairs)
    rpe_metric.process_data(data)

    # Get statistics
        # single
    rpe_stat = rpe_metric.get_statistic(metrics.StatisticsType.rmse)
    ape_stat = ape_metric.get_statistic(metrics.StatisticsType.rmse)
    print('RPE: ',rpe_stat)
    print('APE: ',ape_stat)

        # all
    rpe_stats = rpe_metric.get_all_statistics()
    ape_stats = rpe_metric.get_all_statistics()
    pprint.pprint(rpe_stats)
    pprint.pprint(ape_stats)


    # if rpe:
    #     # normal mode
    #     delta = 1
    #     delta_unit = Unit.frames

    #     # all pairs mode
    #     all_pairs = False  # activate

    #     rpe_metric = metrics.RPE(pose_relation=pose_relation, delta=delta, delta_unit=delta_unit, all_pairs=all_pairs)
    #     rpe_metric.process_data(data)

    #     rpe_stat = rpe_metric.get_statistic(metrics.StatisticsType.rmse)
    #     help(metrics.StatisticsType)
    #     print(rpe_stat)

    # else:
    #     ape_metric = metrics.APE(pose_relation)
    #     ape_metric.process_data(data)

    #     ape_stat = ape_metric.get_statistic(metrics.StatisticsType.rmse)
    #     print(ape_stat)

    # rpe_stats = rpe_metric.get_all_statistics()
    # pprint.pprint(rpe_stats)

    # # important: restrict data to delta ids for plot
    # import copy
    # traj_ref_plot = copy.deepcopy(traj_ref)
    # traj_est_plot = copy.deepcopy(traj_est)
    # traj_ref_plot.reduce_to_ids(rpe_metric.delta_ids)
    # traj_est_plot.reduce_to_ids(rpe_metric.delta_ids)
    # seconds_from_start = [t - traj_est.timestamps[0] for t in traj_est.timestamps[1:]]

    # fig = plt.figure()
    # plot.error_array(fig.gca(), rpe_metric.error, x_array=seconds_from_start,
    #                 statistics={s:v for s,v in rpe_stats.items() if s != "sse"},
    #                 name="RPE", title="RPE w.r.t. " + rpe_metric.pose_relation.value, xlabel="$t$ (s)")
    # plt.show()

    # plot_mode = plot.PlotMode.xy
    # fig = plt.figure()
    # ax = plot.prepare_axis(fig, plot_mode)
    # plot.traj(ax, plot_mode, traj_ref_plot, '--', "gray", "reference")
    # plot.traj_colormap(ax, traj_est_plot, rpe_metric.error, plot_mode, min_map=rpe_stats["min"], max_map=rpe_stats["max"])
    # ax.legend()
    # plt.show()

    # fig = plt.figure()
    # traj_by_label = {
    #     "estimate (not aligned)": traj_est,
    #     "estimate (aligned)": traj_est_aligned,
    #     "reference": traj_ref
    # }
    # plot.trajectories(fig, traj_by_label, plot.PlotMode.xyz)
    # plt.show()
