<!-- SOLUTE-MANAGED: repository instructions. Removing this repository removes this file. -->

# Solute repository instructions

When the user asks to install this repository, read `README.md`, detect the operating system, and run the matching launcher:

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/solute.ps1 install
Linux/macOS: sh scripts/solute.sh install
```

Use the same launcher with `doctor` to check the result. When the user asks to remove or uninstall Solute, run it with `uninstall`. If the repository is unavailable, run:

```text
codex plugin remove solute@solute
codex plugin marketplace remove solute
```

Do not edit global `AGENTS.md` or copy Solute files into loose user directories. Preserve unrelated Codex settings and plugins.

For repository changes, use an available Python 3 interpreter to run `-m unittest discover -s tests -v` and the validators named in `README.md`.
