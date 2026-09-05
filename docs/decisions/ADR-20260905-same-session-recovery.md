# ADR-20260905：bounded recovery reuses one RecordingSession

PR-13 connects the current bounded recording retry path to the durable
`RecordingSession` identity introduced by PR-12. A failed FFmpeg attempt does
not by itself prove that the public livestream ended.

## Decision

- Keep one in-memory active `RecordingSession` per room while automatic retry is
  still allowed, and upsert its durable state after each attempt boundary.
- Reuse the session's `session_dir` for every automatic retry after a failed
  attempt. Resolve the stream again, then use the highest existing numeric
  output number plus one for default output, or the first available suffixed
  custom name.
- Use the session ID as the compatibility `group_id` and the session attempt as
  the compatibility `recovery_index`, so existing history aggregation continues
  to show one logical history item.
- Mark sessions `COMPLETED` after a clean recording/conversion, `ABANDONED`
  after a manual stop, and `FAILED` after a protective stop or exhausted retry
  budget or a recovery preflight disk guard. Keep an eligible failed attempt
  `ACTIVE` for the next resolver cycle; a manual pause while waiting for retry
  abandons it.
- Keep each resolved playback URL in memory only; it is never part of the
  session record, logging, or repository evidence.

## Considered alternatives

- Creating a new timestamped directory on every retry would split one public
  livestream into multiple apparent sessions and contradict Issue #2.
- Reusing only the old `group_id` would preserve history aggregation but would
  leave the directory and attempt ownership implicit in `RecordingManager`.
- Loading active sessions during manager startup would claim crash recovery,
  which belongs to the later startup-recovery scope.

## Consequences

Automatic retries now preserve the stable directory and media numbering while
remaining bounded by the existing retry policy. A clean resolver offline result
closes a pending session, while resolver failures remain eligible for later
retry; offline hysteresis, explicit recovery-state transitions, and startup
repair remain separate follow-up work.
