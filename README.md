<!-- SOLUTE-MANAGED: public repository entry point. -->

# Solute

Sol judgment, Luna execution.

Solute is a Codex plugin that gives every Sol user turn a compact delegation policy. Sol keeps problem framing, design, integration, and final judgment. Luna xhigh handles bounded work that Sol can brief and verify cheaply.

It sends no policy tokens to Terra or Luna. Codex still starts the small native gate because `UserPromptSubmit` does not support model matchers. Say `Don't use /solute` to disable it for one turn. Invoke `$solute` directly when you want the same policy without automatic activation.

## Supported systems

Solute supports Codex Desktop and CLI on Windows, plus Codex CLI on Linux and macOS. Its per-turn gate is a small Rust executable with no interpreter or package startup. The full source is in `native-hook`; GitHub Actions builds the release artifacts. The installer downloads the correct artifact and verifies its SHA-256 hash. Users do not need Rust or a compiler. Python 3 and PowerShell or POSIX `sh` are used only during installation.

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

### Required trust step

Codex cannot trust a third-party hook on your behalf. Installation is incomplete until you do this:

1. Start a new Codex CLI session.
2. Enter `/hooks`.
3. Select the Solute `UserPromptSubmit` hook. Confirm that it points to `bin/solute-hook` inside the Solute plugin.
4. Choose **Trust**.
5. Exit that session and run the matching launcher with `verify`:

```text
Windows: powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts/solute.ps1 verify
Linux/macOS: sh scripts/solute.sh verify
```

Only the `Solute verified` result confirms automatic Sol activation. Updating Solute changes the hook hash, so Codex will require this review again.

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

Run `cargo test --manifest-path native-hook/Cargo.toml`, build the release runtime, set `SOLUTE_RUNTIME_BINARY` to that binary, then run the Python suite. The setup agent should also locate and run Codex's `validate_plugin.py` and `quick_validate.py` against `plugins/solute` and `plugins/solute/skills/solute`.

The optional [delegation guide](plugins/solute/skills/solute/references/delegation-guide.md) records the tested mapping, limits, and brief format. It is not loaded unless Sol needs it.
