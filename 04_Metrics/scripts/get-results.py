import metrics

est_path = './input/landmarks_d/d/estimates.txt'
gt_path = './input/landmarks_d/d/groundtruth.txt'

metrics = metrics.Metrics(est_path, gt_path)
metrics.set_poseRelation('translation')
metrics.compute_ape_rmse()
metrics.compute_rpe_rmse()