import os
from os.path import basename, dirname, split
from collections import defaultdict
import pprint
import copy
import numpy as np

from evo.core import metrics
from evo.core.units import Unit

from evo.tools import log
log.configure_logging(verbose=False, debug=False, silent=False)

from evo.tools import plot
import matplotlib.pyplot as plt

# temporarily override some package settings
from evo.tools.settings import SETTINGS
SETTINGS.plot_usetex = False

plot.apply_settings(SETTINGS)

from evo.tools import file_interface

from evo.core import sync


# TODO from path get data
# TODO from data compute errors and display paths

# import evo.core.trajectory as traj
# from evo.tools import file_interface
# from evo.core.metrics import PoseRelation, calculate_trajectory_error

# # Load ground truth and estimated trajectory
# gt_traj = file_interface.read_tum_trajectory_file("test_evo/stamped_groundtruth.txt")
# est_traj = file_interface.read_tum_trajectory_file("test_evo/stamped_traj_estimate.txt")

# # Compute Absolute Trajectory Error
# alignment = traj.align_trajectories(est_traj, gt_traj)
# ate = calculate_trajectory_error(alignment, PoseRelation.translation_part)
# print("ATE:", ate)

def get_dataset_paths(directory):
    dataset_paths = defaultdict(lambda: defaultdict(lambda: defaultdict((lambda: defaultdict(lambda: defaultdict(list))))))
    
    for root, dirs, files in os.walk(directory):
        if files:
            #TODO convertir files en liste de robots avec gt et est
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

if __name__ == "__main__":
    rpe = True
    directory = 'output/results/syscon25'
    results = get_dataset_paths(directory)

    for key in results['pose_nb'].keys():
        print(key)
        if results['pose_nb'][key]['centralized']:
            est_file = results['pose_nb'][key]['centralized']['c']['estimates']
            ref_file = results['pose_nb'][key]['centralized']['c']['groundtruth']

            traj_ref = file_interface.read_tum_trajectory_file(ref_file)
            traj_est = file_interface.read_tum_trajectory_file(est_file)

            max_diff = 0.01
            traj_ref, traj_est = sync.associate_trajectories(traj_ref, traj_est, max_diff)

            # traj_est_aligned = copy.deepcopy(traj_est)
            # traj_est_aligned.align(traj_ref, correct_scale=False, correct_only_scale=False)

            # fig = plt.figure()
            # traj_by_label = {
            #     "estimate (not aligned)": traj_est,
            #     "estimate (aligned)": traj_est_aligned,
            #     "reference": traj_ref
            # }
            # plot.trajectories(fig, traj_by_label, plot.PlotMode.xyz)
            # plt.show()

            # pose_relation = metrics.PoseRelation.rotation_angle_deg
            pose_relation = metrics.PoseRelation.translation_part
            # pose_relation = metrics.PoseRelation.full_transformation

            data = (traj_ref, traj_est)

            if rpe:
                # normal mode
                delta = 1
                delta_unit = Unit.frames

                # all pairs mode
                all_pairs = False  # activate

                rpe_metric = metrics.RPE(pose_relation=pose_relation, delta=delta, delta_unit=delta_unit, all_pairs=all_pairs)
                rpe_metric.process_data(data)

                rpe_stat = rpe_metric.get_statistic(metrics.StatisticsType.rmse)
                print(rpe_stat)

            else:
                use_aligned_trajectories = False
                ape_metric = metrics.APE(pose_relation)
                ape_metric.process_data(data)

                ape_stat = ape_metric.get_statistic(metrics.StatisticsType.rmse)
                print(ape_stat)

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
