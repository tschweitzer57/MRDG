import jrl
import gtsam
from gtsam import Rot3, Pose3
import numpy as np
from collections import defaultdict
from string import ascii_letters
from collections import defaultdict

from configuration import DatasetConfiguration

#TODO: Extraire Landmarks / Groundtruth / Initialization / Noise sous forme de classes
#TODO transform gt var into simple gtsam.Values (dont require rid since there is a key)
#TODO init start point
#TODO add scenario add reset add save -> same dataset with different factors
#TODO add a mapping function generating a common map for trajectories and lks
#TODO améliorer intégration des random seed

class DatasetGenerator(jrl.DatasetBuilder):
    def __init__(self, config_path):

        # Get configuration from config file
        self.config = DatasetConfiguration(config_path)

        # Define variables
        self.gt_poses = gtsam.Values()
        self.init_values = gtsam.Values()
        self.odom = defaultdict(list)
        self.landmarks = gtsam.Values()

        self.stamp = 0
        #self.pose_number = 0
        self.seen_keys = defaultdict(set)
        
        self.odom_choice = {}
        
        # Setup ID's for each robot
        self.robots = []
        for i in range(self.config.dataset_opts['number_robots']):
            rid = ascii_letters[i]
            self.robots.append(rid)
        
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
        if self.config.dataset_opts.get('outliers') == "False":
            self.outliers = False
        else:
            self.outliers = True

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
    
    def incr_stamp(self):
        self.stamp += 1

    def is_key_in(self,rid, key):
        if key not in self.seen_keys[rid]:
            self.seen_keys[rid].add(key)
            return False
        else:
            return True

    def get_closest_lk(self, rid, pose_number):
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

    def check_limits(self, pose, dpl):
        if pose.x() < self.config.limits['x'][0]:
            end_pose = Pose3(
                gtsam.Rot3.Identity(), np.array([self.config.limits['x'][0], pose.y(), pose.z()])
            )
            return pose.inverse().compose(end_pose)
        elif pose.x() > self.config.limits['x'][1]:
            end_pose = Pose3(
                Rot3.RzRyRx(np.pi, 0, 0),
                np.array([self.config.limits['x'][1], pose.y(), pose.z()]),
            )
            return pose.inverse().compose(end_pose)
        elif pose.y() < self.config.limits['y'][0]:
            end_pose = Pose3(
                Rot3.RzRyRx(np.pi / 2, 0, 0),
                np.array([pose.x(), self.config.limits['y'][0], pose.z()]),
            )
            return pose.inverse().compose(end_pose)
        elif pose.y() > self.config.limits['y'][1]:
            end_pose = Pose3(
                Rot3.RzRyRx(-np.pi / 2, 0, 0),
                np.array([pose.x(), self.config.limits['y'][1], pose.z()]),
            )
            return pose.inverse().compose(end_pose)
        elif pose.z() < self.config.limits['z'][0]:
            end_pose = Pose3(
                Rot3.RzRyRx(0, -np.pi / 2, 0),
                np.array([pose.x(), pose.y(), self.config.limits['z'][0]]),
            )
            return pose.inverse().compose(end_pose)
        elif pose.z() > self.config.limits['z'][1]:
            end_pose = Pose3(
                Rot3.RzRyRx(0, np.pi / 2, 0),
                np.array([pose.x(), pose.y(), self.config.limits['z'][1]]),
            )
            return pose.inverse().compose(end_pose)
        else:
            return dpl

    #-----------------------------------------------------------------------------------------
    #   Define data generators
    #-----------------------------------------------------------------------------------------

    # Generator for groundtruth trajectories
    def gen_gt_trajectories(self, nb_poses=None):

        # Define number of poses
        if nb_poses is None:
            nb_poses = self.config.dataset_opts['number_poses']
        # Define initial Pose
        if "trajectory_seed" in self.config.dataset_opts:
            np.random.seed(self.config.dataset_opts['trajectory_seed'])
        else:
            np.random.seed()

        for rid in self.robots:
            initial_rot = np.random.choice(self.ODOM_OPTIONS_GRIDWORLD).rotation()
            initial_position = np.array(
            [
                np.random.uniform(self.config.limits['x'][0] / 2, self.config.limits['x'][1] / 2),
                np.random.uniform(self.config.limits['y'][0] / 2, self.config.limits['y'][1] / 2),
                np.random.uniform(self.config.limits['z'][0] / 2, self.config.limits['z'][1] / 2),
            ])
            init_pose = gtsam.Pose3(initial_rot, initial_position)

            self.gt_poses.insert(gtsam.symbol(rid, 0), init_pose)
            self.init_values.insert(gtsam.symbol(rid, 0), init_pose)

        # Define displacements
        if "trajectory_seed" in self.config.dataset_opts:
            np.random.seed(self.config.dataset_opts['trajectory_seed'])
        else:
            np.random.seed()

        for rid in self.robots:
            dpl_index = np.random.choice(np.arange(len(self.config.odometry['odom_probs'])), 
                                   p= self.config.odometry['odom_probs'],
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
    
    # Generator for landmarks amers
    def gen_lk_amers(self, nb=None):

        if nb is None and self.config.landmarks is not None:
            nb = self.config.landmarks['number']

        if "seed" in self.config.landmarks:
            np.random.seed(self.config.landmarks['seed'])
        else:
            np.random.seed()

        for i in range(nb):
            lk_coordinates = np.array([
                np.random.uniform(self.config.limits['x'][0], self.config.limits['x'][1]),
                np.random.uniform(self.config.limits['y'][0], self.config.limits['y'][1]),
                np.random.uniform(self.config.limits['z'][0], self.config.limits['z'][1])
            ])
            lk_pose = gtsam.Point3(lk_coordinates)
            self.landmarks.insert(gtsam.symbol('#', i + 1), lk_pose)
        
        np.random.seed()

    #-----------------------------------------------------------------------------------------
    #   Define error noise generators
    #-----------------------------------------------------------------------------------------

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
    
    #----------------------------
    #   Factor generators
    #----------------------------

    def make_range_factor(self, k1, k2):
        fg = gtsam.NonlinearFactorGraph()
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
    
    def make_pose_factor(self, k1, k2):
        fg = gtsam.NonlinearFactorGraph()
        noise = self.pose_loop_noise_gen()
        noise_model = self.pose_loop_noise_model

        measure = self.gt_poses.atPose3(k1).inverse().compose(self.gt_poses.atPose3(k2)).compose(noise)
        fg.add(gtsam.BetweenFactorPose3(k1, k2, measure, noise_model))
        return fg

    def make_lc_factor(self,k1,k2):
        fg = gtsam.NonlinearFactorGraph()
        noise = self.loop_noise_gen()
        noise_model = self.loop_noise_model

        measure = self.gt_poses.atPose3(k1).inverse().compose(self.gt_poses.atPose3(k2)).compose(noise)
        fg.add(gtsam.BetweenFactorPose3(k1, k2, measure, noise_model))
        return fg

    #----------------------------
    #   Dataset builder functions
    #----------------------------

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
        
        odom = self.odom[rid][p1]
        noise = self.odom_noise_gen()
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

    def add_lc_intra(self, rid, pose_number, prev_pose_number):
        key = gtsam.symbol(rid, pose_number)
        prev_key = gtsam.symbol(rid, prev_pose_number)

        self.addEntry(
            rid,
            self.stamp,
            self.make_lc_factor(key, prev_key),
            [jrl.BetweenFactorPose3Tag],
            {},
        )

    def add_lc_inter_direct(self, type, pose_number, ra, rb, modality='duplex'):
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
            factor_ab = self.make_pose_factor(ka,kb)
            factor_ba = self.make_pose_factor(kb,ka)
            tag = jrl.BetweenFactorPose3Tag
        elif type == 'range':
            factor_ab = self.make_range_factor(ka,kb)
            factor_ba = self.make_range_factor(kb,ka)
            tag = jrl.RangeFactorPose3Tag
        else:
            raise Exception("Invalid type")

        if modality == 'duplex':
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
            
        elif modality == 'simplex-a':
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

        elif modality == 'simplex-b':
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

    def add_lc_inter_indirect(self, ra, pn_a, rb, pn_b, modality='duplex'):
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

        if modality == 'duplex':
            self.addEntry(
                ra,
                self.stamp,
                self.make_pose_factor(ka,kb),
                [jrl.BetweenFactorPose3Tag],
                {},
            )
            self.addEntry(
                rb,
                self.stamp,
                self.make_pose_factor(kb,ka),
                [jrl.BetweenFactorPose3Tag],
                {},
            )
            if not self.is_key_in(ra, kb):
                self.addInitialization(ra, jrl.TypedValues(est_val_rb, {kb: jrl.Pose3Tag}))
                self.addGroundTruth(ra, jrl.TypedValues(gt_val_rb, {kb: jrl.Pose3Tag}))

            if not self.is_key_in(rb, ka):
                self.addInitialization(rb, jrl.TypedValues(est_val_ra, {ka: jrl.Pose3Tag}))
                self.addGroundTruth(rb, jrl.TypedValues(gt_val_ra, {ka: jrl.Pose3Tag}))

        elif modality == 'simplex-a':
            self.addEntry(
                ra,
                self.stamp,
                self.make_pose_factor(ka,kb),
                [jrl.BetweenFactorPose3Tag],
                {},
            )
            if not self.is_key_in(ra, kb):
                self.addInitialization(ra, jrl.TypedValues(est_val_rb, {kb: jrl.Pose3Tag}))
                self.addGroundTruth(ra, jrl.TypedValues(gt_val_rb, {kb: jrl.Pose3Tag}))

        elif modality == 'simplex-b':
            self.addEntry(
                rb,
                self.stamp,
                self.make_pose_factor(kb,ka),
                [jrl.BetweenFactorPose3Tag],
                {},
            )
            if not self.is_key_in(rb, ka):
                self.addInitialization(rb, jrl.TypedValues(est_val_ra, {ka: jrl.Pose3Tag}))
                self.addGroundTruth(rb, jrl.TypedValues(gt_val_ra, {ka: jrl.Pose3Tag}))

        else:
            raise Exception("Invalid modality")

    def add_lk(self, lid, rid, pose_number, outlier=(False, None)):
        r_key = gtsam.symbol(rid, pose_number)
        l_key = lid

        # Initialize noise and fg
        fg = gtsam.NonlinearFactorGraph()
        gt_val_lk = gtsam.Values()
        est_val_lk = gtsam.Values()
        if outlier[0]:
            noise = self.bearing_range_noise_gen(force_outlier=outlier[1])
        else:
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