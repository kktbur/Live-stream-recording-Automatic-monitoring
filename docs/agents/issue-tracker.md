# Issue tracker

This file records the repository's active maintenance issue references. It does
not replace GitHub conversation history.

| Issue | Status | Current repository scope | Completion gate |
| --- | --- | --- | --- |
| [#1 Restore TLS certificate verification where possible](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/issues/1) | OPEN | PR-06 matrix plus PR-07 Bilibili first-party anonymous API migration; other platforms remain on the pinned upstream path | Verify normal certificate behavior platform by platform; record any exact endpoint exception with a regression test; update README, PRIVACY, and audit evidence before closing |

PR-06 and PR-07 intentionally do not claim Issue #1 is closed. The pinned
upstream shared async helper still has an unverified default for other platform
paths, and Bilibili still needs public-room/CDN/short-recording validation even
though its first-party request boundary is covered by offline tests.
