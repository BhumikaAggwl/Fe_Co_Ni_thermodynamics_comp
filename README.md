# Fe_Co_Ni_thermodynamics_comp

# 📘 Stacking Fault Energy Analysis in Co–Fe–Ni Ternary Alloys

This repository contains LAMMPS simulation inputs, Python analysis scripts, and visualization outputs for evaluating stacking fault energies (γISF, γESF, γTwin) in Co–Fe–Ni alloys at different temperatures.

---

## 📁 Directory Structure

├── input/ # LAMMPS input scripts (in.fcc.lmp, in.hcp.lmp, in.dhcp.lmp)
├── work/
│ ├── data/ # Generated .data and .cif structures (21 compositions)
│ ├── logs/ # Output logs from LAMMPS runs
│ └── results/ # Final LAMMPS output data for each structure
├── potentials/
│ └── FeNiCrCoAl-heaweight.setfl # EAM potential file used in all simulations
├── scripts/
│ ├── generate.py # Generates LAMMPS structure input files
│ ├── analyse_sfe.py # Parses logs and extracts stacking fault energies
│ ├── plt_ter_2.py # Generates ternary contour plots
│ ├── run_fcc.sh # Shell script to run FCC jobs
│ ├── run_hcp.sh # Shell script to run HCP jobs
│ ├── run_dhcp.sh # Shell script to run DHCP jobs
│ └── run_all.sh # Executes all three in sequence
├── lattice/ # Lattice parameter plots
├── pe/ # Cohesive energy comparison plots
├── benchmark/ # Literature benchmarking figures
├── plots_by_composition/ # ISF vs temperature and composition plots
├── ternary/ # Contour plots for γISF, γESF, γTwin
├── main.tex # LaTeX report source
└── README.md # This file



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
   Charpagne et al., Acta Materialia, 2023 — DOI

   Zhao et al., Nature Communications, 2017 — DOI

  Xu et al., Scripta Materialia, 2021 — DOI
