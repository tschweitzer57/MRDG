import os
import sys
from datetime import date

import random
import gtsam
import jrl
import json

import numpy as np
from gtsam.symbol_shorthand import X
from gtsam.symbol_shorthand import L
from scipy.stats import chi2
from copy import copy
from string import ascii_letters

from helpers.parameters import DatasetParameters
from helpers.generator import DatasetGenerator

# TODO: possibility to suppress comm range

def get_close_pose_keys(vals, rid, pose_index, index_tresh, dist_thresh):
    current_pose = vals[rid].atPose3(gtsam.symbol(rid, pose_index))
    close_pose_keys = []
    for oid in vals.keys():
        if oid != rid:
            for i in range(pose_index - (index_tresh + 1)):
                key = gtsam.symbol(oid, i)
                pose = vals[oid].atPose3(key)
                if (
                    np.linalg.norm(current_pose.inverse().compose(pose).translation())
                    < dist_thresh
                ):
                    close_pose_keys.append(key)
            if len(close_pose_keys) > 1:
                return np.random.choice(close_pose_keys)
            else:
                return None

def get_close_pose_idx(vals, rid, pose_index, index_tresh, dist_thresh):
    current_pose = vals.atPose3(gtsam.symbol(rid, pose_index))
    close_pose_indexes = []
    for i in range(pose_index - (index_tresh + 1)):
        pose = vals.atPose3(gtsam.symbol(rid, i))
        if (
            np.linalg.norm(current_pose.inverse().compose(pose).translation())
            < dist_thresh
        ):
            close_pose_indexes.append(i)
    if len(close_pose_indexes) > 1:
        return np.random.choice(close_pose_indexes)
    else:
        return None

def get_comm_robot(vals, robots, rid, pose_index, dist_thresh):
    current_pose = vals[rid].atPose3(gtsam.symbol(rid, pose_index))
    shuffled_robots = copy(robots)
    random.shuffle(shuffled_robots)
    for other_rid in shuffled_robots:
        if rid != other_rid:
            pose = vals[other_rid].atPose3(gtsam.symbol(other_rid, pose_index))
            if (
                np.linalg.norm(current_pose.inverse().compose(pose).translation())
                < dist_thresh
            ):
                return other_rid
    return None

def get_available_comms(vals, robots, pose_index, dist_thresh):
    # should give tuple of comms for all robots in range of communication
    available = copy(robots)
    comms = []

    for rid in robots:
        if rid in available:
            other_rid = get_comm_robot(vals, available, rid, pose_index, dist_thresh)
            if other_rid:
                comms.append((rid, other_rid))
                available.remove(rid)
                available.remove(other_rid)
    return comms

if __name__ == "__main__":

    # Setup the Dataset Builder
    builder = DatasetGenerator('./configs/default1.json')
    if builder.params.lc_inter_direct is not None:
        init_range_freq = np.random.randint(builder.params.lc_inter_direct['range']['frequency'])
        init_pose_freq = np.random.randint(builder.params.lc_inter_direct['pose']['frequency'])

    # Setup groundTruths
    builder.gen_gt_trajectories(500)

    for rid in builder.robots:
        builder.add_prior(rid, 0)
    builder.incr_stamp()

    for pose_num in range(1, builder.params.dataset_opts['number_poses']):
        # Add odometry measurements
        for rid in builder.robots:
            builder.add_odom_step(rid, pose_num)
        builder.incr_stamp()

        # Add loop closure : intra
        if builder.params.lc_intra is not None:
            for rid in builder.robots:
                close_pose_idx = get_close_pose_idx(builder.gt_vals[rid],
                                                    rid,
                                                    pose_num,
                                                    builder.params.lc_intra['index_threshold'],
                                                    builder.params.lc_intra['distance_threshold'])
                if close_pose_idx and np.random.rand() < builder.params.lc_intra['probability']:
                    builder.add_lc_intra(rid, pose_num, close_pose_idx)
                    builder.incr_stamp()

        # Add loop closure : inter - indirect
        if builder.params.lc_inter_indirect is not None:
            for rid in builder.robots:
                close_pose_key = get_close_pose_keys(builder.gt_vals,
                                                    rid, 
                                                    pose_num,
                                                    builder.params.lc_inter_indirect['index_threshold'],
                                                    builder.params.lc_inter_indirect['distance_threshold'])

                if close_pose_key is not None and np.random.rand() < builder.params.lc_inter_indirect['probability']:
                    oid = chr(gtsam.Symbol(close_pose_key).chr())
                    other_pose = int(gtsam.Symbol(close_pose_key).index())
                    builder.add_lc_inter_indirect(rid, pose_num, oid, other_pose)
                    builder.incr_stamp()

        # Add loop closure : intrer - direct
        if builder.params.lc_inter_direct is not None:
            for rid in builder.robots:
                # Add range loop
                freq = builder.params.lc_inter_direct['range']['frequency']
                if pose_num % freq == init_range_freq:
                    builder.incr_stamp()
                    comms = get_available_comms(builder.gt_vals, 
                                                builder.robots, 
                                                pose_num, 
                                                builder.params.lc_inter_direct['range']['range'])
                    for ra,rb in comms:
                        builder.add_lc_inter_direct('range', pose_num, ra, rb, modality='duplex')

                # Add pose loop
                freq = builder.params.lc_inter_direct['pose']['frequency']
                if pose_num % freq == init_pose_freq:
                    builder.incr_stamp()
                    comms = get_available_comms(builder.gt_vals, 
                                                builder.robots, 
                                                pose_num, 
                                                builder.params.lc_inter_direct['pose']['range'])
                    for ra,rb in comms:
                        builder.add_lc_inter_direct('pose', pose_num, ra, rb, modality='duplex')

    dataset = builder.build()
    writer = jrl.Writer()

    dataset_count = 0

    writer.writeDataset(
        dataset,
        os.path.join(builder.params.output_dir, builder.params.name + "_{:01d}.jrl".format(dataset_count)),
        #os.path.join(params.output_dir, params.name + "_{:04d}.jrl".format(dataset_count)),
        False,
    )