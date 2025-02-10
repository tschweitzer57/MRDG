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

class rpeSettings():
    def __init__(self, delta = 1, delta_unit = Unit.frames, all_pairs = False):
        self.delta = delta
        self.delta_unit = delta_unit
        self.all_pairs = all_pairs

class apeSettings():
    def __init__(self, use_aligned_trajectories = False)
        self.use_aligned_trajectories = use_aligned_trajectories

class Metrics():
    def __init__(self, est_path, gt_path):

        self.traj_gt = file_interface.read_tum_trajectory_file(gt_path)
        self.traj_est = file_interface.read_tum_trajectory_file(est_path)
        self.traj_est_aligned = copy.deepcopy(self.traj_est)

        self.rpe_settings = rpeSettings()
        self.ape_settings = apeSettings()

        self.pose_relation = metrics.PoseRelation.point_distance

    def matchTimestamps(self, maxDiff = 0.01):
        self.traj_gt, self.traj_est = sync.associate_trajectories(self.traj_gt, self.traj_est, maxDiff)

    def alignTrajectory(self, correct_scale=False, correct_only_scale=False):
        self.traj_est_aligned.align(self.traj_gt, correct_scale, correct_only_scale)

    def set_RPE(self, delta = 1, delta_unit = Unit.frames, all_pairs = False):
        self.rpe_settings.delta = delta
        self.rpe_settings.delta_unit = delta_unit
        self.rpe_settings.all_pairs = all_pairs
    
    def set_APE(self, use_aligned_trajectories = False):
        self.ape_settings.use_aligned_trajectories = use_aligned_trajectories

    def set_poseRelation(self, pose_rel):
        if pose_rel == 'translation':
            self.pose_relation = metrics.PoseRelation.translation_part
        elif pose_rel == 'transformation':
            self.pose_relation = metrics.PoseRelation.full_transformation
        elif pose_rel == 'rotation':
            self.pose_relation = metrics.PoseRelation.rotation_part
        elif pose_rel == 'rot_angle_deg':
            self.pose_relation = metrics.PoseRelation.rotation_angle_deg
        elif pose_rel == 'rot_angle_rad':
            self.pose_relation = metrics.PoseRelation.rotation_angle_rad
        elif pose_rel == 'point_distance':
            self.pose_relation = metrics.PoseRelation.point_distance
        else:
            raise ValueError("Unknown pose_relation argument")