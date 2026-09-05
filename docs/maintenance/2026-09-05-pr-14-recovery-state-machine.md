# PR-14：Recovery State Machine

- Status: local implementation and verification complete; remote PR, independent review, Windows CI, and owner acceptance pending
- Roadmap target: `0.3.0-06` Recovery State Machine; package version remains `0.2.1`
- Local branch: `codex/0.3.0-06-recovery-state-machine`
- Base: PR-13 same-session recovery final local tip `bdcfb0e`

## Scope

Introduce a strict runtime lifecycle state machine shared by monitoring and
recording. The machine must distinguish a resolver check, live preparation,
recording, an eligible recovery attempt, a clean end awaiting offline
confirmation, a real offline result, an error, and a manual stop. FFmpeg exit
alone must not be treated as proof that the public livestream ended.

## Implemented

- Added `RecoveryState`, `RecoveryEvent`, `RecoveryStateMachine`, and
  `RecoveryStateStore` in `src/reco_box/recovery.py`.
- Wired `MonitoringCoordinator` and `RecordingManager` to one shared store in
  the application composition root.
- Resolver checks enter `CHECKING`; live results enter `PREPARING`; a started
  process enters `RECORDING`; eligible recording failures enter `RECOVERING`;
  and retry exhaustion enters `ERROR`.
- Clean recording/conversion completion enters `CONFIRMING_OFFLINE`; an
  error-free offline resolver result is the event that enters `OFFLINE`.
- Manual stops enter `STOPPING` before ending in `OFFLINE` or `DISABLED`.
- A clean exit keeps the logical `RecordingSession` ACTIVE until offline
  confirmation, so a still-live room reuses the same session directory and
  session ID. Manual stop requests are idempotent, and the stall watchdog does
  not race an intentional graceful stop.
- A pause request during conversion is recorded until the worker callback
  arrives; both successful and failed late callbacks preserve the disabled
  projection. `QProcess.errorOccurred` enters `RECOVERING`, while the monitor
  waits for finalization before scheduling another resolver check.
- `stopAllAndPause` now includes rooms whose recordings are already converting.
- Existing `RoomStatus` values remain the user-facing and persisted projection;
  no runtime state snapshot or schema migration is added.
- Disabled rooms cannot be started by a late resolver/live callback.

## Explicit non-goals

- No offline hysteresis or configurable offline confirmation count/interval.
- No startup scan, ffprobe repair, interrupted-session recovery, or persisted
  runtime state-machine snapshot.
- No resolver registry refactor, package-version change, merge, tag, formal
  Release, or `main` modification.

## Local verification

- Focused state-machine, monitor-wiring, recording-wiring, session, stall, and
  retry tests: `43 passed`.
- Full suite: `210 collected, 208 passed, 2 known prerequisite failures`; both
  failures require the local `runtime/ffmpeg/ffmpeg.exe` and `ffprobe.exe`
  assets.
- Ruff, compileall, and `git diff --check` passed.

## Acceptance gates

- [x] State/event table is strict and invalid transitions do not mutate state.
- [x] Monitor and recorder share one per-room runtime state store.
- [x] Live, recording, recovery, clean-end/offline-confirmation, error, and
  manual-stop boundaries are wired.
- [x] Existing retry, stall, conversion, and disabled-room behavior remains
  covered by regression tests.
- [ ] Independent Standards/Spec review.
- [ ] Draft PR and remote Windows CI with installer E2E.
- [ ] Owner acceptance.

## Rollback

Revert the PR-14 recovery module, monitor/recording/app wiring, tests, and
documentation to return to the PR-13 runtime. Do not rewrite PR-13, earlier
branches, `main`, or persisted recording history.

