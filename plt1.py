import pandas as pd
import matplotlib.pyplot as plt
import os

# ---- CONFIGURATION ----
DATA_PATH = "sfe_results.csv"  # Replace with your actual CSV file
OUT_DIR = "plots_sfe"          # Output folder for figures
Y_LIMITS = (0, 0.005)           # Fixed Y-axis range for all plots
os.makedirs(OUT_DIR, exist_ok=True)

# ---- Load Data ----
df = pd.read_csv(DATA_PATH)

# ---- Get all unique compositions ----
df['composition'] = df.apply(lambda row: f"Co{row.Co:.2f}_Fe{row.Fe:.2f}_Ni{row.Ni:.2f}", axis=1)
unique_compositions = df['composition'].unique()

# ---- Plotting Loop ----
for comp in unique_compositions:
    subdf = df[df['composition'] == comp].sort_values(by='Temperature')

    plt.figure(figsize=(10,6))
    plt.plot(subdf['Temperature'], subdf['γISF'], marker='o', label='γISF')
    plt.plot(subdf['Temperature'], subdf['γESF'], marker='s', label='γESF')
    plt.plot(subdf['Temperature'], subdf['γTwin'], marker='^', label='γTwin')

    plt.xlabel("Temperature (K)")
    plt.ylabel("SFE (mJ/m²)")
    plt.title(f"SFE vs Temperature for {comp}")
    plt.legend()
    plt.grid(True)
    plt.ylim(Y_LIMITS)
    plt.tight_layout()

    # Save plot
    fname = os.path.join(OUT_DIR, f"SFE_vs_Temp_{comp}.png")
    plt.savefig(fname, dpi=300)
    plt.close()

print(f"✅ Plots saved in '{OUT_DIR}' for all {len(unique_compositions)} compositions.")
