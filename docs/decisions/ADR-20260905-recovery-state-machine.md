# ADR-20260905：explicit room recovery state machine

PR-14 makes the room lifecycle explicit at runtime after PR-13 connected
automatic retry to one durable `RecordingSession`. The state machine is a
runtime coordination boundary; it is not a claim that the application can
repair an interrupted process after a restart.

## Decision

- Keep one strict `RecoveryStateMachine` per room in a shared
  `RecoveryStateStore` used by both `MonitoringCoordinator` and
  `RecordingManager`.
- Accept named `RecoveryEvent` values only when the current state allows them.
  Raise `InvalidRecoveryTransition` and leave the current state unchanged for
  an illegal event.
- Model these states: `IDLE`, `CHECKING`, `PREPARING`, `RECORDING`,
  `RECOVERING`, `CONFIRMING_OFFLINE`, `CONVERTING`, `OFFLINE`, `ERROR`,
  `STOPPING`, and `DISABLED`.
- Use these important boundaries:
  - `CHECKING → PREPARING → RECORDING` for a live result and a started process;
  - `RECORDING → RECOVERING → PREPARING` for an eligible failed attempt and a
    later live retry;
  - `RECORDING → CONFIRMING_OFFLINE → OFFLINE` for a clean end followed by an
    error-free offline resolver result;
  - `RECOVERING → ERROR` when the bounded recovery budget is exhausted;
  - `RECORDING → STOPPING → DISABLED` for a manual pause, or
    `STOPPING → OFFLINE` when monitoring remains enabled.
- Keep the existing `RoomStatus` enum as the UI and room-persistence projection
  for compatibility. `RETRYING` and `STALLED` continue to communicate the
  visible recovery/safe-stop condition without exposing transient internal
  states as persisted room statuses.
- Do not persist the runtime machine snapshot in this PR. The persisted
  `RecordingSession` remains the durable identity/result boundary; startup
  repair is a separate roadmap task.

## Rationale

An FFmpeg process can exit because of a transient CDN, URL, or network failure
while the public livestream continues. A direct `RECORDING → OFFLINE` assignment
would split one broadcast into multiple sessions. Separating `RECOVERING` and
`CONFIRMING_OFFLINE` makes the distinction testable and gives the future offline
hysteresis task a stable seam.

## Consequences

- Monitor and recorder event paths now have a shared vocabulary and an
  independently testable transition table.
- The UI keeps its existing status strings and filters, so this PR does not
  require a broad visual redesign or a database migration.
- Direct calls to private callbacks used by legacy tests may represent an
  uninitialized runtime process; those compatibility fixtures remain outside
  the production state-machine path. Normal application-created processes
  enter through `PREPARING` and `RECORDING`.

## Follow-up boundaries

Offline hysteresis will add repeated offline confirmation without weakening the
strict transitions. Startup crash recovery will decide how persisted active
sessions are inspected and repaired; neither behavior is inferred from this
runtime-only state machine.

