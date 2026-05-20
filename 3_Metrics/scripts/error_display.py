import os
import numpy as np

from results import Results, Results2, Results3, ResultsGroup
from loader import Loader
from display_metrics import DisplayMetrics

# ============================================================
#  Configuration — adapt these paths for each experiment
# ============================================================
DATASET_FOLDER_1 = './datasets/VLD1_detection'
DATASET_FOLDER_2 = './datasets/VLD1_detection_lk'
DATASET_FOLDER_3 = './datasets/VLD1_lk'

RESULTS_FOLDER_1 = './input/VLD1_detection_2026_05_19_01_50'
RESULTS_FOLDER_2 = './input/VLD1_detection_2026_05_19_12_09'
RESULTS_FOLDER_3 = './input/VLD1_detection_lk_2026_05_19_02_55'
RESULTS_FOLDER_4 = './input/VLD1_detection_lk_2026_05_19_13_39'
RESULTS_FOLDER_5 = './input/VLD1_lk_2026_05_19_03_59'

# ============================================================
DATASET_FOLDERS = [DATASET_FOLDER_1, DATASET_FOLDER_2, DATASET_FOLDER_3]
RESULTS_FOLDERS = [RESULTS_FOLDER_1, RESULTS_FOLDER_2, RESULTS_FOLDER_3,
                   RESULTS_FOLDER_4, RESULTS_FOLDER_5]
SOLVERS        = ['geodesic-mesa-2', 'geodesic-pyxis']
OUTPUT_FOLDER  = 'saved_output'

# ============================================================
#  Pipeline
# ============================================================
# loader = Loader(SOLVERS, RESULTS_FOLDER, DATASET_FOLDER)
DataGroup = ResultsGroup(SOLVERS, RESULTS_FOLDERS, DATASET_FOLDERS)

for key in DataGroup.sorted_results.keys():
    print(f'Solver: {key}')
    for result in DataGroup.sorted_results[key]:
        print(result.dataset_name)
        result.compute_metrics()
        break
    break
#     print(f"\n[{dg.dataset}] solver={dg.solver}")

#     test = GroupResults('value')
#     print(test)

    # ---- RTE & APE via final trajectory results ----
    # res = Results(dg.result_path, dg.dataset_path, OUTPUT_FOLDER)
    # res.generate_intermediate_results()
    # res.generate_metrics_results(minimal=False, pose_types=['point_distance'])

    # rte_errors = res.errors['point_distance_rpe']   # {'Robot a': [...], ...}
    # ape_errors = res.errors['point_distance_ape']   # {'Robot a': [...], ...}

    # print("  Mean RTE per robot:")
    # for robot, errs in rte_errors.items():
    #     print(f"    {robot}: {np.mean(errs):.4f} m  (std={np.std(errs):.4f})")

    # print("  Mean APE per robot:")
    # for robot, errs in ape_errors.items():
    #     print(f"    {robot}: {np.mean(errs):.4f} m  (std={np.std(errs):.4f})")

    # ---- Consensus via iteration-based results (shared landmarks only) ----
    # res2 = Results2(dg.result_path, dg.dataset_path, OUTPUT_FOLDER)
    # cs_errors = res2.get_mean_consensus_all_lk()

    # if cs_errors:
    #     print("  Mean consensus error per pair (averaged over all shared landmarks):")
    #     for pair, errs in cs_errors.items():
    #         print(f"    {pair[0]}-{pair[1]}: {np.mean(errs):.4f} m  (std={np.std(errs):.4f})")
    # else:
    #     print("  No shared landmarks — consensus not computed.")

    # ---- Visualizations ----
    # tag = f"{dg.dataset}_{dg.solver}"
    # dsp = DisplayMetrics(OUTPUT_FOLDER)

    # dsp.plot_rte_ape_per_robot(
    #     rte_errors, ape_errors,
    #     title=f"RTE & APE par robot  ({dg.dataset} — {dg.solver})",
    #     fig_name=f"rte_ape_{tag}",
    # )

    # if cs_errors:
    #     dsp.plot_consensus_per_pair(
    #         cs_errors,
    #         title=f"Consensus par paire  ({dg.dataset} — {dg.solver})",
    #         fig_name=f"consensus_{tag}",
    #     )
