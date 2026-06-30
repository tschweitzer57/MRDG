#!/usr/bin/env python3
"""
Validation script for MRDG — Chapter 3 validation section figures and table data.
Produces:
  - ch3/fig/gt_paths.pdf         : 3D trajectories + landmarks  (fig:gt_paths)
  - ch3/fig/scalability_time_mem.pdf : time/memory vs N robots  (fig:ch3-scalability)
  - Console: inventory table data (tab:ch3-inventory)
  - Console: determinism check    (EX-NF1)
  - Console: noise fidelity table (tab:ch3-cov-check)
"""

import os, sys, json, time, hashlib, copy, tracemalloc, tempfile
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import gtsam, jrl
from string import ascii_letters

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'helpers'))
from generator import DatasetGenerator

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT       = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FIG_DIR    = os.path.join(ROOT, 'ch3', 'fig')
OUT_DIR    = os.path.join(ROOT, 'output', 'validation')
CFG_COMPLET = os.path.join(ROOT, 'configs', 'VLD_COMPLET', 'complet.json')
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(OUT_DIR, exist_ok=True)

# ── Matplotlib style (publication, no GUI) ─────────────────────────────────
plt.rcParams.update({
    'font.family'      : 'serif',
    'font.size'        : 10,
    'axes.labelsize'   : 10,
    'axes.titlesize'   : 10,
    'legend.fontsize'  : 9,
    'lines.linewidth'  : 1.4,
    'figure.dpi'       : 150,
})
ROBOT_COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# ═══════════════════════════════════════════════════════════════════════════
# 1. GENERATE COMPLET DATASET
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("1. GÉNÉRATION DU JEU DE DONNÉES COMPLET")
print("═"*60)

gen = DatasetGenerator(CFG_COMPLET, output_dir=OUT_DIR)
t0 = time.perf_counter()
gen.generate_dataset()
t_gen = time.perf_counter() - t0
jrl_path = os.path.join(OUT_DIR, 'complet.jrl')
print(f"   Temps de génération : {t_gen:.3f} s")

# ═══════════════════════════════════════════════════════════════════════════
# 2. FIGURE gt_paths — 3D trajectories + landmarks
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("2. FIGURE gt_paths")
print("═"*60)

fig = plt.figure(figsize=(6, 5))
ax  = fig.add_subplot(111, projection='3d')

for idx, rid in enumerate(gen.robots):
    keys = [gtsam.symbol(rid, k) for k in range(gen.config.trajectory['poses'])
            if gen.gt_poses.exists(gtsam.symbol(rid, k))]
    pts = np.array([gen.gt_poses.atPose3(k).translation() for k in keys])
    ax.plot(pts[:, 0], pts[:, 1], pts[:, 2],
            color=ROBOT_COLORS[idx], linewidth=1.2, label=f'Robot {rid}')
    ax.scatter(pts[0, 0], pts[0, 1], pts[0, 2],
               color=ROBOT_COLORS[idx], marker='o', s=30, zorder=5)

if gen.config.landmarks is not None:
    lk_keys = list(gen.landmarks.keys())
    lk_pts  = np.array([gen.landmarks.atPoint3(k) for k in lk_keys])
    ax.scatter(lk_pts[:, 0], lk_pts[:, 1], lk_pts[:, 2],
               color='black', marker='x', s=50, linewidths=1.5, label='Amers', zorder=6)

ax.set_xlabel('x (m)'); ax.set_ylabel('y (m)'); ax.set_zlabel('z (m)')
ax.legend(loc='upper left', fontsize=8)
ax.set_box_aspect([1, 1, 0.5])
plt.tight_layout()
out_gt = os.path.join(FIG_DIR, 'gt_paths.pdf')
fig.savefig(out_gt, bbox_inches='tight')
plt.close(fig)
print(f"   Sauvegardée : {out_gt}")

# ═══════════════════════════════════════════════════════════════════════════
# 3. INVENTORY TABLE — count each factor type in the Complet dataset
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("3. INVENTAIRE DES FACTEURS (tab:ch3-inventory)")
print("═"*60)

parser    = jrl.Parser()
dataset   = parser.parseDataset(jrl_path, False)
robots    = dataset.robots()

counts = {
    'odom'             : 0,
    'lc_intra'         : 0,
    'lc_inter_indirect': 0,
    'lc_inter_direct_pose' : 0,
    'lc_inter_direct_range': 0,
    'landmarks'        : 0,
    'prior'            : 0,
}

for rid in robots:
    for entry in dataset.measurements(rid):
        for i in range(entry.measurements.nrFactors()):
            f    = entry.measurements.at(i)
            keys = f.keys()
            if len(keys) == 1:
                counts['prior'] += 1
                continue
            k1, k2   = keys[0], keys[1]
            c1 = chr(gtsam.Symbol(k1).chr())
            c2 = chr(gtsam.Symbol(k2).chr())
            i1 = gtsam.Symbol(k1).index()
            i2 = gtsam.Symbol(k2).index()

            is_lk     = c1 == '#' or c2 == '#'
            is_same   = c1 == c2
            is_consec = abs(i1 - i2) == 1
            is_direct = i1 == i2

            if is_lk:
                counts['landmarks'] += 1
            elif is_same and is_consec:
                counts['odom'] += 1
            elif is_same and not is_consec:
                counts['lc_intra'] += 1
            elif not is_same and is_direct:
                if isinstance(f, gtsam.RangeFactorPose3):
                    counts['lc_inter_direct_range'] += 1
                else:
                    counts['lc_inter_direct_pose'] += 1
            elif not is_same and not is_direct:
                counts['lc_inter_indirect'] += 1

# Expected values from config
N, K = gen.config.trajectory['robots'], gen.config.trajectory['poses']
n_lk = gen.config.landmarks['number'] if gen.config.landmarks else 0
expected = {
    'odom'                 : N * (K - 1),
    'lc_intra'             : N * gen.config.lc_intra['number'],
    'lc_inter_indirect'    : N * gen.config.lc_inter_indirect['number'],
    'lc_inter_direct_pose' : N * gen.config.lc_inter_direct['pose']['number'],
    'lc_inter_direct_range': N * gen.config.lc_inter_direct['range']['number'],
    'landmarks'            : gen.config.landmarks['detection_num'] * N,
    'prior'                : N,
}

labels = {
    'odom'                 : 'Odométrie visuelle-inertielle',
    'lc_intra'             : 'Fermeture de boucle intra-robot',
    'lc_inter_indirect'    : 'Fermeture de boucle inter-robot',
    'lc_inter_direct_pose' : 'Détection visuelle inter-robot',
    'lc_inter_direct_range': 'Mesure de distance UWB',
    'landmarks'            : 'Observation de repères',
}
print(f"\n  {'Type de facteur':<40} {'Attendu':>8} {'Généré':>8} {'Conforme':>9}")
print(  "  " + "-"*68)
all_ok = True
for key, label in labels.items():
    exp = expected[key]
    got = counts[key]
    ok  = "✓" if got > 0 else "✗"
    if got == 0:
        all_ok = False
    print(f"  {label:<40} {exp:>8} {got:>8} {ok:>9}")
print(f"\n  Tous les types présents : {'OUI ✓' if all_ok else 'NON ✗'}")

# ═══════════════════════════════════════════════════════════════════════════
# 4. DETERMINISM CHECK — SHA-256 (EX-NF1)
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("4. DÉTERMINISME SHA-256 (EX-NF1)")
print("═"*60)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()

hashes = []
for run in range(5):
    tmp_dir = tempfile.mkdtemp()
    g = DatasetGenerator(CFG_COMPLET, output_dir=tmp_dir)
    g.generate_dataset()
    jrl_file = os.path.join(tmp_dir, 'complet.jrl')
    hashes.append(sha256_file(jrl_file))

all_identical = len(set(hashes)) == 1
print(f"\n  Hash (5 exécutions, graine fixée) :")
for i, h in enumerate(hashes, 1):
    print(f"    Run {i}: {h[:32]}...")
print(f"\n  Toutes identiques : {'OUI ✓' if all_identical else 'NON ✗'}")

# Vérification que changer la graine produit un hash différent
with open(CFG_COMPLET) as f:
    cfg_mod = json.load(f)
cfg_mod['trajectory']['seed'] = 999
tmp_dir2 = tempfile.mkdtemp()
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tf:
    json.dump(cfg_mod, tf)
    cfg_mod_path = tf.name
cfg_mod['output_dir'] = tmp_dir2
with open(cfg_mod_path, 'w') as f:
    json.dump(cfg_mod, f)
g2 = DatasetGenerator(cfg_mod_path, output_dir=tmp_dir2)
g2.generate_dataset()
jrl_mod = os.path.join(tmp_dir2, os.path.basename(cfg_mod_path).replace('.json', '.jrl'))
# find the generated file
for fn in os.listdir(tmp_dir2):
    if fn.endswith('.jrl'):
        jrl_mod = os.path.join(tmp_dir2, fn)
        break
hash_mod = sha256_file(jrl_mod)
different = hash_mod != hashes[0]
print(f"  Hash différent si graine changée : {'OUI ✓' if different else 'NON ✗'}")

# ═══════════════════════════════════════════════════════════════════════════
# 5. NOISE FIDELITY — empirical sigma vs configured (tab:ch3-cov-check)
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("5. FIDÉLITÉ DU MODÈLE DE BRUIT (tab:ch3-cov-check)")
print("═"*60)

sigma_cfg = np.array(gen.config.sigmas['odom'])
components = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz']

# Extract noise vectors from odom topology: noise = Log(odom^{-1} * measured)
# In gen: measured = odom.compose(noise), so noise_vec = Log(odom^{-1} * measured) = Log(noise)
noise_vecs = []
for rid in gen.robots:
    for odom, noise in gen.odom[rid]:
        xi = gtsam.Pose3.Logmap(noise)
        noise_vecs.append(xi)

noise_vecs = np.array(noise_vecs)    # shape (M, 6)
sigma_emp  = np.std(noise_vecs, axis=0)
mean_emp   = np.mean(noise_vecs, axis=0)
rel_err    = np.abs(sigma_emp - sigma_cfg) / sigma_cfg * 100

print(f"\n  {'Composante':<12} {'σ configuré':>12} {'σ empirique':>12} {'Erreur rel. (%)':>16}")
print(  "  " + "-"*54)
for i, comp in enumerate(components):
    print(f"  σ_{comp:<9} {sigma_cfg[i]:>12.4f} {sigma_emp[i]:>12.4f} {rel_err[i]:>15.1f}")
print(f"\n  Erreur relative maximale : {rel_err.max():.1f} %")
print(f"  Nombre de mesures : {len(noise_vecs)}")

# ═══════════════════════════════════════════════════════════════════════════
# 6. SCALABILITY BENCHMARK — time/memory vs N (fig:ch3-scalability)
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("6. BENCHMARK SCALABILITÉ (fig:ch3-scalability)")
print("═"*60)

N_vals = [2, 5, 10, 20, 50, 90]
K_FIXED = 200
times_gen  = []
mems_peak  = []

with open(os.path.join(ROOT, 'configs', 'VLD_SCALABLE', 'scalable_base.json')) as f:
    base_cfg = json.load(f)

print(f"\n  {'N robots':>8} {'Temps (s)':>10} {'Mémoire (Mo)':>13}")
print(  "  " + "-"*34)

for N in N_vals:
    cfg = copy.deepcopy(base_cfg)
    cfg['trajectory']['robots'] = N
    cfg['trajectory']['poses']  = K_FIXED
    cfg['name']                 = f'vld_scalable_{N}'
    tmp_dir = tempfile.mkdtemp()

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tf:
        json.dump(cfg, tf)
        cfg_path = tf.name

    tracemalloc.start()
    t0 = time.perf_counter()
    g = DatasetGenerator(cfg_path, output_dir=tmp_dir)
    g.generate_dataset()
    t_elapsed = time.perf_counter() - t0
    _, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    mem_mb = mem_peak / 1e6
    times_gen.append(t_elapsed)
    mems_peak.append(mem_mb)
    print(f"  {N:>8}   {t_elapsed:>9.3f}   {mem_mb:>11.1f}")

# ─── Plot scalability figure ───────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(8, 3.5))

N_arr = np.array(N_vals, dtype=float)
T_arr = np.array(times_gen)
M_arr = np.array(mems_peak)

# Fit log-log exponents
exp_t = np.polyfit(np.log(N_arr), np.log(T_arr), 1)[0]
exp_m = np.polyfit(np.log(N_arr), np.log(M_arr), 1)[0]

# Reference lines at the scale of the data
ref_x = np.array([N_arr[0], N_arr[-1]])
ref_On  = T_arr[0] * (ref_x / N_arr[0])**1
ref_On2 = T_arr[0] * (ref_x / N_arr[0])**2

# Time subplot
ax = axes[0]
ax.loglog(N_arr, T_arr, 'o-', color='#1f77b4', label=f'MRDG ($\\alpha \\approx {exp_t:.2f}$)')
ax.loglog(ref_x, ref_On,  '--', color='gray', linewidth=1, label='$\\mathcal{O}(N)$')
ax.loglog(ref_x, ref_On2, ':',  color='gray', linewidth=1, label='$\\mathcal{O}(N^2)$')
ax.set_xlabel('Nombre de robots $N$')
ax.set_ylabel('Temps de génération (s)')
ax.legend()
ax.grid(True, which='both', linestyle=':', linewidth=0.5, alpha=0.7)

# Memory subplot
ref_Mm  = M_arr[0] * (ref_x / N_arr[0])**1
ref_Mm2 = M_arr[0] * (ref_x / N_arr[0])**2
ax = axes[1]
ax.loglog(N_arr, M_arr, 's-', color='#ff7f0e', label=f'MRDG ($\\alpha \\approx {exp_m:.2f}$)')
ax.loglog(ref_x, ref_Mm,  '--', color='gray', linewidth=1, label='$\\mathcal{O}(N)$')
ax.loglog(ref_x, ref_Mm2, ':',  color='gray', linewidth=1, label='$\\mathcal{O}(N^2)$')
ax.set_xlabel('Nombre de robots $N$')
ax.set_ylabel('Mémoire pic (Mo)')
ax.legend()
ax.grid(True, which='both', linestyle=':', linewidth=0.5, alpha=0.7)

plt.tight_layout()
out_scale = os.path.join(FIG_DIR, 'scalability_time_mem.pdf')
fig.savefig(out_scale, bbox_inches='tight')
plt.close(fig)
print(f"\n   Exposant temps (log-log) : {exp_t:.3f}")
print(f"   Exposant mémoire (log-log): {exp_m:.3f}")
print(f"   Sauvegardée : {out_scale}")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("RÉSUMÉ — VALEURS POUR LE LATEX")
print("═"*60)
print(f"\n% Protocole")
print(f"%   Temps génération dataset Complet  : {t_gen:.2f} s")
print(f"\n% EX-F1 : chargement GTSAM")
total_factors = sum(counts.values())
print(f"%   Nombre total de facteurs          : {total_factors}")
print(f"\n% EX-F2 : inventaire")
for key, label in labels.items():
    print(f"%   {label:<40}: {counts[key]}")
print(f"\n% EX-NF1 : déterminisme")
print(f"%   Toutes empreintes identiques       : {'OUI' if all_identical else 'NON'}")
print(f"\n% Fidélité bruit")
for i, comp in enumerate(components):
    print(f"%   sigma_{comp}: cfg={sigma_cfg[i]:.3f}  emp={sigma_emp[i]:.4f}  err={rel_err[i]:.1f}%")
print(f"\n% Scalabilité")
for i, N in enumerate(N_vals):
    print(f"%   N={N:3d}: t={times_gen[i]:.3f}s  mem={mems_peak[i]:.1f}Mo")
print(f"%   Exposant temps   alpha_t = {exp_t:.2f}")
print(f"%   Exposant mémoire alpha_m = {exp_m:.2f}")
print("\n✓ Script terminé.")
