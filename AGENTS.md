<!-- SOLUTE-MANAGED: repository instructions. Removing this repository removes this file. -->

# Solute repository instructions

When the user asks to install this repository, read `README.md`, detect the operating system, and run the matching launcher:

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/solute.ps1 install
Linux/macOS: sh scripts/solute.sh install
```

After installation, tell the user to open a new Codex CLI session, enter `/hooks`, review the Solute hook, and choose Trust. Then use the launcher with `verify`. Do not claim automatic activation until verification prints `Solute verified`. When the user asks to remove or uninstall Solute, run the launcher with `uninstall`. If the repository is unavailable, run:

```text
codex plugin remove solute@solute
codex plugin marketplace remove solute
```

Do not edit global `AGENTS.md` or copy Solute files into loose user directories. Preserve unrelated Codex settings and plugins.

For repository changes, run the Rust and Python tests plus the validators named in `README.md`.
