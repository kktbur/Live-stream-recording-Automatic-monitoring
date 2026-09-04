# PR-02 Local Maintenance Record

- Status: LOCAL, awaiting owner acceptance
- Target repository: `kktbur/Live-stream-recording-Automatic-monitoring`
- Baseline: `main` at `0637a7eca5dc41dabe0ac50dd2e17bf053f49641`
- Working branch: `codex/0.2.1-02-single-source-version`
- Version under test: `0.2.0`; this maintenance change does not publish or bump a release

## Scope

Make `pyproject.toml` the only direct release-version input for the Python
package, Windows executable metadata, Inno Setup metadata and filenames, CI
artifact names, the installer self-test, and the visible application version.
Add automated checks for the package, generated lock metadata, executable,
installer, and artifact filename version surfaces. Do not change recording
logic or platform adapters.

`uv.lock` remains a generated dependency-lock snapshot. Its editable root
package version must match `pyproject.toml`; the version test makes stale lock
metadata fail visibly, while `uv lock` remains the regeneration command.

## Backup and recovery

The baseline commit remains available locally and the work is isolated on the
working branch. Build output is ignored and is not part of the change. Before
any remote operation, inspect the branch diff and preserve the baseline as the
recovery point.

Rollback condition: if the version consistency checks, installer behavior, or
owner acceptance fails, do not publish the branch. Revert the local PR-02
commits back to the baseline commit, preserving the worklog and test evidence
outside the source checkout.

## Release gate

No `git push`, Pull Request, Issue update, tag, or Release is authorized by
this record. Publication requires separate owner confirmation after the
recorded verification and independent Standards/Spec review pass.
