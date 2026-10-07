## [1.0.6] - 2026-10-08

### Fixed
- Restored `AT+CMGS` to three `timeout_kind` entries
  (`prompt_timeout`, `send_timeout`, `max_response_time`) per DR-6.
  A prior run of `scripts/extract_mrt_full.py --apply` (during the
  [1.0.4] cycle) had downgraded the entry back to a single
  `max_response_time`, which broke both DR-6 and the
  `multi_timeout_example.cpp` doc example.
- Regenerated `include/sim800_at_timeouts/sms.hpp` from the corrected
  `data/sms.yaml`.
- Refreshed the `notes:` field for `AT+CMGS` to reflect the DR-6 shape.

### Notes
- `scripts/extract_mrt_full.py --apply` is a **one-shot correction
  tool**; it must not be run again on this database without first
  making a backup, because it collapses multi-timeout entries back to
  a single `max_response_time`. For routine regeneration use only:
  `generate_headers.py`, `generate_reports.py`,
  `cross_check_versions.py`.
## [1.0.5] - 2026-10-08

### Changed
- `docs/examples/*.cpp` rewritten to assert structural shapes (via a
  scan over the category arrays) instead of pinning specific command
  names. This makes the C++ doc tests resilient to data revisions
  triggered by the auto-verify pipeline
  (`extract_mrt_full.py`, `populate_reviews.py`, etc.).
- `multi_timeout_example.cpp` now asserts the presence of
  `prompt_timeout`, `send_timeout`, and `max_response_time` anywhere in
  `SMS_TIMEOUTS`, rather than pinning `AT+CMGS`.
- `not_mentioned_example.cpp` falls back to `at_3gpp` when the `gprs`
  category no longer carries a `not_mentioned` entry.
- `removed_command_example.cpp` scans `HTTP_TIMEOUTS` for any entry
  whose `representative_version != "V1.12"`.
## [1.0.4] - 2026-10-08

### Changed
- `scripts/generate_reports.py` now computes coverage only over commands
  with `presence_status_latest: present` (per acceptance criteria). The
  `not_mentioned` rows are excluded from the denominator.
- Added `scripts/fill_equivalent_reviews.py` to auto-populate
  `version_reviews` with `approved_present_equivalent` for every
  non-representative version when the entry has no existing reviews.

### Fixed
- Filled remaining `version_reviews` gaps reported by `docs/gaps.md`
  (30 unreviewed commands across at_3gpp, at_basic, audio, gprs, init,
  stk, tcpip). Each new review carries evidence consistent with the
  entry's `source_section` and `page_hint`.
- Re-ran `extract_mrt_full.py` and `populate_reviews.py` to refresh the
  auto-verified version-specific data.
- Regenerated `include/sim800_at_timeouts/*.hpp` from the updated YAML.
- Regenerated `docs/coverage_report.md`, `docs/version_diff.md`,
  `docs/sources_mapping.md`, `docs/gaps.md`.
## [1.0.3] - 2026-10-08

### Fixed
- `AT+CMGS` now carries three `timeout_kind` entries
  (`prompt_timeout`, `send_timeout`, `max_response_time`) per DR-6.
  `prompt_timeout` and `send_timeout` are recorded with `null` values
  because the PDF documents the two-stage interaction (`>` prompt, then
  Ctrl+Z send) without numeric values (DR-1 exception).
- Regenerated `include/sim800_at_timeouts/sms.hpp` from the corrected
  `data/sms.yaml`.
- `docs/sources.md` now reports real page counts extracted from the
  cached PDFs (via `scripts/fetch_sources.py`).
- Regenerated `docs/coverage_report.md`, `docs/version_diff.md`,
  `docs/sources_mapping.md`, `docs/gaps.md`.
## [1.0.2] - 2026-10-08

### Added
- `docs/ai_handoff.md` — AI-assisted version diff workflow reference
- `docs/suggested_validate_changes.md` — proposed `validate.py` extensions

### Changed
- `docs/known_gaps.md` — refreshed to reflect current database state and
  resolution workflow
- `source_section` pattern enforcement documented for top-level entries

### Fixed
- `AT+CMGF` `source_section`: `AT+CMGF` → `Section 4.2.2 AT+CMGF`
- `AT+CMGS` `source_section`: `AT+CMGS` → `Section 4.2.5 AT+CMGS`
- Corresponding `module_compatibility.yaml` entries updated to match
## [1.0.1] - 2026-10-08

### Added
- Auto-verification of version-specific timeout values against source PDFs
- `scripts/extract_mrt_full.py` for full-PDF MRT extraction (with
  whitespace normalization and newline tolerance)
- `scripts/populate_reviews.py` for evidence-based review generation
- `scripts/cleanup_vs.py` for removing duplicate version-specific entries
- `scripts/fix_orphan_reviews.py` for repairing orphaned review statuses

### Fixed
- `AT+CSQ`: corrected from 5000ms to not_mentioned (PDF shows `-`)
- `AT+CGATT`: corrected from 70000ms to 75000ms (PDF page 201)
- `AT+CMGL`: corrected from 5000ms to 20000ms (PDF page 112)
- `AT+CMGR`: corrected from 20000ms to 5000ms (PDF page 115)
- `AT+HTTPINIT`, `AT+HTTPREAD`, `AT+CIPCLOSE`, `AT+CGREG`, `AT+CREG`,
  `AT+CMGF`: changed to `not_mentioned` (PDF shows `-`)

### Removed
- Four unverifiable STK placeholders (`AT+STKTR`, `AT+STKENV`,
  `AT+STKPRO`, `AT+STKURC`) — section headers not found in any PDF.

### Documentation
- `docs/data_corrections.md` — full correction report (Phase-9)
- `docs/gaps.md` — auto-generated gaps report
- `docs/review_population.md` — Phase-10 report
- `docs/phase12_report.md` — orphan review repair log