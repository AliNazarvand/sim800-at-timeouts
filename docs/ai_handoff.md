# AI Handoff

This document describes the workflow for AI-assisted version diff
extraction across the tracked SIM800 documentation versions.

## Overview

The project tracks three AT Command Manual versions (V1.01, V1.10, V1.12)
and several Hardware Design documents. Filling ``version_specific`` and
``version_reviews`` requires comparing the same command across versions.

## Workflow

1.  Fetch PDFs (or reuse ``.cache/sources/``):

    ```
    python scripts/fetch_sources.py
    ```

2.  Dump PDF text to ``build/pdf_text/``:

    ```
    python scripts/fetch_and_parse_pdfs.py --dump-all --save
    ```

3.  Extract per-command excerpts for commands that still have an empty
    ``version_specific``:

    ```
    python scripts/extract_command_excerpts.py
    ```

4.  Review ``build/pdf_excerpts/INDEX.md`` and pick a command.

5.  Generate a review stub:

    ```
    python scripts/ai_version_diff.py --cmd "AT+CSQ"
    ```

6.  Fill ``version_specific`` / ``version_reviews`` in ``data/*.yaml``
    using the stub in ``docs/ai_review_<command>.md``.

7.  Run:

    ```
    python scripts/validate.py
    python scripts/check_doc_examples.py
    ```

## Review Status Decision Table

| Observation in PDF               | Review status                          | ``version_specific`` entry |
|----------------------------------|----------------------------------------|----------------------------|
| Identical timeout                | ``approved_present_equivalent``        | none                       |
| Different timeout                | ``approved_present_different``         | required                   |
| Timeout not mentioned            | ``approved_present_not_mentioned``     | required                   |
| Timeout explicitly removed       | ``approved_present_explicitly_removed``| required                   |
| Command absent                   | ``approved_absent_command``            | none                       |
| Command removed in newer version | ``approved_removed_command``           | none                       |
| PDF unavailable                  | ``rejected_pdf_unavailable``           | none                       |
| Uncertain                        | ``rejected_uncertain``                 | none                       |
| Not yet reviewed                 | ``pending_review``                     | none                       |

## Evidence Requirements

Every ``approved_*`` review must carry an ``evidence`` block:

-   ``section`` : must start with one of ``Table``, ``Section``,
    ``Chapter``, ``Page``, ``Figure`` followed by whitespace.
-   ``page`` : PDF page number.
-   ``note`` : human-readable description.
-   ``compared_to_version`` : representative version (for equivalents).

## Structure Rules

-   ``source_same_as_representative: true`` implies ``source_document: null``,
    ``source_section: null``, and ``page_hint_same_as_representative: true``.
-   ``page_hint_same_as_representative: true`` implies ``page_hint: null``.
-   ``version_specific`` must be sorted ascending by ``versions.yaml`` order.
-   Timeouts array order (DR-17):
    ``prompt_timeout``, ``send_timeout``, ``max_response_time``,
    ``max_timeout``, ``urc_report_timeout``, ``boot_time``,
    ``init_delay``, ``hardware_settle_time``, ``min_delay``, ``max_wait``,
    ``retry_interval``.

## Automation

The following scripts assist the workflow and never edit ``data/*.yaml``
directly:

-   ``scripts/fetch_and_parse_pdfs.py`` : fetch + dump PDF text.
-   ``scripts/extract_command_excerpts.py`` : per-command excerpts.
-   ``scripts/ai_version_diff.py`` : review stub generator.
-   ``scripts/extract_mrt_full.py`` : MRT extractor with correction report.
-   ``scripts/populate_reviews.py`` : evidence-driven review population.
-   ``scripts/cleanup_vs.py`` : duplicate ``version_specific`` cleanup.
-   ``scripts/fix_orphan_reviews.py`` : orphaned review repair.