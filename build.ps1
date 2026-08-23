[CmdletBinding()]
param(
	[string]$OutputDirectory = (Join-Path $PSScriptRoot 'dist')
)

$ErrorActionPreference = 'Stop'
$addonDirectory = Join-Path $PSScriptRoot 'addon'
$manifestPath = Join-Path $addonDirectory 'manifest.ini'
$manifestText = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8
$versionMatch = [regex]::Match($manifestText, '(?m)^version\s*=\s*"?([^"\r\n]+)"?\s*$')
if (-not $versionMatch.Success) {
	throw 'The add-on version could not be read from addon\manifest.ini.'
}
$version = $versionMatch.Groups[1].Value.Trim()

$poPath = Join-Path $addonDirectory 'locale\pl\LC_MESSAGES\nvda.po'
$moPath = Join-Path $addonDirectory 'locale\pl\LC_MESSAGES\nvda.mo'
$msgfmt = Get-Command msgfmt.exe -ErrorAction SilentlyContinue
if ($null -ne $msgfmt) {
	& $msgfmt.Source --check --output-file=$moPath $poPath
	if ($LASTEXITCODE -ne 0) { throw "msgfmt returned exit code $LASTEXITCODE." }
}
elseif (-not (Test-Path -LiteralPath $moPath -PathType Leaf)) {
	throw 'nvda.mo is missing and msgfmt.exe is not available to compile it.'
}

New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
$outputPath = Join-Path $OutputDirectory "autorunOrganizerAccess-$version.nvda-addon"
if (Test-Path -LiteralPath $outputPath) {
	Remove-Item -LiteralPath $outputPath -Force
}

$sourceFiles = Get-ChildItem -LiteralPath $addonDirectory -Recurse -File | Where-Object {
	$relative = $_.FullName.Substring($addonDirectory.Length).TrimStart('\')
	$relative -notmatch '(^|\\)__pycache__(\\|$)' -and
	$_.Extension -ne '.pyc' -and
	$_.Extension -ne '.po'
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
Add-Type -AssemblyName System.IO.Compression
$stream = [IO.File]::Open($outputPath, [IO.FileMode]::CreateNew)
try {
	$archive = [IO.Compression.ZipArchive]::new($stream, [IO.Compression.ZipArchiveMode]::Create, $false)
	try {
		foreach ($file in $sourceFiles) {
			$entryName = $file.FullName.Substring($addonDirectory.Length).TrimStart('\').Replace('\', '/')
			[void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile(
				$archive,
				$file.FullName,
				$entryName,
				[IO.Compression.CompressionLevel]::Optimal
			)
		}
	}
	finally {
		$archive.Dispose()
	}
}
finally {
	$stream.Dispose()
}

$archive = [IO.Compression.ZipFile]::OpenRead($outputPath)
try {
	$entries = @($archive.Entries.FullName -replace '\\', '/')
	foreach ($required in @(
		'manifest.ini',
		'appModules/autorunorganizer.py',
		'doc/en/readme.html',
		'doc/pl/readme.html',
		'locale/pl/manifest.ini',
		'locale/pl/LC_MESSAGES/nvda.mo'
	)) {
		if ($required -notin $entries) { throw "Package entry is missing: $required" }
	}
}
finally {
	$archive.Dispose()
}

$hash = (Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash
Write-Host "Built: $outputPath"
Write-Host "SHA256: $hash"
