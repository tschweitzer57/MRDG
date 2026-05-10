import os
import jrl
import gtsam
from gtsam import Rot3, Pose3
import numpy as np
from collections import defaultdict
from string import ascii_letters
from collections import defaultdict
from copy import copy
import random

from configuration import DatasetConfiguration

#TODO Extraire Landmarks / Groundtruth / Initialization / Noise sous forme de classes
#TODO transform gt var into simple gtsam.Values (dont require rid since there is a key)
#TODO init start point
#TODO add scenario add reset add save -> same dataset with different factors
#TODO add a mapping function generating a common map for trajectories and lks
#TODO améliorer intégration des random seed
#TODO Trouver un nouvel ordre de génération des mesures

class DatasetGenerator(jrl.DatasetBuilder):
    def __init__(self, config_path, output_dir=None):

        # Get configuration from config file
        self.config = DatasetConfiguration(config_path)
        self.config_file_path = config_path

        # Define output directory
        if output_dir is not None:
            self.output_dir = output_dir
        else:
            self.output_dir = self.__set_output_dir(config_path)
        # Define variables
        self.gt_poses = gtsam.Values()
        self.init_values = gtsam.Values()
        self.landmarks = gtsam.Values()

        self.odom = defaultdict(list)
        self.lk_measurements = defaultdict(list)
        self.lc_intra = defaultdict(list)
        self.lc_inter_direct_range = defaultdict(list)
        self.lc_inter_direct_pose = defaultdict(list)
        self.lc_inter_indirect = defaultdict(list)

        self.stamp = 0
        #self.pose_number = 0
        self.seen_keys = defaultdict(set)
        
        self.odom_choice = {}
        
        # Setup ID's for each robot
        n = self.config.trajectory['robots']
        self.robots = list(ascii_letters[:n])
        
        # Add robot to handle landmarks
        if self.config.landmarks is not None:
            self.landmarks = gtsam.Values()

        # Create jrl.DatasetBuilder
        super().__init__(self.config.name, self.robots)

        # Define noise models
        self.odom_noise_model = gtsam.noiseModel.Diagonal.Sigmas(
            self.config.sigmas['odom'])
        self.loop_noise_model = gtsam.noiseModel.Diagonal.Sigmas(
            self.config.sigmas['lc_intra'])
        self.pose_loop_noise_model = gtsam.noiseModel.Diagonal.Sigmas(
            self.config.sigmas['lc_inter_direct_pose'])
        self.range_loop_noise_model = gtsam.noiseModel.Diagonal.Sigmas(
            [self.config.sigmas['lc_inter_direct_range']])
        self.bearing_range_noise_model = gtsam.noiseModel.Diagonal.Sigmas(
            self.config.sigmas['landmarks'])

        # Define if dataset include outliers
        if self.config.outliers is not None:
            self.outliers = True
        else:
            self.outliers = False

        # Rotation matrices (NED)
        Rxp = Rot3(np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]))
        Rxn = Rot3(np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]))

        Ryp = Rot3(np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]))
        Ryn = Rot3(np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]))

        Rzp = Rot3(np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]))
        Rzn = Rot3(np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]))

        # GLOBALS
        self.ODOM_OPTIONS_GRIDWORLD = [
            Pose3(gtsam.Rot3.Identity(), np.array([1, 0, 0])),  # Move forward
            Pose3(Rzp, np.array([0, 0, 0])),  # Turn z    (90° Right)
            Pose3(Rzn, np.array([0, 0, 0])),  # Turn -z   (90° Left)
            Pose3(Ryp, np.array([0, 0, 0])),  # Turn y    (90°)
            Pose3(Ryn, np.array([0, 0, 0])),  # Turn -y   (90°)
            Pose3(Rxp, np.array([0, 0, 0])),  # Turn x    (90°)
            Pose3(Rxn, np.array([0, 0, 0])),  # Turn -x   (90°)
        ]

    #--------------------------------------------
    #   Getters / Setters
    #--------------------------------------------

    @property
    def gt_vals(self):
        gt_out = {}
        for rid in self.robots:
            gt_out[rid] = gtsam.Values()
        for key in self.gt_poses.keys():
            rid = chr(gtsam.Symbol(key).chr())
            pose = self.gt_poses.atPose3(key)
            gt_out[rid].insert(key, pose)
        return gt_out

    #--------------------------------------------
    #   Auxiliary functions
    #--------------------------------------------
    def __set_output_dir(self, config_path):
        config_folder_name = 'configs'

        path_parts = config_path.split(os.sep)
        index = path_parts.index(config_folder_name)
        path_parts[index] = "saved_outputs"
        output_path = os.sep.join(path_parts[0:-1])
        # print("Output directory set to:", output_path)
        return output_path

    def __get_all_edges(self):
        '''
        Generate all possible communication edges between robots
        '''
        edges = set()
        for rid in self.robots:
            for oid in self.robots:
                if rid != oid:
                    edge = (min(rid,oid),max(rid,oid))
                    edges.add(edge)
        return edges
    
    def incr_stamp(self):
        self.stamp += 1

    def is_key_in(self,rid, key):
        if key not in self.seen_keys[rid]:
            self.seen_keys[rid].add(key)
            return False
        else:
            return True

    @staticmethod
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

    @staticmethod
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

    @staticmethod
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

    def get_closest_lk(self, rid, pose_number):
        """
        Get the closest landmark to a given robot pose
        
        :param rid: Robot ID
        :param pose_number: Pose number
        :return: Key of the closest landmark
        """
        r_key = gtsam.symbol(rid, pose_number)
        r_pose = self.gt_poses.atPose3(r_key).translation()
        first_lk = True

        for key in self.landmarks.keys():
            pt = self.landmarks.atPoint3(key)
            norm = np.linalg.norm(pt - r_pose)

            if first_lk:
                smallest_norm = norm
                l_key = key

            elif smallest_norm > norm:
                smallest_norm = norm
                l_key = key
        return l_key

    @staticmethod
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

    def check_limits(self, pose, dpl):
        if pose.x() < self.config.trajectory['x_lim'][0]:
            end_pose = Pose3(
                gtsam.Rot3.Identity(), np.array([self.config.trajectory['x_lim'][0], pose.y(), pose.z()])
            )
            return pose.inverse().compose(end_pose)
        elif pose.x() > self.config.trajectory['x_lim'][1]:
            end_pose = Pose3(
                Rot3.RzRyRx(np.pi, 0, 0),
                np.array([self.config.trajectory['x_lim'][1], pose.y(), pose.z()]),
            )
            return pose.inverse().compose(end_pose)
        elif pose.y() < self.config.trajectory['y_lim'][0]:
            end_pose = Pose3(
                Rot3.RzRyRx(np.pi / 2, 0, 0),
                np.array([pose.x(), self.config.trajectory['y_lim'][0], pose.z()]),
            )
            return pose.inverse().compose(end_pose)
        elif pose.y() > self.config.trajectory['y_lim'][1]:
            end_pose = Pose3(
                Rot3.RzRyRx(-np.pi / 2, 0, 0),
                np.array([pose.x(), self.config.trajectory['y_lim'][1], pose.z()]),
            )
            return pose.inverse().compose(end_pose)
        elif pose.z() < self.config.trajectory['z_lim'][0]:
            end_pose = Pose3(
                Rot3.RzRyRx(0, -np.pi / 2, 0),
                np.array([pose.x(), pose.y(), self.config.trajectory['z_lim'][0]]),
            )
            return pose.inverse().compose(end_pose)
        elif pose.z() > self.config.trajectory['z_lim'][1]:
            end_pose = Pose3(
                Rot3.RzRyRx(0, np.pi / 2, 0),
                np.array([pose.x(), pose.y(), self.config.trajectory['z_lim'][1]]),
            )
            return pose.inverse().compose(end_pose)
        else:
            return dpl
            
    #--------------------------------------------
    #   Error noise generators
    #--------------------------------------------

    def init_noise_gen(self, sigma = None):
        if sigma == None:
            sigma = self.config.sigmas['initialization']
        return Pose3.Expmap(
            np.random.multivariate_normal(
                np.zeros((6,)), np.diag(np.array(sigma) ** 2)
            )
        )

    def odom_noise_gen(self, sigma = None):
        if sigma == None:
            sigma = self.config.sigmas['odom']
        
        noise = np.random.multivariate_normal(
                    np.zeros((6,)), np.diag(np.array(sigma) ** 2)
                )

        if not self.outliers:
            noise = np.minimum(noise, np.array(sigma))
            noise = np.maximum(noise, -np.array(sigma))
        return Pose3.Expmap(noise)

    def loop_noise_gen(self, sigma = None):
        if sigma == None:
            sigma = self.config.sigmas['lc_intra']

        noise = np.random.multivariate_normal(
                    np.zeros((6,)), np.diag(np.array(sigma) ** 2)
                )

        if not self.outliers:
            noise = np.minimum(noise, np.array(sigma))
            noise = np.maximum(noise, -np.array(sigma))

        return Pose3.Expmap(noise)

    def loop_inter_noise_gen(self, sigma = None):
        if sigma == None:
            sigma = self.config.sigmas['lc_inter_indirect']

        noise = np.random.multivariate_normal(
                    np.zeros((6,)), np.diag(np.array(sigma) ** 2)
                )

        if not self.outliers:
            noise = np.minimum(noise, np.array(sigma))
            noise = np.maximum(noise, -np.array(sigma))

        return Pose3.Expmap(noise)

    def range_loop_noise_gen(self, sigma = None):
        if sigma == None:
            sigma = self.config.sigmas['lc_inter_direct_range']
        
        noise = np.random.normal(0, sigma)

        if not self.outliers:
            noise = np.minimum(noise, np.array(sigma))
            noise = np.maximum(noise, -np.array(sigma))

        return noise
    
    def pose_loop_noise_gen(self, sigma = None):
        if sigma == None:
            sigma = self.config.sigmas['lc_inter_direct_pose']

        noise = np.random.multivariate_normal(
                    np.zeros((6,)), np.diag(np.array(sigma) ** 2)
                )

        return Pose3.Expmap(noise)
    
    def bearing_range_noise_gen(self, sigma = None, force_outlier = None):
        if sigma == None:
            sigma = self.config.sigmas['landmarks']

        noise = np.random.normal(np.zeros(3,),np.array(sigma))

        if not self.outliers and force_outlier is not None:
            noise = np.minimum(noise, np.array(sigma))
            noise = np.maximum(noise, -np.array(sigma))
        elif force_outlier is not None:
            noise = np.maximum(noise, force_outlier * np.array(sigma))
            noise = np.minimum(noise, -force_outlier * np.array(sigma))
        return noise
    
    #--------------------------------------------
    #    Factor generators
    #--------------------------------------------

    def make_range_factor(self, k1, k2, noise):
        fg = gtsam.NonlinearFactorGraph()
        if noise is None: 
            noise = self.range_loop_noise_gen()
        noise_model = self.range_loop_noise_model

        measure = (
            np.linalg.norm(
                self.gt_poses.atPose3(k1).translation() - self.gt_poses.atPose3(k2).translation()
            )
            + noise
        )
        fg.add(gtsam.RangeFactorPose3(k1, k2, measure, noise_model))
        return fg
    
    def make_pose_factor(self, k1, k2, noise):
        fg = gtsam.NonlinearFactorGraph()
        if noise is None:
            noise = self.pose_loop_noise_gen()
        noise_model = self.pose_loop_noise_model

        measure = self.gt_poses.atPose3(k1).inverse().compose(self.gt_poses.atPose3(k2)).compose(noise)
        fg.add(gtsam.BetweenFactorPose3(k1, k2, measure, noise_model))
        return fg

    def make_lc_factor(self, k1, k2, noise):
        fg = gtsam.NonlinearFactorGraph()
        if noise is None:
            noise = self.loop_noise_gen()
        noise_model = self.loop_noise_model

        measure = self.gt_poses.atPose3(k1).inverse().compose(self.gt_poses.atPose3(k2)).compose(noise)
        fg.add(gtsam.BetweenFactorPose3(k1, k2, measure, noise_model))
        return fg

    #--------------------------------------------
    #   Dataset builder functions
    #--------------------------------------------
    def add_prior(self, rid, pose_number):
        # for i, rid in enumerate(self.robots):
        key = gtsam.symbol(rid, pose_number)
        fg = gtsam.NonlinearFactorGraph()
            
        init_pose = self.init_values.atPose3(key)
        noise_sigmas = self.config.sigmas['prior']

        # Add as factor
        fg.addPriorPose3(
            key,
            init_pose,
            gtsam.noiseModel.Isotropic.Sigmas(noise_sigmas),
        )
        vals = gtsam.Values()
        vals.insert(key, init_pose)
            
        self.addEntry(
            rid,
            self.stamp,
            fg,
            [jrl.PriorFactorPose3Tag],
            {},
            jrl.TypedValues(vals, {key: jrl.Pose3Tag}),
            jrl.TypedValues(vals, {key: jrl.Pose3Tag}),
        )

    def add_odom_step(self, rid, p2):
        # Define previous pose number and keys
        p1 = p2 - 1
        k1 = gtsam.symbol(rid, p1)
        k2 = gtsam.symbol(rid, p2)
        
        odom, noise = self.odom[rid][p1]
        measure = odom.compose(noise)

        gt_pose = self.gt_poses.atPose3(k2)
        gt_val = gtsam.Values()
        gt_val.insert(k2, gt_pose)
        init_pose = self.init_values.atPose3(k1).compose(measure)
        init_val = gtsam.Values()
        init_val.insert(k2, init_pose)

        fg = gtsam.NonlinearFactorGraph()
        fg.add(gtsam.BetweenFactorPose3(k1, k2, measure, self.odom_noise_model))

        self.addEntry(
            rid,
            self.stamp,
            fg,
            [jrl.BetweenFactorPose3Tag],
            {},
            jrl.TypedValues(init_val, {k2: jrl.Pose3Tag}),
            jrl.TypedValues(gt_val, {k2: jrl.Pose3Tag}),
        )

        # Update the prev_vals
        if self.config.dataset_opts['initialization_type'] == "gt":
            self.init_values.insert(k2, gt_pose)
        elif self.config.dataset_opts['initialization_type'] == "noisy_gt":
            self.init_values.insert(k2, gt_pose.compose(self.init_noise_gen()))
        elif self.config.dataset_opts['initialization_type'] == "odom":
            self.init_values.insert(k2, init_pose)
        else:
            raise Exception("Invalid Initialization_type")

    def add_lc_intra(self, rid, pose_number, prev_pose_number, noise=None):
        key = gtsam.symbol(rid, pose_number)
        prev_key = gtsam.symbol(rid, prev_pose_number)

        self.addEntry(
            rid,
            self.stamp,
            self.make_lc_factor(key, prev_key, noise),
            [jrl.BetweenFactorPose3Tag],
            {},
        )

    def add_lc_inter_direct(self, type, pose_number, ra, rb, modality='double', noise=None):
        ka = gtsam.symbol(ra, pose_number)
        kb = gtsam.symbol(rb, pose_number)

        gt_val_ra = gtsam.Values()
        gt_val_ra.insert(ka, self.gt_poses.atPose3(ka))
        est_val_ra = gtsam.Values()
        est_val_ra.insert(ka, self.init_values.atPose3(ka))

        gt_val_rb = gtsam.Values()
        gt_val_rb.insert(kb, self.gt_poses.atPose3(kb))
        est_val_rb = gtsam.Values()
        est_val_rb.insert(kb, self.init_values.atPose3(kb))

        if type == 'pose':
            factor_ab = self.make_pose_factor(ka,kb,noise)
            factor_ba = self.make_pose_factor(kb,ka,noise)
            tag = jrl.BetweenFactorPose3Tag
        elif type == 'range':
            factor_ab = self.make_range_factor(ka,kb,noise)
            factor_ba = self.make_range_factor(kb,ka,noise)
            tag = jrl.RangeFactorPose3Tag
        else:
            raise Exception("Invalid type")

        if modality == 'double':
            self.addEntry(
                ra,
                self.stamp,
                factor_ab,
                [tag],
                {},
            )
            self.addEntry(
                rb,
                self.stamp,
                factor_ba,
                [tag],
                {},
            )
            if not self.is_key_in(ra, kb):
                self.addInitialization(ra, jrl.TypedValues(est_val_rb, {kb: jrl.Pose3Tag}))
                self.addGroundTruth(ra, jrl.TypedValues(gt_val_rb, {kb: jrl.Pose3Tag}))

            if not self.is_key_in(rb, ka):
                self.addInitialization(rb, jrl.TypedValues(est_val_ra, {ka: jrl.Pose3Tag}))
                self.addGroundTruth(rb, jrl.TypedValues(gt_val_ra, {ka: jrl.Pose3Tag}))
            
        elif modality == 'simple-a':
            self.addEntry(
                ra,
                self.stamp,
                factor_ab,
                [tag],
                {},
            )
            if not self.is_key_in(ra, kb):
                self.addInitialization(ra, jrl.TypedValues(est_val_rb, {kb: jrl.Pose3Tag}))
                self.addGroundTruth(ra, jrl.TypedValues(gt_val_rb, {kb: jrl.Pose3Tag}))

        elif modality == 'simple-b':
            self.addEntry(
                rb,
                self.stamp,
                factor_ba,
                [tag],
                {},
            )
            if not self.is_key_in(rb, ka):
                self.addInitialization(rb, jrl.TypedValues(est_val_ra, {ka: jrl.Pose3Tag}))
                self.addGroundTruth(rb, jrl.TypedValues(gt_val_ra, {ka: jrl.Pose3Tag}))

        else:
            raise Exception("Invalid modality")

    def add_lc_inter_indirect(self, ra, pn_a, rb, pn_b, modality='double', noise=None):
        ka = gtsam.symbol(ra, pn_a)
        kb = gtsam.symbol(rb, pn_b)

        gt_val_ra = gtsam.Values()
        gt_val_ra.insert(ka, self.gt_poses.atPose3(ka))
        est_val_ra = gtsam.Values()
        est_val_ra.insert(ka, self.init_values.atPose3(ka))

        gt_val_rb = gtsam.Values()
        gt_val_rb.insert(kb, self.gt_poses.atPose3(kb))
        est_val_rb = gtsam.Values()
        est_val_rb.insert(kb, self.init_values.atPose3(kb))

        if modality == 'double':
            self.addEntry(
                ra,
                self.stamp,
                self.make_pose_factor(ka,kb,noise),
                [jrl.BetweenFactorPose3Tag],
                {},
            )
            self.addEntry(
                rb,
                self.stamp,
                self.make_pose_factor(kb,ka,noise),
                [jrl.BetweenFactorPose3Tag],
                {},
            )
            if not self.is_key_in(ra, kb):
                self.addInitialization(ra, jrl.TypedValues(est_val_rb, {kb: jrl.Pose3Tag}))
                self.addGroundTruth(ra, jrl.TypedValues(gt_val_rb, {kb: jrl.Pose3Tag}))

            if not self.is_key_in(rb, ka):
                self.addInitialization(rb, jrl.TypedValues(est_val_ra, {ka: jrl.Pose3Tag}))
                self.addGroundTruth(rb, jrl.TypedValues(gt_val_ra, {ka: jrl.Pose3Tag}))

        elif modality == 'simple-a':
            self.addEntry(
                ra,
                self.stamp,
                self.make_pose_factor(ka,kb,noise),
                [jrl.BetweenFactorPose3Tag],
                {},
            )
            if not self.is_key_in(ra, kb):
                self.addInitialization(ra, jrl.TypedValues(est_val_rb, {kb: jrl.Pose3Tag}))
                self.addGroundTruth(ra, jrl.TypedValues(gt_val_rb, {kb: jrl.Pose3Tag}))

        elif modality == 'simple-b':
            self.addEntry(
                rb,
                self.stamp,
                self.make_pose_factor(kb,ka,noise),
                [jrl.BetweenFactorPose3Tag],
                {},
            )
            if not self.is_key_in(rb, ka):
                self.addInitialization(rb, jrl.TypedValues(est_val_ra, {ka: jrl.Pose3Tag}))
                self.addGroundTruth(rb, jrl.TypedValues(gt_val_ra, {ka: jrl.Pose3Tag}))

        else:
            raise Exception("Invalid modality")

    def add_lk(self, lid, rid, pose_number, noise=None):
        
        r_key = gtsam.symbol(rid, pose_number)
        l_key = lid

        # Initialize noise and fg
        fg = gtsam.NonlinearFactorGraph()
        gt_val_lk = gtsam.Values()
        est_val_lk = gtsam.Values()
        if noise is None:
            noise = self.bearing_range_noise_gen()
        noise_model = self.bearing_range_noise_model

        # Get robot pose and landmark
        pose_r = self.gt_poses.atPose3(r_key)
        point_l = self.landmarks.atPoint3(l_key)

        # Compute measurement
        t_br = gtsam.BearingRange3D.Measure(pose_r, point_l)
        noise_rot = gtsam.Rot3.Ypr(noise[0], noise[1], 0)
        m_bearing = noise_rot.rotate(t_br.bearing())
        m_range = t_br.range() + noise[2]
        fg.add(gtsam.BearingRangeFactor3D(r_key, l_key, m_bearing, m_range, noise_model))

        # init gt and init vals
        odom_pose_r = self.init_values.atPose3(r_key)
        m_lk = odom_pose_r.transformFrom(m_range * m_bearing.point3())
        gt_val_lk.insert(l_key, point_l)
        est_val_lk.insert(l_key, m_lk)

        self.addEntry(
            rid,
            self.stamp,
            fg,
            [jrl.BearingRangeFactor3DTag],
            {},
        )

        if not self.is_key_in(rid, l_key):
            self.addGroundTruth(rid, jrl.TypedValues(gt_val_lk, {l_key: jrl.Point3Tag}))
            self.addInitialization(rid, jrl.TypedValues(est_val_lk, {l_key: jrl.Point3Tag}))

    # def add_lk_old(self, lid, rid, pose_number, outlier=(False, None)):
        
    #     r_key = gtsam.symbol(rid, pose_number)
    #     l_key = lid

    #     # Initialize noise and fg
    #     fg = gtsam.NonlinearFactorGraph()
    #     gt_val_lk = gtsam.Values()
    #     est_val_lk = gtsam.Values()
    #     if outlier[0]:
    #         noise = self.bearing_range_noise_gen(force_outlier=outlier[1])
    #     else:
    #         noise = self.bearing_range_noise_gen()
    #     noise_model = self.bearing_range_noise_model

    #     # Get robot pose and landmark
    #     pose_r = self.gt_poses.atPose3(r_key)
    #     point_l = self.landmarks.atPoint3(l_key)

    #     # Compute measurement
    #     t_br = gtsam.BearingRange3D.Measure(pose_r, point_l)
    #     noise_rot = gtsam.Rot3.Ypr(noise[0], noise[1], 0)
    #     m_bearing = noise_rot.rotate(t_br.bearing())
    #     m_range = t_br.range() + noise[2]
    #     fg.add(gtsam.BearingRangeFactor3D(r_key, l_key, m_bearing, m_range, noise_model))

    #     # init gt and init vals
    #     odom_pose_r = self.init_values.atPose3(r_key)
    #     m_lk = odom_pose_r.transformFrom(m_range * m_bearing.point3())
    #     gt_val_lk.insert(l_key, point_l)
    #     est_val_lk.insert(l_key, m_lk)

    #     self.addEntry(
    #         rid,
    #         self.stamp,
    #         fg,
    #         [jrl.BearingRangeFactor3DTag],
    #         {},
    #     )

    #     if not self.is_key_in(rid, l_key):
    #         self.addGroundTruth(rid, jrl.TypedValues(gt_val_lk, {l_key: jrl.Point3Tag}))
    #         self.addInitialization(rid, jrl.TypedValues(est_val_lk, {l_key: jrl.Point3Tag}))
    
    #--------------------------------------------
    #   Generation functions
    #--------------------------------------------

    # Generator for groundtruth trajectories
    def gen_gt_trajectories2(self, nb_poses=None):
        """
        Generate groundtruth trajectories for each robot
        
        :param nb_poses: Number of poses to generate (if None, use config file value)
        :return: None
        """

        # Define number of poses
        if nb_poses is None:
            nb_poses = self.config.trajectory['poses']
            
        # Define limits
        if "x_lim" in self.config.trajectory and "x_lim" in self.config.trajectory and "x_lim" in self.config.trajectory:
            limits = True
        else:
            limits = False
            
        # Define generation seeds
        if "seed" in self.config.trajectory:
            np.random.seed(self.config.trajectory['seed'])
            seeds = np.random.choice(2000, size=len(self.robots), replace=False)
        else:
            np.random.seed()
            
        for i, rid in enumerate(self.robots):
            if 'seeds' in vars():
                np.random.seed(seeds[i])
            
            # Define initial position
            initial_rot = np.random.choice(self.ODOM_OPTIONS_GRIDWORLD).rotation()
            initial_position = np.array(
            [
                np.random.uniform(self.config.trajectory['x_lim'][0] / 2, self.config.trajectory['x_lim'][1] / 2),
                np.random.uniform(self.config.trajectory['y_lim'][0] / 2, self.config.trajectory['y_lim'][1] / 2),
                np.random.uniform(self.config.trajectory['z_lim'][0] / 2, self.config.trajectory['z_lim'][1] / 2),
            ])
            init_pose = gtsam.Pose3(initial_rot, initial_position)

            self.gt_poses.insert(gtsam.symbol(rid, 0), init_pose)
            self.init_values.insert(gtsam.symbol(rid, 0), init_pose)
            
            # Define displacements
            dpl = np.random.choice(np.arange(len(self.config.trajectory['traj_probs'])), 
                                   p= self.config.trajectory['traj_probs'],
                                   size= nb_poses - 1)
            prev_pose = init_pose
            
            for pose_nb, i in enumerate(dpl):
                if limits:
                    odom = self.check_limits(prev_pose, self.ODOM_OPTIONS_GRIDWORLD[i])
                else:
                    odom = self.ODOM_OPTIONS_GRIDWORLD[i]
                
                noise = self.odom_noise_gen()
                self.odom[rid].append((odom, noise))
                
                # Compute new pose
                new_pose = prev_pose.compose(odom)
                self.gt_poses.insert(gtsam.symbol(rid, pose_nb + 1), new_pose)
                prev_pose = new_pose
                
    def gen_gt_trajectories(self, nb_poses=None):
        """
        Generate groundtruth trajectories for each robot
        
        :param nb_poses: Number of poses to generate (if None, use config file value)
        :return: None
        """

        # Define number of poses
        if nb_poses is None:
            nb_poses = self.config.trajectory['poses']
        # Define generation seed
        if "seed" in self.config.trajectory:
            np.random.seed(self.config.trajectory['seed'])
        else:
            np.random.seed()

        for rid in self.robots:
            initial_rot = np.random.choice(self.ODOM_OPTIONS_GRIDWORLD).rotation()
            initial_position = np.array(
            [
                np.random.uniform(self.config.trajectory['x_lim'][0] / 2, self.config.trajectory['x_lim'][1] / 2),
                np.random.uniform(self.config.trajectory['y_lim'][0] / 2, self.config.trajectory['y_lim'][1] / 2),
                np.random.uniform(self.config.trajectory['z_lim'][0] / 2, self.config.trajectory['z_lim'][1] / 2),
            ])
            init_pose = gtsam.Pose3(initial_rot, initial_position)

            self.gt_poses.insert(gtsam.symbol(rid, 0), init_pose)
            self.init_values.insert(gtsam.symbol(rid, 0), init_pose)

        # Define displacements
        if "seed" in self.config.landmarks:
            np.random.seed(self.config.landmarks['seed'])
        else:
            np.random.seed()

        for rid in self.robots:
            dpl_index = np.random.choice(np.arange(len(self.config.trajectory['traj_probs'])), 
                                   p= self.config.trajectory['traj_probs'],
                                   size= nb_poses - 1)
            prev_pose = self.gt_poses.atPose3(gtsam.symbol(rid, 0))

            limits = True
            
            for pose_nb, i in enumerate(dpl_index):
                if limits:
                    odom = self.check_limits(prev_pose, self.ODOM_OPTIONS_GRIDWORLD[i])
                else:
                    odom = self.ODOM_OPTIONS_GRIDWORLD[i]
                
                self.odom[rid].append(odom)
                
                new_pose = prev_pose.compose(odom)
                self.gt_poses.insert(gtsam.symbol(rid, pose_nb + 1), new_pose)
                prev_pose = new_pose
    
    # Generator for landmarks used as amers
    # minimum distance between landmarks $d_{min}$
    def gen_gt_lk(self, nb=None):
        """
        Generate landmarks

        :param nb: Number of landmarks to generate (if None, use config file value)
        """

        if nb is None and self.config.landmarks is not None:
            nb = self.config.landmarks['number']

        if "seed" in self.config.landmarks:
            np.random.seed(self.config.landmarks['seed'])
        else:
            np.random.seed()

        for i in range(nb):
            lk_coordinates = np.array([
                np.random.uniform(self.config.trajectory['x_lim'][0], self.config.trajectory['x_lim'][1]),
                np.random.uniform(self.config.trajectory['y_lim'][0], self.config.trajectory['y_lim'][1]),
                np.random.uniform(self.config.trajectory['z_lim'][0], self.config.trajectory['z_lim'][1])
            ])
            lk_pose = gtsam.Point3(lk_coordinates)
            self.landmarks.insert(gtsam.symbol('#', i + 1), lk_pose)
        
        np.random.seed()
        
    def gen_lk_measurements(self):
        
        # Exportation des données
        def export_data(rid, poses, lids):
            # Export data
            output = list(zip(poses, lids))
            for data in output:
                pose, lid = data
                self.lk_measurements[(rid, pose)] = lid # (lid, noise)
                
        def gen_noises():
            for key in self.lk_measurements.keys():
                noise = self.bearing_range_noise_gen()
                self.lk_measurements[key] = (self.lk_measurements[key], noise)
        
        def pack_lid_per_rid(group_type='all'):
            nb_lks = self.config.landmarks['number']
            lk_ids = [gtsam.symbol('#', i + 1) for i in range(nb_lks)]
            lid_dict = {}

            if group_type == 'edges':
                edges = self.__get_all_edges()
                batch_nb = nb_lks // len(edges)

                # init structure
                for rid in self.robots:
                    lid_dict[rid] = set()

                for index, edge in enumerate(edges):
                    lks = [lk_ids[index * batch_nb + i] for i in range(batch_nb)]
                    for lk in lks:
                        lid_dict[edge[0]].add(lk)
                        lid_dict[edge[1]].add(lk)
                
                for rid in self.robots:
                    lid_dict[rid] = list(lid_dict[rid])

            elif group_type == 'all':
                for rid in self.robots:
                    lid_dict[rid] = lk_ids

            return lid_dict
        
        def get_unique_pairs(poses_pool, lids_pool, n):
            all_pairs = [(p, l) for p in poses_pool for l in lids_pool]
            chosen = random.sample(all_pairs, min(n, len(all_pairs)))
            poses, lids = zip(*chosen) if chosen else ([], [])
            return np.array(poses), np.array(lids)
        
        def get_random_poses(probability=0.4):
            rd = np.random.rand(self.config.trajectory['poses'])
            poses = np.where(rd > probability)[0]
            return poses
        
        # Initialisation de la clé de génération
        if "seed" in self.config.lc_intra:
            np.random.seed(self.config.lc_intra['seed'])
        else:
            np.random.seed()
            
        # Landmarks packs for robots detections
        if self.config.landmarks.get('pack') is not None:
            lks_ids = pack_lid_per_rid(group_type=self.config.landmarks['pack'])
        else: 
            lks_ids = pack_lid_per_rid() # all
            
        # Landmark measurements -> risque de double détections
        for rid in self.robots:
            poses_pool = range(self.config.trajectory['poses'])
            lids_pool = lks_ids[rid]
            
            if "detection_num" in self.config.landmarks:
                n = self.config.landmarks['detection_num']
                poses, lids = get_unique_pairs(poses_pool, lids_pool, n)
                
            elif "detection_prob" in self.config.landmarks:
                poses = get_random_poses(self.config.landmarks['poses'])
                poses, lids = get_unique_pairs(poses, lids_pool, len(poses))
                
            else:
                poses = get_random_poses()
                poses, lids = get_unique_pairs(poses, lids_pool, len(poses))
            
            export_data(rid, poses, lids)
        
        gen_noises()
        np.random.seed()

    def gen_lc_intra(self): #-> scalable si un robot est ajouté
        
        # Exportation des données
        def export_data(rid, poses, poses_2nd):
            # Export data
            output = list(zip(poses, poses_2nd))
            for data in output:
                pose, pose_2nd = data
                self.lc_intra[(rid, pose)] = pose_2nd
        
        # Définition de la taille des loop closures
        def get_lc_size(len_index):
            if "size" in self.config.lc_intra: # ajouter l'option de génération aléatoire
                return self.config.lc_intra['size']
            else:
                return np.random.randint(low=10, high=self.config.trajectory['poses'], size=len_index)
        
        def gen_noises():
            for key in self.lc_intra.keys():
                noise = self.loop_noise_gen()
                self.lc_intra[key] = (self.lc_intra[key], noise)
                
        # Initialisation de la clé de génération
        if "seed" in self.config.lc_intra:
            np.random.seed(self.config.lc_intra['seed'])
        else:
            np.random.seed()

        # loop closures périodiques
        if self.config.lc_intra.get('frequency') is not None and self.config.lc_intra.get('number') is None:
            freq = self.config.lc_intra['frequency']

            for rid in self.robots:
                # sélectionner les poses sur lesquelles surviennent une boucle
                init = np.random.randint(low=0, high=freq)
                poses = np.arange(init, self.config.trajectory['poses'], freq)
                lc_size = get_lc_size(len(poses))
                poses_2nd = np.maximum((poses - lc_size), np.zeros((len(poses),), dtype=int))
                export_data(rid, poses, poses_2nd)

        # loop closures à nombre défini
        elif self.config.lc_intra.get('number') is not None:
            for rid in self.robots:
                # sélectionner les poses sur lesquelles surviennent une boucle
                poses = np.random.randint(low=0, high=self.config.trajectory['poses'], size=self.config.lc_intra.get('number'))
                poses = np.sort(poses)
                lc_size = get_lc_size(len(poses))
                poses_2nd = np.maximum((poses - lc_size), np.zeros((len(poses),), dtype=int))
                export_data(rid, poses, poses_2nd)
                
        # loop closures à nombre défini périodiques -> placé en fin de boucle
        else:
            freq = self.config.lc_intra['frequency']
            
            for rid in self.robots:
                init = np.random.randint(low=0, high=freq)
                poses = np.arange(0, (freq*self.config.lc_intra.get('number')), freq)
                poses += self.config.trajectory['poses'] - init
                lc_size = get_lc_size(len(poses))
                poses_2nd = np.maximum((poses - lc_size), np.zeros((len(poses),), dtype=int))
                export_data(rid, poses, poses_2nd)
        
        gen_noises()
        np.random.seed()

    def gen_lc_inter_indirect(self):
        
        # Exportation des données
        def export_data(rid, poses, oids, poses_oid):
            # Export data
            output = list(zip(poses, oids, poses_oid))
            for data in output:
                pose, oid, pose_oid = data
                self.lc_inter_indirect[(rid, pose)] = (oid, pose_oid)
                
        def gen_oids(len_ids, rid):
            ids = copy(self.robots)
            ids.remove(rid)
            return np.random.choice(ids, size=len_ids)
        
        def get_lc_size(len_index):
            if "size" in self.config.lc_inter_indirect: # ajouter l'option de génération aléatoire
                return self.config.lc_inter_indirect['size']
            else:
                return np.random.randint(low=10, high=self.config.trajectory['poses'], size=len_index)
        
        def gen_noises():
            for key in self.lc_inter_indirect.keys():
                noise = self.loop_inter_noise_gen()
                self.lc_inter_indirect[key] = (self.lc_inter_indirect[key][0], self.lc_inter_indirect[key][1], noise)
                
        # Initialisation de la clé de génération
        if "seed" in self.config.lc_inter_indirect:
            np.random.seed(self.config.lc_inter_indirect['seed'])
        else:
            np.random.seed()

        # Loop closures périodiques
        if self.config.lc_inter_indirect.get('frequency') is not None and self.config.lc_inter_indirect.get('number') is None:
            freq = self.config.lc_inter_indirect['frequency']
            
            for rid in self.robots:
                # sélectionner les poses sur lesquelles surviennent les boucles
                init = np.random.randint(low=0, high=freq)
                poses = np.arange(init, self.config.trajectory['poses'], freq)
                lc_size = get_lc_size(len(poses))
                poses_oid = np.maximum((poses - lc_size), np.zeros((len(poses),), dtype=int))
                oids = gen_oids(len(poses_oid),rid)
                export_data(rid, poses, oids, poses_oid)
            
        # Loop closures à nombre défini
        elif self.config.lc_inter_indirect.get('number') is not None:
            for rid in self.robots:
                # sélectionner les poses sur lesquelles surviennent une boucle
                poses = np.random.randint(low=0, high=self.config.trajectory['poses'], size=self.config.lc_inter_indirect.get('number'))
                poses = np.sort(poses)
                lc_size = get_lc_size(len(poses))
                poses_oid = np.maximum((poses - lc_size), np.zeros((len(poses),), dtype=int))
                oids = gen_oids(len(poses_oid),rid)
                export_data(rid, poses, oids, poses_oid)
            
        # Loop closures à nombre défini périodiques
        else:
            freq = self.config.lc_inter_indirect['frequency']
            
            for rid in self.robots:
                init = np.random.randint(low=0, high=freq)
                poses = np.arange(0, (freq*self.config.lc_inter_indirect.get('number')), freq)
                poses += self.config.trajectory['poses'] - init
                lc_size = get_lc_size(len(poses))
                poses_oid = np.maximum((poses - lc_size), np.zeros((len(poses),), dtype=int))
                oids = gen_oids(len(poses_oid),rid)
                export_data(rid, poses, oids, poses_oid)
        
        gen_noises()
        np.random.seed()
            
    def gen_lc_inter_direct(self):
        # Initialisation de la clé de génération
        if "seed" in self.config.lc_inter_direct:
            np.random.seed(self.config.lc_inter_direct['seed'])
        else:
            np.random.seed()
            
        # Exportation des données de range
        def export_range_data(rid, poses, oids):
            output = list(zip(poses, oids))
            for data in output:
                pose, oid = data
                self.lc_inter_direct_range[(rid, pose)] = (oid, 'double')
                
        # Exportation des données de pose
        def export_pose_data(rid, poses, oids):
            output = list(zip(poses, oids))
            for data in output:
                pose, oid = data
                self.lc_inter_direct_pose[(rid, pose)] = (oid, 'double')
            
        def gen_oids(len_ids, rid):
            ids = copy(self.robots)
            ids.remove(rid)
            return np.random.choice(ids, size=len_ids)

        def gen_noises():
            for key in self.lc_inter_direct_range.keys():
                noise = self.range_loop_noise_gen()
                self.lc_inter_direct_range[key] = (self.lc_inter_direct_range[key][0], self.lc_inter_direct_range[key][1], noise)

            for key in self.lc_inter_direct_pose.keys():
                noise = self.pose_loop_noise_gen()
                self.lc_inter_direct_pose[key] = (self.lc_inter_direct_pose[key][0], self.lc_inter_direct_pose[key][1], noise)

        # Generates range measurements
        if self.config.lc_inter_direct.get('range') is not None:
            
            # Mesures périodiques
            if self.config.lc_inter_direct['range'].get('frequency') is not None and self.config.lc_inter_direct['range'].get('number') is None:
                freq = self.config.lc_inter_direct['range']['frequency']
            
                for rid in self.robots:
                    # sélectionner les poses sur lesquelles surviennent les mesures
                    init = np.random.randint(low=0, high=freq)
                    poses = np.arange(init, self.config.trajectory['poses'], freq)
                    oids = gen_oids(len(poses),rid)
                    export_range_data(rid, poses, oids)
            
            # Mesures à nombre défini
            elif self.config.lc_inter_direct['range'].get('number') is not None:
                for rid in self.robots:
                    # sélectionner les poses sur lesquelles surviennent une boucle
                    poses = np.random.randint(low=0, high=self.config.trajectory['poses'], size=self.config.lc_inter_direct['range']['number'])
                    poses = np.sort(poses)
                    oids = gen_oids(len(poses),rid)
                    export_range_data(rid, poses, oids)
            
            # Mesures à nombre défini périodiques
            else:
                freq = self.config.lc_inter_direct['range']['frequency']
                
                for rid in self.robots:
                    init = np.random.randint(low=0, high=freq)
                    poses = np.arange(0, (freq*self.config.lc_inter_direct['range']['number']), freq)
                    poses += self.config.trajectory['poses'] - init
                    oids = gen_oids(len(poses),rid)
                    export_range_data(rid, poses, oids)
                
        # Generates pose measurements
        if self.config.lc_inter_direct.get('pose') is not None:
            
            # Mesures périodiques
            if self.config.lc_inter_direct['pose'].get('frequency') is not None and self.config.lc_inter_direct['pose'].get('number') is None:
                freq = self.config.lc_inter_direct['pose']['frequency']
            
                for rid in self.robots:
                    # sélectionner les poses sur lesquelles surviennent les mesures
                    init = np.random.randint(low=0, high=freq)
                    poses = np.arange(init, self.config.trajectory['poses'], freq)
                    oids = gen_oids(len(poses),rid)
                    export_pose_data(rid, poses, oids)
            
            # Mesures à nombre défini
            elif self.config.lc_inter_direct['pose'].get('number') is not None:
                for rid in self.robots:
                    # sélectionner les poses sur lesquelles surviennent une boucle
                    poses = np.random.randint(low=0, high=self.config.trajectory['poses'], size=self.config.lc_inter_direct['pose']['number'])
                    poses = np.sort(poses)
                    oids = gen_oids(len(poses),rid)
                    export_pose_data(rid, poses, oids)
            
            # Mesures à nombre défini périodiques
            else:
                freq = self.config.lc_inter_direct['pose']['frequency']
                
                for rid in self.robots:
                    init = np.random.randint(low=0, high=freq)
                    poses = np.arange(0, (freq*self.config.lc_inter_direct['pose']['number']), freq)
                    poses += self.config.trajectory['poses'] - init
                    oids = gen_oids(len(poses),rid)
                    export_pose_data(rid, poses, oids)
        
        gen_noises()
        np.random.seed()

    def gen_outliers(self):
        # Initialisation de la clé de génération
        if "seed" in self.config.outliers:
            np.random.seed(self.config.outliers['seed'])
        else:
            np.random.seed()
            
        if self.config.outliers.get('false_matching') is not None:
            print("Generating false matching outliers...")
            for rid in self.config.outliers['false_matching']['robots']:
                print(f"Generating false matching outliers for robot {rid}...")

        if self.config.outliers.get('out_of_bounds') is not None:
            print("Generating out of bounds outliers...")
            for rid in self.config.outliers['out_of_bounds']['robots']:
                print(f"Generating out of bounds outliers for robot {rid}...")

        if self.config.outliers.get('robot_loss') is not None:
            print("Generating robot loss outliers...")
            for rid, pose_num in self.config.outliers['robot_loss']:
                print(f"Generating robot loss outlier for robot {rid} at pose {pose_num}...")

    #     "outliers": {
    #     "seed":15,
    #     "false_matching": {
    #         "robots": ['a'],
    #         "intra": 10,
    #         "inter_indirect": 10,
    #         "inter_direct_range": 10,
    #         "inter_direct_pose": 10,
    #         "landmarks": 10
    #     },
    #     "out_of_bounds": {
    #         "robots": ['a'],
    #         "intra": 10,
    #         "inter_indirect": 10,
    #         "inter_direct_range": 10,
    #         "inter_direct_pose": 10,
    #         "landmarks": 10
    #     },
    #     "robot_loss": [('a', 200)]
    # }

    #--------------------------------------------
    #   Dataset generation (default)
    #--------------------------------------------
    def generate_dataset(self):
        print("Generating dataset for configuration file:\n", self.config_file_path)
        
        # Setup folders
        config_name, _ = os.path.splitext(os.path.basename(self.config_file_path))

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        output_path = os.path.join(self.output_dir, config_name + ".jrl")

        # Generate groundTruths trajectories
        self.gen_gt_trajectories2()
        
        # Generate landmarks
        if self.config.landmarks is not None:
            # Generate landmarks
            self.gen_gt_lk()
            self.gen_lk_measurements()
            # lks_ids = self.__pack_lid_per_rid()

        # Generate loop closure : intra
        if self.config.lc_intra is not None:
            self.gen_lc_intra()
        # Generate loop closure : inter - indirect
        if self.config.lc_inter_direct is not None:
            self.gen_lc_inter_direct()
        # Generate loop closure : inter - direct
        if self.config.lc_inter_indirect is not None:
            self.gen_lc_inter_indirect()
            
        # Generate outliers
        if self.config.outliers is not None:
            self.gen_outliers()

        # Add priors
        for rid in self.robots:
            self.add_prior(rid, 0)
        self.incr_stamp()

        for pose_num in range(1, self.config.trajectory['poses']):
            
            # Add odometry measurements
            for rid in self.robots:
                self.add_odom_step(rid, pose_num)
            
            # Add other measurements:
            for rid in self.robots:
                # Add loop closure : intra
                if bool(self.lc_intra) and (rid, pose_num) in self.lc_intra.keys(): # L'objet n'est pas vide
                    # print("Intra")
                    # print(self.lc_intra[(rid, pose_num)])
                    pose_2nd = self.lc_intra[(rid, pose_num)][0]
                    noise = self.lc_intra[(rid, pose_num)][1]
                    self.add_lc_intra(rid, pose_num, pose_2nd, noise=noise)
                
                # Add loop closure : inter - indirect
                if bool(self.lc_inter_indirect) and (rid, pose_num) in self.lc_inter_indirect.keys():
                    # print("Inter Indirect")
                    # print(self.lc_inter_indirect[(rid, pose_num)])
                    oid = self.lc_inter_indirect[(rid, pose_num)][0]
                    pose_oid = self.lc_inter_indirect[(rid, pose_num)][1]
                    noise = self.lc_inter_indirect[(rid, pose_num)][2]
                    self.add_lc_inter_indirect(rid, pose_num, oid, pose_oid, noise=noise)
                    
                # Add loop closure : intrer - direct
                if bool(self.lc_inter_direct_range) and (rid, pose_num) in self.lc_inter_direct_range.keys():
                    # print("Inter Direct Range")
                    # print(self.lc_inter_direct_range[(rid, pose_num)])
                    oid = self.lc_inter_direct_range[(rid, pose_num)][0]
                    noise = self.lc_inter_direct_range[(rid, pose_num)][2]
                    self.add_lc_inter_direct('range', pose_num, rid, oid, modality='double', noise=noise)
                
                if bool(self.lc_inter_direct_pose) and (rid, pose_num) in self.lc_inter_direct_pose.keys():
                    # print("Inter Direct Pose")
                    # print(self.lc_inter_direct_pose[(rid, pose_num)])
                    oid = self.lc_inter_direct_pose[(rid, pose_num)][0]
                    noise = self.lc_inter_direct_pose[(rid, pose_num)][2]
                    self.add_lc_inter_direct('pose', pose_num, rid, oid, modality='simple-a', noise=noise)
            
                # Add landmarks measurements
                if bool(self.lk_measurements) and (rid, pose_num) in self.lk_measurements.keys():
                    # print("Landmarks")
                    # print(self.lk_measurements[(rid, pose_num)])
                    lid = self.lk_measurements[(rid, pose_num)][0]
                    noise = self.lk_measurements[(rid, pose_num)][1]
                    self.add_lk(lid, rid, pose_num, noise=noise)
                         
            self.incr_stamp()

        # Build dataset and generate jrl file
        dataset = self.build()
        writer = jrl.Writer()

        dataset_count = 0

        writer.writeDataset(
            dataset,
            output_path,
            False,
        )
        print('--->  ',output_path)

if __name__ == "__main__":

    # Setup the Dataset Builder
    builder = DatasetGenerator('./configs/default.json')
    # builder.gen_gt_trajectories(500)
    # builder.add_prior('a',0)
    # builder.add_prior('b',0)
    # builder.add_odom_step('a',1)
    # builder.add_odom_step('b',1)
    # builder.add_odom_step('a',2)
    # builder.add_odom_step('b',2)
    # builder.add_odom_step('a',3)
    # builder.add_odom_step('b',3)
    # builder.add_odom_step('a',4)
    # builder.add_odom_step('b',4)
    # builder.add_lc_intra('a',1,3)
    builder.gen_lk_amers()
    #print(builder.gt_vals)