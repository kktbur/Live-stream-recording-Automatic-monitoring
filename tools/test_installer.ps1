$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $PSScriptRoot
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"
$VersionScript = Join-Path $ProjectDir "tools\project_version.py"
$VersionCheckScript = Join-Path $ProjectDir "tools\check_version_consistency.ps1"
if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "Project virtual environment is missing: $PythonExe"
}
if (-not (Test-Path -LiteralPath $VersionScript)) {
    throw "Project version reader is missing: $VersionScript"
}
if (-not (Test-Path -LiteralPath $VersionCheckScript)) {
    throw "Version consistency checker is missing: $VersionCheckScript"
}
$Version = (& $PythonExe $VersionScript).Trim()
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($Version)) {
    throw "Could not read the project version from pyproject.toml"
}
$Installer = Join-Path $ProjectDir "dist\installer\RecoBox-Setup-$Version.exe"
$Target = Join-Path $ProjectDir "artifacts\install-test-$Version"
$DataDir = Join-Path $Target "self-test-data"
$Arguments = '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /DIR="' + $Target + '"'

$InstallProcess = Start-Process -FilePath $Installer -ArgumentList $Arguments -Wait -PassThru
if ($InstallProcess.ExitCode -ne 0) {
    throw "Installer exited with code $($InstallProcess.ExitCode)"
}
$Exe = Join-Path $Target "RecoBox.exe"
if (-not (Test-Path -LiteralPath $Exe)) {
    throw "Installer did not create $Exe"
}
$env:RECO_BOX_DATA_DIR = $DataDir
$SelfTest = Start-Process -FilePath $Exe -ArgumentList "--self-test" -Wait -PassThru
if ($SelfTest.ExitCode -ne 0) {
    throw "Installed self-test exited with code $($SelfTest.ExitCode)"
}
$Report = Get-Content -Raw (Join-Path $DataDir "self-check.json") | ConvertFrom-Json
if (-not $Report.passed) {
    throw "Installed self-test report did not pass"
}
& pwsh -NoProfile -File $VersionCheckScript -ExecutablePath $Exe -InstallerPath $Installer
Write-Output "Installed self-test passed: $Exe"
