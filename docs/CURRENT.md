# CURRENT

- Status: ACTIVE
- Current package version: `0.2.1` (single source: `pyproject.toml`).
- Current maintenance roadmap target: `0.2.2`.
- The latest maintenance record is [PR-06 TLS network matrix and first-party
  policy](maintenance/2026-09-04-pr-06-tls-network-matrix.md).

## Confirmed PR-06 boundary

- The repository contains a matrix for all 18 exposed `Platform` enum entries.
- Reco Box-owned TwitCasting anonymous page and streamserver requests use an
  explicit verified-by-default policy.
- Compatibility overrides are restricted to platform plus exact Host.
- Other platforms still use the pinned upstream async helper's unverified
  default until their own compatibility evidence and migration are completed.
- The first phase does not close GitHub Issue #1 by itself.

For the active branch, commit, CI, and recovery snapshot, use the linked
maintenance record and the pull request description rather than inferring state
from this durable product document.
