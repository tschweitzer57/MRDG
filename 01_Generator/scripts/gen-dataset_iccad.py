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

def pack_lid(robots, nb_lks, group_type):
    lk_ids = [gtsam.symbol('l', i + 1) for i in range(nb_lks)]
    lid_dict = {}
    if group_type == 'edges':
        edges = get_all_edges(robots)
        batch_nb = nb_lks // len(edges)
        for index, edge in enumerate(edges):
            lid_dict[edge] = [lk_ids[i + index] for i in range(batch_nb)]
    elif group_type == 'all':
        lid_dict['all'] = lk_ids
    return lid_dict
        
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
    input_dir = './configs/ICCAD_2'
    output_dir = './saved_outputs/iccad3'
    config_name = 'no_lk'
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
    # TODO solve problem with indirect
    # TODO solve problem with landmarks
    
    lk_options = 'all'
    # Iccad 2 -> edges
    # Iccad 1 -> All

    # Setup groundTruths
    builder.gen_gt_trajectories()
    
    # Add landmarks
    if builder.params.landmarks is not None:
        # Generate landmarks
        builder.gen_lk_amers()

        # Define landmarks
        if lk_options == 'all':
            shared_lids = pack_lid(builder.robots, builder.params.landmarks['number'], 'all')
        else:
            shared_lids = pack_lid(builder.robots, builder.params.landmarks['number'], 'edges')
        #

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
                pose_oid = max(pose_num - builder.params.lc_inter_indirect['index'], 0)
                ids = copy(builder.robots)
                ids.remove(rid) 
                oid = np.random.choice(ids)

                freq = builder.params.lc_inter_indirect['frequency']

                if pose_num % freq == 0:
                    builder.add_lc_inter_indirect(rid, pose_num, oid, pose_oid)
                    builder.incr_stamp()

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
                if np.random.rand() < builder.params.landmarks['probability']:
                    if lk_options == 'all':
                        lid = random.choice(shared_lids['all'])
                    else:
                        possible_edges = [edge for edge in shared_lids.keys() if edge[0]==rid or edge[1]==rid]
                        selected_edge = random.choice(possible_edges)
                        lid = random.choice(shared_lids[selected_edge])

                    builder.add_lk(lid, rid, pose_num)

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
