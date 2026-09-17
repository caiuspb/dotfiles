#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${1:-$HERE/config.yaml}"
STAMP="$(date +%Y-%m-%d_%H%M%S)"
OUT="$HERE/reports/$STAMP"
mkdir -p "$OUT"
python3 "$HERE/scripts/audit.py" "$CONFIG" --out "$OUT"
python3 "$HERE/scripts/generate_report.py" "$OUT/audit-results.json" "$HERE/assets/audit-template.docx" "$OUT/Website-Wartung-Audit.docx"
echo "Report: $OUT/Website-Wartung-Audit.docx"
