# CURRENT

- Last updated: 2026-09-05

- Status: ACTIVE
- Current package version: `0.2.1` (single source: `pyproject.toml`).
- Current maintenance roadmap target: `0.2.2`.
- The latest maintenance record is [PR-08 YouTube first-party TLS migration](maintenance/2026-09-05-pr-08-youtube-tls.md).

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
  proxy forwarding, short-link redirects, HTTP/anonymous-access errors and exact-host TLS policy behavior.
- Expected anonymous request failures retain the upstream public contract and normalize to an
  offline result; detailed retry/error taxonomy remains a later reliability-stage change.
- The latest independent Standards/Spec review found no remaining hard issue; public-room,
  dynamic-CDN and short-recording validation remain explicitly outstanding.
- Draft PR [#11](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/11)
  is open/draft and Windows CI [#33](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33908466198)
  passed the remote Windows validation stages; the PR remains unmerged.
- Public-room network and short-recording validation remain outstanding; PR-07 does not
  close Issue #1 globally.

For the active branch, commit, CI, and recovery snapshot, use the linked
maintenance record and the pull request description rather than inferring state
from this durable product document.

## Confirmed PR-08 boundary

- `src/reco_box/youtube.py` now owns the anonymous YouTube page and HLS manifest
  requests that previously used the pinned upstream shared helper.
- The YouTube client passes the first-party network policy, proxy, HTTP/2 and
  manual redirect settings explicitly; the default policy verifies each request.
- YouTube page redirects are restricted to YouTube Hosts, manifest and variant
  URLs must use HTTP(S), and the adapter has no Cookie or account-credential input.
- Offline protocol tests cover live/offline page responses, HLS bandwidth ordering,
  quality selection, `youtu.be` redirects, per-hop TLS policy, anonymous HTTP
  failures and malformed responses.
- The local implementation and focused tests are complete; independent review,
  Draft PR, Windows CI, public-room/CDN reachability and short-recording validation
  remain outstanding. PR-08 does not close Issue #1 globally.
