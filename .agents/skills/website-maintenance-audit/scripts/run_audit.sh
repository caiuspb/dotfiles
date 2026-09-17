#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="${1:-$HERE/config.yaml}"
STAMP="$(date +%Y-%m-%d_%H%M%S)"
OUTPUT_ROOT="${AUDIT_OUTPUT_DIR:-$PWD/reports}"
OUT="$OUTPUT_ROOT/$STAMP"
if [[ -x "$HERE/.venv/bin/python3" ]]; then
	PYTHON="$HERE/.venv/bin/python3"
else
	PYTHON="$(command -v python3 || true)"
	if [[ -z "$PYTHON" ]]; then
		echo "No Python interpreter found." >&2
		exit 1
	fi
fi
mkdir -p "$OUT"
"$PYTHON" "$HERE/scripts/audit.py" "$CONFIG" --out "$OUT"
"$PYTHON" "$HERE/scripts/generate_report.py" "$OUT/audit-results.json" "$HERE/assets/audit-template.docx" "$OUT/Website-Wartung-Audit.docx"
echo "Report: $OUT/Website-Wartung-Audit.docx"
