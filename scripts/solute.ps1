# SOLUTE-MANAGED: Windows installer and uninstaller launcher.
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('install', 'uninstall', 'doctor')]
    [string]$Command
)

$soluteScript = Join-Path $PSScriptRoot 'solute.py'
$solutePython3 = Get-Command python3 -ErrorAction SilentlyContinue
$solutePython = Get-Command python -ErrorAction SilentlyContinue
$solutePy = Get-Command py -ErrorAction SilentlyContinue

if ($solutePython3) {
    & $solutePython3.Source $soluteScript $Command
    exit $LASTEXITCODE
}
if ($solutePython) {
    & $solutePython.Source $soluteScript $Command
    exit $LASTEXITCODE
}
if ($solutePy) {
    & $solutePy.Source -3 $soluteScript $Command
    exit $LASTEXITCODE
}

Write-Error 'Solute requires Python 3.'
exit 1
