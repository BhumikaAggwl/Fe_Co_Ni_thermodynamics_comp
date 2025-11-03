#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a clean, publication-ready bar chart
of average cohesive energy for FCC, HCP, and DHCP phases.
"""

import pandas as pd
import matplotlib.pyplot as plt

# -------------------- Load your extracted data --------------------
df = pd.read_csv("potential_energy_all.csv")

# Clean structure names
df["Structure"] = df["Structure"].str.upper().str.strip()

# Compute mean and std cohesive energy per structure
means = df.groupby("Structure", as_index=False)["E_per_atom"].mean()
stds = df.groupby("Structure", as_index=False)["E_per_atom"].std()

# -------------------- Plot setup --------------------
plt.rcParams.update({
    "font.family": "serif",
    "axes.labelsize": 14,
    "axes.titlesize": 15,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "figure.dpi": 300
})

plt.figure(figsize=(6.5, 4.5))

colors = ["#1f77b4", "#ff7f0e", "#2ca02c"]

bars = plt.bar(
    means["Structure"],
    means["E_per_atom"],
    yerr=stds["E_per_atom"],
    capsize=5,
    color=colors,
    alpha=0.9,
    edgecolor="black"
)

# -------------------- Scaling for better visibility --------------------
ymin = means["E_per_atom"].min() - 0.05
ymax = means["E_per_atom"].max() + 0.05
plt.ylim(ymin, ymax)

plt.ylabel("Mean Potential Energy per Atom (eV)")
plt.title("Average Cohesive Energy by Structure")
plt.grid(axis="y", linestyle="--", alpha=0.4)

# -------------------- Annotate bar values --------------------
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.002,
        f"{height:.4f}",
        ha="center",
        va="bottom",
        fontsize=11
    )

plt.tight_layout()
plt.savefig("pe_by_structure_better_scaled.png", dpi=600)
plt.close()

print("✅ Saved: pe_by_structure_better_scaled.png")
