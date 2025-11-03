#!/usr/bin/env bash
set -euo pipefail

# ---- CONFIG (edit if your paths differ) ----
ROOT="/Users/Lenovo/projects/comp2"
LMP="/opt/homebrew/bin/lmp_serial"
DATA_DIR="$ROOT/work/data"
LOG_DIR="$ROOT/work/logs"
RES_DIR="$ROOT/work/results"
IN_FCC="$ROOT/inputs/in.fcc.lmp"
IN_HCP="$ROOT/inputs/in.hcp.lmp"
IN_DHCP="$ROOT/inputs/in.dhcp.lmp"

# Temperature order you asked for
TEMPS=("100" "550" "350")

mkdir -p "$LOG_DIR" "$RES_DIR"

# quick sanity checks
[[ -x "$LMP" ]] || { echo "ERROR: lmp_serial not found at $LMP"; exit 1; }
[[ -f "$IN_FCC" && -f "$IN_HCP" && -f "$IN_DHCP" ]] || { echo "ERROR: missing one of in.fcc.lmp / in.hcp.lmp / in.dhcp.lmp"; exit 1; }
[[ -d "$DATA_DIR" ]] || { echo "ERROR: data dir not found: $DATA_DIR"; exit 1; }

# ---- RUN LOOP (serial) ----
shopt -s nullglob
for data in "$DATA_DIR"/*.data; do
  base="$(basename "$data")"
  struct="${base%%_*}"           # fcc_..., hcp_..., dhcp_...
  struct_lower="$(echo "$struct" | tr '[:upper:]' '[:lower:]')"

  case "$struct_lower" in
    fcc)  IN_FILE="$IN_FCC" ;;
    hcp)  IN_FILE="$IN_HCP" ;;
    dhcp) IN_FILE="$IN_DHCP" ;;
    *)    echo "Skipping $base (unknown struct prefix: $struct)"; continue ;;
  esac

  # per-file results directory
  outdir="$RES_DIR/${base%.data}"
  mkdir -p "$outdir"

  for T in "${TEMPS[@]}"; do
    tag="${base%.data}_${T}K"
    logfile="$LOG_DIR/$tag.log"

    echo "[RUN] $tag with $IN_FILE"
    # ensure LAMMPS can write data files even if input forgets to mkdir
    # (still recommended to keep 'shell mkdir -p ${OUTDIR}' inside your .lmp files)
    mkdir -p "$outdir"

    "$LMP" \
      -in "$IN_FILE" \
      -var DATA "$data" \
      -var TEMP "$T" \
      -var STRUCT "$struct_lower" \
      -var OUTDIR "$outdir" \
      > "$logfile" 2>&1 || {
        echo "  ❌ Failed: $tag (see $logfile)"
        continue
      }

    echo "  ✅ Done: $tag (log: $logfile)"
  done
done
echo "All jobs submitted."
