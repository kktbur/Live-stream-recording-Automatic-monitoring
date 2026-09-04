$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $PSScriptRoot
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"
$VersionScript = Join-Path $ProjectDir "tools\project_version.py"
$SpecFile = Join-Path $PSScriptRoot "reco_box.spec"
$BuildDir = Join-Path $ProjectDir "build"
$DistDir = Join-Path $ProjectDir "dist"
$SourceDir = Join-Path $ProjectDir "src"
$VersionInfoTemplate = Join-Path $PSScriptRoot "version_info.txt.in"
$VersionInfoFile = Join-Path $BuildDir "version_info.txt"

if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "Project virtual environment is missing: $PythonExe"
}
if (-not (Test-Path -LiteralPath $VersionScript)) {
    throw "Project version reader is missing: $VersionScript"
}
if (-not (Test-Path -LiteralPath $VersionInfoTemplate)) {
    throw "PyInstaller version template is missing: $VersionInfoTemplate"
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
    throw "PyInstaller Windows metadata requires a three-part numeric version: $Version"
}
$VersionPartsText = "$($VersionParts[0]), $($VersionParts[1]), $($VersionParts[2]), 0"
New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null
$VersionInfo = Get-Content -Raw -LiteralPath $VersionInfoTemplate
$VersionInfo = $VersionInfo.Replace("@VERSION_PARTS@", $VersionPartsText).Replace("@VERSION@", $Version)
[IO.File]::WriteAllText($VersionInfoFile, $VersionInfo, [Text.UTF8Encoding]::new($false))

$PreviousPythonPath = $env:PYTHONPATH
$PreviousPath = $env:PATH
$PreviousVersionFile = $env:RECO_BOX_VERSION_FILE
$env:PYTHONPATH = if ($PreviousPythonPath) {
    "$SourceDir$([IO.Path]::PathSeparator)$PreviousPythonPath"
} else {
    $SourceDir
}
$env:PATH = @(
    (Split-Path -Parent $PythonExe),
    (Join-Path $env:SystemRoot "System32"),
    $env:SystemRoot
) -join [IO.Path]::PathSeparator
$env:RECO_BOX_VERSION_FILE = $VersionInfoFile

try {
    & $PythonExe -m PyInstaller --noconfirm --clean --workpath $BuildDir --distpath $DistDir $SpecFile
} finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PATH = $PreviousPath
    if ($null -eq $PreviousVersionFile) {
        Remove-Item Env:RECO_BOX_VERSION_FILE -ErrorAction SilentlyContinue
    } else {
        $env:RECO_BOX_VERSION_FILE = $PreviousVersionFile
    }
}
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed with exit code $LASTEXITCODE"
}

$ExePath = Join-Path $DistDir "Reco Box\RecoBox.exe"
if (-not (Test-Path -LiteralPath $ExePath)) {
    throw "Packaged executable was not created: $ExePath"
}

# Keep Windows/Qt runtime resolution deterministic.  PyInstaller can collect
# ICU, API-MS, UCRT and MSVC compatibility DLLs from the build environment at
# the application root.  Those files can override the ABI-matched copies
# shipped under PySide6 and make Qt6Core.dll fail with a missing ICU symbol
# (for example UCNV_TO_U_CALLBACK_SUBSTITUTE).  The known-good distribution
# keeps the PySide6 copies in their own directory and retains only the app's
# normal VCRUNTIME files at the root.
$InternalDir = Join-Path $DistDir "Reco Box\_internal"
$ConflictingRuntimePatterns = @(
    "icu*.dll",
    "api-ms-win-*.dll",
    "ucrtbase.dll",
    "MSVCP140*.dll"
)
$RemovedRuntimeFiles = foreach ($Pattern in $ConflictingRuntimePatterns) {
    Get-ChildItem -LiteralPath $InternalDir -File -Filter $Pattern -ErrorAction SilentlyContinue |
        Where-Object { $_.DirectoryName -eq $InternalDir } |
        ForEach-Object {
            $RemovedName = $_.Name
            Remove-Item -LiteralPath $_.FullName -Force
            $RemovedName
        }
}
if ($RemovedRuntimeFiles) {
    Write-Output ("Removed conflicting root runtime DLLs: " + ($RemovedRuntimeFiles -join ", "))
}

# Keep the recorder FFmpeg runtime outside PyInstaller dependency analysis.
# Qt Multimedia ships a different ABI-matched FFmpeg set; analyzing both sets
# together can copy unrelated system DLLs into the application root.
$RuntimeSource = Join-Path $ProjectDir "runtime\ffmpeg"
$RuntimeDestination = Join-Path $DistDir "Reco Box\_internal\runtime\ffmpeg"
New-Item -ItemType Directory -Path $RuntimeDestination -Force | Out-Null
Get-ChildItem -LiteralPath $RuntimeSource -File |
    Copy-Item -Destination $RuntimeDestination -Force

$NodeSource = Join-Path $ProjectDir "runtime\node"
$NodeDestination = Join-Path $DistDir "Reco Box\_internal\runtime\node"
if (-not (Test-Path -LiteralPath (Join-Path $NodeSource "node.exe"))) {
    throw "Node.js runtime is missing: $NodeSource\node.exe"
}
New-Item -ItemType Directory -Path $NodeDestination -Force | Out-Null
Get-ChildItem -LiteralPath $NodeSource -File |
    Copy-Item -Destination $NodeDestination -Force

$MediaBackend = Join-Path $DistDir "Reco Box\_internal\PySide6\plugins\multimedia\ffmpegmediaplugin.dll"
if (-not (Test-Path -LiteralPath $MediaBackend)) {
    throw "Qt FFmpeg multimedia backend was not packaged: $MediaBackend"
}

Write-Output $ExePath
