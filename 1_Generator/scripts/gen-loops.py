import numpy as np
import gtsam

def get_all_edges(robots):
    edges = set()
    for rid in robots:
        for oid in robots:
            if rid != oid:
                edge = (min(rid,oid),max(rid,oid))
                edges.add(edge)
    return edges

def pack_lid_per_rid(robots, nb_lks, group_type):
    lk_ids = [gtsam.symbol('#', i + 1) for i in range(nb_lks)]
    lid_dict = {}

    if group_type == 'edges':
        edges = get_all_edges(robots)
        batch_nb = nb_lks // len(edges)

        # init structure
        for rid in robots:
            lid_dict[rid] = set()

        for index, edge in enumerate(edges):
            lks = [lk_ids[index * batch_nb + i] for i in range(batch_nb)]
            for lk in lks:
                lid_dict[edge[0]].add(lk)
                lid_dict[edge[1]].add(lk)
        
        for rid in robots:
            lid_dict[rid] = list(lid_dict[rid])

    elif group_type == 'all':
        for rid in robots:
            lid_dict[rid] = lk_ids

    return lid_dict

def gen_lc_indirect(robots, nb_poses, nb_lc, ind_thr, seed):
    data = {}
    np.random.seed(seed)
    seeds = np.random.randint(nb_poses, size=2*len(robots)).reshape(-1,2)

    for idx, rid in enumerate(robots):
        o_robots = robots.copy()
        o_robots.remove(rid)

        np.random.seed(seeds[idx][0])
        pose_num = np.random.randint(ind_thr, nb_poses, size=lc_ind_nb)
        pose_num.sort()
        data[rid + '_poses'] = pose_num

        np.random.seed(seeds[idx][1])
        data[rid + '_oids'] = np.random.choice(o_robots, size=lc_ind_nb)

        data[rid + '_index'] = 0

    return data

def gen_landmarks(robots, nb_poses, nb_lks, landmarks, seed):
    data = {}
    np.random.seed(seed)
    seeds = np.random.randint(nb_poses, size=2*len(robots)).reshape(-1,2)

    for idx, rid in enumerate(robots):

        np.random.seed(seeds[idx][0])
        pose_num = np.random.randint(nb_poses, size=nb_lks)
        pose_num.sort()
        data[rid + '_poses'] = pose_num

        np.random.seed(seeds[idx][1])
        lks = np.random.choice(landmarks[rid], size=nb_lks)
        data[rid + '_lks'] = lks

        data[rid + '_index'] = 0

    return data

robots = ['a','b','c','d']
seed = 53
lc_ind_nb = 20
ind_thr = 20
nb_poses = 500

nb_lks = 20
group_type = 'edges'

landmarks = pack_lid_per_rid(robots, nb_lks, group_type)

lc_ind_data = gen_lc_indirect(robots, nb_poses, lc_ind_nb, ind_thr, seed)
lks_data = gen_landmarks(robots, nb_poses, nb_lks, landmarks, 38)
print(lks_data['a_lks'])



# var.sort()
# print(var)

# set seeds for each robots

# for robot in robots:
#     print(np.random.randint(500))