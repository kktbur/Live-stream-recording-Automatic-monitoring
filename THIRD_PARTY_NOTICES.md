# Third-party notices

Reco Box is MIT-licensed, but the installer contains or uses third-party
components under their own licenses. Those licenses remain controlling for
the corresponding components.

## DouyinLiveRecorder v4.0.7 resolver source

- Project: https://github.com/ihmily/DouyinLiveRecorder
- Copyright: 2025 Hmily
- License: MIT
- Included path: `vendor/DouyinLiveRecorder`
- License text: `vendor/DouyinLiveRecorder/LICENSE`

Reco Box uses a pinned, anonymous-only adapter and does not import platform
account cookies.

## FFmpeg 9.0.1 LGPL shared build

- Project: https://ffmpeg.org/
- Windows build provider: https://github.com/BtbN/FFmpeg-Builds
- Binary family: `ffmpeg-n9.0-latest-win64-lgpl-shared-9.0.zip`
- Build date used for 0.1.3: 2026-08-28
- FFmpeg commit: `e47273f4d9227152dcbf543cebaf9e2430ddbcc4`
- License: GNU Lesser General Public License version 3 or later
- Binary archive SHA-256: `939f64da0f77a21837a17928afcf25a32280e16269fe0732bbfbe2d2bbc83086`
- Corresponding FFmpeg source: https://github.com/FFmpeg/FFmpeg/archive/e47273f4d9227152dcbf543cebaf9e2430ddbcc4.zip
- Build scripts: https://github.com/BtbN/FFmpeg-Builds
- Bundled license text: `runtime/ffmpeg/LICENSE.txt`

The installer keeps FFmpeg as separately invoked executables and shared DLLs.
The full FFmpeg configure line is available from `ffmpeg -version`.

## Python and Qt components

The frozen application also contains Python packages listed in
`pyproject.toml`/`uv.lock`, including PySide6 (Qt for Python), platformdirs,
requests, Loguru, PyCryptodome, distro, tqdm, httpx and PyExecJS. Each package
is redistributed under its own upstream license. PySide6/Qt is dynamically
packaged by PyInstaller and is subject to the applicable Qt for Python and Qt
open-source license terms.

## Inno Setup

The Windows installer is produced with Inno Setup. Inno Setup is a build tool
and is not included as a runtime component. See https://jrsoftware.org/isinfo.php
for its license and trademark information.
