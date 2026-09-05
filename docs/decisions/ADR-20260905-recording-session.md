# ADR-20260905：RecordingSession as the logical broadcast identity

PR-12 introduces `RecordingSession` as the domain identity for one public livestream occurrence. A session owns one stable output directory and may contain multiple FFmpeg attempts; the current retry and monitoring behavior remains unchanged until the following recovery PRs.

## Decision

- Keep the session model separate from the existing per-process `recordings` rows. The new persistence table stores the session identity, room, start time, stable directory, attempt number, lifecycle state, and safe recovery reason.
- Keep `last_stream_url` on the in-memory domain object only. Resolved playback URLs are transient and must not be persisted, logged, or copied into repository evidence.
- Extract session-directory selection into `SessionPathPlanner` and add `FFmpegPlanner.build_for_session(...)` for a caller-owned directory. The compatibility `build(...)` path still creates a fresh directory exactly as before.
- Defer linking live recording behavior, attempt-specific output numbering, same-session recovery, and recovery-state transitions to the next PRs.

## Considered alternatives

- Reusing `group_id` and `recovery_index` as the public domain model would leave identity and persistence semantics distributed across `RecordingManager` and SQL aggregation.
- Persisting the last playback URL would make recovery depend on an expiring address and would violate the repository privacy boundary.

## Consequences

The new model and schema can be tested independently and provide a narrow seam for later recovery work. Existing recording history remains backward-compatible, while a later migration must explicitly associate attempts with sessions before claiming same-session recovery.

