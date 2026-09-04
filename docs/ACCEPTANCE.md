# ACCEPTANCE

## Repository maintenance minimums

1. State the target repository, current and target version, scope, and recovery
   point before changing code.
2. Keep changes anonymous-only and free of credentials, cookies, transient
   playback URLs, and unreviewed binary assets.
3. Add focused regression coverage for behavior changes and run the relevant
   full or filtered test suite with the limitation recorded.
4. Run Ruff and `git diff --check`; use the Windows CI result for checks that
   depend on omitted runtime assets or Windows-only packaging.
5. Keep README, PRIVACY, audit records, and maintenance records consistent with
   the actual completion state.
6. Do not call a Draft PR, Tag, formal Release, or merge a completion result
   without direct evidence for that operation.

## TLS changes

TLS compatibility exceptions must be explicit and narrow: platform, exact Host,
reason, and regression test. A static endpoint inventory is not a substitute
for platform-by-platform certificate-compatibility evidence.

## PR-07 current acceptance

- Scope: Bilibili only; the package version remains `0.2.1`.
- First-party request code: `src/reco_box/bilibili.py` uses explicit HTTPX TLS policy,
  proxy, HTTP/2 and redirect settings without account credentials or Cookie.
- Local evidence: 29 focused tests passed; the full suite has 103 passed and 2
  prerequisite-dependent failures; Ruff, compileall and `git diff --check` passed.
- Independent Standards/Spec review at the latest fixed point found no remaining hard
  implementation or specification issue.
- Limitation: the focused suite uses an injected offline client. It does not establish
  current public-room availability, dynamic CDN reachability or a short recording.
- Release boundary: no merge, Tag, formal Release or `main` modification is part of PR-07.
