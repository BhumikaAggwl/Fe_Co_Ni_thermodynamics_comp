#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional benchmarking comparison plot for Co–Fe–Ni γISF data.

Produces two figures:
  1. benchmark_horizontal.png  – mirror bars: simulation vs literature
  2. benchmark_logscale.png    – both values on log scale for huge range clarity
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ------------------ CONFIG ------------------
T_fixed = 350
property_name = "γISF"

plt.rcParams.update({
    "font.family": "serif",
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "legend.fontsize": 11,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "figure.dpi": 300
})

# ------------------ LOAD DATA ------------------
df = pd.read_csv("sfe_results.csv")
df = df[df["Temperature"] == T_fixed].copy()
df["Alloy"] = df.apply(lambda r: f"Co{r.Co:.2f}Fe{r.Fe:.2f}Ni{r.Ni:.2f}", axis=1)

literature = pd.DataFrame([
    {"Alloy": "Ni", "γISF": 214, "Ref": "Schramm76"},
    {"Alloy": "Fe-40Ni", "γISF": 70, "Ref": "Schramm76"},
    {"Alloy": "Co-50Ni", "γISF": -10, "Ref": "Zhao17"},
    {"Alloy": "Fe-50Ni", "γISF": 100, "Ref": "Xu21"}
])

# ------------------ UNION OF LABELS ------------------
labels = sorted(set(df["Alloy"].tolist() + literature["Alloy"].tolist()))
y = np.arange(len(labels))

sim_values = [df.loc[df["Alloy"]==lab, property_name].values[0] if lab in df["Alloy"].values else np.nan for lab in labels]
lit_values = [literature.loc[literature["Alloy"]==lab, property_name].values[0] if lab in literature["Alloy"].values else np.nan for lab in labels]

# ------------------ 1️⃣ Mirror (horizontal) bars ------------------
fig, ax = plt.subplots(figsize=(8,5))
ax.barh(y - 0.2, sim_values, height=0.35, color="#1f77b4", label="Simulation")
ax.barh(y + 0.2, lit_values, height=0.35, color="#ff7f0e", label="Literature")

ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_xlabel(r"$\gamma_{\mathrm{ISF}}$ (mJ/m$^2$)")
ax.set_title(rf"Simulation vs Literature of $\gamma_{{ISF}}$ at {T_fixed} K")

# numeric labels
for i, (s,l) in enumerate(zip(sim_values, lit_values)):
    if not np.isnan(s):
        ax.text(s + 3, i - 0.2, f"{s:.1f}", va="center", fontsize=9)
    if not np.isnan(l):
        ax.text(l + 3, i + 0.2, f"{l:.0f}", va="center", fontsize=9)

ax.legend(frameon=True, loc="lower right")
ax.axvline(0, color="k", lw=0.5)
plt.tight_layout()
plt.savefig("benchmark_horizontal.png", dpi=600)
plt.close()

# ------------------ 2️⃣ Logarithmic axis plot ------------------
fig, ax = plt.subplots(figsize=(8,5))
width = 0.35
ax.bar(y - width/2, np.abs(sim_values), width, color="#1f77b4", alpha=0.9, label="Simulation")
ax.bar(y + width/2, np.abs(lit_values), width, color="#ff7f0e", alpha=0.8, label="Literature")

ax.set_yscale("log")
ax.set_xticks(y)
ax.set_xticklabels(labels, rotation=40, ha="right")
ax.set_ylabel(r"$|\gamma_{\mathrm{ISF}}|$ (mJ/m$^2$)")
ax.set_title(rf"Log-scale Comparison of Simulation vs Literature at {T_fixed} K")
ax.legend()
plt.tight_layout()
plt.savefig("benchmark_logscale.png", dpi=600)
plt.close()

print("✅ Saved: benchmark_horizontal.png and benchmark_logscale.png")
