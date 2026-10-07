# Methodology

## Extraction

1. Parse PDFs with PyMuPDF.
2. Identify Max Response Time tables.
3. Extract timeout values from text using regex patterns.
4. No guessed values are recorded.

## `default_value_ms`

Sourced exclusively from PDF text. `null` if not specified in PDF.

## Decision Table: `page_hint` (§C1)

| source_same_as_representative | page_hint_same_as_representative | page_hint |
|---|---|---|
| true | true | null (same page as representative) |
| true | false | **not allowed** |
| false | true | null (same page as representative, different source) |
| false | false | **required integer** (unless PDF has no page numbering) |

### Example (C1): `source_same_as_representative: true`

`AT+CSQ` in `representative_version: V1.12` from
`SIM800 Series_AT Command Manual_V1.12.pdf`, section `AT+CSQ`, page 88.
V1.10 uses the same section and same page. The `VersionEntry` for V1.10:

```yaml
- version: "V1.10"
  source_same_as_representative: true
  source_document: null
  source_section: null
  page_hint_same_as_representative: true
  page_hint: null
  presence_status: "present"
  extraction_status: "extracted_from_table"
  timeouts: [...]
```

## Decision Table: multi-timeout `timeout_kind` (§C2)

All timeouts mentioned in the PDF are recorded. Example `AT+CIPSEND`:

- `prompt_timeout`: waiting for `>`.
- `send_timeout`: waiting for `SEND OK`.
- `max_timeout` / `urc_report_timeout`: maximum time for connection close
  (e.g. 11 minutes / 660 s in `AT+CIPSEND`).

## Decision Table: `urc_report_timeout` (§C3)

`urc_report_timeout` is used when the PDF describes "after X seconds, URC Y is
reported". The timeout is recorded on the command that **produces** the URC.
Example: if `CLOSE` is reported after 645 s of no response from the server,
the timeout is recorded on `AT+CIPSTART` (which initiated the connection),
not on the command that received the URC.

## Decision Table: INIT `timeout_kind` (§C4)

| PDF phrase | timeout_kind |
|---|---|
| pull down PWRKEY for at least X s | `hardware_settle_time` |
| wait X s after power-on before AT commands | `boot_time` |
| wait X ms between INIT commands | `init_delay` |
| the module is ready after X s | `boot_time` |
| delay of X s before next step | `init_delay` |

## `review_scope` / `pending_versions`

- `absent`: no version reviewed. `pending_versions` = all versions.
- `partial`: at least one reviewed. `pending_versions` = union across all
  `CommandEntry` of versions not present in their `version_reviews`.
- `complete`: every entry has one review per version except the representative.

## External checks (not machine-verifiable)

`page_hint` (when non-null) must be consistent with the page count of the
referenced PDF. Page counts are read from the PDF with PyMuPDF, not from
`docs/sources.md`. This rule is enforced by human review + CI artifact.
