param(
    [string]$ExecutablePath = "",
    [string]$InstallerPath = ""
)

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

$PackageVersion = (& $PythonExe -c "import reco_box; print(reco_box.__version__)").Trim()
if ($LASTEXITCODE -ne 0 -or $PackageVersion -ne $Version) {
    throw "Python package version mismatch: expected $Version, got $PackageVersion"
}

if ($ExecutablePath) {
    if (-not (Test-Path -LiteralPath $ExecutablePath)) {
        throw "Executable is missing: $ExecutablePath"
    }
    $ExecutableInfo = (Get-Item -LiteralPath $ExecutablePath).VersionInfo
    foreach ($field in @("FileVersion", "ProductVersion")) {
        $actualVersion = [string]$ExecutableInfo.$field
        if ($actualVersion.Trim() -ne $Version) {
            throw "Executable $field mismatch: expected $Version, got $actualVersion"
        }
    }
}

if ($InstallerPath) {
    if (-not (Test-Path -LiteralPath $InstallerPath)) {
        throw "Installer is missing: $InstallerPath"
    }
    $InstallerName = (Get-Item -LiteralPath $InstallerPath).Name
    $ExpectedInstallerName = "RecoBox-Setup-$Version.exe"
    if ($InstallerName -ne $ExpectedInstallerName) {
        throw "Installer filename mismatch: expected $ExpectedInstallerName, got $InstallerName"
    }
    $InstallerInfo = (Get-Item -LiteralPath $InstallerPath).VersionInfo
    foreach ($field in @("FileVersion", "ProductVersion")) {
        $actualVersion = [string]$InstallerInfo.$field
        if ($actualVersion.Trim() -ne $Version) {
            throw "Installer $field mismatch: expected $Version, got $actualVersion"
        }
    }
}

$surfaces = @("Python package=$PackageVersion")
if ($ExecutablePath) {
    $surfaces += "executable=$(([string]$ExecutableInfo.ProductVersion).Trim())"
}
if ($InstallerPath) {
    $surfaces += "installer=$(([string]$InstallerInfo.ProductVersion).Trim())"
    $surfaces += "artifact filename=$InstallerName"
}
Write-Output ("Version consistency PASS: " + ($surfaces -join "; "))
