import os
import sys
import jrl
import gtsam
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from gtsam.utils import plot
import seaborn as sns
from collections import defaultdict

from functools import partial
from typing import List, Optional

from helpers.parameters import MESAParameters

#TODO: dev getdim function
#TODO: check and / ou symbols

class distributed_Solver:
    def __init__(self, dataset_path):
        # Parse dataset
        parser = jrl.Parser()
        self.dataset = parser.parseDataset(dataset_path, False)
        self.colors = sns.color_palette("colorblind", len(self.dataset.robots()))

        # Initialize global variables
        self.robots = []
        self.robot_graphs = {}
        self.robot_estimates = {}
        self.robot_groundtruth = {}
        self.robot_initializations = {}
        self.robot_shared_variables = None
        self.robot_base_marginals = {}

        self.robot_determined_graphs = None
        self.robot_counts_since_last_comm = defaultdict(lambda: defaultdict(int))

        self.comm_network = None

        self.edge_beta_variables = {}
        self.edge_shared_noise_models = defaultdict(lambda: defaultdict(gtsam.noiseModel.Unit))
        self.edge_shared_estimates = {}
        self.edge_robot_dual_variables = defaultdict(lambda: defaultdict(lambda: defaultdict(np.ndarray)))
        self.edge_robot_lie_dual_variables = defaultdict(lambda: defaultdict(lambda: defaultdict(np.ndarray)))

        self.first_iterate = True

        self.norm_history = []
        self.converged = False

        self.params = MESAParams()
        self.set_geodesic()
    
    def set_geodesic(self):
        self.params.beta_init = 200.0
        self.params.beta_multipliers_increase = 1.0
        self.params.prior_shared_vars_on_indep_solve = True
        self.params.shared_var_prior_sigmas = np.array([2,2,2,1e2,1e2,1e2])
        self.params.z_compute_method ='INTERPOLATE_SPLIT'
        self.params.weight_z_compute = False
        self.params.dual_compute_target ='OTHER_ESTIMATE'

    def set_split(self):
        self.params.beta_init = 1.0
        self.params.beta_multipliers_increase = 1.0
        self.params.prior_shared_vars_on_indep_solve = True
        self.params.shared_var_prior_sigmas = np.array([2,2,2,1e2,1e2,1e2])
        self.params.z_compute_method ='INTERPOLATE_SPLIT'
        self.params.weight_z_compute = False
        self.params.dual_compute_target ='OTHER_ESTIMATE'

    def set_chordal(self):
        self.params.beta_init = 1.0
        self.params.beta_multipliers_increase = 1.0
        self.params.prior_shared_vars_on_indep_solve = True
        self.params.shared_var_prior_sigmas = np.array([2,2,2,1e2,1e2,1e2])
        self.params.z_compute_method ='INTERPOLATE_SPLIT'
        self.params.weight_z_compute = False
        self.params.dual_compute_target ='OTHER_ESTIMATE'
    
    def set_apxgeo(self):
        self.params.beta_init = 1.0
        self.params.beta_multipliers_increase = 1.0
        self.params.prior_shared_vars_on_indep_solve = True
        self.params.shared_var_prior_sigmas = np.array([2,2,2,1e2,1e2,1e2])
        self.params.z_compute_method ='INTERPOLATE_SPLIT'
        self.params.weight_z_compute = False
        self.params.dual_compute_target ='OTHER_ESTIMATE'

    def set_linear_geodesic(self):
        self.params.beta_init = 200
        self.params.beta_multipliers_increase = 1.0
        self.params.prior_shared_vars_on_indep_solve = True
        self.params.shared_var_prior_sigmas = np.array([2,2,2,1e2,1e2,1e2])
        self.params.z_compute_method ='INTERPOLATE_SPLIT'
        self.params.weight_z_compute = False
        self.params.dual_compute_target ='OTHER_ESTIMATE'

    def error_correct_prior(self, 
                            prior: gtsam.Pose3, 
                            this: gtsam.CustomFactor,
                            values: gtsam.Values,
                            jacobians: Optional[List[np.ndarray]]) -> np.ndarray:
        """Correct prior Factor error function
        :param prior: prior value, to be filled with `partial`
        :param this: gtsam.CustomFactor handle
        :param values: gtsam.Values
        :param jacobians: Optional list of Jacobians
        :return: the unwhitened error
        """
        key = this.keys()[0]
        estimate = values.atPose3(key)
        if jacobians is not None:
            jacobians[0] = -np.eye(6)
        return prior.localCoordinates(estimate)

    def error_geodesic_biased_prior(self,
                                    dual: np.ndarray, 
                                    beta: float,
                                    prior: gtsam.Pose3, 
                                    this: gtsam.CustomFactor, 
                                    values: gtsam.Values,
                                    jacobians: Optional[List[np.ndarray]]) -> np.ndarray:
        """Biased prior Factor error function
        :param measurement: GPS measurement, to be filled with `partial`
        :param this: gtsam.CustomFactor handle
        :param values: gtsam.Values
        :param jacobians: Optional list of Jacobians
        :return: the unwhitened error
        """
        key = this.keys()[0]
        estimate = values.atPose3(key)
        q = prior.localCoordinates(estimate)
        error = np.sqrt(beta) * (q + (dual/beta))
        if jacobians is not None:
            jacobians[0] = -np.sqrt(beta) * np.eye(6)
        return error

    def error_inverse_geodesic_biased_prior(self,
                                            dual: np.ndarray, 
                                            beta: float, 
                                            prior: gtsam.Pose3, 
                                            this: gtsam.CustomFactor, 
                                            values: gtsam.Values,
                                            jacobians: Optional[List[np.ndarray]]) -> np.ndarray:
        """Biased prior Factor error function
        :param prior: shared variable to be filled with `partial`
        :param this: gtsam.CustomFactor handle
        :param values: gtsam.Values
        :param jacobians: Optional list of Jacobians
        :return: the unwhitened error
        """
        key = this.keys()[0]
        estimate = values.atPose3(key)
        q = estimate.localCoordinates(prior)
        error = np.sqrt(beta) * (q + (dual/beta))
        if jacobians is not None:
            jacobians[0] = np.sqrt(beta) * np.eye(6)
        return error

    # def error_apxgeo_biased_prior(measurement: gtsam.Pose3, 
    #                               this: gtsam.CustomFactor,
    #                               values: gtsam.Values,
    #                               jacobians: Optional[List[np.ndarray]]) -> np.ndarray:
    # """Biased prior Factor error function
    # :param measurement: GPS measurement, to be filled with `partial`
    # :param this: gtsam.CustomFactor handle
    # :param values: gtsam.Values
    # :param jacobians: Optional list of Jacobians
    # :return: the unwhitened error
    # """
    # key = this.keys()[0]
    # val = values.atPose3(key)
    # q = val.Logmap(val) - measurement.Logmap(measurement)
    # error = np.sqrt(beta) * (q + (dual/beta))
    # if jacobians is not None:
    #     jacobians[0] = np.sqrt(beta) * jacobians[0]
    # return error

    # def error_inverse_apxgeo_biased_prior(measurement: gtsam.Pose3, 
    #                                       this: gtsam.CustomFactor,
    #                                       values: gtsam.Values,
    #                                       jacobians: Optional[List[np.ndarray]]) -> np.ndarray:
    # """Biased prior Factor error function
    # :param measurement: GPS measurement, to be filled with `partial`
    # :param this: gtsam.CustomFactor handle
    # :param values: gtsam.Values
    # :param jacobians: Optional list of Jacobians
    # :return: the unwhitened error
    # """
    # key = this.keys()[0]
    # val = values.atPose3(key)
    # q = measurement.Logmap(measurement) - val.Logmap(val)
    # error = np.sqrt(beta) * (q + (dual/beta))
    # if jacobians is not None:
    #     jacobians[0] = np.sqrt(beta) * jacobians[0]
    # return error

    def computeNewDualPose(self, dual, beta, p, z):
        return dual + beta * z.localCoordinates(p)

    def computeNewDualShared(self, dual, beta, p, z):
        return computeNewDualPose(dual,beta,p,z)

    def interpolate_SPLIT(self, pa: gtsam.Pose3, pb: gtsam.Pose3, alpha: float):
        # interpolate rotation spherically
        ra = pa.rotation()
        rb = pb.rotation()
        interp_rot = ra.compose(ra.Expmap(alpha * ra.Logmap(ra.inverse().compose(rb))))
        # interpolate rotation linearly
        ta = pa.translation()
        tb = pb.translation()
        interp_trans = ta + alpha * (tb - ta)

        return gtsam.Pose3(interp_rot,interp_trans)

    def interpolate_SLERP(self, pa: gtsam.Pose3, pb: gtsam.Pose3, alpha: float):
        return pa.retract(alpha * pa.localCoordinates(pb))

    def parse_communication_network(self):
        result = set()
        
        for rid in self.robots:
            for oid in self.robots:
                # If these two robots share any variables
                if len(self.robot_shared_variables[rid][oid]) > 0:
                    # Insert a tuple with the minimum and maximum robot id, ensuring uniqueness
                    result.add((min(rid, oid), max(rid, oid)))

        return list(result)

    def parse_shared_variables(self):
        # Result is a nested dictionary with a set as the innermost structure
        result = defaultdict(lambda: defaultdict(set))

        # Setup the structure
        for rid in self.robots:
            for oid in self.robots:
                result[rid][oid] = set()

        # Fill in the structure
        for rid in self.robots:
            for i in range(self.robot_graphs[rid].nrFactors()):
                factor = self.robot_graphs[rid].at(i)
                for key in factor.keys():
                    key_rid = chr(gtsam.Symbol(key).chr())  # Extract key's corresponding robot
                    if key_rid != rid:
                        result[rid][key_rid].add(key)
                        result[key_rid][rid].add(key)

        return result

    def constructDeterminedGraphs(self):
        determined_graphs = {}
        prior_shared_vars = self.params.prior_shared_vars_on_indep_solve
        shared_prior_sigmas = self.params.shared_var_prior_sigmas
        
        for rid in self.robots:
            determined_factor_graph = self.robot_graphs[rid].clone()

            if prior_shared_vars:
                seen_shared = set()
                for oid in self.robots:
                    for key in self.robot_shared_variables[rid][oid]:
                        if key not in seen_shared:
                            factor = gtsam.CustomFactor(gtsam.noiseModel.Isotropic.Sigmas(shared_prior_sigmas),
                                                        [key],
                                                        partial(self.error_correct_prior, self.robot_estimates[rid].atPose3(key)))
                            determined_factor_graph.add(factor)
                            seen_shared.add(key)
            determined_graphs[rid] = determined_factor_graph
        
        return determined_graphs

    def updateCountsSinceLastComm(self, current_edge):
        cond1 = self.robot_counts_since_last_comm[current_edge[0]][current_edge] >= len(self.robots) - 1
        cond2 = self.robot_counts_since_last_comm[current_edge[1]][current_edge] >= len(self.robots) - 1
        should_update_beta = cond1 and cond2
        
        for edge in self.communication_network:
            if (edge == current_edge and should_update_beta):
                self.robot_counts_since_last_comm[current_edge[0]][edge] = 0
                self.robot_counts_since_last_comm[current_edge[1]][edge] = 0
            else:
                self.robot_counts_since_last_comm[current_edge[0]][edge] += 1
                self.robot_counts_since_last_comm[current_edge[1]][edge] += 1

        return should_update_beta

    def updateConvergence(self, step_norm):

        # add step norm
        self.norm_history.append(step_norm)

        # if history is too long pop oldest
        if len(self.norm_history) > len(self.robots):
            self.norm_history.pop(0)

        if len(self.norm_history) == len(self.robots):
            total_norm = 0.0
            for sn in self.norm_history:
                total_norm += sn
                self.converged = total_norm / len(self.norm_history) <= self.params.convergence_threshold

    def computeNewZ(self, pa, dual_a, info_a, pb, dual_b, info_b, beta):
        if self.params.weight_z_compute:
            interp_weight = 1.0 - (np.linalg.norm(info_a) / (np.linalg.norm(info_a) + np.linalg.norm(info_b)))
            noise_model_a = gtsam.noiseModel.Gaussian.Information(info_a)
            noise_model_b = gtsam.noiseModel.Gaussian.Information(info_b)
        else: 
            interp_weight = 0.5
            noise_model_a = gtsam.noiseModel.Unit.Create(6)
            noise_model_b = gtsam.noiseModel.Unit.Create(6)

        # construct graph
        graph = gtsam.NonlinearFactorGraph()
        #graph.add(0, pa, noise_model_a, dual_a, beta)
        factor_a = gtsam.CustomFactor(noise_model_a, [0],
                                      partial(self.error_inverse_geodesic_biased_prior,
                                              dual_a, beta, pa))
        factor_b = gtsam.CustomFactor(noise_model_b, [0],
                                      partial(self.error_inverse_geodesic_biased_prior,
                                              dual_b, beta, pb))
        graph.add(factor_a)
        graph.add(factor_b)

        # Solve using configured method
        if self.params.z_compute_method == 'INTERPOLATE_SPLIT':
            solution_z = self.interpolate_SPLIT(pa, pb, interp_weight)
        elif self.params.z_compute_method == 'INTERPOLATE_SLERP':
            solution_z = self.interpolate_SLERP(pa, pb, interp_weight)
        elif self.params.z_compute_method == 'OPTIMIZE':
            initialization = gtsam.Values()
            init_z = self.interpolate_SLERP(pa, pb, interp_weight)
            initialization.insert(0, init_z)
            optimizer = gtsam.GaussNewtonOptimizer(graph, initialization)
            optimized = optimizer.optimize()
            solution_z = optimized.atPose3(0)

        # Compute the marginal
        solution_values = gtsam.Values()
        solution_values.insert(0, solution_z)
        optimized_marginal = gtsam.Marginals(graph, solution_values)

        # Return the optimized value and the corresponding marginal
        if self.params.weight_z_compute:
            return (solution_z, optimized_marginal.marginalInformation(0))
        else:
            return (solution_z, np.eye(6,6))

    def updateDualVariables(self, comm_edge):
        beta = self.edge_beta_variables[comm_edge]

        for shared_key in self.robot_shared_variables[comm_edge[0]][comm_edge[1]]:

            # Get poses for the 2 robots
            pa = self.robot_estimates[comm_edge[0]].atPose3(shared_key)
            pb = self.robot_estimates[comm_edge[1]].atPose3(shared_key)

            # Get dual variables for the 2 robots
            a_dual = self.edge_robot_dual_variables[comm_edge][comm_edge[0]].atVector(shared_key)
            b_dual = self.edge_robot_dual_variables[comm_edge][comm_edge[1]].atVector(shared_key)

            # Handle Choudhary special case
            if self.params.dual_compute_target == 'CHOUDHARY_TARGET':
                new_a_dual = self.computeNewDualPose(a_dual, beta, pa, pb)
                new_b_dual = -new_a_dual
            else:
                # Get the target for each of the robots using the configured method
                if self.params.dual_compute_target == 'SHARED_ESTIMATE':
                    dual_target_robot_a = self.edge_shared_estimates[comm_edge].atPose3(shared_key)
                    dual_target_robot_b = self.edge_shared_estimates[comm_edge].atPose3(shared_key)
                    # Compute the new dual estimate
                    new_a_dual = self.computeNewDualShared(a_dual, beta, pa, dual_target_robot_a)
                    new_b_dual = self.computeNewDualShared(b_dual, beta, pb, dual_target_robot_b)
                elif self.params.dual_compute_target == 'OTHER_ESTIMATE':
                    new_a_dual = self.computeNewDualPose(a_dual, beta, pa, pb)
                    new_b_dual = self.computeNewDualPose(b_dual, beta, pb, pa)
                elif self.params.dual_compute_target == 'UNWEIGHTED_SLERP':
                    slerp_z = self.interpolate_SLERP(pa, pb, 0.5)
                    new_a_dual = self.computeNewDualShared(a_dual, beta, pa, slerp_z)
                    new_b_dual = self.computeNewDualShared(b_dual, beta, pb, slerp_z)

            # Update the dual variables in memory
            self.edge_robot_dual_variables[comm_edge][comm_edge[0]].update(shared_key, new_a_dual)
            self.edge_robot_dual_variables[comm_edge][comm_edge[1]].update(shared_key, new_b_dual)

    def updateSharedVariables(self, comm_edge):
        for shared_key in self.robot_shared_variables[comm_edge[0]][comm_edge[1]]:
            value_info_pair = self.computeNewZ(self.robot_estimates[comm_edge[0]].atPose3(shared_key),
                                               self.edge_robot_dual_variables[comm_edge][comm_edge[0]].atVector(shared_key),
                                               self.robot_base_marginals[comm_edge[0]].marginalInformation(shared_key),
                                               self.robot_estimates[comm_edge[1]].atPose3(shared_key),
                                               self.edge_robot_dual_variables[comm_edge][comm_edge[1]].atVector(shared_key),
                                               self.robot_base_marginals[comm_edge[1]].marginalInformation(shared_key),
                                               self.edge_beta_variables[comm_edge])

            # Update/Insert data in edges variables
            if self.edge_shared_estimates[comm_edge].exists(shared_key):
                self.edge_shared_estimates[comm_edge].update(shared_key, value_info_pair[0])
            else:
                self.edge_shared_estimates[comm_edge].insert(shared_key, value_info_pair[0])
            self.edge_shared_noise_models[comm_edge][shared_key] = gtsam.noiseModel.Gaussian.Information(value_info_pair[1])

    def updateRobotEstimateAndMarginals(self, rid):
        biased_factor_graph = gtsam.NonlinearFactorGraph()
        biased_factor_graph.push_back(self.robot_graphs[rid])

        for oid in self.robots:
            comm_robots = (min(rid, oid), max(rid, oid))

            for sk in self.robot_shared_variables[rid][oid]:
                print("Biased Prior :")
                print(self.edge_shared_noise_models[comm_robots][sk])
                print([sk])
                print(self.edge_robot_dual_variables[comm_robots][rid].atVector(sk))
                print(self.edge_beta_variables[comm_robots])
                print(self.edge_shared_estimates[comm_robots].atPose3(sk))
                sys.exit()

                biased_factor = gtsam.CustomFactor(self.edge_shared_noise_models[comm_robots][sk], 
                                                   [sk],
                                                   partial(self.error_geodesic_biased_prior,
                                                           self.edge_robot_dual_variables[comm_robots][rid].atVector(sk),
                                                           self.edge_beta_variables[comm_robots], 
                                                           self.edge_shared_estimates[comm_robots].atPose3(sk)))
                biased_factor_graph.push_back(biased_factor)

        # Optimize and update relevant info
        optimizer = gtsam.LevenbergMarquardtOptimizer(biased_factor_graph, self.robot_estimates[rid])
        self.robot_estimates[rid] = optimizer.optimize()
        self.robot_base_marginals[rid] = gtsam.Marginals(self.robot_determined_graphs[rid], self.robot_estimates[rid])

    def performCommunicationStep(self, comm_robots):
        print("Run step: ",comm_robots[0] , " - ", comm_robots[1])

        should_update_beta = self.updateCountsSinceLastComm(comm_robots)

        # x-update (local optimization) : step 1
        self.updateRobotEstimateAndMarginals(comm_robots[0])
        self.updateRobotEstimateAndMarginals(comm_robots[1])

        # z-update (local information) : step 2
        self.updateSharedVariables(comm_robots)

        # dual variable update : step 3
        self.updateDualVariables(comm_robots)

        # beta variable update : step 4
        if (not self.params.pseudo_sync_beta or should_update_beta):
            self.edge_beta_variables[comm_robots] *= self.params.beta_multipliers_increase

    def init(self):
        # Get dataset data for all robots in the dataset
        for robot in self.dataset.robots():
            self.robot_graphs[robot] = gtsam.NonlinearFactorGraph()
            self.robot_estimates[robot] = self.dataset.initialization(robot)
            self.robot_initializations[robot] = self.dataset.initialization(robot)
            self.robot_groundtruth[robot] = self.dataset.groundTruth(robot)
            self.robots.append(robot)

            for entry in self.dataset.measurements(robot):
                self.robot_graphs[robot].push_back(entry.measurements)

        # Initialize shared variables -> shared_variables
        self.robot_shared_variables = self.parse_shared_variables()

        # Initialize communication Network -> comm_network
        self.communication_network = self.parse_communication_network()

        # Generate distribution over communication edges -> communication_edge_distribution
        # No required init and global for python -> cf iterate

        # Initialize determined graphs -> robot_determined_graphs
        self.robot_determined_graphs = self.constructDeterminedGraphs()

        # Initialize counts since last communication
        for rid in self.robots:
            for edge in self.communication_network:
                self.robot_counts_since_last_comm[rid][edge] = 0

        # Populate edge counts, beta variables, shared_estimates, dual variables
        for comm_edge in self.communication_network:
            self.edge_beta_variables[comm_edge] = self.params.beta_init
            self.edge_shared_estimates[comm_edge] = gtsam.Values()

            self.edge_robot_dual_variables[comm_edge][comm_edge[0]] = gtsam.Values()
            self.edge_robot_dual_variables[comm_edge][comm_edge[1]] = gtsam.Values()

            self.edge_robot_lie_dual_variables[comm_edge][comm_edge[0]] = gtsam.Values()
            self.edge_robot_lie_dual_variables[comm_edge][comm_edge[1]] = gtsam.Values()

            for sk in self.robot_shared_variables[comm_edge[0]][comm_edge[1]]:
                dim = 6

                dual_first = np.zeros(dim)
                dual_second = np.zeros(dim)

                # Initialize the variant's dual variables
                self.edge_robot_dual_variables[comm_edge][comm_edge[0]].insert(sk, dual_first)
                self.edge_robot_dual_variables[comm_edge][comm_edge[1]].insert(sk,dual_second)

                # Initialize the Lie formulation dual variables for computing the dual residual
                self.edge_robot_lie_dual_variables[comm_edge][comm_edge[0]].insert(sk, dual_first)
                self.edge_robot_lie_dual_variables[comm_edge][comm_edge[1]].insert(sk, dual_second)

        # !Note! : Marginals, shared variables are initialized during first iterate

    def iterate(self):      
        # Save old estimates
        prev_estimates = self.robot_estimates

        # First iterate init
        if self.first_iterate:
            self.first_iterate = False

            # optimize for each robot individually
            for rid in self.robots:
                optimizer = gtsam.LevenbergMarquardtOptimizer(self.robot_determined_graphs[rid],self.robot_estimates[rid])
                self.robot_estimates[rid] = optimizer.optimize()

            # initialize marginals
            for rid in self.robots:
                self.robot_base_marginals[rid] = gtsam.Marginals(self.robot_determined_graphs[rid], self.robot_estimates[rid])

            # run a round of comm to init all shared estimates
            for comm_edge in self.communication_network:
                for shared_key in self.robot_shared_variables[comm_edge[0]][comm_edge[1]]:
                    key_owner = chr(gtsam.Symbol(shared_key).chr())

                    if key_owner == comm_edge[0]:
                        value = self.robot_estimates[comm_edge[0]].atPose3(shared_key)
                        self.robot_estimates[comm_edge[1]].update(shared_key, value)
                    else:
                        value = self.robot_estimates[comm_edge[1]].atPose3(shared_key)
                        self.robot_estimates[comm_edge[0]].update(shared_key, value)
            
                self.updateSharedVariables(comm_edge)

        # if not first iterate : get a random edge
        else:
            # Get a random edge
            n = np.random.randint(0, len(self.communication_network)-1)
            # Perform ADMM iteration over selected edge
            self.performCommunicationStep(self.communication_network[n])

        # check convergence
        norm = 0.0
        for rid in self.robots:
            norm += prev_estimates[rid].localCoordinates(self.robot_estimates[rid]).norm()
            print(norm)
        self.updateConvergence(norm)

    def solve(self):
        self.init()
        self.set_geodesic()
        while not self.converged:
            self.iterate()

    def save_results(self, folder_path):
        # Generate 3 files in folder path
        # -> Groundtruth
        # -> Estimates
        # -> Initializations
        # Format : time x y z qx qy qz qw
        os.makedirs(folder_path, exist_ok=True)

        for rid in self.robots:
            result_file = folder_path + '/' + 'resultsd_' + rid + '_' + self.dataset.name()
            gtFilename = result_file + '_groundtruth.txt'
            estFilename = result_file + '_estimates.txt'
            initFilename = result_file + '_init.txt'

            f_gt = open(gtFilename,'w')
            f_es = open(estFilename,'w')
            f_init = open(initFilename,'w')
            
            f_gt.write("# time x y z qx qy qz qw\n")
            f_es.write("# time x y z qx qy qz qw\n")
            f_init.write("# time x y z qx qy qz qw\n")

            stamp = 0

            for key in self.robot_groundtruth[rid].keys():
                if chr(gtsam.Symbol(key).chr()) == rid:
                    # Export groundtruth
                    tr = self.robot_groundtruth[rid].atPose3(key).translation()
                    quat = self.robot_groundtruth[rid].atPose3(key).rotation().toQuaternion()
                    line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
                    f_gt.write(' '.join(map(str, line)) + '\n')

                    # Export estimates
                    tr = self.robot_estimates[rid].atPose3(key).translation()
                    quat = self.robot_estimates[rid].atPose3(key).rotation().toQuaternion()
                    line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
                    f_es.write(' '.join(map(str, line)) + '\n')

                    # Export initilizations
                    tr = self.robot_initializations[rid].atPose3(key).translation()
                    quat = self.robot_initializations[rid].atPose3(key).rotation().toQuaternion()
                    line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
                    f_init.write(' '.join(map(str, line)) + '\n')

                    # Handle stamp
                    stamp += 1
                # else:
                #   do nothing with other robots poses

class centralized_Solver:
    def __init__(self, dataset_path):
        # Parse dataset
        parser = jrl.Parser()
        self.dataset = parser.parseDataset(dataset_path, False)
        self.robots = self.dataset.robots()
        self.colors = sns.color_palette("colorblind", len(self.robots))

        self.joint_graph = gtsam.NonlinearFactorGraph()
        self.joint_init = gtsam.Values()

        for rid in self.robots:
            for entry in self.dataset.measurements(rid):
                self.joint_graph.push_back(entry.measurements)
            
            for kvp in self.dataset.initialization(rid).keys():
                if not self.joint_init.exists(kvp):
                    if chr(gtsam.Symbol(kvp).chr()) == 'l':
                        self.joint_init.insert(kvp, self.dataset.initialization(rid).atPoint3(kvp))
                    else:
                        self.joint_init.insert(kvp, self.dataset.initialization(rid).atPose3(kvp))

        self.initializations = {}
        self.groundtruths = {}
        self.estimates = {}

    def solve(self):
        optimizer = gtsam.LevenbergMarquardtOptimizer(self.joint_graph, self.joint_init)
        joint_solution = optimizer.optimize()
        
        for rid in self.robots:
            self.groundtruths[rid] = self.dataset.groundTruth(rid)
            self.initializations[rid] = self.dataset.initialization(rid)
            self.estimates[rid] = gtsam.Values()

            for key in joint_solution.keys():
                if chr(gtsam.Symbol(key).chr()) == rid:
                    self.estimates[rid].insert(key, joint_solution.atPose3(key))

    def save_results(self, folder_path):
        # Generate 3 files in folder path
        # -> Groundtruth
        # -> Estimates
        # -> Initializations
        # Format : time x y z qx qy qz qw
        os.makedirs(folder_path, exist_ok=True)

        for rid in self.robots:
            result_file = folder_path + '/' + 'resultsc_' + rid + '_' + self.dataset.name()
            gtFilename = result_file + '_groundtruth.txt'
            estFilename = result_file + '_estimates.txt'
            initFilename = result_file + '_init.txt'

            f_gt = open(gtFilename,'w')
            f_es = open(estFilename,'w')
            f_init = open(initFilename,'w')
            
            f_gt.write("# time x y z qx qy qz qw\n")
            f_es.write("# time x y z qx qy qz qw\n")
            f_init.write("# time x y z qx qy qz qw\n")

            stamp = 0

            for key in self.groundtruths[rid].keys():
                if chr(gtsam.Symbol(key).chr()) == rid:
                    # Export groundtruth
                    tr = self.groundtruths[rid].atPose3(key).translation()
                    quat = self.groundtruths[rid].atPose3(key).rotation().toQuaternion()
                    line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
                    f_gt.write(' '.join(map(str, line)) + '\n')

                    # Export estimates
                    tr = self.estimates[rid].atPose3(key).translation()
                    quat = self.estimates[rid].atPose3(key).rotation().toQuaternion()
                    line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
                    f_es.write(' '.join(map(str, line)) + '\n')

                    # Export initilizations
                    tr = self.initializations[rid].atPose3(key).translation()
                    quat = self.initializations[rid].atPose3(key).rotation().toQuaternion()
                    line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
                    f_init.write(' '.join(map(str, line)) + '\n')

                    # Handle stamp
                    stamp += 1
                # else:
                #   do nothing with other robots poses

class separated_Solver:
    def __init__(self, dataset_path):
        # Parse dataset
        parser = jrl.Parser()
        self.dataset = parser.parseDataset(dataset_path, False)
        self.robots = self.dataset.robots()
        self.colors = sns.color_palette("colorblind", len(self.robots))

        self.graphs = {}
        self.initializations = {}
        self.groundtruths = {}
        self.estimates = {}
    
    def set_graph(self, rid):
        self.graphs[rid] = gtsam.NonlinearFactorGraph()

        for entry in self.dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                shared_factor = False
                for key in factor.keys():
                    key_rid = chr(gtsam.Symbol(key).chr())
                    if key_rid != rid:
                        shared_factor = True

                if not shared_factor:
                    self.graphs[rid].push_back(factor)

    def set_initialization(self, rid):
        self.initializations[rid] = self.dataset.initialization(rid)
        for key in self.initializations[rid].keys():
            key_rid = chr(gtsam.Symbol(key).chr())
            if key_rid != rid:
                self.initializations[rid].erase(key)

    def set_groundtruth(self, rid):
        self.groundtruths[rid] = self.dataset.groundTruth(rid)
        for key in self.groundtruths[rid].keys():
            key_rid = chr(gtsam.Symbol(key).chr())
            if key_rid != rid:
                self.groundtruths[rid].erase(key)

    def solve(self):
        for rid in self.robots:
            # Initialize graphs and initial values for each robot
            self.set_graph(rid)
            self.set_initialization(rid)
            self.set_groundtruth(rid)

            # Find results for each robot
            optimizer = gtsam.LevenbergMarquardtOptimizer(self.graphs[rid], self.initializations[rid])
            self.estimates[rid] = optimizer.optimize()

    def save_results(self, folder_path):
        # Generate 3 files in folder path
        # -> Groundtruth
        # -> Estimates
        # -> Initializations
        # Format : time x y z qx qy qz qw
        os.makedirs(folder_path, exist_ok=True)

        for rid in self.robots:
            result_file = folder_path + '/' + 'resultss_' + rid + '_' + self.dataset.name()
            gtFilename = result_file + '_groundtruth.txt'
            estFilename = result_file + '_estimates.txt'
            initFilename = result_file + '_init.txt'

            f_gt = open(gtFilename,'w')
            f_es = open(estFilename,'w')
            f_init = open(initFilename,'w')
            
            f_gt.write("# time x y z qx qy qz qw\n")
            f_es.write("# time x y z qx qy qz qw\n")
            f_init.write("# time x y z qx qy qz qw\n")

            stamp = 0

            for key in self.groundtruths[rid].keys():
                # Export groundtruth
                tr = self.groundtruths[rid].atPose3(key).translation()
                quat = self.groundtruths[rid].atPose3(key).rotation().toQuaternion()
                line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
                f_gt.write(' '.join(map(str, line)) + '\n')

                # Export estimates
                tr = self.estimates[rid].atPose3(key).translation()
                quat = self.estimates[rid].atPose3(key).rotation().toQuaternion()
                line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
                f_es.write(' '.join(map(str, line)) + '\n')

                # Export initilizations
                tr = self.initializations[rid].atPose3(key).translation()
                quat = self.initializations[rid].atPose3(key).rotation().toQuaternion()
                line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
                f_init.write(' '.join(map(str, line)) + '\n')

                # Handle stamp
                stamp += 1

if __name__ == "__main__":

    dataset = '../output/datasets/syscon25/pose_nb/pose_nb_6_0000.jrl'
    solver_d = distributed_Solver(dataset)
    solver_c = centralized_Solver(dataset)
    solver_s = separated_Solver(dataset)
    
    # solver_d.solve()
    # solver_d.save_results('../output/results')

    # solver_s.solve()
    # solver_s.save_results('../output/results')

    # solver_c.solve()
    # solver_c.save_results('../output/results')