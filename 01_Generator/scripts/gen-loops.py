import numpy as np

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
        oids = np.random.choice(o_robots, size=lc_ind_nb)
        data[rid + '_oids'] = oids

    return data

def gen_landmarks(robots, nb_poses, nb_lk, landmarks, repartition, seed):
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
        oids = np.random.choice(o_robots, size=lc_ind_nb)
        data[rid + '_oids'] = oids

    return data

robots = ['a','b','c','d']
seed = 53
lc_ind_nb = 20
ind_thr = 20
nb_poses = 500

lc_ind_data = gen_lc_indirect(robots, nb_poses, lc_ind_nb, ind_thr, seed)

# var.sort()
# print(var)

# set seeds for each robots

# for robot in robots:
#     print(np.random.randint(500))