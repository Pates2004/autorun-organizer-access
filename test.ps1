[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
python -m unittest discover -s (Join-Path $PSScriptRoot 'tests') -v
if ($LASTEXITCODE -ne 0) { throw "Unit tests returned exit code $LASTEXITCODE." }

$pythonModules = @(
	(Join-Path $PSScriptRoot 'addon\appModules\autorunorganizer.py'),
	(Join-Path $PSScriptRoot 'addon\globalPlugins\autorunOrganizerAccess.py')
)
python -m py_compile @pythonModules
if ($LASTEXITCODE -ne 0) { throw "Python compilation returned exit code $LASTEXITCODE." }

$forbiddenPolishPaths = @(
	(Join-Path $PSScriptRoot 'README.pl.md'),
	(Join-Path $PSScriptRoot 'addon\doc\pl'),
	(Join-Path $PSScriptRoot 'addon\locale\pl')
)
foreach ($path in $forbiddenPolishPaths) {
	if (Test-Path -LiteralPath $path) {
		throw "English-only package contains a Polish localization path: $path"
	}
}

& (Join-Path $PSScriptRoot 'build.ps1')
