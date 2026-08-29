# Reco Box 0.2.0

## Existing stable platforms

Douyin, Kuaishou, Bilibili, Xiaohongshu, TikTok, YouTube, and JD retain their
existing anonymous monitoring and recording paths. Taobao remains disabled
because the pinned resolver requires an authenticated session.

## New Beta platform adapters

Twitch, SOOP Global, CHZZK, TwitCasting, SHOWROOM, BIGO LIVE, 17LIVE, LiveMe,
Picarto, and Shopee Live now have anonymous-only adapters. Restricted content
is never logged into and no account or cookie is imported. These adapters must
pass the live validation gate in `docs/platform-validation-0.2.0.md` before this
release is published.

## Internationalization and networking

- Ten complete Qt UI catalogs and ten complete README languages.
- Immediate language switching for the main UI, dialogs, status text, and tray.
- Ten-language Inno Setup installer.
- Persistent global default proxy and per-room proxy override.
- Credential-free HTTP/HTTPS proxy validation and FFmpeg proxy forwarding.
- Verified minimal Node.js v24.20.0 LTS runtime for LiveMe.

## Compatibility and verification

- Existing databases and recording data are preserved.
- Stable business values remain independent from translated labels.
- CI verifies all catalogs and README navigation, tests domain spoofing, and
  downloads pinned FFmpeg and Node.js archives by SHA-256.
- Final local result: Ruff passed, 65 tests passed, packaged self-test passed,
  and isolated installer self-test passed.

Release assets, once the live validation gate passes:

- `RecoBox-Setup-0.2.0.exe`
- `RecoBox-Setup-0.2.0.exe.sha256.txt`
