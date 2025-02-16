import jrl
import gtsam
import os

parser = jrl.Parser()
results = parser.parseResults('./input/landmarks_geodesic-mesa_2025-02-13_09-21-15/final_results.jrr.cbor',True)
# print(results.robots)
# print(results.robot_solutions['a'].values.keys())
# print('name: ',results.dataset_name)
# print('method_name: ',results.method_name)

for rid in results.robots:
    folder = 'test'
    raw_path = os.path.join('.',folder,results.dataset_name + '_d',rid)
    os.makedirs(raw_path, exist_ok=True)
    gtFName = os.path.join(raw_path, 'groundtruth.txt')
    estFName = os.path.join(raw_path, 'estimates.txt')
    initFName = os.path.join(raw_path, 'initialization.txt')

    # f_gt = open(gtFName,'w')
    f_es = open(estFName,'w')
    # f_init = open(initFName,'w')

    # f_gt.write("# time x y z qx qy qz qw\n")
    f_es.write("# time x y z qx qy qz qw\n")
    # f_init.write("# time x y z qx qy qz qw\n")
    estimates = results.robot_solutions[rid].values
    stamp = 0

    for key in estimates.keys():
        # Export groundtruth
        # tr = self.groundtruths[rid].atPose3(key).translation()
        # quat = self.groundtruths[rid].atPose3(key).rotation().toQuaternion()
        # line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
        # f_gt.write(' '.join(map(str, line)) + '\n')

        # Export estimates
        s = chr(gtsam.Symbol(key).chr())
        #id = gtsam.Symbol(key).index()
        if s != 'l':
            tr = estimates.atPose3(key).translation()
            quat = estimates.atPose3(key).rotation().toQuaternion()
            line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
            f_es.write(' '.join(map(str, line)) + '\n')
            stamp += 1

        # Export initilizations
        # tr = self.initializations[rid].atPose3(key).translation()
        # quat = self.initializations[rid].atPose3(key).rotation().toQuaternion()
        # line = [stamp,tr.T[0],tr.T[1],tr.T[2],quat.x(),quat.y(),quat.z(),quat.w()]
        # f_init.write(' '.join(map(str, line)) + '\n')

        # Handle stamp
        
        #break