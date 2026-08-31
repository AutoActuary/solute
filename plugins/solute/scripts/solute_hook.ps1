# SOLUTE-MANAGED: Windows launcher for the installed Solute hook.
$soluteScript = Join-Path $PSScriptRoot 'solute_hook.py'
$solutePython3 = Get-Command python3 -ErrorAction SilentlyContinue
$solutePython = Get-Command python -ErrorAction SilentlyContinue
$solutePy = Get-Command py -ErrorAction SilentlyContinue

if ($solutePython3) {
    & $solutePython3.Source $soluteScript
    exit $LASTEXITCODE
}
if ($solutePython) {
    & $solutePython.Source $soluteScript
    exit $LASTEXITCODE
}
if ($solutePy) {
    & $solutePy.Source -3 $soluteScript
    exit $LASTEXITCODE
}

Write-Error 'Solute hook skipped: Python 3 is unavailable.'
exit 0
