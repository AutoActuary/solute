#!/bin/sh
# SOLUTE-MANAGED: POSIX installer and uninstaller launcher.
set -eu

solute_script="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/solute.py"

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$solute_script" "$@"
fi
if command -v python >/dev/null 2>&1; then
    exec python "$solute_script" "$@"
fi

echo "Solute requires Python 3." >&2
exit 1
