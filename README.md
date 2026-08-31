<!-- SOLUTE-MANAGED: public repository entry point. -->

# Solute

Sol judgment, Luna execution.

Solute is a Codex plugin that gives every Sol user turn a compact delegation policy. Sol keeps problem framing, design, integration, and final judgment. Luna xhigh handles bounded work that Sol can brief and verify cheaply.

It does nothing on Terra or Luna. Say `Don't use /solute` to disable it for one turn. Invoke `$solute` directly when you want the same policy without automatic activation.

## Supported systems

Solute supports Codex Desktop and CLI on Windows, plus Codex CLI on Linux and macOS. It needs Python 3. Windows uses PowerShell; Linux and macOS use POSIX `sh`. CI runs the complete suite on Windows and Ubuntu.

## Install

Give Codex this repository and say:

```text
Install <path-to-this-repository>
```

Codex should follow `AGENTS.md` and choose the correct launcher:

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/solute.ps1 install
Linux/macOS: sh scripts/solute.sh install
```

Codex will ask you to review and trust the hook. Start a new task after installation.

## Uninstall

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/solute.ps1 uninstall
Linux/macOS: sh scripts/solute.sh uninstall
```

The equivalent manual commands are:

```text
codex plugin remove solute@solute
codex plugin marketplace remove solute
```

Solute does not alter global `AGENTS.md` or install loose skill files. See [UNINSTALL.md](UNINSTALL.md) for recovery and residue checks.

## Verify the repository

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/solute.ps1 doctor
Linux/macOS: sh scripts/solute.sh doctor
```

Run the test suite with any Python 3 interpreter: `python3 -m unittest discover -s tests -v` or `python -m unittest discover -s tests -v`. The setup agent should also locate and run Codex's `validate_plugin.py` and `quick_validate.py` against `plugins/solute` and `plugins/solute/skills/solute`.

The optional [delegation guide](plugins/solute/skills/solute/references/delegation-guide.md) records the tested mapping, limits, and brief format. It is not loaded unless Sol needs it.
