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
#from scipy.stats import chi2
from copy import copy
from string import ascii_letters

from itertools import combinations

from parameters import DatasetParameters
from generator import DatasetGenerator

def get_all_edges(robots):
    edges = set()
    for rid in robots:
        for oid in robots:
            if rid != oid:
                edge = (min(rid,oid),max(rid,oid))
                edges.add(edge)
    return edges

def pack_lid_per_rid(robots, nb_lks, group_type):
    lk_ids = [gtsam.symbol('l', i + 1) for i in range(nb_lks)]
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
        pose_num = np.random.randint(ind_thr, nb_poses, size=lc_ind_nb)
        pose_num.sort()
        data[rid + '_poses'] = pose_num

        np.random.seed(seeds[idx][1])
        data[rid + '_oids'] = np.random.choice(o_robots, size=lc_ind_nb)

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

if __name__ == "__main__":

    # Setup the Dataset Builder
    input_dir = './configs/ICCAD/lc_direct/range'
    output_dir = './saved_outputs/iccad_4/lc_direct/range'
    config_name = 'lc_dir_range10'
    builder = DatasetGenerator(os.path.join(input_dir, config_name + ".json"))
    if builder.params.lc_inter_direct is not None:
        if builder.params.lc_inter_direct.get('range') is not None:
            init_range_freq = np.random.randint(builder.params.lc_inter_direct['range']['frequency'])
        if builder.params.lc_inter_direct.get('pose') is not None:
            init_pose_freq = np.random.randint(builder.params.lc_inter_direct['pose']['frequency'])
    # Add in config ?
    # TODO handle multiple configurations
    # TODO make evolve to handle freq or probability
    # TODO get rid of name of config and dataset
    
    lk_options = 'edges'
    seed = 53

    # Setup groundTruths
    builder.gen_gt_trajectories()
    
    # Add landmarks detections
    if builder.params.landmarks is not None:
        # Generate landmarks
        builder.gen_lk_amers()

        # Define landmarks
        landmarks = pack_lid_per_rid(builder.robots, builder.params.landmarks['number'], lk_options)

        # Define landmarks detections
        lks_detections = gen_landmarks(builder.robots, 
                                       builder.params.dataset_opts['number_poses'], 
                                       200,
                                       landmarks, 
                                       seed)
        
    # Add loop closure : inter - indirect detections
    if builder.params.lc_inter_indirect is not None:
        lc_ind_nb = builder.params.dataset_opts['number_poses'] // builder.params.lc_inter_indirect['frequency']
        lc_ind_det = gen_lc_indirect(builder.robots,
                                                 builder.params.dataset_opts['number_poses'], 
                                                 lc_ind_nb,
                                                 builder.params.lc_inter_indirect['index'], 
                                                 seed)

    # Setup com_map
    com_map = list(combinations(builder.robots, 2))

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
                pose_oid = max(pose_num - builder.params.lc_intra['index'], 0)

                # TODO initialize all freqs at beginning
                freq = builder.params.lc_intra['frequency']

                if pose_num % freq == 0:
                    builder.add_lc_intra(rid, pose_num, pose_oid)
                    builder.incr_stamp()

        # Add loop closure : inter - indirect
        if builder.params.lc_inter_indirect is not None:
            for rid in builder.robots:
                stop_condition = False
                while lc_ind_det[rid + '_poses'][lc_ind_det[rid + '_index']] == pose_num and not stop_condition:
                    
                    oid = lc_ind_det[rid + '_oids'][lc_ind_det[rid + '_index']]
                    pose_oid = pose_num - builder.params.lc_inter_indirect['index']
                    
                    builder.add_lc_inter_indirect(rid, pose_num, oid, pose_oid)
                    builder.incr_stamp()

                    if lc_ind_det[rid + '_index'] < len(lc_ind_det[rid + '_poses']) - 1:
                        lc_ind_det[rid + '_index'] += 1
                    else:
                        stop_condition = True

        # Add loop closure : intrer - direct
        if builder.params.lc_inter_direct is not None:

            # Add range measurement
            if builder.params.lc_inter_direct.get('range') is not None:
                freq = builder.params.lc_inter_direct['range']['frequency']
                if pose_num % freq == 0:
                    builder.incr_stamp()
                    for ra, rb in com_map:
                        builder.add_lc_inter_direct('range', pose_num, ra, rb, modality='duplex')
            
            # Add pose measurement
            if builder.params.lc_inter_direct.get('pose') is not None:
                freq = builder.params.lc_inter_direct['pose']['frequency']
                if pose_num % freq == 0:
                    builder.incr_stamp()
                    for ra, rb in com_map:
                        builder.add_lc_inter_direct('pose', pose_num, ra, rb, modality='duplex')
        
        # Add landmarks
        if builder.params.landmarks is not None:

            # Add landmark measurement
            for rid in builder.robots:
                stop_condition = False
                while lks_detections[rid + '_poses'][lks_detections[rid + '_index']] == pose_num and not stop_condition:
                    
                    lid = lks_detections[rid + '_lks'][lks_detections[rid + '_index']]
                    builder.add_lk(lid, rid, pose_num)

                    if lks_detections[rid + '_index'] < len(lks_detections[rid + '_poses']) - 1:
                        lks_detections[rid + '_index'] += 1
                    else:
                        stop_condition = True

    dataset = builder.build()
    writer = jrl.Writer()

    dataset_count = 0

    writer.writeDataset(
        dataset,
        os.path.join(output_dir, config_name + ".jrl"),
        #os.path.join(builder.params.output_dir, builder.params.name + "_{:01d}.jrl".format(dataset_count)),
        #os.path.join(params.output_dir, params.name + "_{:04d}.jrl".format(dataset_count)),
        False,
    )
