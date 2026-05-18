import os
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import seaborn as sns


class DisplayMetrics:
    """Visualization of RTE, APE per robot and consensus error per robot pair."""

    def __init__(self, output_folder):
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def plot_rte_per_robot(self, rte_errors, title=None, fig_name='rte_per_robot'):
        """Box plot of Relative Translation Error per robot.

        Args:
            rte_errors: dict {'Robot <id>': [per-pose errors]} — Results.errors['point_distance_rpe']
        """
        self._boxplot(rte_errors, ylabel='RTE (m)', title=title, fig_name=fig_name)

    def plot_ape_per_robot(self, ape_errors, title=None, fig_name='ape_per_robot'):
        """Box plot of Absolute Position Error per robot.

        Args:
            ape_errors: dict {'Robot <id>': [per-pose errors]} — Results.errors['point_distance_ape']
        """
        self._boxplot(ape_errors, ylabel='APE (m)', title=title, fig_name=fig_name)

    def plot_rte_ape_per_robot(self, rte_errors, ape_errors, title=None,
                               fig_name='rte_ape_per_robot'):
        """Side-by-side box plots of RTE and APE for all robots.

        Args:
            rte_errors: dict from Results.errors['point_distance_rpe']
            ape_errors: dict from Results.errors['point_distance_ape']
        """
        robots = list(rte_errors.keys())
        colors = sns.color_palette("colorblind", len(robots))

        plt.style.use('bmh')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(max(12, len(robots) * 3), 5))

        for idx, robot in enumerate(robots):
            bp_kw = self._bp_kwargs(colors[idx])
            ax1.boxplot(rte_errors[robot], positions=[idx + 1], **bp_kw)
            ax2.boxplot(ape_errors[robot], positions=[idx + 1], **bp_kw)

        for ax, ylabel, sub_title in [
            (ax1, 'RTE (m)', 'Relative Translation Error per robot'),
            (ax2, 'APE (m)', 'Absolute Position Error per robot'),
        ]:
            ax.set_xticks(range(1, len(robots) + 1))
            ax.set_xticklabels(robots, rotation=45, fontsize=9)
            ax.set_ylabel(ylabel)
            ax.set_xlabel('Robot')
            ax.set_title(sub_title)

        if title:
            fig.suptitle(title, fontsize=12)

        self._save(fig, fig_name)

    def plot_consensus_per_pair(self, cs_errors, title=None, fig_name='consensus_per_pair'):
        """Two-panel figure: consensus evolution (left) and mean per pair (right).

        Args:
            cs_errors: dict {(rid1, rid2): [error_per_iteration]}
                       from Results2.get_consensuslk_error() or get_mean_consensus_all_lk()
        """
        pairs  = sorted(cs_errors.keys())
        n      = len(pairs)
        colors = sns.color_palette("colorblind", min(n, 10)) if n <= 10 \
                 else sns.color_palette("husl", n)
        labels = [f"{p[0]}-{p[1]}" for p in pairs]

        bar_width = max(14, n * 0.35 + 6)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(bar_width, 5))

        # Left: evolution over iterations
        for idx, pair in enumerate(pairs):
            ax1.plot(range(len(cs_errors[pair])), cs_errors[pair],
                     color=colors[idx], alpha=0.6, linewidth=1.0)
        if n <= 15:
            handles = [plt.Line2D([0], [0], color=colors[i], linewidth=2) for i in range(n)]
            ax1.legend(handles, labels, fontsize=7, loc='upper right', ncol=max(1, n // 8))
        ax1.set_xlabel('Iteration')
        ax1.set_ylabel('Consensus error (m)')
        ax1.set_title('Consensus error over iterations')

        # Right: mean ± std per pair
        means = [np.mean(cs_errors[p]) for p in pairs]
        stds  = [np.std(cs_errors[p])  for p in pairs]
        x = np.arange(n)

        ax2.bar(x, means, yerr=stds,
                color=colors, edgecolor='black', linewidth=0.8,
                capsize=3, error_kw={"linewidth": 1.0, "ecolor": "black"})
        ax2.set_xticks(x)
        label_fs = max(5, min(9, int(180 / n)))
        ax2.set_xticklabels(labels, rotation=90, fontsize=label_fs)
        ax2.set_ylabel('Mean consensus error (m)')
        ax2.set_title('Mean consensus error per pair (± std)')

        if title:
            fig.suptitle(title, fontsize=12)

        self._save(fig, fig_name)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _boxplot(self, errors, ylabel, title, fig_name):
        robots = list(errors.keys())
        colors = sns.color_palette("colorblind", len(robots))

        plt.style.use('bmh')
        fig, ax = plt.subplots(figsize=(max(6, len(robots) * 1.8), 5))

        for idx, robot in enumerate(robots):
            ax.boxplot(errors[robot], positions=[idx + 1], **self._bp_kwargs(colors[idx]))

        ax.set_xticks(range(1, len(robots) + 1))
        ax.set_xticklabels(robots, rotation=45, fontsize=9)
        ax.set_ylabel(ylabel)
        ax.set_xlabel('Robot')
        if title:
            ax.set_title(title)

        self._save(fig, fig_name)

    @staticmethod
    def _bp_kwargs(color):
        return dict(
            widths=0.5,
            patch_artist=True,
            showmeans=True,
            showfliers=False,
            medianprops={"color": "red", "linewidth": 1.5},
            meanprops={"marker": "D", "markerfacecolor": "white",
                       "markeredgecolor": "black", "markersize": 6},
            boxprops={"facecolor": color, "edgecolor": "black", "linewidth": 1.5},
            whiskerprops={"color": "black", "linewidth": 1.5},
            capprops={"color": "black", "linewidth": 1.5},
        )

    def _save(self, fig, fig_name):
        fig.tight_layout()
        path = os.path.join(self.output_folder, fig_name + '.png')
        fig.savefig(path, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"  Saved: {path}")
