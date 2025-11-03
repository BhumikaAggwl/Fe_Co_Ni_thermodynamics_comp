#!/usr/bin/env python3
"""
generate_structures.py

Generates FCC, HCP, and DHCP supercells for all Co–Fe–Ni ternary compositions.

Phase folders:
    work/data/fcc/
    work/data/hcp/
    work/data/dhcp/

Output:
    data.<phase>.CoXXFeXXNiXX  (LAMMPS 'atomic' data files)
"""

import os, random
import numpy as np
from ase.build import bulk
from ase.io import write

# ---- Settings ----
random.seed(42); np.random.seed(42)
N_SUPERCELL = 4  # 4×4×4 → ~256 atoms

COMPOSITIONS = [
    {"Co":100.0,"Fe":0.0,"Ni":0.0}, {"Co":0.0,"Fe":100.0,"Ni":0.0}, {"Co":0.0,"Fe":0.0,"Ni":100.0},
    {"Co":75.0,"Fe":25.0,"Ni":0.0}, {"Co":50.0,"Fe":50.0,"Ni":0.0}, {"Co":25.0,"Fe":75.0,"Ni":0.0},
    {"Co":0.0,"Fe":75.0,"Ni":25.0}, {"Co":0.0,"Fe":50.0,"Ni":50.0}, {"Co":0.0,"Fe":25.0,"Ni":75.0},
    {"Co":25.0,"Fe":0.0,"Ni":75.0}, {"Co":50.0,"Fe":0.0,"Ni":50.0}, {"Co":75.0,"Fe":0.0,"Ni":25.0},
    {"Co":12.5,"Fe":62.5,"Ni":25.0}, {"Co":37.5,"Fe":37.5,"Ni":25.0}, {"Co":62.5,"Fe":12.5,"Ni":25.0},
    {"Co":25.0,"Fe":50.0,"Ni":25.0}, {"Co":50.0,"Fe":25.0,"Ni":25.0},
    {"Co":12.5,"Fe":37.5,"Ni":50.0}, {"Co":37.5,"Fe":12.5,"Ni":50.0}, {"Co":25.0,"Fe":25.0,"Ni":50.0},
]

PHASES = {
    "fcc": {"crystal": "fcc", "a": 3.55, "c_over_a": None},   # cubic
    "hcp": {"crystal": "hcp", "a": 2.50, "c_over_a": 1.633},  # hexagonal
    "dhcp": {"crystal": "hcp", "a": 2.50, "c_over_a": 3.266}, # long-cell HCP
}

OUT_ROOT = os.path.join("work", "data")
os.makedirs(OUT_ROOT, exist_ok=True)

def rand_elements(n, fracs, labels):
    n_each = [int(round(f * n)) for f in fracs]
    n_each[-1] = n - sum(n_each[:-1])  # adjust to fix rounding
    lst = sum(([lab] * count for lab, count in zip(labels, n_each)), [])
    random.shuffle(lst)
    return lst

for phase, pinfo in PHASES.items():
    print(f"Generating {phase.upper()} structures...")
    out_dir = os.path.join(OUT_ROOT, phase)
    os.makedirs(out_dir, exist_ok=True)

    for comp in COMPOSITIONS:
        xCo, xFe, xNi = comp['Co'], comp['Fe'], comp['Ni']
        fracs = [xCo/100, xFe/100, xNi/100]
        labels = ["Co", "Fe", "Ni"]

        atoms = bulk("Ni", crystalstructure=pinfo["crystal"], a=pinfo["a"],
                     c=pinfo["a"] * pinfo["c_over_a"] if pinfo["c_over_a"] else None,
                     cubic=True)
        atoms = atoms.repeat((N_SUPERCELL, N_SUPERCELL, N_SUPERCELL))
        atoms.set_chemical_symbols(rand_elements(len(atoms), fracs, labels))

        tag = f"Co{xCo:05.1f}Fe{xFe:05.1f}Ni{xNi:05.1f}".replace(".", "")
        out_path = os.path.join(out_dir, f"data.{tag}")
        write(out_path, atoms, format="lammps-data", atom_style="atomic")
        print(f"✓ {phase.upper():<4} {tag} → {len(atoms):3} atoms")

print("\n✅ All structures generated in 'work/data/<phase>/'")

