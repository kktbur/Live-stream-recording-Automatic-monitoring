# CI FFmpeg source fix — 2026-09-22

Status: **implemented; awaiting the new Windows CI run**.

## Scope

This maintenance slice fixes the Windows CI dependency download. It does not change
Reco Box production code, package contents, the release version, or the Task 14/15
validation status.

## Failure evidence

Windows CI run `#51` (`35686886609`) failed in `Prepare verified FFmpeg runtime`.
The pinned BtbN asset URL returned HTTP `404 Not Found`, so tests, packaging, and
the packaged self-check were not reached.

## Replacement binding

- Source: [BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds).
- Release: `autobuild-2026-08-31-13-27`.
- Asset: `ffmpeg-n9.0.1-11-ge47273f4d9-win64-lgpl-shared-9.0.zip`.
- URL: `https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2026-08-31-13-27/ffmpeg-n9.0.1-11-ge47273f4d9-win64-lgpl-shared-9.0.zip`.
- SHA-256 from the release `checksums.sha256`: `83a824f0729a69d143c9865125bb86988a11dd388325f0033711045522068aa0`.
- Pre-commit availability check: HTTP `200`, content length `67,201,333` bytes.

The workflow continues to download the archive, calculate its SHA-256, fail closed
on mismatch, extract it, and require `ffmpeg.exe` before later CI steps run.

## Verification boundary

- Local change is limited to `.github/workflows/ci.yml` plus this maintenance record.
- The next Windows CI run must reach the FFmpeg preparation step successfully before
  its test/build results can be evaluated.
- No `main` merge, tag, or formal Release is included.
