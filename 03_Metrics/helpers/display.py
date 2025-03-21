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

    def plot_trajectories(self, data_type=None):
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
    
    def plot_trajectories_all(self, data_type=None):
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

        colors = sns.color_palette("colorblind", len(self.robots))
        ax = plt.figure().add_subplot(111,projection='3d')
        for idx, rid in enumerate(self.robots):
            positions = []
            for k in data[rid].keys():
                s = gtsam.Symbol(k)
                if chr(s.chr()) == rid:
                    positions.append(self.getPoint(k, data[rid]))
            positions = np.stack(positions)
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
        

        # plot
        # fig, ax = plt.subplots()
        # VP = ax.boxplot(D, positions=[2, 4, 6], widths=1, patch_artist=True,
        #                 showmeans=False, showfliers=False,
        #                 medianprops={"color": "red", "linewidth": 1},
        #                 boxprops={"facecolor": "white", "edgecolor": "black",
        #                         "linewidth": 0.5},
        #                 whiskerprops={"color": "black", "linewidth": 1.5},
        #                 capprops={"color": "black", "linewidth": 1.5})
        # VP = ax.boxplot(D, positions=[2, 4, 6], widths=1, patch_artist=True,
        #                 showmeans=False, showfliers=False,
        #                 medianprops={"color": "white", "linewidth": 0.5},
        #                 boxprops={"facecolor": "C0", "edgecolor": "white",
        #                         "linewidth": 0.5},
        #                 whiskerprops={"color": "C0", "linewidth": 1.5},
        #                 capprops={"color": "C0", "linewidth": 1.5})

        # plt.setp(VP['boxes'], color='black')
        # plt.setp(VP['whiskers'], color='black')
        # plt.setp(VP['fliers'], color='red', marker='+')

        # ax.set_xticklabels(['label 1','label 2','label 3'],
        #                    rotation=45, fontsize=8)
        # ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        #     ylim=(0, 8), yticks=np.arange(1, 8))

        # plt.show()

    def errorbar(self, err_type=None):
        print('not implemented')

    def violin(self, err_type=None):
        print('not implemented')

    ## HELPERS section
    def getPoint(self, key, values):
        return values.atPose3(key).translation()

    def getLandmark(self, key, values):
        return values.atPoint3(key)

# def path_to_dataset(path):
#     parser = jrl.Parser()
#     dataset = parser.parseDataset(path, False)
#     return dataset

# def plot_groundtruth(path):
#     if path[-4:] == '.jrl':
#         dataset = path_to_dataset(path)
#         colors = sns.color_palette("colorblind", len(dataset.robots()))
#         for idx, rid in enumerate(dataset.robots()):
#             positions = []
#             gtvals = dataset.groundTruth(rid)
#             for k in gtvals.keys():
#                 s = gtsam.Symbol(k)
#                 if chr(s.chr()) == rid:
#                     positions.append(getPoint(k, gtvals))
#             positions = np.stack(positions)
#             ax = plt.figure().add_subplot(projection='3d')
#             plt.plot(
#                 positions.T[0],
#                 positions.T[1],
#                 positions.T[2],
#                 alpha=1,
#                 color=colors[idx],
#             )
#         plt.axis('equal')
#         plt.show()


# def plot_odom(dataset, colors, args):
#     for idx, robot in enumerate(dataset.robots()):
#         if dataset.containsGroundTruth():
#             positions = []
#             gtvals = dataset.groundTruth(robot)
#             for k in gtvals.keys():
#                 s = gtsam.Symbol(k)
#                 if chr(s.chr()) == robot:
#                     positions.append(getPoint(k, gtvals, args))
#             positions = np.stack(positions)
#             if args.is3d:
#                 plt.plot(
#                     positions.T[0],
#                     positions.T[1],
#                     positions.T[2],
#                     alpha=1,
#                     color=colors[idx],
#                 )
#             else:
#                 plt.plot(
#                     positions.T[0],
#                     positions.T[1],
#                     alpha=1,
#                     color=colors[idx],
#                 )
#         """
#         if dataset.containsInitialization():
#             init_positions = []
#             initvals = dataset.initialization(robot)
#             for k in initvals.keys():
#                 s = gtsam.Symbol(k)
#                 if chr(s.chr()) == robot:
#                     init_positions.append(getPoint(k, initvals, args))
#             init_positions = np.stack(init_positions)

#             if args.is3d:
#                 plt.plot(
#                     init_positions.T[0],
#                     init_positions.T[1],
#                     init_positions.T[2],
#                     alpha=0.5,
#                     color=colors[idx],
#                     #marker=".",
#                 )
#             else:
#                 plt.plot(
#                     init_positions.T[0],
#                     init_positions.T[1],
#                     alpha=0.5,
#                     color=colors[idx],
#                     #marker=".",
#                 )
#         """

# def plot_loops(dataset, colors, args):
#     for ridx, robot in enumerate(dataset.robots()):
#         if dataset.containsGroundTruth():
#             gtvals = dataset.groundTruth(robot)
#             for entry in dataset.measurements(robot):
#                 for i in range(entry.measurements.nrFactors()):
#                     factor = entry.measurements.at(i)
#                     keys = factor.keys()
#                     if len(keys) > 1:
#                         k1, k2 = keys
#                         s1, s2 = gtsam.Symbol(k1), gtsam.Symbol(k2)

#                         pts = np.array([getPoint(k1, gtvals, args), getPoint(k2, gtvals, args)])

#                         if chr(s1.chr()) == chr(s2.chr())  and (abs(s1.index() - s2.index()) != 1) and args.plot_loops:
#                             if args.is3d:
#                                 plt.plot(
#                                     pts.T[0],
#                                     pts.T[1],
#                                     pts.T[2],
#                                     color=colors[ridx],
#                                     alpha=0.5,
#                                     marker=".",
#                                 )
#                             else:
#                                 plt.plot(
#                                     pts.T[0],
#                                     pts.T[1],
#                                     color=colors[ridx],
#                                     alpha=0.5,
#                                     marker=".",
#                                 )

#                         if chr(s1.chr()) != chr(s2.chr()) and args.plot_comms:
#                             if args.is3d:
#                                 plt.plot(pts.T[0], pts.T[1], pts.T[2], color="black", alpha=0.1)
#                             else:
#                                 plt.plot(pts.T[0], pts.T[1], color="black", alpha=0.1)


# def main():
#     args = handle_args()

#     colors = sns.color_palette("colorblind", len(dataset.robots()))

#     print(dataset.robots())

#     fig = plt.figure(dpi=200, figsize=[3,3])
#     if args.is3d:
#         ax = fig.add_subplot(projection="3d")
#     else:
#         ax = plt.gca()
#     plot_odom(dataset, colors, args)
#     plot_loops(dataset, colors, args)

#     # Turn off numbers on axes
#     ax.set_xticklabels([])
#     ax.set_yticklabels([])
#     if (args.is3d):
#         ax.set_zticklabels([])
#         ax.view_init(elev=30, azim=45)
#     ax.set_aspect("equal")
#     ax.set_axis_off()
#     plt.tight_layout(pad=0.25)
#     if args.save:
#         plt.savefig("{}_fig.png".format(dataset.name()))

#     plt.show()

# Tracer le graphe de facteurs
# marginals = gtsam.Marginals(graph, result)

# p3d_es = []
# p3d_gt = []
# for k in result.keys():
#     #plot.plot_pose3(k, result.atPose3(k), 0.5,marginals.marginalCovariance(k))
#     p3d_es.append(result.atPose3(k).translation())
#     p3d_gt.append(initial_estimates.atPose3(k).translation())
# pos_es = np.stack(p3d_es)
# pos_gt = np.stack(p3d_gt)
# ax = plt.figure().add_subplot(projection='3d')
# plt.plot(pos_gt.T[0],pos_gt.T[1],pos_gt.T[2],alpha=1,color='g')
# plt.plot(pos_es.T[0],pos_es.T[1],pos_es.T[2],alpha=1,color='r')
# plt.axis('equal')
# plt.show()

#     keys = factor.keys()
        #     if len(keys) ==1:
        #         s = gtsam.Symbol(keys[0])
        #         if chr(s.chr()) == robot:
        #             graph.add(factor)
        #         #graph.add(gtsam.PriorFactorPose3(factor.keys()[0], factor.prior(), factor.noiseModel()))
        #     if len(keys) > 1:
        #         k1, k2 = keys
        #         s1, s2 = gtsam.Symbol(k1), gtsam.Symbol(k2)

        #         #pts = np.array([getPoint(k1, gtvals, args), getPoint(k2, gtvals, args)])

        #         if chr(s1.chr()) == chr(s2.chr())  and chr(s1.chr()) == robot:
        #             graph.add(factor)

        #             if k1 not in allkeys:
        #                 initial_estimates.insert(k1, gtvals.atPose3(k1))
        #                 allkeys.append(k1)
        #             if k2 not in allkeys:
        #                 initial_estimates.insert(k2, gtvals.atPose3(k2))
        #                 allkeys.append(k2)

                #if chr(s1.chr()) != chr(s2.chr()) and args.plot_comms:
                #    pass

class MultiDisplay():

    def __init__(self):
        self.data = {}

    def add_results(self, name, Results)
        self.data[name] = Data(Results)

    def plot_trajectories(self, data_type=None):
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
    
    def plot_trajectories_all(self, data_type=None):
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

        colors = sns.color_palette("colorblind", len(self.robots))
        ax = plt.figure().add_subplot(111,projection='3d')
        for idx, rid in enumerate(self.robots):
            positions = []
            for k in data[rid].keys():
                s = gtsam.Symbol(k)
                if chr(s.chr()) == rid:
                    positions.append(self.getPoint(k, data[rid]))
            positions = np.stack(positions)
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