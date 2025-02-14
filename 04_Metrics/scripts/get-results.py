import metrics

est_path = './test/landmarks_d/a/estimates.txt'
gt_path = './test/landmarks_d/a/groundtruth.txt'

metrics = metrics.Metrics(est_path, gt_path)