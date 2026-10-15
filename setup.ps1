# Safe setup helper for Windows PowerShell.
# This script prepares the profile files locally; it does not create repositories,
# change GitHub settings, or push code without your explicit commands.
$ErrorActionPreference = "Stop"

Write-Host "`nHaimanot25 GitHub Profile Kit" -ForegroundColor Cyan
Write-Host "This will copy the kit into a local folder and preserve existing files." -ForegroundColor Gray

$Target = Read-Host "Enter destination folder (default: .\Haimanot25-profile)"
if ([string]::IsNullOrWhiteSpace($Target)) {
    $Target = Join-Path (Get-Location) "Haimanot25-profile"
}
$Target = [System.IO.Path]::GetFullPath($Target)

if (Test-Path $Target) {
    $existing = Get-ChildItem -Force $Target -ErrorAction SilentlyContinue
    if ($existing) {
        Write-Host "Destination already exists and is not empty: $Target" -ForegroundColor Yellow
        $confirm = Read-Host "Continue? Existing files with the same names may be overwritten (y/N)"
        if ($confirm -notin @("y", "Y")) {
            Write-Host "Cancelled; no files changed."
            exit 0
        }
    }
} else {
    New-Item -ItemType Directory -Path $Target -Force | Out-Null
}

$Source = $PSScriptRoot
Get-ChildItem -LiteralPath $Source -Force |
    Where-Object { $_.Name -notin @("setup.ps1", "haimanot-github-profile-kit.zip") } |
    ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $Target -Recurse -Force
    }

Write-Host "`nFiles copied to: $Target" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review README.md and assets/hero.svg."
Write-Host "  2. Create a PUBLIC repository named exactly Haimanot25 if you do not already have one."
Write-Host "  3. In that repository, enable Actions and allow workflow write access."
Write-Host "  4. From the target folder, run: git init; git branch -M main; git add .; git commit -m 'Add profile'; git remote add origin https://github.com/Haimanot25/Haimanot25.git; git push -u origin main"
Write-Host "`nNo GitHub changes have been made yet." -ForegroundColor Gray
