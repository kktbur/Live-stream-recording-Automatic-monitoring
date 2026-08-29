$ErrorActionPreference = "Stop"

$ProjectDir = Split-Path -Parent $PSScriptRoot
$Archive = Join-Path $ProjectDir "artifacts\node-v24.20.0-win-x64.zip"
$Extract = Join-Path $ProjectDir "artifacts\node-v24.20.0-win-x64"
$Runtime = Join-Path $ProjectDir "runtime\node"
$ExpectedHash = "6cac9ffbca8f6a47091e4b5c772e0606049c3871cb67d900c0cedde630e545ba"

New-Item -ItemType Directory -Force -Path (Split-Path $Archive), $Runtime | Out-Null
Invoke-WebRequest -Uri "https://nodejs.org/dist/v24.20.0/node-v24.20.0-win-x64.zip" -OutFile $Archive
$ActualHash = (Get-FileHash -LiteralPath $Archive -Algorithm SHA256).Hash.ToLowerInvariant()
if ($ActualHash -ne $ExpectedHash) {
    throw "Node.js archive SHA-256 mismatch: $ActualHash"
}
Expand-Archive -LiteralPath $Archive -DestinationPath $Extract -Force
$Source = Join-Path $Extract "node-v24.20.0-win-x64"
Copy-Item -LiteralPath (Join-Path $Source "node.exe") -Destination $Runtime -Force
Copy-Item -LiteralPath (Join-Path $Source "LICENSE") -Destination (Join-Path $Runtime "LICENSE.txt") -Force
& (Join-Path $Runtime "node.exe") --version
