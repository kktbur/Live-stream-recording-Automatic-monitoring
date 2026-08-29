$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $PSScriptRoot
$Installer = Join-Path $ProjectDir "dist\installer\RecoBox-Setup-0.2.0.exe"
$Target = Join-Path $ProjectDir "artifacts\install-test-0.2.0"
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
Write-Output "Installed self-test passed: $Exe"
