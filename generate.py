#!/usr/bin/env python3
"""
generate_structures.py

Generates FCC, HCP, and DHCP supercells for all Co–Fe–Ni ternary compositions.

Output (in ./work/data/):
    fcc_Co0.25_Fe0.25_Ni0.50.data
    fcc_Co0.25_Fe0.25_Ni0.50.cif
    ... for all 3 phases and 20 compositions
"""

import os, random
import numpy as np
from ase.build import bulk
from ase.io import write

# ---- Settings ----
random.seed(42); np.random.seed(42)
N_SUPERCELL = 4  # 4×4×4 → ~256 atoms

# Compositions (fractional form for filenames)
COMPOSITIONS = [
    {"Co":1.00,"Fe":0.00,"Ni":0.00}, {"Co":0.00,"Fe":1.00,"Ni":0.00}, {"Co":0.00,"Fe":0.00,"Ni":1.00},
    {"Co":0.75,"Fe":0.25,"Ni":0.00}, {"Co":0.50,"Fe":0.50,"Ni":0.00}, {"Co":0.25,"Fe":0.75,"Ni":0.00},
    {"Co":0.00,"Fe":0.75,"Ni":0.25}, {"Co":0.00,"Fe":0.50,"Ni":0.50}, {"Co":0.00,"Fe":0.25,"Ni":0.75},
    {"Co":0.25,"Fe":0.00,"Ni":0.75}, {"Co":0.50,"Fe":0.00,"Ni":0.50}, {"Co":0.75,"Fe":0.00,"Ni":0.25},
    {"Co":0.125,"Fe":0.625,"Ni":0.25}, {"Co":0.375,"Fe":0.375,"Ni":0.25}, {"Co":0.625,"Fe":0.125,"Ni":0.25},
    {"Co":0.25,"Fe":0.50,"Ni":0.25}, {"Co":0.50,"Fe":0.25,"Ni":0.25},
    {"Co":0.125,"Fe":0.375,"Ni":0.50}, {"Co":0.375,"Fe":0.125,"Ni":0.50}, {"Co":0.25,"Fe":0.25,"Ni":0.50},
]

# Phases
PHASES = {
    "fcc":  {"crystal": "fcc", "a": 3.55, "c_over_a": None},
    "hcp":  {"crystal": "hcp", "a": 2.50, "c_over_a": 1.633},
    "dhcp": {"crystal": "hcp", "a": 2.50, "c_over_a": 3.266},
}

OUT_DIR = "work/data"
os.makedirs(OUT_DIR, exist_ok=True)

def rand_elements(n, fracs, labels):
    """Shuffle element types based on fractions."""
    n_each = [int(round(f * n)) for f in fracs]
    n_each[-1] = n - sum(n_each[:-1])
    lst = sum(([lab] * count for lab, count in zip(labels, n_each)), [])
    random.shuffle(lst)
    return lst

for phase, pinfo in PHASES.items():
    print(f"Generating {phase.upper()} structures...")
    for comp in COMPOSITIONS:
        xCo, xFe, xNi = comp["Co"], comp["Fe"], comp["Ni"]
        fracs = [xCo, xFe, xNi]
        labels = ["Co", "Fe", "Ni"]

        # Build unit cell
        if phase == "fcc":
            atoms = bulk("Ni", crystalstructure=pinfo["crystal"], a=pinfo["a"], cubic=True)
        else:
            atoms = bulk("Ni", crystalstructure=pinfo["crystal"], a=pinfo["a"],
                         c=pinfo["a"] * pinfo["c_over_a"], cubic=False)

        atoms = atoms.repeat((N_SUPERCELL, N_SUPERCELL, N_SUPERCELL))
        atoms.set_chemical_symbols(rand_elements(len(atoms), fracs, labels))

        # Format: fcc_Co0.25_Fe0.25_Ni0.50.data
        def f(x): return f"{x:.2f}"
        fname_base = f"{phase}_Co{f(xCo)}_Fe{f(xFe)}_Ni{f(xNi)}"

        path_data = os.path.join(OUT_DIR, fname_base + ".data")
        path_cif  = os.path.join(OUT_DIR, fname_base + ".cif")

        write(path_data, atoms, format="lammps-data", atom_style="atomic")
        write(path_cif, atoms, format="cif")

        print(f"✓ {fname_base} → {len(atoms)} atoms")

print("\n✅ All .data and .cif files written to work/data/")
