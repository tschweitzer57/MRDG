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

def get_close_pose_idx(vals, rid, pose_index, index_tresh, dist_thresh):
    current_pose = vals.atPose3(gtsam.symbol(rid, pose_index))
    close_pose_indexes = []
    for i in range(pose_index - 1):
        pose = vals.atPose3(gtsam.symbol(rid, i))
        if (
            np.linalg.norm(current_pose.inverse().compose(pose).translation())
            < dist_thresh
            and abs(i - pose_index) > index_tresh
        ):
            close_pose_indexes.append(i)
    if len(close_pose_indexes) > 1:
        return np.random.choice(close_pose_indexes)
    else:
        return None

def get_comm_robot(vals, robots, rid, pose_index, dist_thresh):
    current_pose = vals.atPose3(gtsam.symbol(rid, pose_index))
    shuffled_robots = copy(robots)
    random.shuffle(shuffled_robots)
    for other_rid in shuffled_robots:
        if rid != other_rid:
            pose = vals.atPose3(gtsam.symbol(other_rid, pose_index))
            if (
                np.linalg.norm(current_pose.inverse().compose(pose).translation())
                < dist_thresh
            ):
                return other_rid
    return None
def test():
    for i in range(10):
        return i

def get_available_comms(vals, robots, pose_index, dist_thresh):
    # should give tuple of comms for all robots in range of communication
    avaliable = copy(robots)
    comms = []

    for rid in robots:
        if rid in avaliable:
            other_rid = get_comm_robot(vals, avaliable, rid, pose_index, dist_thresh)
            if other_rid:
                comms.append((rid, other_rid))
                avaliable.remove(rid)
                avaliable.remove(other_rid)
    return comms

def make_dataset(params, dataset_count):

    # Setup ID's for each robot
    robots = []
    for i in range(params.number_robots):
        robots.append(ascii_letters[i])

    # Setup the Dataset Builder
    builder = DatasetGenerator(params.name + "_{:04d}".format(dataset_count), robots, params)
    # Setup seed
    builder.set_traj(2000)
    
    builder.add_priors(0)

    for pose_num in range(1, params.number_poses):
        # Add odometry measurements
        builder.incr_stamp()
        builder.add_odom_step(pose_num)

        # Add self loop closure
        builder.incr_stamp()
        for rid in robots:
            close_pose_idx = get_close_pose_idx(
                builder.gt_values,
                rid,
                pose_num,
                params.lc_index_threshold,
                params.lc_distance_threshold,
            )
            if close_pose_idx and np.random.rand() < params.lc_probability:
                builder.add_self_loop_closure(rid, pose_num, close_pose_idx)

        # # Add inter loop closures
        # builder.incr_stamp()
        # for rid in robots:

        # Add range loop
        if pose_num % params.dt_range_freq == 0:
            builder.incr_stamp()
            comms = get_available_comms(builder.gt_values, robots, pose_num, params.dt_range_range)
            for ra,rb in comms:
                builder.add_range_detections(pose_num, ra, rb, modality='duplex')

        # Add pose loop
        if pose_num % params.dt_pose_freq == 0:
            builder.incr_stamp()
            comms = get_available_comms(builder.gt_values, robots, pose_num, params.dt_pose_range)
            for ra,rb in comms:
                builder.add_pose_detections(pose_num, ra, rb, modality='duplex')

    dataset = builder.build()
    writer = jrl.Writer()
    writer.writeDataset(
        dataset,
        os.path.join(params.output_dir, params.name + "_{:04d}.jrl".format(dataset_count)),
        #os.path.join(params.output_dir, params.name + "_{:04d}.jrl".format(dataset_count)),
        False,
    )

if __name__ == "__main__":

    testfile = 'configs/syscon25/test.json'
    testfolder = 'configs/syscon25/'
    output_dir = 'output/datasets/syscon25/'
    
    with open(testfile, 'r') as file:
        data = json.load(file)

    for key in data.keys():
        print('Generating dataset : ', data[key]['name']) # datasetname
        Params = DatasetParameters(testfolder + data[key]['default-file'])
        data_output_dir = output_dir + '/' + data[key]['name']
        Params.output_dir = data_output_dir
        os.makedirs(data_output_dir, exist_ok=True)

        for key1 in data[key]['test-parameters'][0].keys():
            if key1 == 'variable' and not hasattr(Params, data[key]['test-parameters'][0][key1]):
                raise ValueError(f"Invalid attribute name : {data[key]['test-parameters'][0][key1]}")
            elif key1 != 'variable':
                var_name = data[key]['test-parameters'][0]['variable']
                value = data[key]['test-parameters'][0][key1]
                setattr(Params, '_' + var_name, value)
                print('param set :', data[key]['test-parameters'][0][key1])
                Params.name = data[key]['name'] + '_' + key1

                for i in range(Params.repeats):
                    make_dataset(Params, i)