#!/usr/bin/env bash
set -euo pipefail

echo "Starting HCP simulations using /opt/homebrew/bin/lmp_serial"

LMP="/opt/homebrew/bin/lmp_serial"
IN_FILE="/Users/Lenovo/projects/comp2/inputs/in.hcp.lmp"
DATA_DIR="/Users/Lenovo/projects/comp2/work/data"
LOG_DIR="/Users/Lenovo/projects/comp2/work/logs"
RES_DIR="/Users/Lenovo/projects/comp2/work/results"
TEMPS=(100 350 550)

mkdir -p "$LOG_DIR" "$RES_DIR"

shopt -s nullglob
for data in "$DATA_DIR"/hcp_*.data; do
  base=$(basename "$data" .data)

  for T in "${TEMPS[@]}"; do
    outdir="$RES_DIR/${base}_${T}K"
    logfile="$LOG_DIR/${base}_${T}K.log"

    echo "▶ Running $base.data at ${T}K"
    mkdir -p "$outdir"

    "$LMP" -in "$IN_FILE" \
      -var DATA "$data" \
      -var TEMP "$T" \
      -var STRUCT "hcp" \
      -var OUTDIR "$outdir" \
      > "$logfile" 2>&1 || {
        echo "❌ Failed (see: $logfile)"
        continue
      }

    echo "✅ Done (log: $logfile)"
  done
done

echo "🎉 All HCP simulations finished!"
