# CURRENT

- Last updated: 2026-09-05

- Status: ACTIVE
- Current package version: `0.2.1` (single source: `pyproject.toml`).
- Current maintenance roadmap target: `0.3.0`.
- The latest maintenance record is [PR-09 Resolver scheduling and limits](maintenance/2026-09-05-pr-09-scheduler.md).

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
- The local implementation and focused tests are complete. Draft PR [#12](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/12)
  remains open/draft, and Windows CI [#36](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33914674544)
  passed the remote validation stages. A corrected follow-up independent review did not
  return a final report; public-room/CDN reachability and short-recording validation also
  remain outstanding. PR-08 does not close Issue #1 globally.

## Confirmed PR-09 boundary

- `src/reco_box/scheduler.py` calculates per-room deadlines with injectable `0.9..1.1`
  jitter, uses 5→10→20→40→60 second Resolver backoff with a final 60-second cap, and keeps
  caller-selected recording delays explicit.
- `src/reco_box/rate_limit.py` provides a configurable global Resolver limit (default 4),
  platform concurrency (default 1), and platform cooldown (default 1 second), with explicit
  acquisition and release state. The existing global settings page persists the three values
  within validated ranges and applies changes to new monitoring requests immediately.
- `MonitoringCoordinator` uses an independent Resolver `QThreadPool`; it does not change the
  global Qt pool used by recording and conversion work.
- Local focused tests are `27 passed`; the full suite is `142 passed、2 failed、5 warnings`,
  with the same missing-FFmpeg prerequisite recorded in the PR-09 maintenance record.
- Error taxonomy, stall detection, RecordingSession, recovery state machine, offline hysteresis,
  crash recovery and pressure/fault injection remain later roadmap tasks.
