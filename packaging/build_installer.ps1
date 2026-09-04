$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $PSScriptRoot
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"
$VersionScript = Join-Path $ProjectDir "tools\project_version.py"
if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "Project virtual environment is missing: $PythonExe"
}
if (-not (Test-Path -LiteralPath $VersionScript)) {
    throw "Project version reader is missing: $VersionScript"
}
$Version = (& $PythonExe $VersionScript).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Version)) {
    throw "Could not read the project version from pyproject.toml"
}
$VersionParts = $Version.Split(".")
if (
    $VersionParts.Count -ne 3 -or
    ($VersionParts | Where-Object { $_ -notmatch "^\d+$" })
) {
    throw "Inno Setup version metadata requires a three-part numeric version: $Version"
}
$CompilerCandidates = @(
    (Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 7\ISCC.exe"),
    (Join-Path $env:LOCALAPPDATA "Programs\Inno Setup 6\ISCC.exe"),
    (Join-Path $env:ProgramFiles "Inno Setup 7\ISCC.exe"),
    (Join-Path $env:ProgramFiles "Inno Setup 6\ISCC.exe"),
    (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 7\ISCC.exe"),
    (Join-Path ${env:ProgramFiles(x86)} "Inno Setup 6\ISCC.exe")
)
$Compiler = $CompilerCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $Compiler) {
    throw "Inno Setup compiler was not found. Install Inno Setup 7 or 6 first."
}

$AppExe = Join-Path $ProjectDir "dist\Reco Box\RecoBox.exe"
if (-not (Test-Path -LiteralPath $AppExe)) {
    throw "Packaged application is missing. Run packaging\build.ps1 first."
}

& $Compiler "/DMyAppVersion=$Version" (Join-Path $PSScriptRoot "installer.iss")
if ($LASTEXITCODE -ne 0) {
    throw "Inno Setup failed with exit code $LASTEXITCODE"
}

$SetupExe = Join-Path $ProjectDir "dist\installer\RecoBox-Setup-$Version.exe"
if (-not (Test-Path -LiteralPath $SetupExe)) {
    throw "Installer was not created: $SetupExe"
}

Write-Output $SetupExe
