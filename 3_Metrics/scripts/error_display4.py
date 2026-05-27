import os
import numpy as np
from collections import defaultdict
import matplotlib.cm as cm

from results import Results, Results2, Results3, ResultsGroup
from display_metrics import DisplayMetrics

# ============================================================
#  Dataset folder paths — adapt these paths for each experiment
# ============================================================
DATASET_FOLDER_1 = './datasets/VLD1_lk'
DATASET_FOLDER_2 = './datasets/OUT10_lk'
DATASET_FOLDER_3 = './datasets/OUT20_lk'

# ============================================================
#  C-SLAM results folder paths — adapt these paths for each experiment
# ============================================================
RESULTS_FOLDER_1 = './input/OUT20_lk_hpyxisA_2026_05_27_11_39'
RESULTS_FOLDER_2 = './input/OUT20_lk_hpyxisC_2026_05_27_11_39'

DATASET_FOLDERS = [DATASET_FOLDER_1, DATASET_FOLDER_2, DATASET_FOLDER_3]
RESULTS_FOLDERS = [RESULTS_FOLDER_1, RESULTS_FOLDER_2]
SOLVERS        = ['hierarchical-admm-optC', 'hierarchical-admm']
OUTPUT_FOLDER  = 'saved_output'

# Check detection_lk before detection (more specific)
SCENARIOS = ['lk']
ROBOTS    = [5, 15, 25, 35, 45, 55]

# 2 base colormaps — one per solver
SOLVER_CMAPS = {
    'hierarchical-admm': cm.Blues,
    'hierarchical-admm-optC':  cm.Oranges,
}

# ============================================================
#  Helper functions
# ============================================================

def parse_dataset_name(name):
    """Return (scenario, dtype) extracted from a dataset name, or (None, None)."""
    scenario = next((s for s in SCENARIOS if s in name), None)
    if '_edge_' in name or name.endswith('_edge'):
        dtype = 'edge'
    elif '_shared_' in name or name.endswith('_shared'):
        dtype = 'shared'
    else:
        dtype = None
    return scenario, dtype


def extract_robot_count(dataset_name):
    """Return the numeric suffix of a dataset name, e.g. 'detection_edge_25' -> 25."""
    try:
        return int(dataset_name.rsplit('_', 1)[-1])
    except ValueError:
        return 0


def build_colors(group):
    """Return {label: rgba} mapping.

    Each solver gets its own colormap; within a solver, shades are spread
    across the sorted robot counts present in this group.
    """
    solver_counts = defaultdict(set)
    for lbl, r in group:
        solver_counts[r.solver].add(extract_robot_count(r.dataset_name))
    solver_sorted = {s: sorted(c) for s, c in solver_counts.items()}

    colors = {}
    for lbl, r in group:
        cmap = SOLVER_CMAPS.get(r.solver, cm.Greys)
        sorted_counts = solver_sorted[r.solver]
        n = len(sorted_counts)
        idx = sorted_counts.index(extract_robot_count(r.dataset_name))
        t = 0.35 + (idx / max(n - 1, 1)) * 0.50  # shade range [0.35, 0.85]
        colors[lbl] = cmap(t)
    return colors


# ============================================================
#  Build groups: (scenario, dtype) -> [(label, result)]
# ============================================================
DataGroup = ResultsGroup(SOLVERS, RESULTS_FOLDERS, DATASET_FOLDERS)
dsp = DisplayMetrics(OUTPUT_FOLDER)

groups = defaultdict(list)

for solver, results in DataGroup.sorted_results.items():
    for result in results:
        scenario, dtype = parse_dataset_name(result.dataset_name)
        if scenario and dtype:
            print(f"Computing metrics: {result.dataset_name} [{solver}]")
            result.compute_metrics()
            n_robots = extract_robot_count(result.dataset_name)
            label = f"{n_robots} robots ({solver})"
            groups[(scenario, dtype)].append((label, result))

# ============================================================
#  5 plots per (scenario, dtype) group
# ============================================================
for scenario in SCENARIOS:
    for dtype in ['edge', 'shared']:
        group = groups.get((scenario, dtype), [])
        if not group:
            continue

        tag    = f"{scenario}_{dtype}"
        colors = build_colors(group)
        print(f"\nPlotting: {tag}  ({len(group)} results)")

        rpe_ptdist   = {lbl: r.metrics_re_ptdist for lbl, r in group}
        ape_ptdist   = {lbl: r.metrics_ae_ptdist for lbl, r in group}
        rpe_deg      = {lbl: r.metrics_re_rotdeg for lbl, r in group}
        ape_deg      = {lbl: r.metrics_ae_rotdeg for lbl, r in group}
        consensus_lk = {
            lbl: {it: v['landmarks'] for it, v in r.metrics_consensus.items()}
            for lbl, r in group
        }

        dsp.plot_error_over_iterations(
            rpe_ptdist,
            ylabel='RPE point distance (m)',
            title=f"RPE point distance — {tag}",
            fig_name=f"rpe_ptdist_{tag}",
            colors=colors,
        )
        dsp.plot_error_over_iterations(
            ape_ptdist,
            ylabel='APE point distance (m)',
            title=f"APE point distance — {tag}",
            fig_name=f"ape_ptdist_{tag}",
            colors=colors,
        )
        dsp.plot_error_over_iterations(
            rpe_deg,
            ylabel='RPE rotation (°)',
            title=f"RPE rotation — {tag}",
            fig_name=f"rpe_rotdeg_{tag}",
            colors=colors,
        )
        dsp.plot_error_over_iterations(
            ape_deg,
            ylabel='APE rotation (°)',
            title=f"APE rotation — {tag}",
            fig_name=f"ape_rotdeg_{tag}",
            colors=colors,
        )
        dsp.plot_error_over_iterations(
            consensus_lk,
            ylabel='Consensus landmarks (m)',
            title=f"Consensus landmarks — {tag}",
            fig_name=f"consensus_lk_{tag}",
            colors=colors,
        )
