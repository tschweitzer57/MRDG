# General librairies
import os
from pathlib import Path
import shutil
import re
import sys
import glob
import json
import numpy as np
from collections import defaultdict

# Third party librairies
import jrl
import gtsam

# Custom librairies
from metrics import Metrics

# class DatasetGroup(): # Fusionner à results3
#     def __init__(self, solver, dataset, result_path, dataset_path):
#         self.solver = solver
#         self.dataset = dataset
#         self.result_path = result_path
#         self.dataset_path = dataset_path

class ResultsGroup():
    def __init__(self, solvers, results_folders, dataset_folders):
        self.solvers = solvers
        self.results_paths = self.__get_results_paths(results_folders)
        self.dataset_paths = self.__get_dataset_paths(dataset_folders)
        
        # Associate all results to dataset
        self.results = self.__group_all_results()
        self.sorted_results = self.group_by_solvers()
        
    def group_by_solvers(self):
        sorted_results = {}
        
        # initialize dict
        for solver in self.solvers:
            sorted_results[solver] = []
            
        for result3 in self.results:
            sorted_results[result3.solver].append(result3)
        
        return sorted_results

    def group_scenario(self):
        sorted_results = {}
        
        # initialize dict
        for solver in self.solvers:
            sorted_results[solver] = []
            
        for result3 in self.results:
            sorted_results[result3.solver].append(result3)
        
        return sorted_results
    
    def __group_all_results(self):
        # Sort by name length descending: longer names are more specific and match first,
        # preventing "edge_5" from matching inside "edge_55" folders.
        dataset_info = sorted(
            [(os.path.splitext(os.path.basename(p))[0], p) for p in self.dataset_paths],
            key=lambda x: len(x[0]),
            reverse=True
        )
        solvers_sorted = sorted(self.solvers, key=len, reverse=True)

        # Pre-compile all patterns once, reused across every result_path
        _pat = lambda name: re.compile(r'(?<![a-zA-Z0-9])' + re.escape(name) + r'(?![a-zA-Z0-9])')
        dataset_patterns = [(name, path, _pat(name)) for name, path in dataset_info]
        solver_patterns  = [(solver, _pat(solver)) for solver in solvers_sorted]

        dataGroups = []
        for result_path in self.results_paths:
            basename = os.path.basename(result_path.rstrip('/'))

            matched_dataset = next(
                ((name, path) for name, path, pat in dataset_patterns if pat.search(basename)),
                None
            )
            matched_solver = next(
                (solver for solver, pat in solver_patterns if pat.search(basename)),
                None
            )

            if matched_dataset and matched_solver:
                dataGroups.append(Results3(
                    matched_solver, matched_dataset[0], result_path, matched_dataset[1]
                ))

        return dataGroups
    
    def __get_dataset_paths(self, paths):
        file_paths = []
        for folder_path in paths:
            file_paths_sample = glob.glob(os.path.join(folder_path, '*.jrl'))
            file_paths += file_paths_sample
        return file_paths
    
    def __get_results_paths(self, paths):
        file_paths = []
        for folder_path in paths:
            file_paths_sample = glob.glob(os.path.join(folder_path, '*/'))
            file_paths += file_paths_sample
        return file_paths
    
    def __str__(self):
        
        out_str = f'Results - Dataset associations:\n\n'
        
        for d in data:
            out_str += f'{d.path_results}:\n {d.solver}, {d.dataset_name}\n\n'
        return out_str
        
class Results3():
    def __init__(self, solver, dataset_name, results_path, dataset_path):
        # Identification data
        self.dataset_name = dataset_name
        self.solver = solver

        # paths
        self.path_results = results_path
        self.path_iterations = self.__get_iteration_paths()
        self.path_dataset = dataset_path
        self.path_cache = os.path.join('./cache', os.path.basename(self.path_results.rstrip('/')))

        # Métriques à calculer
        self.metrics_ae_ptdist = {}
        self.metrics_ae_rotdeg = {}
        self.metrics_re_ptdist = {}
        self.metrics_re_rotdeg = {}
        self.metrics_consensus = {}
        
        # Utilities
        self.__parser = jrl.Parser()
        self.__results = None
        self.__iterationNb = None
        self.__dataset = None

        # Intermediate folders -> dict['est'][rid]:path
        self.__gtrPathCache = None
        self.__iniPathCache = None
        self.__estPathCache = None
    
    def compute_metrics(self):
        self.__get_dataset_data()
        for path in self.path_iterations:
            self.__update_results(path)
            self.__generate_intermediate_results()
            self.__get_metrics('mean')
            self.__get_consensus()
            if self.__iterationNb > 50:
                break
    
    def __update_results(self, path):
        self.__results = self.__parser.parseResults(path, True)
        self.__iterationNb = self.__get_itaration_nb(path)
        
    def __get_iteration_paths(self):
        iterations_dir = os.path.join(self.path_results, 'iterations')
        if not os.path.isdir(iterations_dir):
            return []
        return sorted(glob.glob(os.path.join(iterations_dir, '*')))
    
    def __get_dataset_data(self):
        # Dataset data
        self.__dataset = self.__parser.parseDataset(self.path_dataset, False)
        
    def __get_shared_variables(self):
        occurences = defaultdict(list)
        for rid in self.__results.robots:
            for key in self.__results.robot_solutions[rid].values.keys():
                occurences[key].append(rid)
        return {key: rids for key, rids in occurences.items() if len(rids) > 1}

    def __get_consensus(self):
        if self.__iterationNb == 0:
            self.shared_variables = self.__get_shared_variables()

        self.metrics_consensus[self.__iterationNb] = {}
        errors_g = []
        errors_l = []
        for key, rids in self.shared_variables.items():
            vals = [self.__results.robot_solutions[rid].values for rid in rids]
            is_landmark = chr(gtsam.Symbol(key).chr()) == '#'
            errors_k = []

            for i in range(len(rids)):
                for j in range(i + 1, len(rids)):
                    if is_landmark:
                        err = np.linalg.norm(vals[i].atPoint3(key) - vals[j].atPoint3(key))
                        errors_l.append(err)
                    else:
                        err = np.linalg.norm(vals[i].atPose3(key).translation() - vals[j].atPose3(key).translation())
                    errors_g.append(err)
                    errors_k.append(err)
            
            self.metrics_consensus[self.__iterationNb][key] = np.mean(errors_k)
        self.metrics_consensus[self.__iterationNb]['all'] = np.mean(errors_g) if errors_g else 0.0
        self.metrics_consensus[self.__iterationNb]['landmarks'] = np.mean(errors_l) if errors_l else 0.0


    def __generate_intermediate_results(self): # Eviter de réécrire gt et init
        
        # Generate folder architecture
        if os.path.isdir(self.path_cache):
            shutil.rmtree(self.path_cache)
        self.__estPathCache = os.path.join(self.path_cache, 'est/')
        self.__iniPathCache = os.path.join(self.path_cache, 'ini/')
        self.__gtrPathCache = os.path.join(self.path_cache, 'gtr/')
        
        os.makedirs(self.__estPathCache)
        os.makedirs(self.__iniPathCache)
        os.makedirs(self.__gtrPathCache)

        # Save grountruth and estimates data
        for rid in self.__results.robots:

            gt_fname = os.path.join(self.__gtrPathCache, rid + '_groundtruth.txt')
            est_fname = os.path.join(self.__estPathCache, rid + '_estimates.txt')
            init_fname = os.path.join(self.__iniPathCache, rid + '_initialization.txt')

            f_es = open(est_fname,'w')
            f_gt = open(gt_fname,'w')
            f_init = open(init_fname,'w')

            f_es.write("# time x y z qx qy qz qw\n")
            f_gt.write("# time x y z qx qy qz qw\n")
            f_init.write("# time x y z qx qy qz qw\n")
            
            estimates = self.__results.robot_solutions[rid].values
            groundtruths = self.__dataset.groundTruth(rid)
            initializations = self.__dataset.initialization(rid)
            
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

    def __get_metrics(self, statistic_type):
        temp_ape_ptdist = []
        temp_rpe_ptdist = []
        temp_ape_deg = []
        temp_rpe_deg = []

        for rid in self.__results.robots:
            gt_file = os.path.join(self.__gtrPathCache, rid + '_groundtruth.txt')
            input_file = os.path.join(self.__estPathCache, rid + '_estimates.txt')
            init_file = os.path.join(self.__iniPathCache, rid + '_initialization.txt')

            metrics = Metrics(input_file, gt_file)
            metrics.set_poseRelation('point_distance')
            metrics.compute_stats()
            temp_ape_ptdist.append(metrics.compute_ape(err_type=statistic_type))
            temp_rpe_ptdist.append(metrics.compute_rpe(err_type=statistic_type))
            metrics.set_poseRelation('rot_angle_deg')
            metrics.compute_stats()
            temp_ape_deg.append(metrics.compute_ape(err_type=statistic_type))
            temp_rpe_deg.append(metrics.compute_rpe(err_type=statistic_type))
        
        # Save iteration data
        self.metrics_ae_ptdist[self.__iterationNb] = np.mean(temp_ape_ptdist)
        self.metrics_ae_rotdeg[self.__iterationNb] = np.mean(temp_ape_deg)
        self.metrics_re_ptdist[self.__iterationNb] = np.mean(temp_rpe_ptdist)
        self.metrics_re_rotdeg[self.__iterationNb] = np.mean(temp_rpe_deg)
        
    
    def __format_dataline(self, pose_nr, val):
        tr = val.translation()
        quat = val.rotation().toQuaternion()
        return [pose_nr, tr.T[0], tr.T[1], tr.T[2], quat.x(), quat.y(),quat.z(), quat.w()]

    def __get_itaration_nb(self, path):
        return int(Path(path).name.split('.')[0])
    
    def __get_jrr_name(self, iteration):
        file_name = '0'*(12-len(str(iteration))) + str(iteration) + '.jrr.cbor'
        return file_name

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

        # Get shared variables
        self.__get_shared_variables()

    def __get_shared_variables(self):
        occurences = defaultdict(list)

        for rid in self.robots:
            for key in self.iteration_results[0].robot_solutions[rid].values.keys():
                occurences[key].append(rid)
        
        self.shared_variables = {key: value for key, value in occurences.items() if len(value) > 1}

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
        error = defaultdict(list)

        # Get data
        for iteration in self.iteration_results.keys():
            for edge in self.comm_edges:
                estimation_1 = self.iteration_results[iteration].robot_solutions[edge[0]].values.atPoint3(key)
                estimation_2 = self.iteration_results[iteration].robot_solutions[edge[1]].values.atPoint3(key)
                error[edge].append(np.linalg.norm(estimation_1 - estimation_2))

        return error

    def get_mean_consensus_all_lk(self):
        """Mean consensus error per edge, averaged over all shared Point3 (#) landmarks.

        Only pairs where both robots actually hold the landmark at a given iteration
        contribute to the average. Returns {} if no shared landmarks exist.
        """
        lk_keys = [k for k in self.shared_variables
                   if chr(gtsam.Symbol(k).chr()) == '#']
        if not lk_keys:
            return {}

        n_iter = len(self.iteration_results)
        sorted_iters = sorted(self.iteration_results.keys())

        acc   = defaultdict(lambda: np.zeros(n_iter))
        count = defaultdict(lambda: np.zeros(n_iter))

        for key in lk_keys:
            for it_idx, iteration in enumerate(sorted_iters):
                for edge in self.comm_edges:
                    v1 = self.iteration_results[iteration].robot_solutions[edge[0]].values
                    v2 = self.iteration_results[iteration].robot_solutions[edge[1]].values
                    if key in v1.keys() and key in v2.keys():
                        acc[edge][it_idx]   += np.linalg.norm(v1.atPoint3(key) - v2.atPoint3(key))
                        count[edge][it_idx] += 1

        return {
            edge: np.where(count[edge] > 0, acc[edge] / count[edge], 0.0).tolist()
            for edge in acc
        }

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
                        
    def __get_jrr_name(self, iteration):
        file_name = '0'*(12-len(str(iteration))) + str(iteration) + '.jrr.cbor'
        return file_name

    def generate_summary_file(self):
        summary_path = os.path.join(self.output_path , 'summary.txt')
        f_summary = open(summary_path,'w')

        f_summary.write(f'Dataset name : {self.results.dataset_name}\n')
        f_summary.write(f'Solver method : {self.results.method_name}\n')

    
    


    