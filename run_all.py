#!/usr/bin/env python3
"""
Robust batch runner for Co–Fe–Ni SFE simulations (EAM/alloy version).
Loops over all .data files and executes temperature sweeps via LAMMPS.
"""

import os, re, time, shutil, subprocess
from datetime import datetime

# --- Paths ---
ROOT      = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))
LMP       = "/opt/homebrew/bin/lmp_serial"
DATA_DIR  = os.path.join(ROOT, "work", "data")
LOG_DIR   = os.path.join(ROOT, "work", "logs")
RES_DIR   = os.path.join(ROOT, "work", "results")
IN_FCC    = os.path.join(ROOT, "inputs", "in.fcc.lmp")
IN_HCP    = os.path.join(ROOT, "inputs", "in.hcp.lmp")
IN_DHCP   = os.path.join(ROOT, "inputs", "in.dhcp.lmp")

STRUCT_MAP = {"fcc": IN_FCC, "hcp": IN_HCP, "dhcp": IN_DHCP}
TEMPS      = [100, 550, 350]

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def check_data_file(df):
    try:
        head = open(df).read(1000)
    except Exception as e:
        return False, f"cannot read: {e}"
    ntypes = re.search(r"^(\s*\d+)\s+atom\s+types", head, flags=re.I|re.M)
    if not ntypes or int(ntypes.group(1)) != 3:
        return False, "Expected 3 atom types"
    if "Masses" not in open(df).read():
        return False, "No 'Masses' section"
    return True, "ok"

def run_one(struct, df, T, in_file, attempt=1):
    base = os.path.splitext(os.path.basename(df))[0]
    tag  = f"{base}_{T}K"
    log  = os.path.join(LOG_DIR, f"{tag}.log")
    outd = os.path.join(RES_DIR, base)
    os.makedirs(outd, exist_ok=True)

    cmd = [
        LMP, "-var", "DATA", df, "-var", "TEMP", str(T),
        "-var", "STRUCT", struct, "-var", "OUTDIR", outd,
        "-in", in_file
    ]

    print(f"[{ts()}] ▶ run {tag} (attempt {attempt})")
    t0 = time.time()
    with open(log, "w") as lf:
        proc = subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT)
    mins = (time.time() - t0)/60.0

    if proc.returncode == 0:
        print(f"[{ts()}] ✅ done {tag} in {mins:.2f} min\n")
        return True, mins
    else:
        print(f"[{ts()}] ❌ fail {tag} (see {log})\n")
        return False, mins

def main():
    datafiles = sorted([os.path.join(DATA_DIR, f) for f in os.listdir(DATA_DIR) if f.endswith(".data")])
    if not datafiles:
        raise RuntimeError("No .data files in work/data")

    total_jobs, total_min = 0, 0.0
    tstart = time.time()
    print("\n======= Co–Fe–Ni SFE Automation (EAM) =======\n")

    for df in datafiles:
        struct = os.path.basename(df).split("_")[0].lower()
        if struct not in STRUCT_MAP:
            print(f"⚠️  skip {os.path.basename(df)} (unknown struct)\n")
            continue

        ok, reason = check_data_file(df)
        if not ok:
            print(f"❌ {os.path.basename(df)}: {reason} — skipping.\n")
            continue

        in_file = STRUCT_MAP[struct]

        for T in TEMPS:
            total_jobs += 1
            ok, mins = run_one(struct, df, T, in_file, attempt=1)
            total_min += mins
            if not ok:
                print("↻ retrying once...")
                ok2, mins2 = run_one(struct, df, T, in_file, attempt=2)
                total_min += mins2

    elapsed = (time.time() - tstart)/60.0
    print("===============================================")
    print(f"🏁 Finished {total_jobs} jobs in {elapsed:.2f} min "
          f"(avg {elapsed/max(total_jobs,1):.2f} min/job)")
    print("Logs   →", LOG_DIR)
    print("Results→", RES_DIR)
    print("===============================================\n")

if __name__ == "__main__":
    main()
