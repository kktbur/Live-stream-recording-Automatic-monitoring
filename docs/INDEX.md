# Reco Box repository documentation index

This is the navigation entry for repository-maintained documentation. The
outer raco box project index contains the broader maintenance plan and
cross-check evidence.

| Document | Purpose | Status | When to read |
| --- | --- | --- | --- |
| [Repository instructions](../AGENTS.md) | Repository safety, testing, and release rules | ACTIVE | Before making changes |
| [PRODUCT](PRODUCT.md) | Product purpose and boundary | ACTIVE | Confirm product scope |
| [ACCEPTANCE](ACCEPTANCE.md) | Maintenance acceptance rules | ACTIVE | Plan or accept a change |
| [CURRENT](CURRENT.md) | Durable current state | ACTIVE | Check current maintenance status |
| [CODEMAP](CODEMAP.md) | Repository structure map | ACTIVE | Locate code and documentation |
| [Issue tracker](agents/issue-tracker.md) | Active GitHub maintenance issue references | ACTIVE | Track issue scope and completion gates |
| [Platform validation](platform-validation-0.2.0.md) | Recorded platform validation results | ACTIVE | Review platform coverage |
| [Live samples](platform-live-samples-0.2.0.md) | Platform sample evidence | ACTIVE | Inspect sample evidence |
| [PR-02 maintenance record](maintenance/2026-09-04-pr-02-single-source-version.md) | Version-source maintenance scope and recovery point | ACTIVE | Review PR-02 changes |
| [PR-03 maintenance record](maintenance/2026-09-04-pr-03-uv-ci.md) | Locked uv CI maintenance scope and acceptance gate | ACTIVE | Review PR-03 changes |
| [PR-04 maintenance record](maintenance/2026-09-04-pr-04-actions-release-separation.md) | Action SHA pinning and release-candidate boundary | ACTIVE | Review PR-04 changes |
| [PR-05 maintenance record](maintenance/2026-09-04-pr-05-installer-e2e-attestation.md) | Installer upgrade/uninstall E2E and release provenance boundary | ACTIVE | Review PR-05 changes |
| [PR-06 maintenance record](maintenance/2026-09-04-pr-06-tls-network-matrix.md) | TLS network matrix and first-party policy boundary | ACTIVE | Review PR-06 changes |
| [PR-07 maintenance record](maintenance/2026-09-05-pr-07-bilibili-tls.md) | Bilibili first-party TLS migration and anonymous request boundary | ACTIVE | Review PR-07 changes |
| [PR-08 maintenance record](maintenance/2026-09-05-pr-08-youtube-tls.md) | YouTube first-party TLS migration and anonymous request boundary | ACTIVE | Review PR-08 changes |
| [PR-09 maintenance record](maintenance/2026-09-05-pr-09-scheduler.md) | Resolver scheduling, concurrency limits, cooldown, and jitter | ACTIVE | Review PR-09 changes |
| [Platform Network Security Matrix](platform-network-security.md) | Endpoint inventory, TLS status, and anonymous-access boundaries | ACTIVE | Plan platform-by-platform TLS migration |
| [ADR-20260904-tls-network-policy](decisions/ADR-20260904-tls-network-policy.md) | Exact-host TLS exception policy | ACTIVE | Change first-party network requests |
| [ADR-20260905-bilibili-tls-policy](decisions/ADR-20260905-bilibili-tls-policy.md) | Bilibili first-party request boundary | ACTIVE | Change Bilibili network requests |
| [ADR-20260905-youtube-tls-policy](decisions/ADR-20260905-youtube-tls-policy.md) | YouTube first-party request boundary | ACTIVE | Change YouTube network requests |
| [ADR-20260905-scheduler-limits-jitter](decisions/ADR-20260905-scheduler-limits-jitter.md) | Resolver scheduling and rate-limit boundary | ACTIVE | Change monitoring concurrency or retry timing |
| [0.2.1 release notes](../RELEASE_NOTES_0.2.1.md) | Version 0.2.1 maintenance and release boundary | ACTIVE | Review the candidate release scope |
