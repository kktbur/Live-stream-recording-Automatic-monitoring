import os
from pathlib import Path

import PySide6
from PyInstaller.utils.hooks import copy_metadata

PACKAGING_DIR = Path(SPECPATH).resolve()
PROJECT_DIR = PACKAGING_DIR.parent
UPSTREAM_DIR = PROJECT_DIR / "vendor" / "DouyinLiveRecorder"
PYSIDE_DIR = Path(PySide6.__file__).resolve().parent
MULTIMEDIA_PLUGIN_DIR = PYSIDE_DIR / "plugins" / "multimedia"

datas = [
    (str(PROJECT_DIR / "assets"), "assets"),
    (str(PROJECT_DIR / "src" / "reco_box" / "ui"), "reco_box/ui"),
    (str(PROJECT_DIR / "src" / "reco_box" / "translations"), "reco_box/translations"),
    (str(UPSTREAM_DIR / "src"), "vendor/DouyinLiveRecorder/src"),
    (str(UPSTREAM_DIR / "LICENSE"), "vendor/DouyinLiveRecorder"),
    *copy_metadata("reco-box"),
]

version_file = os.environ.get("RECO_BOX_VERSION_FILE")
if version_file:
    version_file = str(Path(version_file).resolve())

hiddenimports = [
    "Crypto.Cipher.AES",
    "Crypto.Util.Padding",
    "distro",
    "execjs",
    "httpx",
    "loguru",
    "requests",
    "tqdm",
]

# PyInstaller's PySide6 hook currently collects QtMultimedia itself but can
# omit the actual Windows playback backends. Without these DLLs MediaPlayer
# opens normally yet renders a permanently black video surface.
binaries = [
    (str(MULTIMEDIA_PLUGIN_DIR / "ffmpegmediaplugin.dll"), "PySide6/plugins/multimedia"),
    (str(MULTIMEDIA_PLUGIN_DIR / "windowsmediaplugin.dll"), "PySide6/plugins/multimedia"),
]

a = Analysis(
    [str(PACKAGING_DIR / "entrypoint.py")],
    pathex=[str(PROJECT_DIR / "src")],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter"],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="RecoBox",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    version=version_file,
    # Keep the unsigned Windows build conservative: UPX can increase
    # antivirus false positives and provides little value for this bundle.
    upx=False,
    console=False,
    icon=str(PROJECT_DIR / "assets" / "reco-box.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="Reco Box",
)
