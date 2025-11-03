#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extracts lattice vectors and orientation from FCC/HCP/DHCP .log files,
computes conventional lattice parameters (a, c), and generates three
clear plots (one per structure type).

Outputs:
    lattice_results.csv
    lattice_FCC.png
    lattice_HCP.png
    lattice_DHCP.png
"""

import re
import glob
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# ------------------ Helper: parse metadata ------------------
def parse_metadata(fname):
    """Extract structure, composition, and temperature from filename."""
    pat = r'(fcc|hcp|dhcp)_Co([0-9.]+)_Fe([0-9.]+)_Ni([0-9.]+)_([0-9]+)K'
    m = re.search(pat, Path(fname).stem)
    if not m:
        return None
    struct, Co, Fe, Ni, T = m.groups()
    return struct.upper(), float(Co), float(Fe), float(Ni), int(T)

# ------------------ Helper: extract lattice vectors ------------------
def parse_lattice_vectors(text):
    """Extract lattice vectors a1, a2, a3 and orientation axes."""
    a1 = a2 = a3 = np.nan
    orient = None

    # find lattice vector lines
    m1 = re.search(r"Lattice vector a1\s*=\s*([0-9.]+)", text)
    m2 = re.search(r"Lattice vector a2\s*=\s*([0-9.]+)", text)
    m3 = re.search(r"Lattice vector a3\s*=\s*([0-9.]+)", text)
    if m1: a1 = float(m1.group(1))
    if m2: a2 = float(m2.group(1))
    if m3: a3 = float(m3.group(1))

    # orientation info
    o = re.search(r"Orientation:\s*x=\[([^\]]+)\],\s*y=\[([^\]]+)\],\s*z=\[([^\]]+)\]", text)
    if o:
        orient = {
            "x": o.group(1).strip(),
            "y": o.group(2).strip(),
            "z": o.group(3).strip()
        }
    return a1, a2, a3, orient

# ------------------ Collect all .log files ------------------
records = []
for f in glob.glob("*.log"):
    meta = parse_metadata(f)
    if not meta:
        continue
    struct, Co, Fe, Ni, T = meta
    with open(f, "r", errors="ignore") as fh:
        txt = fh.read()
    a1, a2, a3, orient = parse_lattice_vectors(txt)
    # compute lattice parameters
    if struct == "FCC":
        a, c = a1, a1
    else:  # HCP and DHCP
        a = np.mean([a1, a2])
        c = a3
    # mark non-conventional orientation
    nonconv = "True" if orient and orient["x"] != "1 0 0" else "False"

    records.append({
        "Structure": struct,
        "Co": Co, "Fe": Fe, "Ni": Ni,
        "Temperature": T,
        "a1": a1, "a2": a2, "a3": a3,
        "a": a, "c": c,
        "Orientation_x": orient["x"] if orient else "",
        "Orientation_y": orient["y"] if orient else "",
        "Orientation_z": orient["z"] if orient else "",
        "NonConventional": nonconv
    })

df = pd.DataFrame(records)
df.to_csv("lattice_results.csv", index=False)
print(f"✅ Extracted {len(df)} structures → lattice_results.csv")

# ------------------ Plotting setup ------------------
plt.rcParams.update({
    "font.family": "serif",
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "legend.fontsize": 10,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.dpi": 300
})

# ------------------ Plot function ------------------
def plot_lattice(df_struct, name):
    """Plot lattice parameters vs temperature."""
    plt.figure(figsize=(7,5))
    for comp, g in df_struct.groupby(["Co","Fe","Ni"]):
        g = g.sort_values("Temperature")
        lbl = f"Co{comp[0]:.2f}_Fe{comp[1]:.2f}_Ni{comp[2]:.2f}"
        if g["a"].notna().any():
            plt.plot(g["Temperature"], g["a"], "o-", label=f"{lbl} – a")
        if g["c"].notna().any() and (name != "FCC"):
            plt.plot(g["Temperature"], g["c"], "s--", label=f"{lbl} – c")
    plt.xlabel("Temperature (K)")
    plt.ylabel("Lattice Parameter (Å)")
    plt.title(f"{name} Phase: Lattice Parameter Variation")
    plt.grid(True, alpha=0.4)
    plt.legend(ncol=2, frameon=True)
    plt.tight_layout()
    plt.savefig(f"lattice_{name}.png", dpi=600)
    plt.close()

# ------------------ Generate three concise plots ------------------
for struct in ["FCC", "HCP", "DHCP"]:
    dsub = df[df["Structure"] == struct]
    if not dsub.empty:
        plot_lattice(dsub, struct)

print("✅ Generated: lattice_FCC.png, lattice_HCP.png, lattice_DHCP.png")
