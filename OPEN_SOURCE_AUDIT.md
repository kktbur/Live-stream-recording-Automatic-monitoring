# Open-source publication audit

Audit date: 2026-08-29

## Publication boundary

Included: application source, tests, UI assets, packaging scripts, pinned
DouyinLiveRecorder resolver source and license, documentation, and third-party
notices.

Excluded: `.venv`, build output, installers in Git history, local databases,
recording history, runtime logs, import backups/reports, cookies, credentials,
platform tokens, recordings and user configuration.

## Privacy and secret scan

- No real access token, API key, private key, email address, Windows user path,
  installed-software path or imported room list was found in the publication
  set.
- A fake Cookie string remains in a unit test solely to prove that the legacy
  importer discards credentials. It is not a real credential.
- Numeric live-room URLs in tests and UI rendering tools are non-user example
  values.
- The vendored upstream resolver contains public, upstream-supplied request
  cookies and client constants used to emulate anonymous web requests. They
  are already present in the public DouyinLiveRecorder source and are not the
  Reco Box user's cookies, imported accounts, or private configuration.
- The previous 0.1.2 installer was scanned for the local Windows username,
  project path, installation path and test-cookie marker; none was found.

## Release hardening

- The old GPL-enabled FFmpeg runtime is not used for the public build.
- Version 0.1.3 uses a SHA-256-verified LGPL shared FFmpeg build and carries its
  license/source details.
- The installer is not code-signed. Windows SmartScreen may therefore show an
  unknown-publisher warning; users must verify the published SHA-256 checksum.
- Final 0.1.3 installer SHA-256:
  `00CD2D11F6ED84C6D5B91C0E06DD3DA24F742C43907DE1E88AA65C7C15920219`.
- The application is an early Windows beta and platform-side changes can break
  anonymous stream resolution without notice.

## Resolver provenance and transport note

- The version-controlled `vendor/DouyinLiveRecorder/LICENSE` and `src/` files
  (20 files total) were compared file by file using Git Blob SHA against the
  official annotated `v4.0.7` tag, commit
  `fec734ae74aabef862996177a78c3e8cc1dcc7ee`; differences: 0. Audit date:
  2026-08-29.
- The resolver's main asynchronous requests currently pass `verify=False` by
  default in `src/http_clients/async_http.py`. The unused `ssl_context` objects
  in `spider.py` and `sync_http.py` are not the effective call path. This is an
  inherited compatibility risk and is disclosed in `README.md` and `PRIVACY.md`.
- The source logo retained an Adobe XMP metadata block in the 0.1.3 release;
  it contains editing timestamps and document identifiers but no user path or
  account identifier. The 0.1.4 source asset removes that unnecessary metadata.
