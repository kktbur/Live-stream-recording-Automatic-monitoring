$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $PSScriptRoot
$CompilerCandidates = @(
    (Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 7\ISCC.exe"),
    (Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 6\ISCC.exe"),
    (Join-Path $env:ProgramFiles "Inno Setup 7\ISCC.exe"),
    (Join-Path $env:ProgramFiles "Inno Setup 6\ISCC.exe")
)
$Compiler = $CompilerCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $Compiler) {
    throw "Inno Setup compiler was not found. Install Inno Setup 7 or 6 first."
}

$AppExe = Join-Path $ProjectDir "dist\Reco Box\RecoBox.exe"
if (-not (Test-Path -LiteralPath $AppExe)) {
    throw "Packaged application is missing. Run packaging\build.ps1 first."
}

& $Compiler (Join-Path $PSScriptRoot "installer.iss")
if ($LASTEXITCODE -ne 0) {
    throw "Inno Setup failed with exit code $LASTEXITCODE"
}

$SetupExe = Join-Path $ProjectDir "dist\installer\RecoBox-Setup-0.1.3.exe"
if (-not (Test-Path -LiteralPath $SetupExe)) {
    throw "Installer was not created: $SetupExe"
}

Write-Output $SetupExe
