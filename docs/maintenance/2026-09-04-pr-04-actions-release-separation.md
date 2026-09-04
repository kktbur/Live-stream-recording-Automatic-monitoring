# PR-04 Maintenance Record: Pin Actions and Separate Release Candidate Builds

- Status: LOCAL IMPLEMENTATION COMPLETE; remote Draft PR awaits CI and owner review
- Target repository: `kktbur/Live-stream-recording-Automatic-monitoring`
- PR-03 recovery point: `b30a266c2c4c32c2967a5bcdaef0fadf98c90165`
- Working branch: `codex/0.2.1-04-actions-sha-release-separation`
- Maintenance target: `0.2.1`; no product-version bump in this CI/release-boundary change
- Final branch-tip commit and remote PR metadata are recorded in the outer PR-04
  worklog and evidence after publication; this repository-local record avoids
  duplicating moving remote metadata.

## Scope

Implement the first supply-chain stage from the maintenance roadmap:

- pin every external GitHub Action used by the repository to a reviewed full
  commit SHA, retaining a human-readable release comment;
- keep the ordinary `ci.yml` on `push` to `main` and `pull_request` with
  `contents: read` only;
- make the Windows build workflow reusable so the release path can request a
  release-candidate artifact without giving ordinary CI release permissions;
- add a separate `release.yml` entry point limited to `v*` tag pushes or manual
  tag selection, with the tag checked out by the reusable build workflow.

The ordinary CI path no longer uploads an installer artifact. The reusable
workflow can upload a release-candidate artifact only when explicitly called by
`release.yml`. PR-04 does not add installer install/uninstall E2E, artifact
attestation, or formal GitHub Release publication; those gates remain in PR-05.

## Reviewed Action pins

| Action | Release | Commit SHA |
| --- | --- | --- |
| `actions/checkout` | `v7.0.1` | `3d3c42e5aac5ba805825da76410c181273ba90b1` |
| `actions/setup-python` | `v7.0.0` | `5fda3b95a4ea91299a34e894583c3862153e4b97` |
| `astral-sh/setup-uv` | `v10.0.1` | `20cfd1bf945f4377ade1205e4dbc17946fc9a30d` |
| `actions/upload-artifact` | `v6.0.0` | `b7c566a772e6b6bfb58ed0dc250532a479d7789f` |

The SHAs were checked against the corresponding official release refs before
editing the workflow. Local reusable-workflow references use the same
repository commit by GitHub's workflow semantics and are not external Action
references.

## Acceptance gate

- workflow metadata tests must prove that every external Action reference uses
  a 40-character SHA and a release comment;
- `ci.yml` must retain only read permissions and must not trigger on release tags;
- `release.yml` must be tag/manual-only, call the reusable build with one tag
  value, and retain read-only build permissions;
- local locked tests, Ruff, and `git diff --check` must pass;
- formal Release publication, attestation, and installer E2E are explicitly
  deferred to PR-05.

## Backup and recovery

PR-03 remains the recovery point. If the reusable workflow or release-candidate
boundary fails remote validation, do not merge or modify PR-03; close or revert
only the PR-04 branch and retain the maintenance records and evidence.
