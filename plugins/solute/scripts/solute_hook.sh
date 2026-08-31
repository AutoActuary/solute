#!/bin/sh
# SOLUTE-MANAGED: POSIX launcher for the installed Solute hook.
set -eu

solute_script="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/solute_hook.py"

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$solute_script"
fi
if command -v python >/dev/null 2>&1; then
    exec python "$solute_script"
fi

echo "Solute hook skipped: Python 3 is unavailable." >&2
exit 0
