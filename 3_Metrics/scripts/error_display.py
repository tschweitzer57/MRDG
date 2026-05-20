import os
import numpy as np

from results import Results, Results2, Results3, GroupResults
from loader import Loader
from display_metrics import DisplayMetrics

# ============================================================
#  Configuration — adapt these paths for each experiment
# ============================================================
DATASET_FOLDER = './datasets/VLD1_detection'
RESULTS_FOLDER = './input/VLD1_detection_2026_05_19_01_50'
OUTPUT_FOLDER  = 'saved_output'
SOLVERS        = ['mesa-2']

# ============================================================
#  Pipeline
# ============================================================
loader = Loader(SOLVERS, RESULTS_FOLDER, DATASET_FOLDER)

for dg in loader:
    print(f"\n[{dg.dataset}] solver={dg.solver}")

    test = GroupResults('value')
    print(test)

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
