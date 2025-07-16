# General librairies
import os
import glob
import json
import numpy as np

# Third party librairies
import jrl
import gtsam

# Custom librairies
from metrics import Metrics

class Data():
    def __init__(self, Results):
        # initialize structure
        self.groundtruths = {}
        self.initializations = {}
        self.estimates = {}

        # Extracct data from Results
        self.robots = Results.dataset.robots()
        self.errors = Results.get_errors('base')

        for rid in self.robots:
            self.groundtruths[rid] = Results.dataset.groundTruth(rid)
            self.initializations[rid] = Results.dataset.initialization(rid)
            self.estimates[rid] = Results.results.robot_solutions[rid].values

class Results2():
    def __init__(self, results_path, dataset_path, export_path):
        # Register paths
        self.results_folder = results_path
        self.output_folder = os.path.join(export_path, os.path.basename(self.results_folder))
        os.makedirs(self.output_folder , exist_ok=True)

        # Get dataset data [Temporary]
        parser = jrl.Parser()
        self.dataset = parser.parseDataset(dataset_path, False)
        self.robots = self.dataset.robots()
        self.comm_edges = self.__get_comm_edges()

        # Get results data
        self.final_results = None
        self.iteration_results = {}

        final_results_path = os.path.join(self.results_folder, 'final_results.jrr.cbor')
        iteration_results_path = os.path.join(self.results_folder, 'iterations')

        if os.path.exists(final_results_path):
            self.final_results = parser.parseResults(final_results_path, True)
        if os.path.exists(iteration_results_path):
            iteration_paths = sorted(glob.glob(os.path.join(iteration_results_path, '*.jrr.cbor')))
            for path in iteration_paths:
                self.iteration_results[self.__get_iteration_step(path)] = parser.parseResults(path, True)

    def get_gtlk_error(self, lnumber):
        key = gtsam.symbol('#', lnumber)
        error = {}

        # Initialize structure
        for rid in self.dataset.robots():
            error[rid] = []

        # Get data
        for iteration in self.iteration_results.keys():
            for rid in self.dataset.robots():
                estimation = self.iteration_results[iteration].robot_solutions[rid].values.atPoint3(key)
                gt = self.dataset.groundTruth(rid).atPoint3(key)
                error[rid].append([iteration,np.linalg.norm(gt - estimation)])

        return error
    
    def get_consensuslk_error(self, lnumber):
        key = gtsam.symbol('#', lnumber)
        error = {}

        # Initialize structure
        for edge in self.comm_edges:
            error[edge] = []

        # Get data
        for iteration in self.iteration_results.keys():
            for edge in self.comm_edges:
                estimation_1 = self.iteration_results[iteration].robot_solutions[edge[0]].values.atPoint3(key)
                estimation_2 = self.iteration_results[iteration].robot_solutions[edge[1]].values.atPoint3(key)
                error[edge].append(np.linalg.norm(estimation_1 - estimation_2))
        
        return error

    def __get_comm_edges(self):
        edges = set()
        for rid in self.robots:
            for oid in self.robots:
                if rid != oid:
                    edge = (min(rid,oid),max(rid,oid))
                    edges.add(edge)
        return edges

    def __get_iteration_step(self, path):
        return int(os.path.splitext(os.path.splitext(os.path.basename(path))[0])[0])

class Results():
    def __init__(self, results_path, dataset_path, export_path, iteration='final', init=False):
        # Define paths
        self.input_path = results_path
        self.output_path = os.path.join(export_path, os.path.basename(self.input_path))
        os.makedirs(self.output_path , exist_ok=True)
        
        # Get results data
        parser = jrl.Parser()
        if iteration == 'final':
            results_path = os.path.join(self.input_path, 'final_results.jrr.cbor')
        else:
            results_path = os.path.join(self.input_path, 'iterations',self.__get_jrr_name(iteration))
            print(results_path)
        self.results = parser.parseResults(results_path, True)

        # Define init option
        self.init_opt = init

        # Should be temporary
        self.dataset = parser.parseDataset(dataset_path, False)
        
        # Define all attributes used
        self.errors = None

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

    def export_results(self, rng='base'):
        """ Saves errors in metrics folder
        Args:
            rng (str, optional): _description_. Defaults to 'base'.
        Raises:
            ValueError: _description_
        """
    
        if rng == 'base':
            self.generate_summary_file()
            self.generate_intermediate_results()
            self.generate_metrics_results(minimal=True, export=True)
        elif rng == 'all':
            self.generate_summary_file()
            self.generate_intermediate_results()
            self.generate_metrics_results(minimal=False, export=True)
        else:
            raise ValueError('Unknown value for rng')

    def get_errors(self, rng='base'):
        # reduce amount of computation
        if rng == 'base':
            self.generate_intermediate_results()
            self.generate_metrics_results(minimal=True)
        elif rng == 'all':
            self.generate_intermediate_results()
            self.generate_metrics_results(minimal=False)
        return self.errors
    
    def generate_metrics_results(self, minimal=True, pose_types=None, export=False):

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

                metrics, errors = self.__get_metrics(pose_type, error_type, self.init_opt)
                self.errors[pose_type + '_' + error_type] = errors

                if export:
                    # Chemin des fichiers JSON
                    file_name = pose_type + '_' + error_type
                    metrics_path = os.path.join(self.metrics_path, file_name + '.json')
                    raw_errors_path = os.path.join(self.raw_metrics_path, file_name + '_raw.json')

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

    def __get_jrr_name(self, iteration):
        file_name = '0'*(12-len(str(iteration))) + str(iteration) + '.jrr.cbor'
        return file_name
    
    def __format_dataline(self, pose_nr, val):
        tr = val.translation()
        quat = val.rotation().toQuaternion()
        return [pose_nr, tr.T[0], tr.T[1], tr.T[2], quat.x(), quat.y(),quat.z(), quat.w()]

    def __get_metrics(self, pose_type, error_type, init):
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