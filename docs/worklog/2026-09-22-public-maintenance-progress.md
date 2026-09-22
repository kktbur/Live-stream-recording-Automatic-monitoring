# Public worklog — Reco Box maintenance progress — 2026-09-22

## Purpose

Publish a small, reviewable progress snapshot while the full reliability evidence remains local. The
public update is deliberately separate from raw validation artifacts and does not claim a release.

## Recorded work

1. Fixed the Task 15 validation wait so `probe_status='pending'` remains part of the shutdown probe wait.
2. Added a focused regression for that validation-only behavior; the affected local short suite reached
   `52 passed`.
3. Re-ran the candidate-bound 10/50/100 synthetic scale gate with fixed seed `20260905`; all three
   accepted scale reports passed their structured checks and ended with zero active resources.
4. Started the candidate-bound 100-room, 7200-second observation while Task 14 waits for a suitable
   public live sample. The observation was still running when this record was prepared.
5. Rechecked public Douyin and Bilibili candidates with the repository's anonymous resolver. No current
   candidate returned a live stream, so no real-platform recording was started.

## Evidence boundary

- Candidate package version: `0.2.1`.
- Production candidate SHA: `680e2fa1bb1b93b6e7f6ea0f90aa36dd454b63ed`.
- Validation runner SHA: `2b5ad15d2d228edd62a1eb11cae1882c0202c6d1`.
- The latest slice changed validation code and tests only; it did not change production recording code.
- Local raw reports, databases, logs, media, and package files remain outside this public snapshot so that
  the repository does not accumulate large or environment-specific artifacts.

## Next review point

Read the completed two-hour report and classify it as `PASS`, `FAIL`, or `INCOMPLETE` using the exact
candidate binding. Only then decide whether to begin the next long observation. Keep Task 14 real-platform
and manual tray results separate from synthetic reliability evidence.

