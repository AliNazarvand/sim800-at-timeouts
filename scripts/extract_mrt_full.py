#!/usr/bin/env python3
"""Phase-9: normalize whitespace AND allow newlines after the label.

Combines Phase-7 (newline tolerance) + Phase-8 (whitespace normalization).

Label forms handled:
    "Max Response Time 85 seconds"
    "Max Response Time\n85 seconds"
    "Max Response Time\n\n85 seconds"
    "Max\nResponse\nTime\n85 seconds"
    "Max\nResponse\nTime\n-"             -> not_mentioned

Value forms:
    "85 seconds" / "85 s" / "85s"
    "85000 ms"
    "-"  (dash)                          -> not_mentioned
"""
import argparse, json, os, re, shutil, sys
try:
    import fitz
except ImportError:
    print("PyMuPDF required: pip install PyMuPDF", file=sys.stderr); sys.exit(1)
try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr); sys.exit(1)

ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR  = os.path.join(ROOT, "data")
CACHE_DIR = os.path.join(ROOT, ".cache", "sources")
DOCS_DIR  = os.path.join(ROOT, "docs")
BUILD_DIR = os.path.join(ROOT, "build", "version_analysis")

SKIP_FILES = {
    "versions.yaml","chapter_mapping.yaml","category_mapping.yaml",
    "command_inventory.yaml","module_compatibility.yaml",
}
PDFS = {
    "V1.01": "SIM800 Series_AT Command Manual_V1.01.pdf",
    "V1.10": "SIM800 Series_AT Command Manual_V1.10.pdf",
    "V1.12": "SIM800 Series_AT Command Manual_V1.12.pdf",
}

HEADER_RE = re.compile(
    r"^[ \t]*(\d+(?:\.\d+)+)[ \t]+(AT\+[A-Z][A-Z0-9]+)\b[^\n]*",
    re.MULTILINE)


def normalize_pdf_text(text):
    """Collapse 'Max\\nResponse\\nTime' -> 'Max Response Time'."""
    if not text:
        return text
    t = text
    for _ in range(3):
        new = t
        new = re.sub(
            r"Max\b\s*\n?\s*Response\b\s*\n?\s*Time\b",
            "Max Response Time", new, flags=re.I)
        new = re.sub(
            r"Response\b\s*\n?\s*Time\b",
            "Response Time", new, flags=re.I)
        if new == t:
            break
        t = new
    return t


# CRITICAL: allow 0, 1 or 2 newlines between "Time" and the value.
# This is the fix that Phase-8 missed.
MRT_RE = re.compile(
    r"Max\s+Response\s+Time[ \t:]*"
    r"(?:\r?\n[ \t]*){0,2}"           # 0, 1 or 2 newlines
    r"([^\n\r]*)",
    re.I)


def ms_from(val_line):
    v = (val_line or "").strip()
    if not v:
        return None, "unparseable"
    # dash -> not_mentioned
    if re.match(r"^[\-\u2013\u2014](?:\s|$)", v) and not re.match(r"^-\s*\d", v):
        return None, "not_mentioned"
    if v in ("-", "\u2013", "\u2014"):
        return None, "not_mentioned"
    m = re.match(r"^(\d+(?:\.\d+)?)\s*([A-Za-z]*)", v)
    if not m:
        return None, "unparseable"
    num = float(m.group(1))
    unit = m.group(2).lower()
    if unit.startswith("ms") or unit.startswith("millisecond"):
        return int(num), "present"
    if unit.startswith("s") or unit.startswith("sec"):
        return int(num * 1000), "present"
    if unit.startswith("min"):
        return int(num * 60000), "present"
    # no unit -> assume seconds
    return int(num * 1000), "present"


def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def dump_yaml(p, data):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)


def load_pdf(path):
    doc = fitz.open(path)
    chunks = []
    offsets = []
    pos = 0
    for i in range(doc.page_count):
        txt = doc.load_page(i).get_text("text") or ""
        offsets.append((pos, i + 1))
        norm = normalize_pdf_text(txt)
        chunks.append(norm)
        chunks.append("\n")
        pos += len(norm) + 1
    doc.close()
    return "".join(chunks), offsets


def page_at(offsets, off):
    for i in range(len(offsets) - 1, -1, -1):
        if offsets[i][0] <= off:
            return offsets[i][1]
    return 0


def find_best_section(full_text, cmd):
    target_re = re.compile(
        r"^[ \t]*(\d+(?:\.\d+)+)[ \t]+(" + re.escape(cmd) + r")\b[^\n]*",
        re.MULTILINE)
    headers = list(HEADER_RE.finditer(full_text))
    candidates = []
    for m in target_re.finditer(full_text):
        end = len(full_text)
        for h in headers:
            if h.start() > m.end():
                end = h.start(); break
        body = full_text[m.start():min(end, m.start() + 8000)]
        score = 0
        head = body[:900]
        if re.search(r"\bResponse\b",  head, re.I): score += 5
        if re.search(r"\bExecution\b", head, re.I): score += 3
        if re.search(r"\bTest\s+Command\b", head, re.I): score += 2
        if re.search(r"\bSyntax\b",    head, re.I): score += 2
        if "...." in body[:400]: score -= 20
        if len(body) < 120:      score -= 5
        candidates.append((score, m.start(), body))
    if not candidates:
        return None
    candidates.sort(key=lambda x: (-x[0], x[1]))
    _, start, body = candidates[0]
    return start, body


def extract_mrt(full_text, offsets, cmd):
    sec = find_best_section(full_text, cmd)
    if sec is None:
        return {"status": "section_not_found"}
    start, body = sec
    m = MRT_RE.search(body)
    if not m:
        return {"status": "no_mrt_label",
                "page": page_at(offsets, start)}
    raw = m.group(1)
    ms, kind = ms_from(raw)
    page = page_at(offsets, start + m.start())
    if kind == "not_mentioned":
        return {"status": "not_mentioned", "page": page, "raw": raw.strip()}
    if kind == "present":
        return {"status": "present", "ms": ms, "page": page, "raw": raw.strip()}
    return {"status": "unparseable", "page": page, "raw": raw.strip()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    pdf_cache = {}
    for ver, fname in PDFS.items():
        path = os.path.join(CACHE_DIR, fname)
        print(f"[load] {ver}: {fname}")
        pdf_cache[ver] = load_pdf(path)

    os.makedirs(DOCS_DIR, exist_ok=True)
    os.makedirs(BUILD_DIR, exist_ok=True)

    report = {"entries": [], "summary": {}}
    total = 0
    kept = 0
    changed = 0
    not_mentioned_confirmed = 0
    skipped = 0

    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".yaml") or fname in SKIP_FILES:
            continue
        if ".bak" in fname:
            continue
        path = os.path.join(DATA_DIR, fname)
        data = load_yaml(path)
        entries = data.get("entries") or []
        entry_changes = []
        for e in entries:
            cmd = e.get("command") or ""
            if not cmd.startswith("AT+"):
                continue
            total += 1
            cur_tv = (e.get("timeouts") or [None])[0]
            cur_ms = cur_tv.get("max_value_ms") if cur_tv else None
            cur_pres = e.get("presence_status_latest")
            e_rep = {
                "file": fname,
                "command": cmd,
                "current": {
                    "presence_status_latest": cur_pres,
                    "max_value_ms": cur_ms,
                },
                "per_version": {},
            }
            for ver in PDFS.keys():
                full_text, offsets = pdf_cache[ver]
                res = extract_mrt(full_text, offsets, cmd)
                e_rep["per_version"][ver] = res

            rep = e.get("representative_version")
            rep_res = e_rep["per_version"].get(rep, {})
            action = "keep"
            if rep_res.get("status") == "not_mentioned":
                if cur_pres != "not_mentioned" or cur_ms is not None:
                    action = "set_not_mentioned"
                    not_mentioned_confirmed += 1
                else:
                    kept += 1
            elif rep_res.get("status") == "present":
                new_ms = rep_res.get("ms")
                if new_ms != cur_ms:
                    action = "set_ms"
                    e_rep["new_max_value_ms"] = new_ms
                    changed += 1
                else:
                    kept += 1
            else:
                action = "skip_" + (rep_res.get("status") or "unknown")
                skipped += 1

            e_rep["action"] = action
            if action not in ("keep",):
                entry_changes.append(e_rep)
            report["entries"].append(e_rep)

        if entry_changes and args.apply:
            import copy
            new_data = copy.deepcopy(data)
            for e_new, e_old in zip(new_data.get("entries") or [], entries):
                cmd = e_old.get("command") or ""
                for ch in entry_changes:
                    if ch["command"] != cmd:
                        continue
                    if ch["action"] == "set_not_mentioned":
                        e_new["timeouts"] = []
                        e_new["presence_status_latest"] = "not_mentioned"
                        e_new["extraction_status_latest"] = "not_specified"
                    elif ch["action"] == "set_ms":
                        new_ms = ch["new_max_value_ms"]
                        e_new["timeouts"] = [{
                            "timeout_kind": "max_response_time",
                            "min_value_ms": None,
                            "max_value_ms": new_ms,
                            "nominal_value_ms": None,
                            "recommended_value_ms": None,
                            "default_value_ms": None,
                        }]
                        e_new["presence_status_latest"] = "present"
                        e_new["extraction_status_latest"] = "extracted_from_table"
                    break
            bak = path + ".pre_phase9.bak"
            if not os.path.exists(bak):
                shutil.copy2(path, bak)
            dump_yaml(path, new_data)

    report["summary"] = {
        "total_at_entries": total,
        "kept": kept,
        "changed": changed,
        "not_mentioned_confirmed": not_mentioned_confirmed,
        "skipped": skipped,
    }
    with open(os.path.join(BUILD_DIR, "corrections.json"),
              "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    lines = ["# Data Corrections Report (Phase-9)", ""]
    lines.append(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    lines.append(f"Total AT entries: {total}")
    lines.append(f"  kept           : {kept}")
    lines.append(f"  changed (ms)   : {changed}")
    lines.append(f"  not_mentioned  : {not_mentioned_confirmed}")
    lines.append(f"  skipped        : {skipped}")
    lines.append("")
    lines.append("| file | command | V1.01 | V1.10 | V1.12 | current_ms | current_pres | action |")
    lines.append("|------|---------|-------|-------|-------|-----------:|--------------|--------|")
    def cell(res):
        s = res.get("status")
        if s == "present":       return f"present={res['ms']}"
        if s == "not_mentioned": return "not_mentioned"
        return s or "?"
    for e in report["entries"]:
        row = [e["file"], e["command"],
               cell(e["per_version"].get("V1.01", {})),
               cell(e["per_version"].get("V1.10", {})),
               cell(e["per_version"].get("V1.12", {})),
               str(e["current"]["max_value_ms"]),
               str(e["current"]["presence_status_latest"]),
               e["action"]]
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")
    with open(os.path.join(DOCS_DIR, "data_corrections.md"),
              "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

    print(f"[phase9] total: {total}  kept: {kept}  "
          f"changed: {changed}  not_mentioned: {not_mentioned_confirmed}  "
          f"skipped: {skipped}")
    print(f"[phase9] wrote docs\\data_corrections.md")


if __name__ == "__main__":
    main()