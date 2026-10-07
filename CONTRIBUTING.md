# Contributing

Please read `docs/methodology.md` before contributing data.

## Data Changes

1. Edit the relevant `data/*.yaml` file.
2. Run `python scripts/validate.py`.
3. Submit a pull request.

## Filling Version Gaps

The project tracks firmware / documentation versions listed in
`data/versions.yaml`. Whenever a command is listed in
`available_in_versions` with more than one version but has an empty
`version_specific` list, it means the version-level differences have not
yet been reviewed.

Workflow:

1. Run `python scripts/cross_check_versions.py` to refresh `docs/gaps.md`.
2. Pick a command from the "empty `version_specific`" table.
3. Open the corresponding PDF for each non-representative version.
4. If the timeout differs, add a `VersionEntry` to `version_specific` with
   `presence_status: present`, its own `timeouts`, and set
   `source_same_as_representative: false` with the correct
   `source_document` / `source_section` / `page_hint`.
5. If the timeout is identical, add a `VersionReview` with
   `status: approved_present_equivalent` and an `evidence` block.
6. Run `python scripts/validate.py` and `python scripts/check_doc_examples.py`.

## AI-Assisted Version Diff Extraction

To fill `version_specific` without downloading PDFs to disk, use the
in-memory extractor:

```bash
pip install requests PyMuPDF
python scripts/fetch_and_parse_pdfs.py --dump-all --save
python scripts/fetch_and_parse_pdfs.py --compare "AT+CSQ"
python scripts/ai_version_diff.py --cmd "AT+CSQ"
```

Then edit `data/*.yaml` using the review stub in
`docs/ai_review_<command>.md`. See `docs/ai_handoff.md` for the full
workflow.
