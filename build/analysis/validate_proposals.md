# validate.py extension proposals

These extensions enforce §C4, §C10, §C22, §C23 at the top level, in line
with the master prompt. Apply to `scripts/validate.py` after review.

## 1. §C4 — top-level source_section

Inside `validate_entry`, right after computing `cmd`:

```python
def _check_source_section(label, value, errors):
    if value and not SECTION_RE.match(value):
        errors.append(f"{label}: source_section does not match "
                      "^(Table|Section|Chapter|Page|Figure)\\s pattern")

_check_source_section(cmd, e.get("source_section"), errors)
for ve in vspec:
    if ve.get("source_same_as_representative") is False:
        _check_source_section(f"{cmd}/{ve.get('version')}",
                              ve.get("source_section"), errors)
```

## 2. §C10 — version_reviews order

After the `vspec` loop in `validate_entry`:

```python
review_orders = [version_order.get(r.get("version"), -1)
                 for r in (e.get("version_reviews") or [])]
if review_orders != sorted(review_orders):
    errors.append(f"{cmd}: version_reviews not sorted by version order")
```

## 3. §C22 — timeouts array order (DR-17)

Add near the top of `validate.py`:

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

Call from `validate_entry`:

```python
_check_timeout_order(cmd, e.get("timeouts") or [], errors)
for ve in vspec:
    _check_timeout_order(f"{cmd}/{ve.get('version')}",
                         ve.get("timeouts") or [], errors)
```

## 4. §C23 — top-level explicitly_removed forbidden

In `validate_entry` after `pres` is read:

```python
if pres == "explicitly_removed":
    errors.append(f"{cmd}: presence_status_latest must not be "
                  "'explicitly_removed' (only allowed in version_specific)")
```
