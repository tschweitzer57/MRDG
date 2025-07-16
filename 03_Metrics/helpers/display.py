import argparse
import os
import sys

import jrl
import gtsam
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import seaborn as sns

from results import Data

class Display2():

    def __init__(self):
        print('Initialized')

    def plot_gtlk_error(self, inp_error):
        # Reorganize data
        ax = plt.figure()
        colors = sns.color_palette("colorblind", len(self.robots))

        for idx, rid in enumerate(self.robots):
            iteration = []
            error = []

            for item in inp_error[rid]:
                iteration.append(item[0])
                error.append(item[1])

            plt.plot(iteration, error, 
                alpha=1,
                color=colors[idx],
                label=f'Robot {rid}'
            )
        ax.title("Test")
        ax.legend()
        plt.show()

    def plot_consensuslk_error(self, cs_errors, labels=None, title=None):
        # Reorganize data
        ax = plt.figure()
        colors = sns.color_palette("colorblind", len(cs_errors))
        
        for idx, cs_error in enumerate(cs_errors):
            
            first_run = True
            for edge in cs_error.keys():
                if first_run:
                    err = np.array(cs_error[edge])
                    iteration = list(range(0,len(cs_error[edge])))
                    first_run = False
                else:
                    err += np.array(cs_error[edge])

            plt.plot(iteration, err, 
                alpha=1,
                color=colors[idx],
                label=labels[idx]
            )

        if title is not None:
            plt.title(title)
        ax.legend()
        plt.show()


class Display():

    def __init__(self, Results):
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
        
    def plot_trajectories(self, data_type=None, ref=None):
        if data_type is None:
            data = self.groundtruths
        elif data_type == 'gt':
            data = self.groundtruths
        elif data_type == 'init':
            data = self.initializations
        elif data_type == 'est':
            data = self.estimates
        else:
            raise ValueError("Unknown data type")
        
        if ref == 'gt':
            data_ref = self.groundtruths
        elif ref is None:
            data_ref = None
        else:
            raise ValueError("Unknown reference type")

        colors = sns.color_palette("colorblind", len(self.robots))
        for idx, rid in enumerate(self.robots):
            positions = []
            for k in data[rid].keys():
                s = gtsam.Symbol(k)
                if chr(s.chr()) == rid:
                    positions.append(self.getPoint(k, data[rid]))
            positions = np.stack(positions)
            ax = plt.figure().add_subplot(projection='3d')
            plt.plot(
                positions.T[0],
                positions.T[1],
                positions.T[2],
                alpha=1,
                color=colors[idx],
                label=f'Robot {rid}'
            )
            ax.legend()
        plt.axis('equal')
        plt.show()
    
    def plot_trajectories_all(self, data_type=None, ref=None, name=None):
        if data_type is None:
            data = self.groundtruths
        elif data_type == 'gt':
            data = self.groundtruths
        elif data_type == 'init':
            data = self.initializations
        elif data_type == 'est':
            data = self.estimates
        else:
            raise ValueError("Unknown error type")
        
        if ref == 'gt':
            data_ref = self.groundtruths
        elif ref == 'init':
            data_ref = self.initializations
        elif ref is None:
            data_ref = None
        else:
            raise ValueError("Unknown reference type")

        colors = sns.color_palette("colorblind", len(self.robots))
        ax = plt.figure().add_subplot(111,projection='3d')

        for idx, rid in enumerate(self.robots):
            positions = []
            landmarks = []
            landmarks_ref = []

            for k in data[rid].keys():
                s = gtsam.Symbol(k)
                if chr(s.chr()) == rid:
                    positions.append(self.getPoint(k, data[rid]))
                elif chr(s.chr()) == 'l':
                    landmarks.append(data[rid].atPoint3(k))
                    if data_ref is not None:
                        landmarks_ref.append(data_ref[rid].atPoint3(k))

            positions = np.stack(positions)
            landmarks = np.stack(landmarks)
            if data_ref is not None:
                landmarks_ref = np.stack(landmarks_ref)

            plt.plot(
                positions.T[0],
                positions.T[1],
                positions.T[2],
                alpha=1,
                color=colors[idx],
                label=f'Robot {rid}'
            )
            ax.scatter(landmarks[0][0], landmarks[0][1], landmarks[0][2], color=colors[idx])
            if data_ref is not None:    
                ax.scatter(landmarks_ref[0][0], landmarks_ref[0][1], landmarks_ref[0][2], color='black')

        ax.legend()
        if name is not None:
            ax.set_title(name)
        plt.axis('equal')
        plt.show()

    def plot_trajectories_comp(self, data_type=None):
        if data_type is None:
            data_ref = self.groundtruths
            data_obs = self.estimates
        elif 'gt' in data_type and 'init' in data_type:
            data_ref = self.groundtruths
            data_obs = self.initializations
        elif 'gt' in data_type and 'est' in data_type:
            data_ref = self.groundtruths
            data_obs = self.estimates
        elif 'init' in data_type and 'est' in data_type:
            data_ref = self.initializations
            data_obs = self.estimates
        else:
            raise ValueError("Unknown error type")

        colors = sns.color_palette("colorblind", len(self.robots))
        for idx, rid in enumerate(self.robots):
            ax = plt.figure().add_subplot(111,projection='3d')
            
            positions_ref = []
            positions_obs = []
            landmarks_ref = []
            landmarks_obs = []

            for k in data_ref[rid].keys():
                s = gtsam.Symbol(k)
                if chr(s.chr()) == rid:
                    positions_ref.append(self.getPoint(k, data_ref[rid]))
                    positions_obs.append(self.getPoint(k, data_obs[rid]))
                
                elif chr(s.chr()) == 'l':
                    landmarks_ref.append(self.getLandmark(k, data_ref[rid]))
                    landmarks_obs.append(self.getLandmark(k, data_obs[rid]))

            positions_ref = np.stack(positions_ref)
            positions_obs = np.stack(positions_obs)
            landmarks_ref = np.stack(landmarks_ref)
            landmarks_obs = np.stack(landmarks_obs)

            plt.plot(
                positions_obs.T[0],
                positions_obs.T[1],
                positions_obs.T[2],
                alpha=1,
                color=colors[idx],
                label=f'Robot {rid}'
            )
            plt.plot(
                positions_ref.T[0],
                positions_ref.T[1],
                positions_ref.T[2],
                alpha=1,
                color='black',
                label=f'Robot {rid} gt'
            )
            
            ax.scatter(
                landmarks_ref.T[0],
                landmarks_ref.T[1],
                landmarks_ref.T[2],
                alpha = 1,
                color='black',
                label=f'Robot {rid} lk'
            )
            ax.scatter(
                landmarks_obs.T[0],
                landmarks_obs.T[1],
                landmarks_obs.T[2],
                alpha = 1,
                color=colors[idx],
                label=f'Robotlk {rid}'
            )
            ax.legend()
        
        plt.axis('equal')
        plt.show()

    def boxplot(self, err_type, output_path=None):
        
        errs = self.errors[err_type]
        colors = sns.color_palette("colorblind", len(self.robots))

        plt.style.use('bmh')
        fig, ax = plt.subplots()
        ax.boxplot(errs['Robot a'], positions=[1], widths=0.5, patch_artist=True,
                   showmeans=False, showfliers=False,
                   medianprops={"color": "red", "linewidth": 1},
                   boxprops={"facecolor": colors[0], "edgecolor": "black",
                             "linewidth": 1.5},
                   whiskerprops={"color": "black", "linewidth": 1.5},
                   capprops={"color": "black", "linewidth": 1.5})

        ax.boxplot(errs['Robot b'], positions=[2], widths=0.5, patch_artist=True,
                   showmeans=False, showfliers=False,
                   medianprops={"color": "red", "linewidth": 1},
                   boxprops={"facecolor": colors[1], "edgecolor": "black",
                             "linewidth": 1.5},
                   whiskerprops={"color": "black", "linewidth": 1.5},
                   capprops={"color": "black", "linewidth": 1.5})

        ax.boxplot(errs['Robot c'], positions=[3], widths=0.5, patch_artist=True,
                   showmeans=False, showfliers=False,
                   medianprops={"color": "red", "linewidth": 1},
                   boxprops={"facecolor": colors[2], "edgecolor": "black",
                             "linewidth": 1.5},
                   whiskerprops={"color": "black", "linewidth": 1.5},
                   capprops={"color": "black", "linewidth": 1.5})
        
        ax.boxplot(errs['Robot d'], positions=[4], widths=0.5, patch_artist=True,
                   showmeans=False, showfliers=False,
                   medianprops={"color": "red", "linewidth": 1},
                   boxprops={"facecolor": colors[3], "edgecolor": "black",
                             "linewidth": 1.5},
                   whiskerprops={"color": "black", "linewidth": 1.5},
                   capprops={"color": "black", "linewidth": 1.5})

        ax.set_xticklabels(['Robot a','Robot b','Robot c','Robot d'],
                           rotation=45, fontsize=8)

        ax.set_title(err_type)

        if output_path is not None:
            plt.savefig(output_path)
        plt.show()
        # style = ['Solarize_Light2', '_classic_test_patch', '_mpl-gallery', '_mpl-gallery-nogrid', 'bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-v0_8', 'seaborn-v0_8-bright', 'seaborn-v0_8-colorblind', 'seaborn-v0_8-dark', 'seaborn-v0_8-dark-palette', 'seaborn-v0_8-darkgrid', 'seaborn-v0_8-deep', 'seaborn-v0_8-muted', 'seaborn-v0_8-notebook', 'seaborn-v0_8-paper', 'seaborn-v0_8-pastel', 'seaborn-v0_8-poster', 'seaborn-v0_8-talk', 'seaborn-v0_8-ticks', 'seaborn-v0_8-white', 'seaborn-v0_8-whitegrid', 'tableau-colorblind10']
        # plt.style.use('_mpl-gallery')

        # plt.setp(VP['boxes'], color='black')
        # plt.setp(VP['whiskers'], color='black')
        # plt.setp(VP['fliers'], color='red', marker='+')

        # ax.set_xticklabels(['label 1','label 2','label 3'],
        #                    rotation=45, fontsize=8)
        # ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        #     ylim=(0, 8), yticks=np.arange(1, 8))

    def errorbar(self, err_type=None):
        print('not implemented')

    def violin(self, err_type=None):
        print('not implemented')

    ## HELPERS section
    def getPoint(self, key, values):
        return values.atPose3(key).translation()

    def getLandmark(self, key, values):
        return values.atPoint3(key)

class MultiDisplay():
    """ This class can handle multiple datasets.
        Its goal is to compare datasets errors.
        Robots errors are aggregated as single errors.
    """

    def __init__(self):
        self.data = {}

    def add_results(self, name, Results):
        self.data[name] = Data(Results)
    
    def reset_results(self):
        self.data = {}

    def boxplot(self, err_type, output_path=None):
        # errs = {}
        colors = sns.color_palette("colorblind", len(self.data.keys()))
        plt.style.use('bmh')
        fig, ax = plt.subplots()

        for idx, data in enumerate(self.data.keys()):
            error = []
            for robot in self.data[data].errors[err_type].keys():
                error += self.data[data].errors[err_type][robot]
            # errs[data] = error

            ax.boxplot(error, positions=[idx + 1], widths=0.5, patch_artist=True,
                       showmeans=False, showfliers=False,
                       medianprops={"color": "red", "linewidth": 1},
                       boxprops={"facecolor": colors[idx], "edgecolor": "black",
                                 "linewidth": 1.5},
                       whiskerprops={"color": "black", "linewidth": 1.5},
                       capprops={"color": "black", "linewidth": 1.5})

        self.ax.set_xticklabels(self.data.keys(), rotation=45, fontsize=8)
        self.ax.set_title(err_type)
        plt.show()
    
    def std_boxplot(self, output_path=None, fig_name="fig"):
        # Set plot parameters
        colors = sns.color_palette("colorblind", len(self.data.keys()))
        plt.style.use('bmh')

        # Define axes
        fig_T_rpe, ax_T_rpe = plt.subplots()
        fig_rpe, ax_rpe = plt.subplots(1,2)
        fig_T_ape, ax_T_ape = plt.subplots()
        fig_ape, ax_ape = plt.subplots(1,2)

        # err_types = ['transformation_rpe',
        #              'point_distance_rpe',
        #              'rot_angle_deg_rpe',
        #              'transformation_ape',
        #              'point_distance_ape',
        #              'rot_angle_deg_ape']

        for idx, data in enumerate(self.data.keys()):
            # Transformation rpe
            error = []
            for robot in self.data[data].errors['transformation_rpe'].keys():
                error += self.data[data].errors['transformation_rpe'][robot]

            ax_T_rpe.boxplot(error, positions=[idx + 1], widths=0.5, patch_artist=True,
                       showmeans=False, showfliers=False,
                       medianprops={"color": "red", "linewidth": 1},
                       boxprops={"facecolor": colors[idx], "edgecolor": "black",
                                 "linewidth": 1.5},
                       whiskerprops={"color": "black", "linewidth": 1.5},
                       capprops={"color": "black", "linewidth": 1.5})

            # Point distance rpe
            error = []
            for robot in self.data[data].errors['point_distance_rpe'].keys():
                error += self.data[data].errors['point_distance_rpe'][robot]

            ax_rpe[0].boxplot(error, positions=[idx + 1], widths=0.5, patch_artist=True,
                       showmeans=False, showfliers=False,
                       medianprops={"color": "red", "linewidth": 1},
                       boxprops={"facecolor": colors[idx], "edgecolor": "black",
                                 "linewidth": 1.5},
                       whiskerprops={"color": "black", "linewidth": 1.5},
                       capprops={"color": "black", "linewidth": 1.5})

            # Rotation (deg) rpe
            error = []
            for robot in self.data[data].errors['rot_angle_deg_rpe'].keys():
                error += self.data[data].errors['rot_angle_deg_rpe'][robot]

            ax_rpe[1].boxplot(error, positions=[idx + 1], widths=0.5, patch_artist=True,
                       showmeans=False, showfliers=False,
                       medianprops={"color": "red", "linewidth": 1},
                       boxprops={"facecolor": colors[idx], "edgecolor": "black",
                                 "linewidth": 1.5},
                       whiskerprops={"color": "black", "linewidth": 1.5},
                       capprops={"color": "black", "linewidth": 1.5})

            # Transformation ape
            error = []
            for robot in self.data[data].errors['transformation_ape'].keys():
                error += self.data[data].errors['transformation_ape'][robot]

            ax_T_ape.boxplot(error, positions=[idx + 1], widths=0.5, patch_artist=True,
                       showmeans=False, showfliers=False,
                       medianprops={"color": "red", "linewidth": 1},
                       boxprops={"facecolor": colors[idx], "edgecolor": "black",
                                 "linewidth": 1.5},
                       whiskerprops={"color": "black", "linewidth": 1.5},
                       capprops={"color": "black", "linewidth": 1.5})

            # Point distance ape
            error = []
            for robot in self.data[data].errors['point_distance_ape'].keys():
                error += self.data[data].errors['point_distance_ape'][robot]

            ax_ape[0].boxplot(error, positions=[idx + 1], widths=0.5, patch_artist=True,
                       showmeans=False, showfliers=False,
                       medianprops={"color": "red", "linewidth": 1},
                       boxprops={"facecolor": colors[idx], "edgecolor": "black",
                                 "linewidth": 1.5},
                       whiskerprops={"color": "black", "linewidth": 1.5},
                       capprops={"color": "black", "linewidth": 1.5})

            # Rotation (deg) ape
            error = []
            for robot in self.data[data].errors['rot_angle_deg_ape'].keys():
                error += self.data[data].errors['rot_angle_deg_ape'][robot]

            ax_ape[1].boxplot(error, positions=[idx + 1], widths=0.5, patch_artist=True,
                       showmeans=False, showfliers=False,
                       medianprops={"color": "red", "linewidth": 1},
                       boxprops={"facecolor": colors[idx], "edgecolor": "black",
                                 "linewidth": 1.5},
                       whiskerprops={"color": "black", "linewidth": 1.5},
                       capprops={"color": "black", "linewidth": 1.5})

        ax_T_rpe.set_xticklabels(self.data.keys(), rotation=45, fontsize=8)
        ax_T_rpe.set_title('transformation_rpe')
        ax_rpe[0].set_xticklabels(self.data.keys(), rotation=45, fontsize=8)
        ax_rpe[0].set_title('point_distance_rpe')
        ax_rpe[1].set_xticklabels(self.data.keys(), rotation=45, fontsize=8)
        ax_rpe[1].set_title('rot_angle_deg_rpe')
        ax_T_ape.set_xticklabels(self.data.keys(), rotation=45, fontsize=8)
        ax_T_ape.set_title('transformation_ape')
        ax_ape[0].set_xticklabels(self.data.keys(), rotation=45, fontsize=8)
        ax_ape[0].set_title('point_distance_ape')
        ax_ape[1].set_xticklabels(self.data.keys(), rotation=45, fontsize=8)
        ax_ape[1].set_title('rot_angle_deg_ape')

        if output_path is not None:
            fig_T_rpe.savefig(os.path.join(output_path, fig_name + '_' + "T_rpe.png"))
            fig_rpe.savefig(os.path.join(output_path, fig_name + '_' + "rpe.png"))
            fig_T_ape.savefig(os.path.join(output_path, fig_name + '_' + "T_ape.png"))
            fig_ape.savefig(os.path.join(output_path, fig_name + '_' + "ape.png"))
        else:
            plt.show()