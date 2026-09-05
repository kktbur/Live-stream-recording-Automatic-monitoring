# PR-12: RecordingSession abstraction

- Status: local model, persistence boundary, tests, documentation, independent review, remote Draft PR, and Windows CI complete; owner acceptance pending
- Roadmap target: `0.3.0-05` RecordingSession; package version remains `0.2.1`
- GitHub issue: [#2 Improve recording recovery after stream interruption](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/issues/2)
- Local branch: `codex/0.3.0-05-recording-session`
- Recovery point: PR-11 implementation and evidence tip before this branch

## Scope

Define one `RecordingSession` for one logical livestream occurrence. The model
contains `session_id`, `room_id`, `started_at`, `session_dir`, `attempt`,
`last_stream_url`, `state`, and `recovery_reason`. A session directory is stable
across future attempts, while a single FFmpeg process remains only one attempt.

This PR creates the domain and persistence seam without activating recovery:
the existing `RecordingManager` still uses its current group/retry behavior and
the existing `FFmpegPlanner.build(...)` compatibility path.

## Implemented

- Added `RecordingSession` and `RecordingSessionState` with identity and
  non-negative-attempt invariants.
- Added schema version 7 and a `recording_sessions` table with room foreign-key
  protection, durable lifecycle fields, and safe recovery-reason storage.
- Added `Database.create_recording_session`, `upsert_recording_session`,
  `get_recording_session`, and room-filtered listing.
- Kept `last_stream_url` out of `to_record()` and the SQLite schema; it remains
  a memory-only field for a later resolver/recovery integration.
- Extracted `SessionPathPlanner` and added `FFmpegPlanner.build_for_session(...)`
  so a future recovery attempt can receive a caller-owned directory without
  changing the existing build behavior today.

## Explicit non-goals

- No `RecordingManager` session wiring or migration of `group_id`/
  `recovery_index`.
- No same-session recovery, attempt-specific file numbering, recovery state
  machine, offline hysteresis, or crash recovery.
- No raw stream URL persistence, logging, screenshots, or repository evidence.
- No package-version change, merge, tag, formal Release, or `main` modification.

## Local verification

- Session, FFmpeg planner, and storage tests: `19 passed`.
- Ruff and compileall passed after the implementation.
- The existing full-suite FFmpeg/ffprobe prerequisite limitation remains
  recorded by PR-11; it is unrelated to this model-only change.

## Acceptance gates

- [x] One domain object represents a logical broadcast independently of a process attempt.
- [x] The session directory is an explicit durable field and can be supplied to the planner.
- [x] Schema migration and round-trip persistence tests pass.
- [x] Negative attempts are rejected; lifecycle state round-trips.
- [x] The transient stream URL is proven not to be serialized or stored.
- [x] Existing `FFmpegPlanner.build(...)` tests remain green.
- [x] Independent Standards/Spec review at the final fixed point; both axes found no P0-P2 or other actionable issue.
- [x] Draft PR [#16](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/pull/16) published at head `7400697d439484311da0860eec69be8229bac7d6`.
- [x] Windows CI [#45](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/actions/runs/33938312883) passed its single job, including the Windows build, installer, and install/upgrade/uninstall smoke.
- [x] Diagnostic artifact `RecoBox-installer-e2e-diagnostics-33938312883` retained until 2026-09-12; digest `sha256:18411502d1f8d6b6d485e4a20b575c5318c265240633d5f763ca43f03a802b15`.
- [ ] Owner acceptance.

## Rollback

Revert the PR-12 domain, schema, storage, planner-seam, tests, and documentation
commits to return to PR-11. Do not rewrite PR-11, earlier branches, `main`, or
the existing recordings table history.

