# PR-13: Same-session recovery

- Status: local implementation, focused verification, independent review, remote Draft PR, and Windows CI complete; owner acceptance pending
- Roadmap target: `0.3.0-06` same-session recovery; package version remains `0.2.1`
- GitHub issue: [#2 Improve recording recovery after stream interruption](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/issues/2)
- Local branch: `codex/0.3.0-06-same-session-recovery`
- Recovery point: PR-12 final local documentation tip

## Scope

Connect the bounded automatic recording retry path to `RecordingSession`. When
an FFmpeg attempt fails for a still-eligible retry, the next resolver result
uses the same session ID and session directory, while selecting the next
collision-free media-file number. A clean end, manual stop, protective stop,
and exhausted retry budget close the session with distinct durable states.

## Implemented

- `RecordingManager` creates and persists an active `RecordingSession` for a
  first attempt and reuses it for eligible retries.
- The session ID feeds the existing `group_id` history compatibility field and
  the session attempt feeds `recovery_index`.
- `FFmpegPlanner.build_for_session(...)` accepts an attempt start number;
  segmented output uses `-segment_start_number`, and unsegmented output uses
  `2.ts`/`3.ts` or suffixed custom names after the first collision. Default
  numeric output advances from the highest existing number and does not reuse
  a deleted number.
- `last_stream_url` remains memory-only; only the safe recovery classification
  is persisted.
- Manual stop is recorded as `ABANDONED`; clean completion is `COMPLETED`; a
  protective, recovery-preflight disk guard, or exhausted retry is `FAILED`;
  eligible failure retains `ACTIVE`. A manual pause while waiting for retry
  records `ABANDONED`.
- A non-live resolver result without a resolver failure closes any recoverable
  active session as `COMPLETED`, so a later broadcast starts a new session.
  Error-bearing offline-shaped results do not close it. PR-14 will gate this
  boundary with offline hysteresis.

## Explicit non-goals

- No startup loading or repair of active sessions.
- No separate recovery state machine, offline hysteresis, or crash recovery.
- No change to resolver scheduling, retry delays, package version, `main`, tags,
  formal Release, or merge behavior.

## Local verification

- Focused session/planner/storage/stall/recovery tests: `50 passed`.
- Full suite: `197 total, 195 passed, 2 known failures`; both failures require
  the local `runtime/ffmpeg/ffmpeg.exe` and `ffprobe.exe` assets, which CI
  prepares.
- Ruff, compileall, and `git diff --check` passed.

## Acceptance gates

- [x] Eligible automatic retries reuse the same session ID and session directory.
- [x] Recovery output advances from the highest existing number in that directory without reuse.
- [x] Compatibility history remains grouped by session ID with incremented attempt index.
- [x] Manual stop, clean completion, protective stop, and exhausted retry have durable session outcomes.
- [x] Manual pause during pending recovery and recovery-preflight disk failure close the session safely.
- [x] Transient playback URLs remain memory-only.
- [x] Existing bounded retry and stall behavior remains covered.
- [x] Final independent Standards/Spec review at fixed point `68a81f3`; both axes returned PASS with no P0–P3 findings.
- [x] Draft PR [#17](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/17) published at remote head `c9735602ad7203394d343be67eb538fafcf5a2df`.
- [x] Windows CI [#47](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33942125612) passed its single job, including the Windows build, installer, and install/upgrade/uninstall smoke.
- [x] Diagnostic artifact `RecoBox-installer-e2e-diagnostics-33942125612` retained until 2026-09-12; digest `sha256:8ad2471302480171351df62d65d78ce2c9a921e8290fe261ff07a6119babb96c`.
- [ ] Owner acceptance.

## Rollback

Revert the PR-13 manager, planner/output-path, test, and documentation commits
to return to PR-12. Do not rewrite PR-12, earlier branches, `main`, or the
existing recordings table history.
