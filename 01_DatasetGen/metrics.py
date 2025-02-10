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

from evo.core import metrics
from evo.core.units import Unit

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

from evo.tools import file_interface

# ref_file = "data/stamped_groundtruth.txt"
# est_file = "data/stamped_traj_estimate.txt"

# est_file = "output/results/centralized/pose_nb_6_0000/estimates_pose_nb_6_0000_a.txt"
# ref_file = "output/results/centralized/pose_nb_6_0000/gtruth_pose_nb_6_0000_a.txt"

est_file = "output/results/syscon25/pose_nb/6_0000/centralized/resultsc_a_pose_nb_6_0000_estimates.txt"
ref_file = "output/results/syscon25/pose_nb/6_0000/centralized/resultsc_a_pose_nb_6_0000_groundtruth.txt"

traj_ref = file_interface.read_tum_trajectory_file(ref_file)
traj_est = file_interface.read_tum_trajectory_file(est_file)

from evo.core import sync

max_diff = 0.01

traj_ref, traj_est = sync.associate_trajectories(traj_ref, traj_est, max_diff)

import copy

traj_est_aligned = copy.deepcopy(traj_est)
traj_est_aligned.align(traj_ref, correct_scale=False, correct_only_scale=False)

# fig = plt.figure()
# traj_by_label = {
#     "estimate (not aligned)": traj_est,
#     "estimate (aligned)": traj_est_aligned,
#     "reference": traj_ref
# }
# plot.trajectories(fig, traj_by_label, plot.PlotMode.xyz)
# plt.show()

pose_relation = metrics.PoseRelation.rotation_angle_deg

# normal mode
delta = 1
delta_unit = Unit.frames

# all pairs mode
all_pairs = False  # activate

data = (traj_ref, traj_est)

rpe_metric = metrics.RPE(pose_relation=pose_relation, delta=delta, delta_unit=delta_unit, all_pairs=all_pairs)
rpe_metric.process_data(data)

rpe_stat = rpe_metric.get_statistic(metrics.StatisticsType.rmse)
print(rpe_stat)

rpe_stats = rpe_metric.get_all_statistics()
pprint.pprint(rpe_stats)

# important: restrict data to delta ids for plot
import copy
traj_ref_plot = copy.deepcopy(traj_ref)
traj_est_plot = copy.deepcopy(traj_est)
traj_ref_plot.reduce_to_ids(rpe_metric.delta_ids)
traj_est_plot.reduce_to_ids(rpe_metric.delta_ids)
seconds_from_start = [t - traj_est.timestamps[0] for t in traj_est.timestamps[1:]]

fig = plt.figure()
plot.error_array(fig.gca(), rpe_metric.error, x_array=seconds_from_start,
                 statistics={s:v for s,v in rpe_stats.items() if s != "sse"},
                 name="RPE", title="RPE w.r.t. " + rpe_metric.pose_relation.value, xlabel="$t$ (s)")
plt.show()

plot_mode = plot.PlotMode.xy
fig = plt.figure()
ax = plot.prepare_axis(fig, plot_mode)
plot.traj(ax, plot_mode, traj_ref_plot, '--', "gray", "reference")
plot.traj_colormap(ax, traj_est_plot, rpe_metric.error, plot_mode, min_map=rpe_stats["min"], max_map=rpe_stats["max"])
ax.legend()
plt.show()
