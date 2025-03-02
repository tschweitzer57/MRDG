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
import json
import jrl
import gtsam

class rpeSettings():
    def __init__(self, delta = 1, delta_unit = Unit.frames, all_pairs = False):
        self.delta = delta
        self.delta_unit = delta_unit
        self.all_pairs = all_pairs

class apeSettings():
    def __init__(self, use_aligned_trajectories = False):
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

    def __statisticsType(self, err_type):
        if err_type == 'max':
            return metrics.StatisticsType.max
        elif err_type == 'min':
            return metrics.StatisticsType.min
        elif err_type == 'mean':
            return metrics.StatisticsType.mean
        elif err_type == 'median':
            return metrics.StatisticsType.median
        elif err_type == 'rmse':
            return metrics.StatisticsType.rmse
        elif err_type == 'sse':
            return metrics.StatisticsType.sse
        elif err_type == 'std':
            return metrics.StatisticsType.std
        else:
            raise ValueError("Unknown statistics type argument")

    def compute_rpe(self, err_type=None):
        data = (self.traj_gt, self.traj_est)
        self.rpe_metric = metrics.RPE(pose_relation=self.pose_relation, delta=self.rpe_settings.delta, delta_unit=self.rpe_settings.delta_unit, all_pairs=self.rpe_settings.all_pairs)
        self.rpe_metric.process_data(data)
        if err_type is not None:
            stat_type = self.__statisticsType(err_type)
            rpe_stat = self.rpe_metric.get_statistic(stat_type)
            # print('RPE [',err_type,'] :',rpe_stat)
        

    def compute_ape(self, err_type=None):
        data = (self.traj_gt, self.traj_est)
        self.ape_metric = metrics.APE(self.pose_relation)
        self.ape_metric.process_data(data)
        if err_type is not None:
            stat_type = self.__statisticsType(err_type)
            ape_stat = self.ape_metric.get_statistic(stat_type)
            # print('APE [',err_type,'] :',ape_stat)

    def compute_stats(self):
        self.compute_rpe()
        self.compute_ape()
        self.rpe_stats = self.rpe_metric.get_all_statistics()
        self.ape_stats = self.ape_metric.get_all_statistics()
        # print('RPE: ', self.rpe_stats)
        # print('APE: ', self.ape_stats)

class Results():
    def __init__(self, results_path, export_path, dataset_path):
        # Define paths
        self.input_path = results_path
        self.output_path = os.path.join(export_path, os.path.basename(self.input_path))
        os.makedirs(self.output_path , exist_ok=True)
        
        # Get results data
        parser = jrl.Parser()
        results_path = os.path.join(self.input_path, 'final_results.jrr.cbor')
        self.results = parser.parseResults(results_path, True)

        # Should be temporary
        self.dataset = parser.parseDataset(dataset_path, False)

    def generate_intermediate_results(self):
        # Generate folder
        folder = 'intermediate'
        self.intermediate_path = os.path.join(self.output_path, folder)

        # Save grountruth and estimates data
        for rid in self.results.robots:
            path_rid = os.path.join(self.intermediate_path, rid)
            os.makedirs(path_rid , exist_ok=True)

            gt_fname = os.path.join(path_rid, rid + '_groundtruth.txt')
            est_fname = os.path.join(path_rid, rid + '_estimates.txt')
            init_fname = os.path.join(path_rid, rid + '_initialization.txt')

            f_es = open(est_fname,'w')
            f_gt = open(gt_fname,'w')
            f_init = open(init_fname,'w')

            f_es.write("# time x y z qx qy qz qw\n")
            f_gt.write("# time x y z qx qy qz qw\n")
            f_init.write("# time x y z qx qy qz qw\n")
            
            estimates = self.results.robot_solutions[rid].values
            groundtruths = self.dataset.groundTruth(rid)
            initializations = self.dataset.initialization(rid)
            
            pose_num = 0
            key = gtsam.symbol(rid, pose_num)

            while key in estimates.keys() and key in groundtruths.keys() and key in initializations.keys():

                # Export estimates
                line = self.__format_dataline(pose_num, estimates.atPose3(key))
                f_es.write(' '.join(map(str, line)) + '\n')

                # Export groundtruth
                line = self.__format_dataline(pose_num, groundtruths.atPose3(key))
                f_gt.write(' '.join(map(str, line)) + '\n')
                
                # Export initialization
                line = self.__format_dataline(pose_num, initializations.atPose3(key))
                f_init.write(' '.join(map(str, line)) + '\n')
            
                # Next key
                pose_num += 1
                key = gtsam.symbol(rid, pose_num)
        
        # Print generated intermediate results
    
    def generate_metrics_results(self):

        # Generate folder
        folder = 'metrics'
        self.metrics_path = os.path.join(self.output_path, folder)
        os.makedirs(self.metrics_path , exist_ok=True)

        # Chemin du fichier JSON
        metrics_path = os.path.join(self.metrics_path, 'translation_ape.json')
        raw_errors_path = os.path.join(self.metrics_path, 'raw_errors.json')

        data = self.__get_metrics('translation', 'APE')
        # Enregistrer les données dans un fichier JSON
        with open(metrics_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

        # Enregistrer les données dans un fichier JSON
        with open(raw_errors_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    def generate_summary_file(self):
        summary_path = os.path.join(self.output_path , 'summary.txt')
        f_summary = open(summary_path,'w')

        f_summary.write(f'Dataset name : {self.results.dataset_name}\n')
        f_summary.write(f'Solver method : {self.results.method_name}\n')

    def generate_raw_errors_file(self):
        print("not implemented")

    def __format_dataline(self, pose_nr, val):
        tr = val.translation()
        quat = val.rotation().toQuaternion()
        return [pose_nr, tr.T[0], tr.T[1], tr.T[2], quat.x(), quat.y(),quat.z(), quat.w()]

    def __get_metrics(self, pose_type, error_type, init=False):
        data = {}

        for rid in self.results.robots:
            
            if init:
                input_path = os.path.join(self.intermediate_path, rid, rid + '_initialization.txt')
            else:
                input_path = os.path.join(self.intermediate_path, rid, rid + '_estimates.txt')
            gt_path = os.path.join(self.intermediate_path, rid, rid + '_groundtruth.txt')
            
            index = 'Robot ' + rid
            
            # Get pose errors
            metrics = Metrics(input_path, gt_path)
            metrics.set_poseRelation(pose_type)
            metrics.compute_stats()
            if error_type == 'APE':
                data[index] = metrics.ape_stats
            elif error_type == 'RPE':
                data[index] = metrics.rpe_stats
            else:
                raise ValueError("Unknown error type")
            # translation
            
            # transformation
            # transformation = {}
            # metrics = Metrics(est_path, gt_path)
            # metrics.set_poseRelation('transformation')
            # metrics.compute_stats()
            # transformation['APE'] = metrics.ape_stats
            # transformation['RPE'] = metrics.rpe_stats

            # # rotation
            # rotation = {}
            # metrics = Metrics(est_path, gt_path)
            # metrics.set_poseRelation('rotation')
            # metrics.compute_stats()
            # rotation['APE'] = metrics.ape_stats
            # rotation['RPE'] = metrics.rpe_stats

            # # rot_angle_deg
            # rot_angle_deg = {}
            # metrics = Metrics(est_path, gt_path)
            # metrics.set_poseRelation('rot_angle_deg')
            # metrics.compute_stats()
            # rot_angle_deg['APE'] = metrics.ape_stats
            # rot_angle_deg['RPE'] = metrics.rpe_stats

            # # rot_angle_rad
            # rot_angle_rad = {}
            # metrics = Metrics(est_path, gt_path)
            # metrics.set_poseRelation('rot_angle_rad')
            # metrics.compute_stats()
            # rot_angle_rad['APE'] = metrics.ape_stats
            # rot_angle_rad['RPE'] = metrics.rpe_stats

            # # point_distance
            # point_distance = {}
            # metrics = Metrics(est_path, gt_path)
            # metrics.set_poseRelation('point_distance')
            # metrics.compute_stats()
            # point_distance['APE'] = metrics.ape_stats
            # point_distance['RPE'] = metrics.rpe_stats

        return data

        
    # Error numbers
    # print(self.ape_metric.error)
    # print(self.rpe_metric.error)