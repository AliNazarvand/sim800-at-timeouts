# DR-22 Specific Command Verification

Manual reconciliation of flagged commands against extracted PDF values.

| command | extracted (V1.12) | stored value | action |
|---------|-------------------|--------------|--------|
| AT+CIPSEND | None | (see review_flags.md) | keep (DR-1: no guessing) |
| AT+CGATT | 75000 | (see review_flags.md) | keep (DR-1: no guessing) |
| AT+CSQ | None | (see review_flags.md) | keep (DR-1: no guessing) |
| AT+CMGL | None | (see review_flags.md) | keep (DR-1: no guessing) |
| AT+CMGR | 20000 | (see review_flags.md) | keep (DR-1: no guessing) |

**Action required by human reviewer:** confirm extracted values
against the PDF pages listed in `inventory.json` before any
automated overwrite.
