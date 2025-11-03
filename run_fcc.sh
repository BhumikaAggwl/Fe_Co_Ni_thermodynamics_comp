#!/usr/bin/env bash
set -euo pipefail

# --- CONFIGURE PATHS ---
LMP="/opt/homebrew/bin/lmp_serial"
IN_FILE="/Users/Lenovo/projects/comp2/inputs/in.fcc.lmp"
DATA_DIR="/Users/Lenovo/projects/comp2/work/data"
LOG_DIR="/Users/Lenovo/projects/comp2/work/logs"
RES_DIR="/Users/Lenovo/projects/comp2/work/results"
TEMPS=(100 350 550)

mkdir -p "$LOG_DIR" "$RES_DIR"

# --- RUN LOOP FOR FCC FILES ---
shopt -s nullglob
for data in "$DATA_DIR"/fcc_*.data; do
  base=$(basename "$data" .data)

  # ✅ Initialize elements array
  elements=()

  # ✅ Extract present elements by checking composition
  [[ "$base" =~ Co0\.([0-9]+) ]] && [[ "${BASH_REMATCH[1]}" != "00" ]] && elements+=("Co")
  [[ "$base" =~ Fe0\.([0-9]+) ]] && [[ "${BASH_REMATCH[1]}" != "00" ]] && elements+=("Fe")
  [[ "$base" =~ Ni0\.([0-9]+) ]] && [[ "${BASH_REMATCH[1]}" != "00" ]] && elements+=("Ni")

  # ✅ Skip files with zero valid elements
  if [ ${#elements[@]} -eq 0 ]; then
    echo "⚠️  Skipping $base — no nonzero elements found."
    continue
  fi

  # ✅ Compose pair_coeff line
  pair_coeff="pair_coeff * * ../potentials/FeNiCrCoAl-heaweight.setfl"
  for el in "${elements[@]}"; do
    pair_coeff+=" $el"
  done

  for T in "${TEMPS[@]}"; do
    outdir="$RES_DIR/${base}_${T}K"
    logfile="$LOG_DIR/${base}_${T}K.log"

    echo "▶ Running ${base}.data at ${T}K"
    mkdir -p "$outdir"

    "$LMP" -in "$IN_FILE" \
      -var DATA "$data" \
      -var TEMP "$T" \
      -var STRUCT "fcc" \
      -var OUTDIR "$outdir" \
      -var PAIR "$pair_coeff" \
      > "$logfile" 2>&1 || {
        echo "❌ Failed (see: $logfile)"
        continue
      }

    echo "✅ Done (log: $logfile)"
  done
done
