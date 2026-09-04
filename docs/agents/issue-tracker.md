# Issue tracker

This file records the repository's active maintenance issue references. It does
not replace GitHub conversation history.

| Issue | Status | Current repository scope | Completion gate |
| --- | --- | --- | --- |
| [#1 Restore TLS certificate verification where possible](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/issues/1) | OPEN | PR-06 matrix plus PR-07 Bilibili and PR-08 YouTube first-party anonymous migrations; other platforms remain on the pinned upstream path | Verify normal certificate behavior platform by platform; record any exact endpoint exception with a regression test; update README, PRIVACY, and audit evidence before closing |

PR-06 through PR-08 intentionally do not claim Issue #1 is closed. The pinned
upstream shared async helper still has an unverified default for other platform
paths, and Bilibili and YouTube still need public-room/CDN/short-recording
validation even though their first-party request boundaries are covered by
offline tests.
