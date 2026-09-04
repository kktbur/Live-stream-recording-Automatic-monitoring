# Issue tracker

This file records the repository's active maintenance issue references. It does
not replace GitHub conversation history.

| Issue | Status | Current repository scope | Completion gate |
| --- | --- | --- | --- |
| [#1 Restore TLS certificate verification where possible](https://github.com/kktbur/Live-stream-recording-Automatic-monitoring/issues/1) | OPEN | PR-06 first phase: inventory all exposed platform paths and connect the first-party TwitCasting anonymous path to verified-by-default policy | Verify normal certificate behavior platform by platform; record any exact endpoint exception with a regression test; update README, PRIVACY, and audit evidence before closing |

PR-06 intentionally does not claim Issue #1 is closed. The pinned upstream
shared async helper still has an unverified default for other platform paths.
