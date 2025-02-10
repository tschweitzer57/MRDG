import gtsam
from gtsam import Pose3, Rot3
from functools import partial
import numpy as np
from typing import List, Optional
    
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

biased_factor_graph = gtsam.NonlinearFactorGraph()

# Add two odometry factors
odometry = gtsam.Pose3(Rot3.RzRyRx(0.0, 0.0, 0.0), gtsam.Point3(2.0,0.0,0.0))
odometry_noise = gtsam.noiseModel.Diagonal.Sigmas([0.2, 0.2, 0.2, 0.1, 0.1, 0.1])
biased_factor_graph.add(gtsam.BetweenFactorPose3(1, 2, odometry, odometry_noise))
biased_factor_graph.add(gtsam.BetweenFactorPose3(2, 3, odometry, odometry_noise))

robot_estimates = gtsam.Values()
robot_estimates.insert(1, gtsam.Pose3(Rot3.RzRyRx(0.0, 0.0, 0.0), gtsam.Point3(0.0,0.0,0.0)))
robot_estimates.insert(2, gtsam.Pose3(Rot3.RzRyRx(0.0, 0.0, 0.0), gtsam.Point3(2.0,0.0,0.0)))
robot_estimates.insert(3, gtsam.Pose3(Rot3.RzRyRx(0.0, 0.0, 0.0), gtsam.Point3(4.0,0.0,0.0)))

shared_estimate = gtsam.Pose3(Rot3.RzRyRx(0.0, 0.0, 0.0), gtsam.Point3(2.0,2.0,0.0))
#shared_estimate.insert(4, gtsam.Pose3(Rot3.RzRyRx(0.0, 0.0, 0.0), gtsam.Point3(2.0,2.0,0.0)))

biased_factor = gtsam.CustomFactor(gtsam.noiseModel.Gaussian.Information(np.eye(6,6)), 
                                   [2],
                                   partial(error_geodesic_biased_prior, np.zeros(6), 1.0, shared_estimate))
biased_factor_graph.add(biased_factor)

# Optimize and update relevant info
print("Biased Prior :")
print(gtsam.noiseModel.Gaussian.Information(np.eye(6,6)))
print(np.zeros(6))

optimizer = gtsam.LevenbergMarquardtOptimizer(biased_factor_graph, robot_estimates)
robot_estimates = optimizer.optimize()

# z = gtsam.Pose3(Rot3.RzRyRx(0.0, 0.0, 0.0), gtsam.Point3(0.0,0.0,0.0))
# p = gtsam.Pose3(Rot3.RzRyRx(0.1, 0.2, 0.3), gtsam.Point3(1.0,1.0,1.0))

# print(z.localCoordinates(p))
# robot_base_marginals = gtsam.Marginals(robot_determined_graphs[rid], robot_estimates[rid])

# def computeNewDualPose(self, dual, beta, p, z):
#         return dual + beta * z.localCoordinates(p)

# size_t d = gtsam::traits<POSE_TYPE>::GetDimension(pa);
#     return std::make_pair(solution_z, gtsam::Matrix::Identity(d, d)); np.eye(6,6)

