<#
.SYNOPSIS
  Run the `strip_tones.py` script over dictionary files and optionally commit results.

.DESCRIPTION
  Searches for files matching "*-terra.dict.yaml" (recursively) and runs
  the Python script to generate tone-free copies (default: removes "-terra"
  from output name). Optionally stages and commits the generated files if
  `-Commit` is supplied and `git` is available.

USAGE
  .\scripts\generate_notone.ps1
  .\scripts\generate_notone.ps1 -RepoRoot . -Commit
#>

param(
    [string]$RepoRoot = '.',
    [switch]$Commit
)

Set-StrictMode -Version Latest
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$pyScript = Join-Path $scriptDir 'strip_tones.py'
if (-not (Test-Path $pyScript)) {
    Write-Error "Could not find strip_tones.py at $pyScript"
    exit 2
}

Write-Host "Searching for '*-terra.dict.yaml' under $RepoRoot" -ForegroundColor Cyan
$files = Get-ChildItem -Path $RepoRoot -Filter '*-terra.dict.yaml' -File -Recurse -ErrorAction SilentlyContinue
if (-not $files) {
    Write-Host "No matching files found." -ForegroundColor Yellow
    exit 0
}

foreach ($f in $files) {
    Write-Host "Processing $($f.FullName)" -ForegroundColor Green
    $args = @($f.FullName)
    $exe = 'python'
    $proc = Start-Process -FilePath $exe -ArgumentList $args -NoNewWindow -Wait -PassThru -ErrorAction SilentlyContinue
    if ($proc.ExitCode -ne 0) {
        Write-Warning "Processing failed for $($f.FullName) (exit $($proc.ExitCode))"
    }
}

if ($Commit) {
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Error "git not found in PATH; cannot commit."
        exit 3
    }
    Push-Location $RepoRoot
    try {
        git add --all
        $status = git status --porcelain
        if ($status) {
            git commit -m "Auto-generate tone-free dictionaries"
            git push
            Write-Host "Committed and pushed changes." -ForegroundColor Green
        } else {
            Write-Host "No changes to commit." -ForegroundColor Yellow
        }
    } finally {
        Pop-Location
    }
}

Write-Host "Done." -ForegroundColor Cyan
