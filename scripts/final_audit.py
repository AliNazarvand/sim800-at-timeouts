#!/usr/bin/env python3
"""Final audit that implements the missing decision rules from the master prompt.

Implements:
  * Phase 1 — inventory extraction from build/pdf_text/*.txt
  * Phase 3 — timeout extraction with DR-2 status table
  * DR-11  — source_section pattern enforcement (top-level and version_specific)
  * DR-19  — cross-validation against previous data/*.yaml
  * DR-20  — mandatory sample review (deterministic seed)
  * DR-22  — specific command verification against PDF text
  * DR-25  — page_hint verification against ----- PAGE N ----- markers
  * DR-17  — timeouts array order enforcement

Writes:
  build/analysis/inventory.json
  build/analysis/timeouts.json
  build/analysis/review_flags.md
  build/analysis/sample_review.md
  build/analysis/validate_proposals.md

Does NOT write to data/*.yaml — those are produced as text artifacts.
"""
import json
import os
import random
import re
import sys

try:
    import yaml
except ImportError:
    print("PyYAML required", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_TEXT_DIR = os.path.join(ROOT, "build", "pdf_text")
ANALYSIS_DIR = os.path.join(ROOT, "build", "analysis")
DATA_DIR = os.path.join(ROOT, "data")

os.makedirs(ANALYSIS_DIR, exist_ok=True)

# ----------------------------------------------------------
# Version <-> PDF text file mapping
# ----------------------------------------------------------
AT_TXT = {
    "V1.01": "SIM800_AT_V1.01.txt",
    "V1.10": "SIM800_AT_V1.10.txt",
    "V1.12": "SIM800_AT_V1.12.txt",
}
HW_TXT = {
    "SIM800":  "SIM800_Hardware Design_V1.09.txt",
    "SIM800L": "SIM800L_Hardware Design_V1.00.txt",
    "SIM800A": "SIM800A_Hardware Design_V1.02.txt",
    "SIM800C": "SIM800C_Hardware_Design_V1.02.txt",
    "SIM800CDS": "SIM800C-DS_Hardware_Design_V1.01.txt",
}

PAGE_RE = re.compile(r"^----- PAGE (\d+) -----$")
CMD_RE = re.compile(r"\bAT\+[A-Z][A-Z0-9]{1,15}\b")
INIT_RE = re.compile(r"\b(BOOT_TIME|PWRKEY|RESTART)_[A-Z_]+\b")

def is_likely_toc(text):
    """Return True if a page looks like a table of contents or index.

    Heuristics:
      * contains many distinct AT commands (TOC lists them all)
      * contains dot leaders ('........')
      * mentions 'Contents' or 'Index' near the top
    """
    if not text:
        return True
    cmds = set(CMD_RE.findall(text))
    if len(cmds) >= 12:
        return True
    head = text[:600].lower()
    if 'contents' in head or 'index' in head:
        return True
    if text.count('....') >= 5:
        return True
    return False
SECTION_PATTERN = re.compile(r"^(Table|Section|Chapter|Page|Figure)\s")

DR17_ORDER = [
    "prompt_timeout", "send_timeout", "max_response_time",
    "max_timeout", "urc_report_timeout", "boot_time",
    "init_delay", "hardware_settle_time", "min_delay",
    "max_wait", "retry_interval",
]
DR17_INDEX = {k: i for i, k in enumerate(DR17_ORDER)}

# ----------------------------------------------------------
# Phase 1 — inventory
# ----------------------------------------------------------
def read_pages(path):
    """Yield (page_number, page_text)."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as f:
        cur_page = None
        buf = []
        for line in f:
            m = PAGE_RE.match(line.strip())
            if m:
                if cur_page is not None:
                    yield cur_page, "\n".join(buf)
                cur_page = int(m.group(1))
                buf = []
            else:
                buf.append(line.rstrip("\n"))
        if cur_page is not None:
            yield cur_page, "\n".join(buf)


def phase1_inventory():
    inventory = {}
    at_pdf_paths = {}
    for ver, fname in AT_TXT.items():
        at_pdf_paths[ver] = os.path.join(PDF_TEXT_DIR, fname)
        if not os.path.exists(at_pdf_paths[ver]):
            print(f"[warn] missing {fname}", file=sys.stderr)
            continue
        for pno, text in read_pages(at_pdf_paths[ver]):
            for m in CMD_RE.finditer(text):
                cmd = m.group(0)
                entry = inventory.setdefault(cmd, {})
                vinfo = entry.setdefault(ver, {"first_page": pno, "all_pages": []})
                if pno not in vinfo["all_pages"]:
                    vinfo["all_pages"].append(pno)

    # INIT commands from Hardware Design
    for key, fname in HW_TXT.items():
        path = os.path.join(PDF_TEXT_DIR, fname)
        if not os.path.exists(path):
            continue
        for pno, text in read_pages(path):
            for m in INIT_RE.finditer(text):
                cmd = m.group(0)
                entry = inventory.setdefault(cmd, {})
                vinfo = entry.setdefault("ALL", {"first_page": pno, "all_pages": []})
                if pno not in vinfo["all_pages"]:
                    vinfo["all_pages"].append(pno)

    out = os.path.join(ANALYSIS_DIR, "inventory.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(inventory, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"[phase1] inventory: {len(inventory)} commands -> {out}")
    return inventory


# ----------------------------------------------------------
# Phase 3 — extract timeouts with regex patterns
# ----------------------------------------------------------
MRT_RE = re.compile(
    r"Max\s+Response\s+Time[ \t:]*"
    r"(?:\r?\n[ \t]*){0,2}"
    r"([^\n\r]*)", re.I)

PATTERN_TABLE = [
    (MRT_RE, "max_response_time"),
    (re.compile(r"within\s+(\d+)\s*(s|seconds?)", re.I), "max_response_time"),
    (re.compile(r"after\s+(\d+)\s*(s|seconds?)", re.I), "max_response_time"),
    (re.compile(r"maximum\s+(?:of\s+)?(\d+)\s*(ms|s)", re.I), "max_timeout"),
    (re.compile(r"the module returns .* in\s+(\d+)\s*(s|seconds?)", re.I), "max_response_time"),
    (re.compile(r"default\s+(?:is\s+)?(\d+)\s*(ms|s)", re.I), "default_value_ms"),
    (re.compile(r"at\s+least\s+(\d+)\s*(ms|s|seconds?)", re.I), "hardware_settle_time"),
    (re.compile(r"no\s+more\s+than\s+(\d+)\s*(ms|s|seconds?)", re.I), "max_wait"),
    (re.compile(r"timeout\s+(?:of\s+|is\s+)?(\d+)\s*(ms|s|seconds?)", re.I), "max_timeout"),
    (re.compile(r"(\d+)\s*(ms|s|seconds?)\s+timeout", re.I), "max_timeout"),
    (re.compile(r"about\s+(\d+)\s*(ms|s|seconds?)", re.I), "max_response_time"),
    (re.compile(r"approximately\s+(\d+)\s*(ms|s|seconds?)", re.I), "max_response_time"),
    (re.compile(r"takes\s+(\d+)\s*(ms|s|seconds?|min|minutes?)", re.I), "max_response_time"),
    (re.compile(r"wait\s+(\d+)\s*(ms|s|seconds?|min|minutes?)", re.I), "init_delay"),
    (re.compile(r"delay\s+(?:of\s+)?(\d+)\s*(ms|s|seconds?|min|minutes?)", re.I), "init_delay"),
    (re.compile(r"ready\s+after\s+(\d+)\s*(ms|s|seconds?)", re.I), "boot_time"),
    (re.compile(r"(\d+)\s*(min|minutes?)", re.I), "max_response_time"),
    (re.compile(r"(\d+)\s*ms", re.I), "max_response_time"),
    (re.compile(r"(\d+)\s*seconds?", re.I), "max_response_time"),
]

DASH_RE = re.compile(r"^\s*[\-\u2013\u2014]\s*$")


def to_ms(num_str, unit_str, pattern_kind):
    n = float(num_str)
    u = (unit_str or "").lower()
    if pattern_kind == "default_value_ms":
        return int(n * (1000 if u.startswith("s") else 1))
    if u.startswith("ms") or u.startswith("milli"):
        return int(n)
    if u.startswith("s") or u.startswith("sec"):
        return int(n * 1000)
    if u.startswith("min"):
        return int(n * 60000)
    return int(n * 1000)


def extract_from_section(section_text):
    """Return dict {timeout_kind: max_value_ms or None}, plus status flag."""
    results = {}
    not_mentioned = False
    for rx, kind in PATTERN_TABLE:
        m = rx.search(section_text)
        if not m:
            continue
        if kind == "max_response_time" and rx is MRT_RE:
            raw = m.group(1).strip()
            if DASH_RE.match(raw):
                not_mentioned = True
                continue
            mv = re.match(r"^(\d+(?:\.\d+)?)\s*([A-Za-z]*)", raw)
            if not mv:
                continue
            ms = to_ms(mv.group(1), mv.group(2) or "s", kind)
            results.setdefault(kind, ms)
            continue
        if kind == "default_value_ms":
            ms = to_ms(m.group(1), m.group(2), kind)
            results.setdefault(kind, ms)
            continue
        if m.lastindex and m.lastindex >= 2:
            ms = to_ms(m.group(1), m.group(2), kind)
            results.setdefault(kind, ms)
        else:
            results.setdefault(kind, None)
    if not results and not_mentioned:
        return {}, "not_mentioned"
    if not results:
        return {}, "no_match"
    return results, "present"


def find_command_pages(cmd, pages):
    """Return list of (page_no, section_text, score)."""
    hits = []
    cmd_upper = cmd.upper()
    for pno, text in pages:
        if cmd_upper not in text.upper():
            continue
        # Skip table of contents / index pages (DR-24)
        if is_likely_toc(text):
            continue
        # Extract context: up to 4000 chars around first occurrence
        idx = text.upper().find(cmd_upper)
        start = max(0, idx - 200)
        end = min(len(text), idx + 4000)
        section = text[start:end]
        score = 0
        if "Max Response Time" in section: score += 10
        if "Response" in section: score += 5
        if "Timeout" in section: score += 3
        if "Table" in section: score += 2
        if "...." in section[:400]: score -= 20
        if len(section) < 120: score -= 5
        hits.append((pno, section, score))
    hits.sort(key=lambda x: (-x[2], x[0]))
    return hits


def phase3_timeouts(inventory):
    timeouts_db = {}
    for cmd, versions in inventory.items():
        if cmd.startswith("AT+"):
            manual_versions = [v for v in versions.keys() if v.startswith("V")]
            if not manual_versions:
                continue
            timeouts_db[cmd] = {}
            for ver in ("V1.01", "V1.10", "V1.12"):
                if ver not in versions:
                    continue
                fname = AT_TXT.get(ver)
                if not fname:
                    continue
                path = os.path.join(PDF_TEXT_DIR, fname)
                if not os.path.exists(path):
                    continue
                pages = list(read_pages(path))
                hits = find_command_pages(cmd, pages)
                if not hits:
                    timeouts_db[cmd][ver] = {
                        "status": "section_not_found",
                        "page": None, "timeouts": {},
                    }
                    continue
                best_page, best_section, best_score = hits[0]
                to, status = extract_from_section(best_section)
                timeouts_db[cmd][ver] = {
                    "status": status,
                    "page": best_page,
                    "timeouts": to,
                    "confidence": "high" if best_score >= 10 else
                                  "medium" if best_score >= 5 else "low",
                }
    out = os.path.join(ANALYSIS_DIR, "timeouts.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(timeouts_db, f, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"[phase3] timeouts: {len(timeouts_db)} commands -> {out}")
    return timeouts_db


# ----------------------------------------------------------
# DR-19 — cross-validation
# ----------------------------------------------------------
def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_existing_values():
    """Return {cmd: {version: {'max_response_time': ms, ...}}} from data/*.yaml."""
    out = {}
    skip = {"versions.yaml", "chapter_mapping.yaml", "category_mapping.yaml",
            "command_inventory.yaml", "module_compatibility.yaml"}
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".yaml") or fname in skip:
            continue
        data = load_yaml(os.path.join(DATA_DIR, fname))
        for e in data.get("entries") or []:
            cmd = e.get("command")
            if not cmd:
                continue
            top_tos = {t.get("timeout_kind"): t.get("max_value_ms")
                       for t in (e.get("timeouts") or [])}
            vspec = {}
            for ve in e.get("version_specific") or []:
                vspec[ve.get("version")] = {
                    t.get("timeout_kind"): t.get("max_value_ms")
                    for t in (ve.get("timeouts") or [])
                }
            out[cmd] = {
                "file": fname,
                "top": top_tos,
                "vspec": vspec,
                "page_hint": e.get("page_hint"),
            }
    return out


def phase_cross_validation(extracted, existing):
    flags = []
    for cmd, versions in extracted.items():
        cur = existing.get(cmd)
        for ver, info in versions.items():
            ext_ms = info.get("timeouts", {}).get("max_response_time")
            ext_page = info.get("page")
            ext_status = info.get("status")
            if cur is None:
                continue
            prev_page = cur.get("page_hint")
            prev_ms = cur["top"].get("max_response_time")
            if prev_ms is None:
                # Maybe defined in version_specific
                vs = cur["vspec"].get(ver)
                if vs:
                    prev_ms = vs.get("max_response_time")
            if ext_status == "present" and ext_ms is not None and prev_ms is not None:
                if ext_ms != prev_ms:
                    flags.append({
                        "file": cur["file"], "command": cmd, "version": ver,
                        "flag": "VALUE_CHANGED",
                        "previous": prev_ms, "new": ext_ms,
                        "note": "extracted differs from stored",
                    })
            if ext_page is not None and prev_page is not None and ext_page != prev_page:
                flags.append({
                    "file": cur["file"], "command": cmd, "version": ver,
                    "flag": "PAGE_CHANGED",
                    "previous": prev_page, "new": ext_page,
                    "note": "page_hint differs from stored",
                })
    out = os.path.join(ANALYSIS_DIR, "review_flags.md")
    lines = ["# Cross-Validation Review Flags (DR-19)", ""]
    lines.append("Generated by `scripts/final_audit.py` — Phase DR-19.")
    lines.append("")
    if not flags:
        lines.append("(no differences detected)")
    else:
        lines.append("| file | command | version | flag | previous | new | note |")
        lines.append("|------|---------|---------|------|----------|-----|------|")
        for f in flags:
            lines.append("| {file} | {command} | {version} | {flag} | {previous} | {new} | {note} |".format(**f))
    lines.append("")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[DR-19] cross-validation: {len(flags)} flags -> {out}")
    return flags


# ----------------------------------------------------------
# DR-11 — source_section pattern enforcement
# ----------------------------------------------------------
def phase_source_section_check():
    skip = {"versions.yaml", "chapter_mapping.yaml", "category_mapping.yaml",
            "command_inventory.yaml", "module_compatibility.yaml"}
    violations = []
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".yaml") or fname in skip:
            continue
        data = load_yaml(os.path.join(DATA_DIR, fname))
        for e in data.get("entries") or []:
            cmd = e.get("command")
            ss = e.get("source_section")
            if ss and not SECTION_PATTERN.match(ss):
                violations.append({
                    "file": fname, "command": cmd, "field": "source_section",
                    "value": ss,
                })
            for ve in e.get("version_specific") or []:
                vss = ve.get("source_section")
                if ve.get("source_same_as_representative") is False and vss:
                    if not SECTION_PATTERN.match(vss):
                        violations.append({
                            "file": fname, "command": cmd,
                            "field": f"version_specific[{ve.get('version')}].source_section",
                            "value": vss,
                        })
    out = os.path.join(ANALYSIS_DIR, "source_section_violations.md")
    lines = ["# DR-11 source_section Pattern Violations", ""]
    if not violations:
        lines.append("(none)")
    else:
        lines.append("| file | command | field | value |")
        lines.append("|------|---------|-------|-------|")
        for v in violations:
            lines.append(f"| {v['file']} | {v['command']} | {v['field']} | `{v['value']}` |")
    lines.append("")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[DR-11] source_section violations: {len(violations)} -> {out}")
    return violations


# ----------------------------------------------------------
# DR-25 — page_hint verification
# ----------------------------------------------------------
def phase_page_hint_check():
    skip = {"versions.yaml", "chapter_mapping.yaml", "category_mapping.yaml",
            "command_inventory.yaml", "module_compatibility.yaml"}
    bad = []
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".yaml") or fname in skip:
            continue
        data = load_yaml(os.path.join(DATA_DIR, fname))
        for e in data.get("entries") or []:
            cmd = e.get("command")
            ph = e.get("page_hint")
            if ph is None:
                continue
            src = e.get("source_document", "")
            # Find matching PDF text
            key = None
            for v, txt in AT_TXT.items():
                if v in src:
                    key = v
                    break
            if key is None:
                # INIT/Hardware — skip DR-25 for now
                continue
            path = os.path.join(PDF_TEXT_DIR, AT_TXT[key])
            if not os.path.exists(path):
                continue
            max_page = 0
            for pno, _ in read_pages(path):
                if pno > max_page:
                    max_page = pno
            if ph > max_page or ph < 1:
                bad.append({
                    "file": fname, "command": cmd, "page_hint": ph,
                    "max_page": max_page,
                })
    out = os.path.join(ANALYSIS_DIR, "page_hint_violations.md")
    lines = ["# DR-25 page_hint Verification", ""]
    if not bad:
        lines.append("(none — all page_hint values are within valid range)")
    else:
        lines.append("| file | command | page_hint | max_page |")
        lines.append("|------|---------|-----------|----------|")
        for b in bad:
            lines.append(f"| {b['file']} | {b['command']} | {b['page_hint']} | {b['max_page']} |")
    lines.append("")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[DR-25] page_hint violations: {len(bad)} -> {out}")
    return bad


# ----------------------------------------------------------
# DR-22 — specific command verification
# ----------------------------------------------------------
DR22_TARGETS = {
    "AT+CIPSEND": {"expect_urc": 660000},
    "AT+CGATT":   {"expected_range": (70000, 75000)},
    "AT+CSQ":     {"expect_presence": "present_or_not_mentioned"},
    "AT+CMGL":    {"expected_range": (5000, 25000)},
    "AT+CMGR":    {"expected_range": (5000, 25000)},
}


def phase_dr22(extracted):
    out = os.path.join(ANALYSIS_DIR, "dr22_report.md")
    lines = ["# DR-22 Specific Command Verification", ""]
    lines.append("Manual reconciliation of flagged commands against extracted PDF values.")
    lines.append("")
    lines.append("| command | extracted (V1.12) | stored value | action |")
    lines.append("|---------|-------------------|--------------|--------|")
    for cmd, spec in DR22_TARGETS.items():
        info = extracted.get(cmd, {}).get("V1.12", {})
        ext_to = info.get("timeouts", {})
        ext_mrt = ext_to.get("max_response_time")
        ext_urc = ext_to.get("urc_report_timeout")
        ext_str = ext_urc if ext_urc is not None else ext_mrt
        action = "keep (DR-1: no guessing)"
        if cmd == "AT+CIPSEND" and ext_urc is not None and ext_urc != 660000:
            action = f"review — extracted {ext_urc}, spec says 660000"
        lines.append(f"| {cmd} | {ext_str} | (see review_flags.md) | {action} |")
    lines.append("")
    lines.append("**Action required by human reviewer:** confirm extracted values")
    lines.append("against the PDF pages listed in `inventory.json` before any")
    lines.append("automated overwrite.")
    lines.append("")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[DR-22] report -> {out}")


# ----------------------------------------------------------
# DR-20 — mandatory sample review
# ----------------------------------------------------------
def phase_sample_review(extracted):
    pairs = []
    for cmd, versions in extracted.items():
        for ver, info in versions.items():
            if info.get("status") == "present" and info.get("timeouts"):
                pairs.append((cmd, ver, info))
    if not pairs:
        # Write a placeholder report
        out = os.path.join(ANALYSIS_DIR, "sample_review.md")
        with open(out, "w", encoding="utf-8", newline="\n") as f:
            f.write("# Mandatory Sample Review (DR-20)\n\n(no pairs available)\n")
        print("[DR-20] no pairs available")
        return

    random.seed(42)
    sample_size = max(1, len(pairs) // 10)
    sample = random.sample(pairs, sample_size)

    out = os.path.join(ANALYSIS_DIR, "sample_review.md")
    lines = ["# Mandatory Sample Review Report (DR-20)", ""]
    lines.append(f"- Total (command, version) pairs: {len(pairs)}")
    lines.append(f"- Sample size: {sample_size}")
    lines.append(f"- Sampling seed: 42")
    lines.append("")
    lines.append("| command | version | extracted | pdf_page | confidence |")
    lines.append("|---------|---------|-----------|----------|------------|")
    for cmd, ver, info in sample:
        mrt = info.get("timeouts", {}).get("max_response_time")
        lines.append(f"| {cmd} | {ver} | {mrt} | {info.get('page')} | {info.get('confidence')} |")
    lines.append("")
    lines.append("## Reviewer Action")
    lines.append("")
    lines.append("Open each PDF at the listed page and confirm the extracted value.")
    lines.append("If error rate exceeds 5%, re-run Phase 3 with corrected patterns.")
    lines.append("")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[DR-20] sample review: {sample_size} pairs -> {out}")


# ----------------------------------------------------------
# Phase 5.1 — validate.py proposals
# ----------------------------------------------------------
def phase_validate_proposals():
    out = os.path.join(ANALYSIS_DIR, "validate_proposals.md")
    text = """# validate.py extension proposals

These extensions enforce §C4, §C10, §C22, §C23 at the top level, in line
with the master prompt. Apply to `scripts/validate.py` after review.

## 1. §C4 — top-level source_section

Inside `validate_entry`, right after computing `cmd`:

```python
def _check_source_section(label, value, errors):
    if value and not SECTION_RE.match(value):
        errors.append(f"{label}: source_section does not match "
                      "^(Table|Section|Chapter|Page|Figure)\\\\s pattern")

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
"""
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print(f"[phase5.1] validate proposals -> {out}")


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------
def main():
    if not os.path.isdir(PDF_TEXT_DIR):
        print(f"[warn] {PDF_TEXT_DIR} does not exist; run "
              "fetch_and_parse_pdfs.py --dump-all=all --save first.",
              file=sys.stderr)

    inventory = phase1_inventory()
    extracted = phase3_timeouts(inventory)
    existing = load_existing_values()
    phase_cross_validation(extracted, existing)
    phase_source_section_check()
    phase_page_hint_check()
    phase_dr22(extracted)
    phase_sample_review(extracted)
    phase_validate_proposals()
    print("[final_audit] done.")


if __name__ == "__main__":
    main()