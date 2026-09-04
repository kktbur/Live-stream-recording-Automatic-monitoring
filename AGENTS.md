# Reco Box repository instructions

## Scope and safety

- Reco Box is a local Windows x64 livestream monitoring and recording application.
- Platform access is anonymous-only. Do not add account login, cookies, tokens,
  notification secrets, or proxy credentials to source, tests, documentation,
  logs, screenshots, or fixtures.
- Do not bypass paywalls, age gates, region restrictions, private rooms, or
  login requirements. Keep the Taobao boundary disabled until an anonymous
  public path is available.
- Do not commit FFmpeg, Node.js, installer outputs, or transient signed media
  URLs. Record third-party runtime sources and checksums in the existing audit
  documentation.

## Engineering workflow

- Use PowerShell 7 (`pwsh -NoProfile`) for Windows scripts and verification.
- Keep the project version in `pyproject.toml` as the single direct version
  input; update `uv.lock` when the version changes.
- Use the repository's existing tests and tools before adding new infrastructure.
  Run the relevant pytest tests, Ruff, and `git diff --check` for every change.
- Keep network security changes platform-scoped. TLS compatibility exceptions
  must name the platform, exact Host, reason, and a regression test; never add a
  global certificate-verification bypass.
- Preserve anonymous behavior and existing proxy semantics when changing a
  resolver. Do not log transient playback URLs.

## Documentation and release boundary

- Keep `docs/INDEX.md`, `PRODUCT.md`, `ACCEPTANCE.md`, `CURRENT.md`, and
  `CODEMAP.md` synchronized with material repository changes.
- Record substantial maintenance work under `docs/maintenance/` and durable
  engineering decisions under `docs/decisions/`.
- Pull requests must remain independently reviewable. Do not merge, tag, or
  publish a formal Release without explicit maintainer approval and direct
  evidence for that operation.
