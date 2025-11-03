#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates smooth, full-triangle ternary contour plots for Co–Fe–Ni alloys
using RBF interpolation over a uniform ternary grid.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import Rbf
from matplotlib import cm

plt.rcParams.update({
    "font.family": "serif",
    "axes.labelsize": 13,
    "axes.titlesize": 14,
    "legend.fontsize": 11,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "figure.dpi": 300
})

# ====================== Barycentric Projection ======================
def barycentric(Co, Fe, Ni):
    s = Co + Fe + Ni
    x = 0.5 * (2 * Fe + Ni) / s
    y = (np.sqrt(3) / 2.0) * Ni / s
    return x, y

# ====================== Draw Triangle ======================
def draw_triangle(ax):
    tri = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2], [0, 0]])
    ax.plot(tri[:, 0], tri[:, 1], color='black', lw=1)
    ax.text(-0.05, -0.05, "Fe", fontsize=12)
    ax.text(1.02, -0.05, "Co", fontsize=12)
    ax.text(0.48, np.sqrt(3)/2 + 0.05, "Ni", fontsize=12)
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.05, np.sqrt(3)/2 + 0.1)
    ax.set_aspect('equal')
    ax.axis('off')

# ====================== Generate Full Ternary Grid ======================
def generate_ternary_grid(n_points=60):
    """Generate a uniform grid of (Co,Fe,Ni) with Co+Fe+Ni=1"""
    grid = []
    for i in range(n_points + 1):
        for j in range(n_points + 1 - i):
            k = n_points - i - j
            Co = i / n_points
            Fe = j / n_points
            Ni = k / n_points
            grid.append((Co, Fe, Ni))
    return np.array(grid)

# ====================== RBF Interpolation ======================
def make_contour(ax, dfT, prop, title):
    """RBF-based full-triangle smooth contour."""
    dfT = dfT.copy()
    total = dfT["Co"] + dfT["Fe"] + dfT["Ni"]
    dfT["Co"] /= total
    dfT["Fe"] /= total
    dfT["Ni"] /= total

    # Input data
    x, y = barycentric(dfT["Co"], dfT["Fe"], dfT["Ni"])
    vals = dfT[prop].values

    # Create RBF interpolator
    rbf = Rbf(x, y, vals, function='multiquadric', smooth=0.0)

    # Generate uniform ternary grid
    grid = generate_ternary_grid(200)
    Xg, Yg = barycentric(grid[:, 0], grid[:, 1], grid[:, 2])
    Zg = rbf(Xg, Yg)

    # Mask outside triangle
    mask = (Yg <= np.sqrt(3) * np.minimum(Xg, 1 - Xg))
    Xg, Yg, Zg = Xg[mask], Yg[mask], Zg[mask]

    # Plot contour
    xi = np.linspace(0, 1, 300)
    yi = np.linspace(0, np.sqrt(3)/2, 300)
    Xi, Yi = np.meshgrid(xi, yi)
    Zi = rbf(Xi, Yi)
    Zi_masked = np.ma.array(Zi, mask=(Yi > np.sqrt(3) * np.minimum(Xi, 1 - Xi)))

    cf = ax.contourf(Xi, Yi, Zi_masked, levels=20, cmap=cm.plasma)
    cs = ax.contour(Xi, Yi, Zi_masked, levels=12, colors='k', linewidths=0.3, alpha=0.4)
    draw_triangle(ax)
    ax.scatter(x, y, c='white', edgecolors='k', s=25, label="Simulated")

    plt.colorbar(cf, ax=ax, shrink=0.8, label=f"{prop} (mJ/m²)")
    ax.set_title(title)
    ax.legend(loc='lower right', frameon=True)

# ====================== Literature Overlay ======================
def add_benchmark(ax):
    refs = [
        {"Co":0.0, "Fe":0.4, "Ni":0.6, "γISF":70, "Ref":"Schramm76"},
        {"Co":0.5, "Fe":0.0, "Ni":0.5, "γISF":-10, "Ref":"Zhao17"},
        {"Co":0.0, "Fe":0.5, "Ni":0.5, "γISF":100, "Ref":"Xu21"}
    ]
    bench = pd.DataFrame(refs)
    xb, yb = barycentric(bench["Co"], bench["Fe"], bench["Ni"])
    ax.scatter(xb, yb, s=60, marker='*', color='red', edgecolor='k', label='Literature')
    for (xpt, ypt, ref) in zip(xb, yb, bench["Ref"]):
        ax.text(xpt + 0.02, ypt, ref, fontsize=8)

# ====================== Main Routine ======================
def main():
    df = pd.read_csv("sfe_results.csv")
    temps = sorted(df["Temperature"].unique())

    for T in temps:
        dfT = df[df["Temperature"] == T].copy()
        for prop in ["γISF", "γESF", "γTwin"]:
            fig, ax = plt.subplots(figsize=(6,5))
            make_contour(ax, dfT, prop, f"{prop} Contour Plot at {T} K")
            add_benchmark(ax)
            plt.tight_layout()
            plt.savefig(f"ternary_{prop}_{T}K_contour_full.png", dpi=600)
            plt.close(fig)

    print("✅ Full-triangle ternary contour plots generated successfully!")

# ====================== Entry ======================
if __name__ == "__main__":
    main()
