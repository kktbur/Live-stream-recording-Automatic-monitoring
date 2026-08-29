$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $PSScriptRoot
$PythonExe = Join-Path $ProjectDir ".venv\Scripts\python.exe"
$SpecFile = Join-Path $PSScriptRoot "reco_box.spec"
$BuildDir = Join-Path $ProjectDir "build"
$DistDir = Join-Path $ProjectDir "dist"
$SourceDir = Join-Path $ProjectDir "src"

if (-not (Test-Path -LiteralPath $PythonExe)) {
    throw "Project virtual environment is missing: $PythonExe"
}

$PreviousPythonPath = $env:PYTHONPATH
$PreviousPath = $env:PATH
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

try {
    & $PythonExe -m PyInstaller --noconfirm --clean --workpath $BuildDir --distpath $DistDir $SpecFile
} finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PATH = $PreviousPath
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
