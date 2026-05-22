"""
Renomme les fichiers d'itérations pour le solver geodesic-pyxis.

Problème : les dossiers iterations/ de pyxis ont les fichiers
  000000000000, 000000000002, 000000000003, ..., 000000000502
(le fichier 1 est absent, tous les suivants sont décalés de +1).

Correction : renuméroter séquentiellement à partir de 0 en comblant les trous.
  0 → 0  (inchangé)
  2 → 1
  3 → 2
  ...
  502 → 501

Usage :
  python fix_pyxis_iterations.py              # dry-run (affiche sans renommer)
  python fix_pyxis_iterations.py --apply      # applique les renommages
"""

import os
import sys
import re
from pathlib import Path

INPUT_ROOT   = '../input'
PYXIS_MARKER = 'geodesic-pyxis'
FILE_PATTERN = re.compile(r'^(\d{12})\.jrr\.cbor$')
DRY_RUN      = '--apply' not in sys.argv


def iter_pyxis_iteration_dirs(root):
    for dirpath, _, _ in os.walk(root):
        if os.path.basename(dirpath) == 'iterations' and PYXIS_MARKER in dirpath:
            yield Path(dirpath)


def get_numbered_files(iterations_dir):
    """Retourne la liste triée des (numero_int, Path) pour les fichiers .jrr.cbor."""
    files = []
    for f in iterations_dir.iterdir():
        m = FILE_PATTERN.match(f.name)
        if m:
            files.append((int(m.group(1)), f))
    files.sort()
    return files


def compute_renames(files):
    """Calcule les renommages nécessaires pour combler les trous."""
    renames = []
    for expected_idx, (current_num, path) in enumerate(files):
        if current_num != expected_idx:
            new_name = f"{expected_idx:012d}.jrr.cbor"
            renames.append((path, path.parent / new_name))
    return renames


def apply_renames(renames, dry_run):
    for src, dst in renames:
        if dry_run:
            print(f"  [dry-run] {src.name} → {dst.name}")
        else:
            src.rename(dst)
            print(f"  {src.name} → {dst.name}")


def main():
    root = Path(__file__).parent / INPUT_ROOT
    if not root.exists():
        print(f"Dossier introuvable : {root.resolve()}")
        sys.exit(1)

    mode = "DRY-RUN" if DRY_RUN else "APPLY"
    print(f"=== fix_pyxis_iterations — mode {mode} ===\n")

    total_dirs    = 0
    total_renames = 0

    for iterations_dir in sorted(iter_pyxis_iteration_dirs(root)):
        files = get_numbered_files(iterations_dir)
        if not files:
            continue

        renames = compute_renames(files)
        if not renames:
            continue

        total_dirs    += 1
        total_renames += len(renames)
        print(f"{iterations_dir.relative_to(root.parent)}  ({len(renames)} renommages)")
        apply_renames(renames, DRY_RUN)
        print()

    print(f"--- Total : {total_renames} fichiers dans {total_dirs} dossiers ---")
    if DRY_RUN:
        print("Relancer avec --apply pour appliquer les changements.")


if __name__ == '__main__':
    main()
