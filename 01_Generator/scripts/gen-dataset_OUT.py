import os
import glob
import sys
from datetime import date

import random
import gtsam
import jrl
import json

import numpy as np
from gtsam.symbol_shorthand import X
from gtsam.symbol_shorthand import L
#from scipy.stats import chi2
from copy import copy
from string import ascii_letters

from itertools import combinations

from generator import DatasetGenerator

def select_outlier_rbts(robots, percentage):
    selection_nb = int(np.round(len(robots)*percentage/100))
    return np.random.choice(robots, selection_nb, replace=False)

def get_all_edges(robots):
    edges = set()
    for rid in robots:
        for oid in robots:
            if rid != oid:
                edge = (min(rid,oid),max(rid,oid))
                edges.add(edge)
    return edges

def pack_lid_per_rid(robots, nb_lks, group_type):
    lk_ids = [gtsam.symbol('#', i + 1) for i in range(nb_lks)]
    lid_dict = {}

    if group_type == 'edges':
        edges = get_all_edges(robots)
        batch_nb = nb_lks // len(edges)

        # init structure
        for rid in robots:
            lid_dict[rid] = set()

        for index, edge in enumerate(edges):
            lks = [lk_ids[index * batch_nb + i] for i in range(batch_nb)]
            for lk in lks:
                lid_dict[edge[0]].add(lk)
                lid_dict[edge[1]].add(lk)
        
        for rid in robots:
            lid_dict[rid] = list(lid_dict[rid])

    elif group_type == 'all':
        for rid in robots:
            lid_dict[rid] = lk_ids

    return lid_dict

def gen_lc_indirect(robots, nb_poses, nb_lc, ind_thr, seed):
    data = {}
    np.random.seed(seed)
    seeds = np.random.randint(nb_poses, size=2*len(robots)).reshape(-1,2)

    for idx, rid in enumerate(robots):
        o_robots = robots.copy()
        o_robots.remove(rid)

        np.random.seed(seeds[idx][0])
        pose_num = np.random.randint(ind_thr, nb_poses, size=nb_lc)
        pose_num.sort()
        data[rid + '_poses'] = pose_num

        np.random.seed(seeds[idx][1])
        data[rid + '_oids'] = np.random.choice(o_robots, size=nb_lc)

        data[rid + '_index'] = 0
    
    np.random.seed()

    return data

def gen_landmarks(robots, nb_poses, nb_lks, landmarks, seed):
    data = {}
    np.random.seed(seed)
    seeds = np.random.randint(nb_poses, size=2*len(robots)).reshape(-1,2)

    for idx, rid in enumerate(robots):

        np.random.seed(seeds[idx][0])
        pose_num = np.random.randint(nb_poses, size=nb_lks)
        pose_num.sort()
        data[rid + '_poses'] = pose_num

        np.random.seed(seeds[idx][1])
        lks = np.random.choice(landmarks[rid], size=nb_lks)
        data[rid + '_lks'] = lks

        data[rid + '_index'] = 0

    np.random.seed()

    return data
        
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

def get_config_paths(config_folder):
    # List all entries in the parent folder
    entries = os.listdir(config_folder)

    # Filter out the entries that are directories
    folder_paths = [os.path.join(config_folder, entry) for entry in entries if os.path.isdir(os.path.join(config_folder, entry))]

    file_paths = []
    jrl_files = glob.glob(os.path.join(config_folder, '*.json'))
    file_paths += jrl_files

    # Print the path of each folder
    for folder_path in folder_paths:
        jrl_files = glob.glob(os.path.join(folder_path, '*.json'))
        file_paths += jrl_files

    return file_paths

def generate_dataset(config_file_path, output_dir):
    # Setup folders
    config_name, _ = os.path.splitext(os.path.basename(config_file_path))
    output_path = output_dir

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_path = os.path.join(output_path, config_name + ".jrl")
    
    # Setup the Dataset Builder
    builder = DatasetGenerator(config_file_path)
    if builder.config.lc_inter_direct is not None:
        if builder.config.lc_inter_direct.get('range') is not None:
            init_range_freq = np.random.randint(builder.config.lc_inter_direct['range']['frequency'])
        if builder.config.lc_inter_direct.get('pose') is not None:
            init_pose_freq = np.random.randint(builder.config.lc_inter_direct['pose']['frequency'])
    
    seed = 53

    # Setup groundTruths
    builder.gen_gt_trajectories()
    
    # Add 1 landmark
    if builder.config.landmarks is not None:
        # Generate landmarks
        builder.gen_lk_amers(1)

    for rid in builder.robots:
        builder.add_prior(rid, 0)
    builder.incr_stamp()

    for pose_num in range(1,builder.config.dataset_opts['number_poses']):
        
        # Add odometry measurements
        for rid in builder.robots:
            builder.add_odom_step(rid, pose_num)
        builder.incr_stamp()
        
        # Add landmarks
        if builder.config.landmarks is not None and pose_num == 19:
            outlier_rbts = select_outlier_rbts(builder.robots, 10)
            
            # Add landmark measurement
            lid = gtsam.symbol('#', 1)
            for rid in builder.robots:
                if rid in outlier_rbts:
                    builder.add_lk(lid, rid, pose_num, outlier=(True,10))
                else:
                    builder.add_lk(lid, rid, pose_num)

    dataset = builder.build()
    writer = jrl.Writer()

    dataset_count = 0

    writer.writeDataset(
        dataset,
        output_path,
        #os.path.join(builder.config.output_dir, builder.config.name + "_{:01d}.jrl".format(dataset_count)),
        #os.path.join(config.output_dir, config.name + "_{:04d}.jrl".format(dataset_count)),
        False,
    )
    print('generated',output_path)

if __name__ == "__main__":

    config_folder = './configs/OUT'
    output_dir = './saved_outputs/OUT'
    
    file_paths = get_config_paths(config_folder)

    for config_file_path in file_paths:
        generate_dataset(config_file_path, output_dir)

