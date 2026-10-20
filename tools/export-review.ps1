param(
    [string]$KiCadCli = 'kicad-cli',
    [string]$OutputDirectory = ''
)

$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $repoRoot 'work/review'
}
$null = New-Item -ItemType Directory -Path $OutputDirectory -Force
$inverter = Join-Path $repoRoot 'hardware/inverter/cirBATTverter_1KWH'
$planar = Join-Path $repoRoot 'hardware/planar-transformer/PlanarW_11082026'

& $KiCadCli version
if ($LASTEXITCODE -ne 0) { throw 'KiCad CLI is unavailable.' }
& $KiCadCli sch erc --severity-all --format json -o (Join-Path $OutputDirectory 'erc.json') ($inverter + '.kicad_sch')
if ($LASTEXITCODE -ne 0) { throw 'ERC report generation failed.' }
& $KiCadCli pcb drc --severity-all --schematic-parity --format json -o (Join-Path $OutputDirectory 'drc-inverter.json') ($inverter + '.kicad_pcb')
if ($LASTEXITCODE -ne 0) { throw 'Inverter DRC report generation failed.' }
& $KiCadCli pcb drc --severity-all --format json -o (Join-Path $OutputDirectory 'drc-planar.json') ($planar + '.kicad_pcb')
if ($LASTEXITCODE -ne 0) { throw 'Planar DRC report generation failed.' }

Write-Output 'Reports generated. Inspect violations and ignored_checks; successful export does not mean the design passed.'
Write-Output 'For clearance checks, use a separate full project copy and explicitly enable the relevant rules there.'
