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
        rid = 'a'
        self.groundtruths = Results.dataset.groundTruth(rid)
        self.initializations = Results.dataset.initialization()
        self.estimates = Results.results.robot_solutions

        print(self.groundtruths[rid].values)


def path_to_dataset(path):
    parser = jrl.Parser()
    dataset = parser.parseDataset(path, False)
    return dataset

def getPoint(key, values):
    return values.atPose3(key).translation()

def plot_groundtruth(path):
    if path[-4:] == '.jrl':
        dataset = path_to_dataset(path)
        colors = sns.color_palette("colorblind", len(dataset.robots()))
        for idx, rid in enumerate(dataset.robots()):
            positions = []
            gtvals = dataset.groundTruth(rid)
            for k in gtvals.keys():
                s = gtsam.Symbol(k)
                if chr(s.chr()) == rid:
                    positions.append(getPoint(k, gtvals))
            positions = np.stack(positions)
            ax = plt.figure().add_subplot(projection='3d')
            plt.plot(
                positions.T[0],
                positions.T[1],
                positions.T[2],
                alpha=1,
                color=colors[idx],
            )
        plt.axis('equal')
        plt.show()


def plot_odom(dataset, colors, args):
    for idx, robot in enumerate(dataset.robots()):
        if dataset.containsGroundTruth():
            positions = []
            gtvals = dataset.groundTruth(robot)
            for k in gtvals.keys():
                s = gtsam.Symbol(k)
                if chr(s.chr()) == robot:
                    positions.append(getPoint(k, gtvals, args))
            positions = np.stack(positions)
            if args.is3d:
                plt.plot(
                    positions.T[0],
                    positions.T[1],
                    positions.T[2],
                    alpha=1,
                    color=colors[idx],
                )
            else:
                plt.plot(
                    positions.T[0],
                    positions.T[1],
                    alpha=1,
                    color=colors[idx],
                )
        """
        if dataset.containsInitialization():
            init_positions = []
            initvals = dataset.initialization(robot)
            for k in initvals.keys():
                s = gtsam.Symbol(k)
                if chr(s.chr()) == robot:
                    init_positions.append(getPoint(k, initvals, args))
            init_positions = np.stack(init_positions)
            
            if args.is3d:
                plt.plot(
                    init_positions.T[0],
                    init_positions.T[1],
                    init_positions.T[2],
                    alpha=0.5,
                    color=colors[idx],
                    #marker=".",
                )
            else:
                plt.plot(
                    init_positions.T[0],
                    init_positions.T[1],
                    alpha=0.5,
                    color=colors[idx],
                    #marker=".",
                )
        """

def plot_loops(dataset, colors, args):
    for ridx, robot in enumerate(dataset.robots()):
        if dataset.containsGroundTruth():
            gtvals = dataset.groundTruth(robot)
            for entry in dataset.measurements(robot):
                for i in range(entry.measurements.nrFactors()):
                    factor = entry.measurements.at(i)
                    keys = factor.keys()
                    if len(keys) > 1:
                        k1, k2 = keys
                        s1, s2 = gtsam.Symbol(k1), gtsam.Symbol(k2)

                        pts = np.array([getPoint(k1, gtvals, args), getPoint(k2, gtvals, args)])

                        if chr(s1.chr()) == chr(s2.chr())  and (abs(s1.index() - s2.index()) != 1) and args.plot_loops:
                            if args.is3d:
                                plt.plot(
                                    pts.T[0],
                                    pts.T[1],
                                    pts.T[2],
                                    color=colors[ridx],
                                    alpha=0.5,
                                    marker=".",
                                )
                            else:
                                plt.plot(
                                    pts.T[0],
                                    pts.T[1],
                                    color=colors[ridx],
                                    alpha=0.5,
                                    marker=".",
                                )

                        if chr(s1.chr()) != chr(s2.chr()) and args.plot_comms:
                            if args.is3d:
                                plt.plot(pts.T[0], pts.T[1], pts.T[2], color="black", alpha=0.1)
                            else:
                                plt.plot(pts.T[0], pts.T[1], color="black", alpha=0.1)


def main():
    args = handle_args()
    
    colors = sns.color_palette("colorblind", len(dataset.robots()))

    print(dataset.robots())

    fig = plt.figure(dpi=200, figsize=[3,3])
    if args.is3d:
        ax = fig.add_subplot(projection="3d")
    else:
        ax = plt.gca()
    plot_odom(dataset, colors, args)
    plot_loops(dataset, colors, args)

    # Turn off numbers on axes
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    if (args.is3d):
        ax.set_zticklabels([])
        ax.view_init(elev=30, azim=45)
    ax.set_aspect("equal")
    ax.set_axis_off()
    plt.tight_layout(pad=0.25)
    if args.save:
        plt.savefig("{}_fig.png".format(dataset.name()))
    
    plt.show()

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


if __name__ == "__main__":
    #main()
    plot_groundtruth('output/datasets/syscon25/pose_nb/pose_nb_6_0000.jrl')
    #plot_groundtruth('output/datasets/syscon25/dataset_4R_0000.jrl')