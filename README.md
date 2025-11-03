# Fe_Co_Ni_thermodynamics_comp

# 📘 Stacking Fault Energy Analysis in Co–Fe–Ni Ternary Alloys

This repository contains LAMMPS simulation inputs, Python analysis scripts, and visualization outputs for evaluating stacking fault energies (γISF, γESF, γTwin) in Co–Fe–Ni alloys at different temperatures.

---

## 📁 Directory Structure

CoFeNi_SFE_Project/
├── input/                       # LAMMPS input scripts
│   ├── in.fcc.lmp
│   ├── in.hcp.lmp
│   └── in.dhcp.lmp
│
├── work/                        # Working directory for simulation data
│   ├── data/                    # Generated .data and .cif files (21 compositions)
│   ├── logs/                    # LAMMPS log files
│   └── results/                 # Final simulation outputs per structure
│
├── potentials/                  # Potential files
│   └── FeNiCrCoAl-heaweight.setfl
│
├── scripts/                     # Simulation + plotting scripts
│   ├── generate.py              # Structure generation
│   ├── analyse_sfe.py           # SFE analysis from logs
│   ├── plt_ter_2.py             # Ternary contour plots
│   ├── plt_pe.py                # Cohesive energy plots
│   ├── plt_benchmark.py         # Benchmark plot vs literature
│   ├── run_fcc.sh               # Shell script: FCC jobs
│   ├── run_hcp.sh               # Shell script: HCP jobs
│   ├── run_dhcp.sh              # Shell script: DHCP jobs
│   └── run_all.sh               # Master script to run all simulations
│
├── lattice/                     # Lattice parameter plots
│   ├── lattice_FCC.png
│   ├── lattice_HCP.png
│   └── lattice_DHCP.png
│
├── pe/                          # Cohesive energy plots
│   └── pe_by_structure_better_scaled.png
│
├── benchmark/                   # γISF benchmarking vs literature
│   └── benchmark_logscale.png
│
├── plots_by_composition/        # ISF vs temperature and composition
│   ├── isf_vs_composition_100K.png
│   ├── isf_vs_composition_350K.png
│   └── isf_vs_composition_550K.png
│
├── ternary/                     # Contour plots for γISF, γESF, γTwin
│   ├── ternary_γISF_100K_contour_full.png
│   ├── ternary_γISF_350K_contour_full.png
│   ├── ternary_γISF_550K_contour_full.png
│   ├── ternary_γESF_100K_contour_full.png
│   ├── ternary_γESF_350K_contour_full.png
│   ├── ternary_γESF_550K_contour_full.png
│   ├── ternary_γTwin_100K_contour_full.png
│   ├── ternary_γTwin_350K_contour_full.png
│   └── ternary_γTwin_550K_contour_full.png
│
├── main.tex                     # LaTeX report source
└── README.md                    # This file (project documentation)


---

## 🧪 Objective

The project aims to:
- Simulate stacking fault energies (SFE) in FCC, HCP, and DHCP phases.
- Evaluate thermodynamic stability via cohesive energy.
- Visualize the effects of temperature (100K, 350K, 550K) and composition.
- Benchmark results against literature.
- Provide insights into mechanical behavior and phase preferences in HEAs.

---

## ⚙️ How to Run

1. **Generate Structure Files**
   ```bash
   cd scripts/
   python generate.py
2. **Run LAMMPS Simulations
   ```bash
   bash run_all.sh
   ```
3  **🧪 Analyze SFE Values
    ```bash
    python analyse_sfe.py
    ```
4. **📊 Plotting
   ```bash
    python plt_ter_2.py         # Generates ternary plots (γISF, γESF, γTwin)
    python plt_pe.py            # Plots cohesive energy across phases
    python plt_benchmark.py     # Benchmarks γISF values against literature
   ```
5. ** 📈 Visualization Outputs
   ```bash
    Ternary Contour Plots: γISF, γESF, γTwin across temperature and composition.

    Lattice Parameters: FCC, HCP, DHCP lattice parameter evolution from 100K to 550K.

    Cohesive Energies: Phase stability comparison (FCC < HCP < DHCP).

    Benchmarking: Simulated γISF values compared to literature (Zhao, Charpagne, Xu).

    ISF vs. Composition/Temp: Effects of chemical makeup and temperature on stacking fault energies.
   ```
6. ** 📎 Included Files
   ```bash
    📄 main.tex — Full LaTeX report with all plots and explanations.

    📁 *.png — All images and result plots included in the report.

    📜 Python scripts:

    generate.py — Structure generation

    analyse_sfe.py — SFE analysis from LAMMPS logs

    plt_ter_2.py — Ternary contour plots

    plt_pe.py — Cohesive energy bar plots

    plt_benchmark.py — Literature comparison
   ```
7. ** 📚 References
   ```bash
   Charpagne et al., Acta Materialia, 2023 — DOI

   Zhao et al., Nature Communications, 2017 — DOI

   Xu et al., Scripta Materialia, 2021 — DOI
   ```
