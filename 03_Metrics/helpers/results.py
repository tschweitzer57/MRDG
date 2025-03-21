# General librairies
import os
import json

# Third party librairies
import jrl
import gtsam

# Custom librairies
from metrics import Metrics
from display import Display

class Data():
    def __init__(self):
        # initialize structure
        self.groundtruths = {}
        self.initializations = {}
        self.estimates = {}
        self.robots = Results.dataset.robots()
        self.errors = Results.errors

        for rid in self.robots:
            self.groundtruths[rid] = Results.dataset.groundTruth(rid)
            self.initializations[rid] = Results.dataset.initialization(rid)
            self.estimates[rid] = Results.results.robot_solutions[rid].values

class Results():
    def __init__(self, results_path, dataset_path, export_path):
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

    def export_all_results(self):
        self.generate_summary_file()
        self.generate_intermediate_results()
        self.generate_metrics_results(minimal=False)

    def export_base_results(self):
        self.generate_summary_file()
        self.generate_intermediate_results()
        self.generate_metrics_results()
    
    def generate_metrics_results(self, minimal=True, pose_types=None):

        # Generate folders
        folder = 'metrics'
        self.metrics_path = os.path.join(self.output_path, folder)
        self.raw_metrics_path = os.path.join(self.metrics_path, 'raw')
        os.makedirs(self.raw_metrics_path , exist_ok=True)

        # generate dict to store errors
        self.errors = {}

        if minimal:
            pose_types = ['transformation','rot_angle_deg','point_distance']
            error_types = ['ape','rpe']
        elif pose_types is not None:
            error_types = ['ape','rpe']
        else:
            pose_types = ['translation','transformation','rotation','rot_angle_deg','point_distance','rot_angle_rad']
            error_types = ['ape','rpe']

        for pose_type in pose_types:
            for error_type in error_types:
                
                # Chemin des fichiers JSON
                file_name = pose_type + '_' + error_type
                metrics_path = os.path.join(self.metrics_path, file_name + '.json')
                raw_errors_path = os.path.join(self.raw_metrics_path, file_name + '_raw.json')

                metrics, errors = self.__get_metrics(pose_type, error_type)
                self.errors[pose_type + '_' + error_type] = errors

                # Export metrics in JSON file
                with open(metrics_path, 'w', encoding='utf-8') as json_file:
                    json.dump(metrics, json_file, ensure_ascii=False, indent=4)

                # Export raw errors in JSON file
                with open(raw_errors_path, 'w', encoding='utf-8') as json_file:
                    json.dump(errors, json_file, ensure_ascii=False, indent=4)

    def generate_summary_file(self):
        summary_path = os.path.join(self.output_path , 'summary.txt')
        f_summary = open(summary_path,'w')

        f_summary.write(f'Dataset name : {self.results.dataset_name}\n')
        f_summary.write(f'Solver method : {self.results.method_name}\n')

    def __format_dataline(self, pose_nr, val):
        tr = val.translation()
        quat = val.rotation().toQuaternion()
        return [pose_nr, tr.T[0], tr.T[1], tr.T[2], quat.x(), quat.y(),quat.z(), quat.w()]

    def __get_metrics(self, pose_type, error_type, init=False):
        statistics = {}
        errors = {}

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
            if error_type == 'ape':
                statistics[index] = metrics.ape_stats
                errors[index] = metrics.ape_metric.error.tolist()
            elif error_type == 'rpe':
                statistics[index] = metrics.rpe_stats
                errors[index] = metrics.rpe_metric.error.tolist()
            else:
                raise ValueError("Unknown error type")

        return statistics, errors