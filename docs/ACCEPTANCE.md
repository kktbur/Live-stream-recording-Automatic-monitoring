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
  is open/draft, and Windows CI [#38](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33923911448)
  passed the remote Windows validation stages, including installer install/upgrade/uninstall smoke.
- The UI evidence screenshot is [PR-09 settings dialog](maintenance/assets/pr-09-settings-dialog.png);
  it uses synthetic data and contains no credentials or real playback URL.
- Release boundary: no merge, Tag, formal Release, or `main` modification is part of PR-09.
