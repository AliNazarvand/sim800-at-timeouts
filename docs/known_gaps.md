# Known Gaps

The following gaps are documented but not yet resolved.

## Resolution Workflow

1. Run `python scripts/cross_check_versions.py` to refresh `docs/gaps.md`.
2. Pick a command from the "empty `version_specific`" table.
3. For each non-representative version, open the corresponding PDF page
   listed in `docs/sources_mapping.md`.
4. If the timeout is identical, add a `version_reviews` entry with
   `status: approved_present_equivalent` and an `evidence` block.
5. If the timeout differs, add a `version_specific` entry with its own
   `timeouts` and set `source_same_as_representative: false`.
6. If the timeout is removed, add a `version_specific` entry with
   `presence_status: explicitly_removed` and empty `timeouts`.
7. Re-run `python scripts/validate.py` and
   `python scripts/check_doc_examples.py`.

## AI-Assisted Workflow

See `docs/ai_handoff.md` for the AI-assisted extraction workflow.

## Acceptance Criteria

- `docs/coverage_report.md` must show 100% extraction coverage for every
  command with `presence_status_latest: present`.
- `docs/gaps.md` must list no command without `version_reviews`, except
  commands that exist in only one version.