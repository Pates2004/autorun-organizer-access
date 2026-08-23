[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
python -m unittest discover -s (Join-Path $PSScriptRoot 'tests') -v
if ($LASTEXITCODE -ne 0) { throw "Unit tests returned exit code $LASTEXITCODE." }

$modulePath = Join-Path $PSScriptRoot 'addon\appModules\autorunorganizer.py'
python -m py_compile $modulePath
if ($LASTEXITCODE -ne 0) { throw "Python compilation returned exit code $LASTEXITCODE." }

& (Join-Path $PSScriptRoot 'build.ps1')
