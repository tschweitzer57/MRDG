import os
from os.path import basename, dirname, split
from collections import defaultdict

def get_dataset_paths(directory):
    dataset_paths = defaultdict(lambda: defaultdict(lambda: defaultdict((lambda: defaultdict(lambda: defaultdict(list))))))
    
    for root, dirs, files in os.walk(directory):
        if files:
            #TODO convertir files en liste de robots avec gt et est
            # dir_solver = split(root)[1]
            # dir_parameterSet = split(split(root)[0])[1]
            # dir_testParameter = split(split(split(root)[0])[0])[1]
            # dataset_paths[dir_testParameter][dir_parameterSet][dir_solver] = files
            dirs = root.split('/')

            for file in files:
                file_name, ext = os.path.splitext(file)
                if ext == '.txt':
                    file_name = file_name.split('_')
                    dataset_paths[dirs[-3]][dirs[-2]][dirs[-1]][file_name[1]][file_name[-1]] = os.path.join(root, file)
            # dir_ = dirname(root)
            # ext = os.path.splitext(files[1])
            # print('basename :', os.path.basename(root))
            # print('split :', os.path.split(root))
            # print('extension :', ext)
            # print('dirname :', basename(dir_))

            # file_paths = []
            # for file in files:
            #     if file[-4:] == '.txt':
            #         file_paths.append(os.path.join(root, file))
            # dataset_paths[os.path.basename(root)] = file_paths
            break
    return dataset_paths

def stack_results(files):
    for file in files:
        print(0)
    return 0

if __name__ == "__main__":

    directory = 'output/results/syscon25'
    results = get_dataset_paths(directory)
    print(results['lc_pose_th']['10_0000']['centralized']['a']['groundtruth'])
    #print(len(results['centralized']))