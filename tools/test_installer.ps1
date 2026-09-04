param(
    [Parameter(Mandatory = $true)]
    [ValidateNotNullOrEmpty()]
    [string]$PreviousInstallerPath
)

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
if (-not (Test-Path -LiteralPath $Installer)) {
    throw "Current installer is missing: $Installer"
}

$ArtifactsDir = Join-Path $ProjectDir "artifacts"
$TestId = [guid]::NewGuid().ToString("N")
$Target = Join-Path $ArtifactsDir "install-test-$Version-$TestId"
$DataDir = Join-Path $ArtifactsDir "install-user-data-$Version-$TestId"
$DatabasePath = Join-Path $DataDir "reco_box.db"
$SentinelPath = Join-Path $DataDir "upgrade-sentinel.txt"
$Sentinel = "raco-box-upgrade-$TestId"

New-Item -ItemType Directory -Force -Path $ArtifactsDir | Out-Null
if (Test-Path -LiteralPath $Target) {
    throw "Refusing to reuse an existing install test directory: $Target"
}
New-Item -ItemType Directory -Force -Path $DataDir | Out-Null
Set-Content -LiteralPath $SentinelPath -Value $Sentinel -NoNewline -Encoding utf8NoBOM

$SeedDatabase = @'
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from reco_box.domain import Platform, Room, RoomStatus
from reco_box.storage import Database

database_path, test_id, marker, data_dir = sys.argv[1:5]
room_id = f"upgrade-room-{test_id}"
recording_history_dir = Path(data_dir) / f"recording-history-{test_id}"
group_id = f"upgrade-group-{test_id}"

database = Database(Path(database_path))
room = Room(
    id=room_id,
    url=f"https://example.invalid/reco-box-upgrade-{test_id}",
    platform=Platform.UNKNOWN,
    streamer_name="Upgrade Sentinel",
    title="Installer upgrade sentinel",
    status=RoomStatus.OFFLINE,
)
database.upsert_room(room)
database.set_setting("upgrade_sentinel_config", marker)
recording_id = database.start_recording(
    room_id,
    datetime.now(timezone.utc),
    recording_history_dir,
    group_id=group_id,
)
database.finish_recording(
    recording_id,
    datetime.now(timezone.utc) + timedelta(seconds=1),
    "completed",
    123,
)
database.update_recording_probe(recording_id, "valid", 1.0, "upgrade-test")

if database.get_setting("upgrade_sentinel_config") != marker:
    raise SystemExit("application setting could not be read after writing")
if not any(item.id == room_id for item in database.list_rooms()):
    raise SystemExit("application room could not be read after writing")
if not any(
    item["id"] == group_id and item["status"] == "completed"
    for item in database.list_recordings()
):
    raise SystemExit("application recording history could not be read after writing")
'@
& $PythonExe -c $SeedDatabase $DatabasePath $TestId $Sentinel $DataDir
if ($LASTEXITCODE -ne 0) {
    throw "Could not seed the SQLite configuration and recording history"
}
$env:RECO_BOX_DATA_DIR = $DataDir

function Invoke-SilentInstaller {
    param(
        [Parameter(Mandatory)]
        [string]$InstallerPath,
        [Parameter(Mandatory)]
        [string]$InstallPath,
        [Parameter(Mandatory)]
        [string]$LogPath
    )

    $arguments = '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /LOG="' + $LogPath + '" /DIR="' + $InstallPath + '"'
    $process = Start-Process -FilePath $InstallerPath -ArgumentList $arguments -Wait -PassThru
    if ($process.ExitCode -ne 0) {
        $details = if (Test-Path -LiteralPath $LogPath) {
            $logLines = Get-Content -LiteralPath $LogPath
            ($logLines | Select-Object -Last 120) -join [Environment]::NewLine
        } else {
            "Installer log was not created: $LogPath"
        }
        throw "Installer $InstallerPath exited with code $($process.ExitCode).`n$details"
    }
}

function Invoke-InstalledSelfTest {
    param(
        [Parameter(Mandatory)]
        [string]$ExecutablePath
    )

    if (-not (Test-Path -LiteralPath $ExecutablePath)) {
        throw "Installed executable is missing: $ExecutablePath"
    }
    $process = Start-Process -FilePath $ExecutablePath -ArgumentList "--self-test" -Wait -PassThru
    if ($process.ExitCode -ne 0) {
        throw "Installed self-test exited with code $($process.ExitCode): $ExecutablePath"
    }
    $reportPath = Join-Path $DataDir "self-check.json"
    if (-not (Test-Path -LiteralPath $reportPath)) {
        throw "Installed self-test did not create $reportPath"
    }
    $report = Get-Content -Raw -LiteralPath $reportPath | ConvertFrom-Json
    if (-not $report.passed) {
        throw "Installed self-test report did not pass: $reportPath"
    }
}

function Assert-PreservedUserData {
    if (-not (Test-Path -LiteralPath $DataDir -PathType Container)) {
        throw "User data directory was removed: $DataDir"
    }
    $actualSentinel = Get-Content -Raw -LiteralPath $SentinelPath
    if ($actualSentinel -ne $Sentinel) {
        throw "User data sentinel changed: expected $Sentinel, got $actualSentinel"
    }
    if (-not (Test-Path -LiteralPath $DatabasePath -PathType Leaf)) {
        throw "SQLite database was removed: $DatabasePath"
    }

$ReadDatabase = @'
import sys
from pathlib import Path

from reco_box.storage import Database

database_path, test_id, marker = sys.argv[1:4]
room_id = f"upgrade-room-{test_id}"
group_id = f"upgrade-group-{test_id}"
database = Database(Path(database_path))
setting_preserved = database.get_setting("upgrade_sentinel_config") == marker
room_preserved = any(
    item.id == room_id
    and item.url == f"https://example.invalid/reco-box-upgrade-{test_id}"
    and item.streamer_name == "Upgrade Sentinel"
    for item in database.list_rooms()
)
recording_preserved = any(
    item["id"] == group_id
    and item["room_id"] == room_id
    and item["status"] == "completed"
    and item["probe_status"] == "valid"
    and item["codec_summary"] == "upgrade-test"
    for item in database.list_recordings()
)
if not all((setting_preserved, room_preserved, recording_preserved)):
    raise SystemExit(
        "preservation checks failed: "
        f"config={setting_preserved}, room={room_preserved}, "
        f"recording={recording_preserved}"
    )
print("1")
'@
    $count = (& $PythonExe -c $ReadDatabase $DatabasePath $TestId $Sentinel).Trim()
    if ($LASTEXITCODE -ne 0 -or $count -ne "1") {
        throw "SQLite configuration and recording history were not preserved: $count"
    }
    if (-not (Test-Path -LiteralPath (Join-Path $DataDir "self-check.json"))) {
        throw "Self-check report was not preserved in the user data directory"
    }
}

$PreviousInstaller = $PreviousInstallerPath.Trim()
if ([string]::IsNullOrWhiteSpace($PreviousInstaller)) {
    throw "A previous release installer is required for the upgrade test"
}
if (-not (Test-Path -LiteralPath $PreviousInstaller -PathType Leaf)) {
    throw "Previous installer is missing: $PreviousInstaller"
}
$PreviousInstaller = (Get-Item -LiteralPath $PreviousInstaller).FullName
Invoke-SilentInstaller -InstallerPath $PreviousInstaller -InstallPath $Target -LogPath (Join-Path $DataDir "installer-0.2.0.log")
$PreviousExe = Join-Path $Target "RecoBox.exe"
Invoke-InstalledSelfTest -ExecutablePath $PreviousExe

Invoke-SilentInstaller -InstallerPath $Installer -InstallPath $Target -LogPath (Join-Path $DataDir "installer-0.2.1.log")
$Exe = Join-Path $Target "RecoBox.exe"
Invoke-InstalledSelfTest -ExecutablePath $Exe
& pwsh -NoProfile -File $VersionCheckScript -ExecutablePath $Exe -InstallerPath $Installer
if ($LASTEXITCODE -ne 0) {
    throw "Version consistency check failed for the installed application"
}
Assert-PreservedUserData

$Uninstaller = Get-ChildItem -LiteralPath $Target -Filter "unins*.exe" -File -Force |
    Select-Object -First 1
if (-not $Uninstaller) {
    throw "Installer did not create an uninstaller under $Target"
}
$UninstallLogPath = Join-Path $DataDir "uninstaller.log"
$uninstallArguments = '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP- /LOG="' + $UninstallLogPath + '"'
$uninstallProcess = Start-Process -FilePath $Uninstaller.FullName -ArgumentList $uninstallArguments -Wait -PassThru
if ($uninstallProcess.ExitCode -ne 0) {
    throw "Uninstaller exited with code $($uninstallProcess.ExitCode)"
}

$deadline = (Get-Date).AddSeconds(30)
while ((Test-Path -LiteralPath $Target) -and (Get-Date) -lt $deadline) {
    Start-Sleep -Milliseconds 250
}
if (Test-Path -LiteralPath $Target) {
    throw "Uninstaller did not remove the exact install root within 30 seconds: $Target"
}
Assert-PreservedUserData

Write-Output "Installer upgrade/install/uninstall E2E passed: $Version"
Write-Output "Preserved user data: $DataDir"
