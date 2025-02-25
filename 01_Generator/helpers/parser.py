import jrl
import gtsam
import numpy as np
from collections import defaultdict

class DatasetParser():
    def __init__(self, dataset_path):
        parser = jrl.Parser()
        self.dataset = parser.parseDataset(dataset_path, False)

    def print(self,file=False, filepath=None, verbose=False):
        output  = "*****************************\n"
        output += "*      Dataset Summary      *\n"
        output += "*****************************\n"

        output += f"dataset name: {self.dataset.name()}\n"
        output += f"robots: {self.dataset.robots()}\n\n"

        for rid in self.dataset.robots():
            output += f"Factors : Robot {rid}\n"
            output += f"-----------------\n"
            output += self.get_general(rid)
            output += f"-----------------\n"
            output += self.get_odometry(rid)
            output += self.get_lc_intra(rid)
            output += self.get_lc_inter_direct(rid)
            output += self.get_lc_inter_indirect(rid)
            output += "\n"
        output += self.get_landmarks()

        if verbose:
            print(output)

        if file:
            if filepath is None:
                file_name = f"{self.dataset.name()}_parsed.txt"
            else:
                file_name = filepath

            with open(file_name, "w") as file:
                file.write(output)

    def get_general(self, rid):
        nr_poses = 0
        nr_prior = 0
        nr_landmarks = 0
        nr_lc_intra = 0
        nr_lc_inter_direct_range = {}
        nr_lc_inter_direct_pose = {}
        nr_lc_inter_indirect = {}

        # Init dictionaries
        for oid in self.dataset.robots():
            if oid != rid:
                nr_lc_inter_direct_range[oid] = 0
                nr_lc_inter_direct_pose[oid] = 0
                nr_lc_inter_indirect[oid] = 0

        for entry in self.dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)

                # Detecting prior knowledge:
                if len(factor.keys()) == 1:
                    nr_prior += 1
                else:
                    key1 = factor.keys()[0]
                    key2 = factor.keys()[1]
                    nr_poses = max(gtsam.Symbol(key1).index(),gtsam.Symbol(key2).index()) + 1

                    is_key1_rid = chr(gtsam.Symbol(key1).chr()) == rid
                    is_key2_rid = chr(gtsam.Symbol(key2).chr()) == rid
                    is_lk = (chr(gtsam.Symbol(key1).chr()) == 'l' or chr(gtsam.Symbol(key2).chr()) == 'l')
                    are_consecutive = gtsam.Symbol(key1).index() + 1 == gtsam.Symbol(key2).index()
                    is_inter = chr(gtsam.Symbol(key1).chr()) != chr(gtsam.Symbol(key2).chr())
                    is_direct = gtsam.Symbol(key1).index() == gtsam.Symbol(key2).index()

                    # Detecting landmark
                    if is_lk:
                        nr_landmarks += 1
                    # Detecting lc intra
                    if is_key1_rid and is_key2_rid and not are_consecutive:
                        nr_lc_intra += 1
                    # Detecting lc inter direct
                    if is_inter and is_direct and not is_lk:
                        if isinstance(factor, gtsam.RangeFactorPose3):
                            if is_key1_rid:
                                nr_lc_inter_direct_range[chr(gtsam.Symbol(key2).chr())] += 1
                            else:
                                nr_lc_inter_direct_range[chr(gtsam.Symbol(key1).chr())] += 1
                        else:
                            if is_key1_rid:
                                nr_lc_inter_direct_pose[chr(gtsam.Symbol(key2).chr())] += 1
                            else:
                                nr_lc_inter_direct_pose[chr(gtsam.Symbol(key1).chr())] += 1
                            
                    # Detecting lc inter indirect
                    if is_inter and not is_direct and not is_lk:
                        if is_key1_rid:
                            nr_lc_inter_indirect[chr(gtsam.Symbol(key2).chr())] += 1
                        else:
                            nr_lc_inter_indirect[chr(gtsam.Symbol(key1).chr())] += 1

        output  = f'Number of poses : {nr_poses}\n'
        output += f'Number of priors : {nr_prior}\n'
        output += f'Number of landmarks : {nr_landmarks}\n\n'
        output += '----- Loop closures -----\n'
        output += f'Intra : {nr_lc_intra}\n'
        for key in nr_lc_inter_direct_range.keys():
            output += f'Inter Direct - range [{key}]: {nr_lc_inter_direct_range[key]}\n'
        for key in nr_lc_inter_direct_pose.keys():
            output += f'Inter Direct - pose [{key}]: {nr_lc_inter_direct_pose[key]}\n'
        for key in nr_lc_inter_indirect.keys():
            output += f'Inter Indirect [{key}]: {nr_lc_inter_indirect[key]}\n'

        return output

    # TODO Merge parsers for a same robot
    def get_odometry(self, rid):
        output = f"--ODOMETRY--\n"
        for entry in self.dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                if len(factor.keys()) > 1:
                    key1 = factor.keys()[0]
                    key2 = factor.keys()[1]
                    is_odom_1 = chr(gtsam.Symbol(key1).chr()) == rid
                    is_odom_2 = chr(gtsam.Symbol(key2).chr()) == rid
                    is_odom_3 = gtsam.Symbol(key1).index() + 1 == gtsam.Symbol(key2).index()
                    if (is_odom_1 and is_odom_2 and is_odom_3):
                        output += f"{chr(gtsam.Symbol(key1).chr())}{gtsam.Symbol(key1).index()}"
                        output += f" - {chr(gtsam.Symbol(key2).chr())}{gtsam.Symbol(key2).index()}\n"
        return output

    def get_lc_intra(self, rid):
        output = f"--LC Intra--\n"
        for entry in self.dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                if len(factor.keys()) > 1:
                    key1 = factor.keys()[0]
                    key2 = factor.keys()[1]
                    is_odom_1 = chr(gtsam.Symbol(key1).chr()) == rid
                    is_odom_2 = chr(gtsam.Symbol(key2).chr()) == rid
                    is_odom_3 = gtsam.Symbol(key1).index() + 1 == gtsam.Symbol(key2).index()
                    if (is_odom_1 and is_odom_2 and not is_odom_3):
                        output += f"{chr(gtsam.Symbol(key1).chr())}{gtsam.Symbol(key1).index()}"
                        output += f" - {chr(gtsam.Symbol(key2).chr())}{gtsam.Symbol(key2).index()}\n"
        return output

    def get_lc_inter_direct(self, rid):
        output = f"--LC INTER - DIRECT--\n"
        for entry in self.dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                if len(factor.keys()) > 1:
                    key1 = factor.keys()[0]
                    key2 = factor.keys()[1]
                    is_lk = (chr(gtsam.Symbol(key1).chr()) == 'l' or chr(gtsam.Symbol(key2).chr()) == 'l')
                    is_inter = chr(gtsam.Symbol(key1).chr()) != chr(gtsam.Symbol(key2).chr())
                    is_direct = gtsam.Symbol(key1).index() == gtsam.Symbol(key2).index()
                    if (is_inter and is_direct and not is_lk):
                        output += f"{chr(gtsam.Symbol(key1).chr())}{gtsam.Symbol(key1).index()}"
                        output += f" - {chr(gtsam.Symbol(key2).chr())}{gtsam.Symbol(key2).index()}\n"
        return output

    def get_lc_inter_indirect(self, rid):
        output = f"--LC INTER - INDIRECT--\n"
        for entry in self.dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                if len(factor.keys()) > 1:
                    key1 = factor.keys()[0]
                    key2 = factor.keys()[1]
                    is_lk = (chr(gtsam.Symbol(key1).chr()) == 'l' or chr(gtsam.Symbol(key2).chr()) == 'l')
                    is_inter = chr(gtsam.Symbol(key1).chr()) != chr(gtsam.Symbol(key2).chr())
                    is_indirect = gtsam.Symbol(key1).index() != gtsam.Symbol(key2).index()
                    if (is_inter and is_indirect and not is_lk):
                        output += f"{chr(gtsam.Symbol(key1).chr())}{gtsam.Symbol(key1).index()}"
                        output += f" - {chr(gtsam.Symbol(key2).chr())}{gtsam.Symbol(key2).index()}\n"
        return output
        

    def has_comm_edge(self):
        has_comm_edge = False

        for rid in self.dataset.robots():
            for entry in self.dataset.measurements(rid):
                for i in range(entry.measurements.nrFactors()):
                    factor = entry.measurements.at(i)
                    for key in factor.keys():
                        key_rid = chr(gtsam.Symbol(key).chr())
                        if rid != key_rid:
                            has_comm_edge = True

        return has_comm_edge

#TODO sort data
    def get_landmarks(self):
        output = f"-- LANDMARKS --"

        self.landmarks = defaultdict(set)
        for rid in self.dataset.robots():
            for entry in self.dataset.measurements(rid):
                for i in range(entry.measurements.nrFactors()):
                    factor = entry.measurements.at(i)
                    if len(factor.keys()) > 1:
                        key1 = factor.keys()[0]
                        key2 = factor.keys()[1]
                        if chr(gtsam.Symbol(key1).chr()) == 'l':
                            self.landmarks[key1].add(key2)
                        elif chr(gtsam.Symbol(key2).chr()) == 'l':
                            self.landmarks[key2].add(key1)

        for l_key in self.landmarks.keys():
            output += f"\n\n# {chr(gtsam.Symbol(l_key).chr())}{gtsam.Symbol(l_key).index()} #\n"
            for key in self.landmarks[l_key]:
                output += f"{chr(gtsam.Symbol(key).chr())}{gtsam.Symbol(key).index()}, "
        
        return output

        
def display_factor(factor, key1, key2=None):
    factor1 = chr(gtsam.Symbol(key1).chr()) +":"+ str(gtsam.Symbol(key1).index())
    
    if isinstance(factor, gtsam.BetweenFactorPose3):
        type_f = 'Between Factor'
    elif isinstance(factor, gtsam.PriorFactorPose3):
        type_f = 'Prior Factor'
    elif isinstance(factor, gtsam.RangeFactorPose3):
        type_f = 'Range Factor'
    else:
        type_f = 'unknown'
    
    if key2 is not None:
        factor2 = chr(gtsam.Symbol(key2).chr()) +":"+ str(gtsam.Symbol(key2).index())
        print(factor1, '-', factor2, '->',type_f)
    else:
        print(factor1,'->',type_f)

def parse_sharedFactors(dataset):
    print("\n########## Shared Factors ##########\n")

    for rid in dataset.robots():
        print("\n########## ","Robot:", rid," ##########\n")

        for entry in dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                keys = factor.keys()

                if len(keys) == 2:
                    if (chr(gtsam.Symbol(keys[0]).chr()) != rid or chr(gtsam.Symbol(keys[1]).chr()) != rid):
                        key1 = keys[0]
                        key2 = keys[1]
                        display_factor(factor, key1, key2)

def parse_edges(dataset):
    print("\n########## Edges ##########\n")
    edges = set()
    for rid in dataset.robots():
        for entry in dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                for key in factor.keys():
                    key_rid = chr(gtsam.Symbol(key).chr())
                    if rid != key_rid:
                        edges.add((min(rid, key_rid), max(rid, key_rid)))

    print(edges)

def parse_priorFactors(dataset):
    print("\n########## Prior Factors ##########")
    
    for rid in dataset.robots():
        print("\n########## ","Robot:", rid," ##########")

        for entry in dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                if isinstance(factor, gtsam.PriorFactorPose3):
                    display_factor(factor,factor.keys()[0])

def parse_odometryFactors(dataset):
    print("\n########## Odometry Factors ##########")

    for rid in dataset.robots():
        print("\n########## ","Robot:", rid," ##########")

        for entry in dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                if len(factor.keys()) > 1:
                    key1 = factor.keys()[0]
                    key2 = factor.keys()[1]
                    is_odom_1 = chr(gtsam.Symbol(key1).chr()) == rid
                    is_odom_2 = chr(gtsam.Symbol(key2).chr()) == rid
                    is_odom_3 = gtsam.Symbol(key1).index() + 1 == gtsam.Symbol(key2).index()
                    if (is_odom_1 and is_odom_2 and is_odom_3):
                        display_factor(factor,key1,key2)

def parse_selfLoopclosure(dataset):
    print("\n########## Loop closure (self) ##########")

    for rid in dataset.robots():
        print("\n########## ","Robot:", rid," ##########")

        for entry in dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                if len(factor.keys()) > 1:
                    key1 = factor.keys()[0]
                    key2 = factor.keys()[1]
                    is_odom_1 = chr(gtsam.Symbol(key1).chr()) == rid
                    is_odom_2 = chr(gtsam.Symbol(key2).chr()) == rid
                    is_odom_3 = gtsam.Symbol(key1).index() + 1 == gtsam.Symbol(key2).index()
                    if (is_odom_1 and is_odom_2 and not is_odom_3):
                        display_factor(factor,key1,key2)

def parse_loopclosure(dataset):
    print("\n########## Loop closure (swarm) ##########")
    
    for rid in dataset.robots():
        print("\n########## ","Robot:", rid," ##########")

        for entry in dataset.measurements(rid):
            for i in range(entry.measurements.nrFactors()):
                factor = entry.measurements.at(i)
                if len(factor.keys()) > 1:
                    key1 = factor.keys()[0]
                    key2 = factor.keys()[1]
                    is_odom_1 = not chr(gtsam.Symbol(key1).chr()) == rid
                    is_odom_2 = not chr(gtsam.Symbol(key2).chr()) == rid
                    index_diff = np.abs(gtsam.Symbol(key1).index() - gtsam.Symbol(key2).index()) > 1
                    if ((is_odom_1 or is_odom_2) and index_diff):
                        display_factor(factor,key1,key2)

if __name__ == '__main__':
    
    parser = jrl.Parser()
    dataset = parser.parseDataset("output/datasets/syscon25/lc_probability/lc_probability_1_0000.jrl", False)
    print("Robots :\n", dataset.robots())

    parse_sharedFactors(dataset)
    parse_edges(dataset)
    # parse_priorFactors(dataset)
    # parse_odometryFactors(dataset)
    # parse_loopclosure(dataset)
    # parse_selfLoopclosure(dataset)