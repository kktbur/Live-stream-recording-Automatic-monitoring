# Reco Box

[简体中文](README.md) | [繁體中文](README.zh-TW.md) | [English](README.en.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt.md) | [Русский](README.ru.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

Reco Box is a local Windows x64 application for automatic livestream monitoring and recording. It provides a card-based desktop UI, batch controls, segmented recording, MP4 remuxing, history, logs, a system tray, and one-click legacy configuration import. Current version: `0.2.0`. No Reco Box or platform account is required, and cookies are never stored.

## Download and installation

Download `RecoBox-Setup-0.2.0.exe` and its `.sha256.txt` file from Releases. The installer is unsigned, so SmartScreen may show an unknown publisher warning. It bundles a verified minimal Node.js v24.20.0 LTS runtime for LiveMe; users do not need to install Node.js.

## Platforms

Existing platforms: Douyin, Kuaishou, Bilibili, Xiaohongshu, TikTok, YouTube, and JD. Taobao remains disabled because the pinned resolver requires an authenticated session.

New Beta platforms: Twitch, SOOP Global, CHZZK, TwitCasting, SHOWROOM, BIGO LIVE, 17LIVE, LiveMe, Picarto, and Shopee Live. Beta means the adapter exists but must still pass public live/offline, stream URL, and short recording checks before release. Restricted rooms return an anonymous-access error and never trigger login. Kick, Facebook Live, and Instagram Live are intentionally out of scope.

## Recording, proxy, and languages

- Segmentation is off by default. When enabled, files are numbered 1, 2, 3… and the last segment keeps its actual duration.
- Output layout: `streamer / YYYYMMDD / session start time / video`. TS may be losslessly remuxed to MP4 after recording.
- A global proxy is inherited only by new rooms; each room may override it. Only credential-free HTTP/HTTPS proxies are accepted. The proxy is passed to both the resolver and FFmpeg and is never written to logs.
- The settings page switches all ten UI languages immediately without restarting. Fresh installs follow a supported Windows language; upgraded databases default to Simplified Chinese; a manual choice is persisted.

## Privacy and security

The database, logs, and settings remain local, and recordings are written only to the selected folder. Some pinned upstream resolver requests disable TLS certificate verification, which increases man-in-the-middle risk; use a trusted network. See [PRIVACY.md](PRIVACY.md), [SECURITY.md](SECURITY.md), and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Run and build from source

Requires Windows x64, Python 3.12, and PowerShell 7. Install `.[dev]`, prepare `runtime/ffmpeg`, and run `pwsh -NoProfile -File tools/prepare_node.ps1` for LiveMe. Run `pytest tests -q`; then use `packaging/build.ps1` and `packaging/build_installer.ps1`. FFmpeg and Node.js binaries are not committed to Git.

## Roadmap

- Restore TLS verification where compatible
- Improve Xiaohongshu, TikTok, and overseas Beta stability
- Add automatic update checking
- Improve recording recovery after interruptions
- Add anonymous public platforms
- Improve Windows signing, packaging, and CI

## Contributing, license, and disclaimer

See [CONTRIBUTING.md](CONTRIBUTING.md) for Issues, PRs, broken-platform reports, and new adapters. First-party code uses the [MIT License](LICENSE). Record only content you are authorized to save and comply with platform terms, copyright, privacy, and local law.
