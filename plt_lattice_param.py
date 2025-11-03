#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lattice Parameter Variation Plots for Co–Fe–Ni alloys.

Input: lattice_results.csv with columns:
    Co,Fe,Ni,Temperature,a,c   (lattice parameters in Å)

Outputs:
    1. lattice_vs_Temperature.png  – a and c vs Temperature for selected compositions
    2. lattice_vs_Composition.png  – a vs Ni-fraction at a fixed temperature
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------------- Style setup ----------------
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "serif",
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "legend.fontsize": 11,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "figure.dpi": 300,
    "lines.linewidth": 2.0
})

# ---------------- Load data ----------------
df = pd.read_csv("sfe_results.csv")

# Optional cleaning (remove NaN)
df = df.dropna(subset=["a", "c"])

# ---------------- 1️⃣ Lattice parameter vs Temperature ----------------
# Choose a few key compositions to highlight
selected_comps = [(0.25, 0.25, 0.50), (0.38, 0.12, 0.50)]

plt.figure(figsize=(7,5))
for (Co,Fe,Ni) in selected_comps:
    subset = df[(df["Co"]==Co) & (df["Fe"]==Fe) & (df["Ni"]==Ni)].copy()
    subset = subset.sort_values("Temperature")
    plt.plot(subset["Temperature"], subset["a"], "o-", label=fr"$a$, Co={Co:.2f}, Fe={Fe:.2f}, Ni={Ni:.2f}")
    plt.plot(subset["Temperature"], subset["c"], "s--", label=fr"$c$, Co={Co:.2f}, Fe={Fe:.2f}, Ni={Ni:.2f}")

plt.xlabel("Temperature (K)")
plt.ylabel("Lattice Parameter (Å)")
plt.title("Lattice Parameters vs Temperature for Selected Compositions")
plt.legend(ncol=2, frameon=True)
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig("lattice_vs_Temperature.png", dpi=600)
plt.close()

# ---------------- 2️⃣ Lattice parameter vs Composition (Ni-fraction) ----------------
T_fixed = 550
dfT = df[df["Temperature"] == T_fixed].copy()
dfT["Ni_fraction"] = dfT["Ni"]

plt.figure(figsize=(7,5))
plt.plot(dfT["Ni_fraction"], dfT["a"], "o-", color="#1f77b4", label="a-lattice")
plt.plot(dfT["Ni_fraction"], dfT["c"], "s--", color="#d62728", label="c-lattice")
plt.xlabel("Ni atomic fraction")
plt.ylabel("Lattice Parameter (Å)")
plt.title(f"Lattice Parameters vs Composition at {T_fixed} K")
plt.legend(frameon=True)
plt.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig("lattice_vs_Composition.png", dpi=600)
plt.close()

print("✅ Lattice parameter plots generated:")
print(" - lattice_vs_Temperature.png")
print(" - lattice_vs_Composition.png")
