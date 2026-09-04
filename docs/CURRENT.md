# CURRENT

- Status: ACTIVE
- Current package version: `0.2.1` (single source: `pyproject.toml`).
- Current maintenance roadmap target: `0.2.2`.
- The latest maintenance record is [PR-07 Bilibili first-party TLS migration](maintenance/2026-09-05-pr-07-bilibili-tls.md).

## Confirmed PR-06 boundary

- The repository contains a matrix for all 18 exposed `Platform` enum entries.
- Reco Box-owned TwitCasting anonymous page and streamserver requests use an
  explicit verified-by-default policy.
- Compatibility overrides are restricted to platform plus exact Host.
- Other platforms still use the pinned upstream async helper's unverified
  default until their own compatibility evidence and migration are completed.
- The first phase does not close GitHub Issue #1 by itself.

## Confirmed PR-07 boundary

- `src/reco_box/bilibili.py` now owns the anonymous Bilibili metadata and playback API
  requests that previously used the pinned upstream shared helper.
- The Bilibili client passes the first-party network policy, proxy, HTTP/2 and redirect
  settings explicitly; the default policy verifies `api.live.bilibili.com`.
- The adapter has no Cookie or account-credential input and does not log dynamic CDN URLs.
- Offline protocol tests cover legacy and modern playback paths, quality selection,
  proxy forwarding, short-link redirects, anonymous-access errors and exact-host TLS policy behavior.
- Public-room network and short-recording validation remain outstanding; PR-07 does not
  close Issue #1 globally.

For the active branch, commit, CI, and recovery snapshot, use the linked
maintenance record and the pull request description rather than inferring state
from this durable product document.
