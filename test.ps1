[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
python -m unittest discover -s (Join-Path $PSScriptRoot 'tests') -v
if ($LASTEXITCODE -ne 0) { throw "Unit tests returned exit code $LASTEXITCODE." }

$pythonModules = @(
	(Join-Path $PSScriptRoot 'addon\autorunOrganizerAccessShared.py'),
	(Join-Path $PSScriptRoot 'addon\appModules\autorunorganizer.py'),
	(Join-Path $PSScriptRoot 'addon\globalPlugins\autorunOrganizerAccess.py')
)
python -m py_compile @pythonModules
if ($LASTEXITCODE -ne 0) { throw "Python compilation returned exit code $LASTEXITCODE." }

$requiredBilingualPaths = @(
	(Join-Path $PSScriptRoot 'README.pl.md'),
	(Join-Path $PSScriptRoot 'addon\doc\pl\readme.html'),
	(Join-Path $PSScriptRoot 'addon\locale\pl\manifest.ini')
)
foreach ($path in $requiredBilingualPaths) {
	if (-not (Test-Path -LiteralPath $path)) {
		throw "Bilingual package is missing: $path"
	}
}

& (Join-Path $PSScriptRoot 'build.ps1')
