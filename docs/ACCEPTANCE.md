# ACCEPTANCE

## Repository maintenance minimums

1. State the target repository, current and target version, scope, and recovery
   point before changing code.
2. Keep changes anonymous-only and free of credentials, cookies, transient
   playback URLs, and unreviewed binary assets.
3. Add focused regression coverage for behavior changes and run the relevant
   full or filtered test suite with the limitation recorded.
4. Run Ruff and `git diff --check`; use the Windows CI result for checks that
   depend on omitted runtime assets or Windows-only packaging.
5. Keep README, PRIVACY, audit records, and maintenance records consistent with
   the actual completion state.
6. Do not call a Draft PR, Tag, formal Release, or merge a completion result
   without direct evidence for that operation.

## TLS changes

TLS compatibility exceptions must be explicit and narrow: platform, exact Host,
reason, and regression test. A static endpoint inventory is not a substitute
for platform-by-platform certificate-compatibility evidence.

## PR-07 current acceptance

- Scope: Bilibili only; the package version remains `0.2.1`.
- First-party request code: `src/reco_box/bilibili.py` uses explicit HTTPX TLS policy,
  proxy, HTTP/2 and redirect settings without account credentials or Cookie.
- Local evidence: 29 focused tests passed; the full suite has 103 passed and 2
  prerequisite-dependent failures; Ruff, compileall and `git diff --check` passed.
- Independent Standards/Spec review at the latest fixed point found no remaining hard
  implementation or specification issue.
- Remote Draft PR [#11](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/11)
  is open/draft. Windows CI [#33](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33908466198)
  passed tests, Windows build, packaged self-check, ten-language installer build, and
  installer install/upgrade/uninstall smoke; its diagnostic artifact is retained for seven days.
- Limitation: the focused suite uses an injected offline client. It does not establish
  current public-room availability, dynamic CDN reachability or a short recording.
- Release boundary: no merge, Tag, formal Release or `main` modification is part of PR-07.

## PR-08 current acceptance

- Scope: YouTube page and HLS manifest requests only; the package version remains
  `0.2.1`.
- First-party request code: `src/reco_box/youtube.py` uses explicit HTTPX TLS policy,
  proxy, HTTP/2 and manual redirect settings without account credentials or Cookie.
- Local evidence: 31 focused tests passed; the full suite has 116 passed and 2
  prerequisite-dependent failures; Ruff, compileall and `git diff --check` passed.
- Protocol boundaries: YouTube page Hosts are enforced across redirects, manifest
  and variant URLs require HTTP(S), and the existing quality index is preserved.
- Remote Draft PR [#12](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/12)
  is open/draft. Windows CI [#36](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33914674544)
  passed lockfile checks, tests, Windows build, packaged self-check, ten-language installer
  build, and installer install/upgrade/uninstall smoke; the diagnostics artifact is retained
  for seven days.
- Limitation: the focused suite uses an injected offline client. It does not establish
  current public-room availability, dynamic CDN reachability, or a short recording.
- A corrected follow-up Standards/Spec review did not return a final report, so independent
  review remains open for maintainer acceptance.
- Release boundary: no merge, Tag, formal Release or `main` modification is part of PR-08.

## PR-09 current acceptance

- Scope: 0.3.0-01 Resolver scheduling only; the package version remains `0.2.1`.
- `MonitoringCoordinator` uses an independent Resolver `QThreadPool` with default maximum
  thread count 4; the Qt global pool remains untouched.
- `ResolverRateLimiter` enforces configurable global concurrency, per-platform concurrency,
  and per-platform cooldown; the defaults are 4, 1, and 1 second respectively. The existing
  global settings page persists these three values with validation ranges of 1–32, 1–16, and
  0–3600 seconds, and applies saved changes to new monitoring requests immediately.
- `MonitoringScheduler` applies injectable `0.9..1.1` jitter to successful checks and Resolver
  retries, uses 5→10→20→40→60 second backoff with a final 60-second cap, and leaves
  recording-provided delays unjittered and uncapped.
- Local evidence: 27 focused tests passed; the full suite has 142 passed and 2 known
  FFmpeg-prerequisite failures; Ruff, compileall, and `git diff --check` passed.
- Limitation: no 100-room pressure test, real platform rate-limit measurement, error taxonomy,
  stall recovery, RecordingSession, or crash recovery is claimed by this PR.
- Final independent Standards/Spec review found no blocking issue. Draft PR
  [#13](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/13)
  is open/draft, and Windows CI [#39](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33924632389)
  passed the remote Windows validation stages, including installer install/upgrade/uninstall smoke.
- The UI evidence screenshot is [PR-09 settings dialog](maintenance/assets/pr-09-settings-dialog.png);
  it uses synthetic data and contains no credentials or real playback URL.
- Release boundary: no merge, Tag, formal Release, or `main` modification is part of PR-09.

## PR-10 current acceptance

- Scope: `0.3.0-03` Resolver and Recording error taxonomy; the package version remains `0.2.1`.
- `src/reco_box/errors.py` defines the planned Resolver and Recording failure types, stable kind
  values, safe error text, and future recovery directives without applying a new retry policy.
- Bilibili/YouTube preserve their offline result dictionaries while reporting structured failures
  through `ResolvedStream.failure`; RecordingManager, UI, events and database boundaries retain
  classified failures and sanitize sensitive error text.
- Failed conversions are persisted with status `failed`; compatibility `ConversionResult` values
  without a failure object are classified at the RecordingManager boundary.
- Focused taxonomy/monitor/recording/Resolver/storage tests are `84 passed`; the full suite is
  `171 total, 169 passed、2 failed、5 warnings`.
  The two failures depend on the local missing `runtime/ffmpeg/ffmpeg.exe` prerequisite.
- `ruff check src tests`, compileall, and `git diff --check` passed. Draft PR [#14](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/14)
  is open/draft, and Windows CI [#41](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33929815223)
  passed the configured lockfile, test, build, self-check, installer, and diagnostics stages. The later
  independent review agents timed out without a final report; owner acceptance remains open.
- Explicit non-goals: no change to PR-09 retry timing, no stall detection, RecordingSession,
  recovery state machine, offline hysteresis, crash recovery, or pressure/fault injection.

## PR-11 current acceptance

- Scope: `0.3.0-04` Stall Detection; the package version remains `0.2.1`.
- The file-growth watchdog starts timing on the QProcess `started` signal, requires a Running FFmpeg
  process, applies a 30-second startup guard, and triggers only when the 120-second no-growth threshold
  is also reached; with zero output, the first trigger is about 120 seconds after process start.
- Trigger handling records `Stalled`, changes the room to `STALLED`, writes `q`, and retains the
  existing terminate/kill fallback and short retry path. Finalization callbacks are bound to the
  original QProcess, and process errors during that finalization retain `STALLED`. It does not claim
  a new recovery state machine.
- `STALLED` is excluded from duplicate monitoring starts; UI status, filtering and conflicting-action
  guards are covered. Persisted `STALLED` is normalized to `OFFLINE` on startup, and all nine
  non-Chinese translation TS/QM catalogs are aligned.
- Local evidence: 28 focused tests passed; the full suite has `179 total, 177 passed、2 failed、5 warnings`.
  The two known failures require local `runtime/ffmpeg/ffmpeg.exe` and `ffprobe.exe` files.
- `ruff check src tests`, compileall, and `git diff --check` passed. Draft PR [#15](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/15)
  is open/draft and Windows CI [#43](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33935714737)
  succeeded; its single job and diagnostic artifact are recorded remotely. The documentation follow-up
  head `ef876a0777578b445322d3aaaff1d8a003edcd6a` also passed Windows CI [#44](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33936295055).
  The final independent Standards/Spec review found no P0/P1/P2 issue, and owner acceptance remains pending.
- Explicit non-goals: no `RecordingSession`, same-session recovery, recovery state machine, offline
  hysteresis, crash recovery, or pressure/fault injection.

## PR-12 current acceptance

- Scope: `0.3.0-05` RecordingSession; the package version remains `0.2.1`.
- `RecordingSession` is the logical broadcast identity and is distinct from an
  individual FFmpeg attempt. Its durable fields are session ID, room ID, start
  time, stable session directory, attempt, state, and safe recovery reason.
- Schema version 7 adds a dedicated session table and database round-trip methods.
  Existing `recordings` history and `RecordingManager` behavior are not migrated
  or changed in this PR.
- `last_stream_url` remains memory-only and is deliberately excluded from
  serialization and SQLite. This preserves the repository rule that transient
  playback addresses are never persisted or logged.
- `SessionPathPlanner` owns directory selection; `FFmpegPlanner.build_for_session(...)`
  accepts a caller-owned directory for future recovery, while `build(...)` retains
  its existing fresh-directory behavior.
- Local Session/planner/storage tests are `19 passed`; Ruff and compileall passed.
- Explicit non-goals: no same-session recovery, attempt-specific output numbering,
  recovery state machine, offline hysteresis, crash recovery, or package-version change.
- Final independent Standards/Spec review found no P0-P2 or other actionable issue.
  Draft PR [#16](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/16)
  is open/draft at head `7400697d439484311da0860eec69be8229bac7d6`. Windows CI
  [#45](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33938312883)
  passed its single job, including Windows build, installer, and install/upgrade/uninstall smoke.
  Diagnostic artifact `RecoBox-installer-e2e-diagnostics-33938312883` has digest
  `sha256:18411502d1f8d6b6d485e4a20b575c5318c265240633d5f763ca43f03a802b15` and is retained until
  2026-09-12; owner acceptance remains pending.

## PR-13 current acceptance

- Scope: `0.3.0-06` same-session recovery; the package version remains `0.2.1`.
- The current bounded retry path creates one active `RecordingSession` per
  logical livestream and reuses its stable directory after eligible FFmpeg
  failures, while resolving a fresh transient stream URL for each attempt.
- Recovery advances from the highest existing output number in the session
  directory without reusing a deleted number; compatibility `group_id` uses the
  session ID and `recovery_index` uses the session attempt.
- Clean completion, manual stop, protective stop, and exhausted retry have
  explicit durable session outcomes. `last_stream_url` is memory-only and is
  excluded from SQLite, logs, and evidence.
- A manual pause while a retry is pending abandons the active Session, and a
  recovery disk preflight failure closes it as `failed`.
- A non-live resolver result closes a recoverable Session only when it carries
  no resolver failure; error-bearing offline-shaped results remain eligible for
  later retry.
- Focused tests are `50 passed`; the full suite is `197 total, 195 passed、2 failed`;
  both failures require the local FFmpeg/ffprobe runtime assets. Ruff,
  compileall, and `git diff --check` passed.
- Final independent Standards and Spec review of fixed point `68a81f3` both
  returned PASS with no P0–P3 findings.
- Explicit non-goals: no startup recovery, recovery state machine, offline
  hysteresis, package-version change, merge, tag, formal Release, or `main`
  modification.
- A successful non-live resolver result closes a recoverable session before a
  later broadcast starts, while continuous offline confirmation remains PR-14
  work.
