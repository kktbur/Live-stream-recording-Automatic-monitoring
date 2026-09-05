# CURRENT

- Last updated: 2026-09-05

- Status: ACTIVE
- Current package version: `0.2.1` (single source: `pyproject.toml`).
- Current maintenance roadmap target: `0.3.0`.
- The latest maintenance record is [PR-12 RecordingSession abstraction](maintenance/2026-09-05-pr-12-recording-session.md).

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
- Final independent Standards/Spec review found no blocking issue. Draft PR
  [#13](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/13)
  remains open/draft, and Windows CI [#39](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33924632389)
  passed the remote Windows build, self-check, installer, and install/upgrade/uninstall gates.
- Error taxonomy, stall detection, RecordingSession, recovery state machine, offline hysteresis,
  crash recovery and pressure/fault injection remain later roadmap tasks.

## Confirmed PR-10 boundary

- `src/reco_box/errors.py` defines separate Resolver and Recording failure hierarchies with stable
  kind values and future recovery directives; the directives are not executed in this PR.
- First-party Bilibili/YouTube adapters preserve their existing offline dictionary contract while
  reporting classified access/limit failures through `ResolvedStream.failure`; the Worker and
  `MonitoringCoordinator` retain the latest structured failure per room.
- Recording and conversion failures retain structured objects; UI, event and database error
  boundaries sanitize URLs, query strings, cookies, authorization headers and credentials. Failed
  conversions are persisted as failed rather than completed.
- HTTP status, HTTPX/Requests timeout, TLS-chain, parse, and unknown Resolver failures have
  deterministic classification; error text is bounded and sensitive details are removed.
- Local PR-10 focused tests are `84 passed`; the full suite is `171 total, 169 passed、2 failed、5 warnings`,
  with the same missing-FFmpeg prerequisite recorded in the PR-10 maintenance record.
- Current branch is `codex/0.3.0-02-error-taxonomy`, local code fixed point `a581da1`; remote Draft PR
  [#14](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/14) is open/draft and
  Windows CI [#41](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33929815223)
  passed all configured stages. Two later independent review agents timed out without a final report, so
  owner acceptance remains open. The next scope after acceptance is `0.3.0-04` Stall Detection.

## Confirmed PR-11 boundary

- `RecordingManager` starts its growth clock from the QProcess `started` signal and only marks a
  still-running process stalled after both the 30-second startup guard and the 120-second no-growth
  threshold; with zero output, the first trigger is therefore about 120 seconds after process start.
- Automatic stall handling enters `RoomStatus.STALLED`, records `Stalled`, sends FFmpeg `q`,
  then uses the existing 8-second terminate and 3-second kill fallbacks; it reuses the existing
  short retry path and does not introduce `RecordingSession` or a recovery state machine.
- Finalization timers are bound to the original QProcess, and process errors during automatic
  finalization do not overwrite `STALLED` before the normal completion/retry path runs.
- Monitoring does not start a second check while a room is `STALLED`; the UI shows “卡顿收尾” and
  disables conflicting edit/delete/check actions while retaining an explicit stop action.
- On application startup, a persisted `STALLED` marker is normalized to `OFFLINE` so an enabled room
  can be monitored again; this guard does not claim full crash recovery.
- Local PR-11 focused tests are `28 passed`; the full suite is `179 total, 177 passed、2 failed、5 warnings`,
  with both failures caused by missing local FFmpeg/ffprobe runtime files.
- Draft PR [#15](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/15) is open/draft,
  with remote implementation head `94caa50f9e56fd8df484127bb0dc39e8e8f51299`; Windows CI [#43](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33935714737)
  succeeded. Its single job and diagnostic artifact are recorded remotely. The follow-up documentation
  head is `ef876a0777578b445322d3aaaff1d8a003edcd6a`, and Windows CI [#44](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33936295055)
  also succeeded. The final independent Standards/Spec review found no P0/P1/P2 issue; owner acceptance
  remains open.
- The next strictly ordered scope after PR-11 is `0.3.0-05` RecordingSession.

## Confirmed PR-12 boundary

- `RecordingSession` represents one logical livestream occurrence independently
  of any single FFmpeg process. It carries the session identity, room, start
  time, stable output directory, attempt, lifecycle state, and recovery reason.
- Schema version 7 adds a dedicated `recording_sessions` table and a small
  database interface for create, upsert, fetch, and room-filtered listing.
- `last_stream_url` is an in-memory-only field and is excluded from model
  serialization and SQLite persistence because resolved playback addresses are
  transient and sensitive.
- `SessionPathPlanner` and `FFmpegPlanner.build_for_session(...)` establish a
  caller-owned directory seam; the existing `FFmpegPlanner.build(...)` path and
  `RecordingManager` behavior are unchanged in this PR.
- Same-session recovery, attempt-specific output numbering, state-machine
  transitions, and stale-session repair remain later roadmap tasks.
- The final independent Standards/Spec review of PR-12 found no P0-P2 or
  other actionable issue. Draft PR [#16](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/16)
  is open/draft at head `7400697d439484311da0860eec69be8229bac7d6`; Windows CI
  [#45](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33938312883)
  passed its single job, including Windows build, installer, and install/upgrade/uninstall smoke.
  The diagnostic artifact is retained until 2026-09-12; owner acceptance remains open.

