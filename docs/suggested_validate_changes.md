# Suggested `validate.py` Extensions

The following extensions are proposed to bring `validate.py` in line with
the decision rules documented in `docs/methodology.md`. They are provided
as text so that a human reviewer can apply them explicitly.

> **Note** — these changes are backwards-compatible with the current
> dataset: the existing entries already follow the intended order and
> patterns. Applying them tightens validation without requiring data
> changes. In an automated CI run, they should be proposed as a separate
> pull request rather than applied inline.

## §C4 — Enforce `source_section` pattern at every level

Currently `validate.py` only enforces the
`^(Table|Section|Chapter|Page|Figure)\s` pattern on `evidence.section`.
Extend the check to top-level `CommandEntry.source_section` and to
`VersionEntry.source_section` when `source_same_as_representative` is
`false`.

Suggested code (insert inside `validate_entry`):

```python
def _check_source_section(label, value, errors):
    if not value:
        errors.append(f"{label}: source_section is required")
    elif not SECTION_RE.match(value):
        errors.append(f"{label}: source_section does not match "
                      "^(Table|Section|Chapter|Page|Figure)\\s pattern")

_check_source_section(cmd, e.get("source_section"), errors)
for ve in vspec:
    if ve.get("source_same_as_representative") is False:
        _check_source_section(f"{cmd}/{ve.get('version')}",
                              ve.get("source_section"), errors)
```

## §C10 — Order of `version_reviews`

Currently only `version_specific` is checked for ascending order. Extend
the check to `version_reviews`.

Suggested code (insert inside `validate_entry` after `vspec` loop):

```python
review_orders = [version_order.get(r.get("version"), -1)
                 for r in (e.get("version_reviews") or [])]
if review_orders != sorted(review_orders):
    errors.append(f"{cmd}: version_reviews not sorted by version order")
```

## §C22 — Order of `timeouts` array (DR-17)

Enforce the canonical order for the `timeouts` array, both top-level and
inside `version_specific`.

Suggested code (add near the top of `validate.py`):

```python
TIMEOUT_ORDER = [
    "prompt_timeout", "send_timeout", "max_response_time",
    "max_timeout", "urc_report_timeout", "boot_time",
    "init_delay", "hardware_settle_time", "min_delay",
    "max_wait", "retry_interval",
]

def _check_timeout_order(label, timeouts, errors):
    index = {k: i for i, k in enumerate(TIMEOUT_ORDER)}
    idx = [index.get(t.get("timeout_kind"), 999) for t in timeouts]
    if idx != sorted(idx):
        errors.append(f"{label}: timeouts array is not in DR-17 order")
```

Suggested call sites (inside `validate_entry`):

```python
_check_timeout_order(cmd, e.get("timeouts") or [], errors)
for ve in vspec:
    _check_timeout_order(f"{cmd}/{ve.get('version')}",
                         ve.get("timeouts") or [], errors)
```

## §C23 — `explicitly_removed` at top level

Currently no explicit check prevents `presence_status_latest` from being
`explicitly_removed`. Add a hard rule:

```python
if pres == "explicitly_removed":
    errors.append(f"{cmd}: presence_status_latest must not be "
                  "'explicitly_removed' (only allowed in version_specific)")
```