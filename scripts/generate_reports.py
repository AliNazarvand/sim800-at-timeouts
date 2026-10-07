#!/usr/bin/env python3
"""Generate coverage, sources-mapping and version-diff reports."""
import os
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
DOCS_DIR = os.path.join(ROOT, "docs")
SKIP_FILES = {
    "versions.yaml","chapter_mapping.yaml","category_mapping.yaml",
    "command_inventory.yaml","module_compatibility.yaml"
}

def load_yaml(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def ms_str(v):
    if v is None:
        return "?"
    return f"{v}ms"

def timeout_summary(timeouts):
    if not timeouts:
        return "-"
    parts = []
    for tv in timeouts:
        kind = tv.get("timeout_kind","?")
        mx = tv.get("max_value_ms")
        mn = tv.get("min_value_ms")
        nm = tv.get("nominal_value_ms")
        val = mx if mx is not None else (nm if nm is not None else (mn if mn is not None else None))
        parts.append(f"{kind}={ms_str(val)}" if val is not None else f"{kind}=unspec")
    return "; ".join(parts)

def gather_files():
    files = []
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".yaml") or fname in SKIP_FILES:
            continue
        files.append((fname, load_yaml(os.path.join(DATA_DIR, fname))))
    return files

def write_coverage(files, versions, global_latest):
    path = os.path.join(DOCS_DIR, "coverage_report.md")
    lines = ["# Coverage Report", ""]
    lines.append("## Section 1 — Extracted value coverage")
    lines.append("")
    lines.append("Coverage is computed **only over commands with")
    lines.append("`presence_status_latest: present`**, per acceptance criteria.")
    lines.append("Commands marked `not_mentioned` are excluded from the")
    lines.append("denominator (the PDF does not specify a timeout for them).")
    lines.append("")
    lines.append("| file | present | extracted | not_extracted | coverage |")
    lines.append("|------|--------:|----------:|--------------:|---------:|")
    total = 0
    extracted = 0
    for fname, data in files:
        ents = data.get("entries", []) or []
        present = [e for e in ents
                   if e.get("presence_status_latest") == "present"]
        n_total = len(present)
        n_ext = sum(1 for e in present
                    if e.get("extraction_status_latest","").startswith("extracted_"))
        total += n_total
        extracted += n_ext
        pct = f"{(100.0*n_ext/n_total):.1f}%" if n_total else "n/a"
        lines.append(f"| {fname} | {n_total} | {n_ext} | {n_total-n_ext} | {pct} |")
    overall = f"{(100.0*extracted/total):.1f}%" if total else "n/a"
    lines.append(f"| **TOTAL** | {total} | {extracted} | {total-extracted} | {overall} |")
    lines.append("")

    lines.append("## Section 2 — Version review status")
    lines.append("")
    lines.append("| file | command | representative | approved_* | pending_* | rejected_* |")
    lines.append("|------|---------|----------------|-----------|-----------|-----------|")
    for fname, data in files:
        for e in data.get("entries", []) or []:
            cmd = e.get("command","?")
            rv = e.get("representative_version","?")
            reviews = e.get("version_reviews", []) or []
            ap = [v.get("version") for v in reviews if (v.get("status") or "").startswith("approved_")]
            pd = [v.get("version") for v in reviews if v.get("status") == "pending_review"]
            rj = [v.get("version") for v in reviews if (v.get("status") or "").startswith("rejected_")]
            lines.append(f"| {fname} | {cmd} | {rv} | "
                         f"{', '.join(ap) or '-'} | {', '.join(pd) or '-'} | {', '.join(rj) or '-'} |")
    lines.append("")

    lines.append("## Section 3 — timeout_kind coverage")
    lines.append("")
    covered = set()
    for _, data in files:
        for e in data.get("entries", []) or []:
            for tv in e.get("timeouts", []) or []:
                covered.add(tv.get("timeout_kind"))
            for ve in e.get("version_specific", []) or []:
                for tv in ve.get("timeouts", []) or []:
                    covered.add(tv.get("timeout_kind"))
    all_kinds = {"max_response_time","prompt_timeout","send_timeout","max_timeout",
                 "min_delay","max_wait","boot_time","retry_interval",
                 "urc_report_timeout","init_delay","hardware_settle_time"}
    lines.append("Covered: " + ", ".join(sorted(k for k in covered if k)))
    gaps = sorted(all_kinds - covered)
    lines.append("")
    lines.append("Gaps: " + (", ".join(gaps) if gaps else "(none)"))
    lines.append("")

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[report] wrote {os.path.relpath(path, ROOT)}")

def write_sources_mapping(files):
    path = os.path.join(DOCS_DIR, "sources_mapping.md")
    lines = ["# Sources Mapping", "",
             "| file | command | representative_version | source_document | source_section | page_hint |",
             "|------|---------|-----------------------|-----------------|----------------|-----------|"]
    for fname, data in files:
        for e in data.get("entries", []) or []:
            lines.append("| {} | {} | {} | {} | {} | {} |".format(
                fname,
                e.get("command","?"),
                e.get("representative_version","?"),
                e.get("source_document","?"),
                e.get("source_section","?"),
                e.get("page_hint","-") if e.get("page_hint") is not None else "-",
            ))
    lines.append("")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[report] wrote {os.path.relpath(path, ROOT)}")

def write_version_diff(files, versions, global_latest):
    path = os.path.join(DOCS_DIR, "version_diff.md")
    header = ["command","representative_version","global_latest"] + versions + ["review_status"]
    lines = ["# Version Diff", "",
             "| " + " | ".join(header) + " |",
             "|" + "|".join(["---"]*len(header)) + "|"]
    for fname, data in files:
        for e in data.get("entries", []) or []:
            cmd = e.get("command","?")
            rv = e.get("representative_version","?")
            avail = set(e.get("available_in_versions") or [])
            vspec = {v.get("version"): v for v in (e.get("version_specific") or [])}
            reviews = {v.get("version"): v for v in (e.get("version_reviews") or [])}
            row = [cmd, rv, global_latest]
            for v in versions:
                if v not in avail:
                    row.append("absent")
                elif v in vspec:
                    ve = vspec[v]
                    ps = ve.get("presence_status")
                    if ps == "not_mentioned":
                        row.append("not_mentioned")
                    elif ps == "explicitly_removed":
                        row.append("explicitly_removed")
                    else:
                        row.append(timeout_summary(ve.get("timeouts") or []))
                else:
                    row.append("= representative")
            rev = reviews.get(rv)
            if rev:
                row.append(rev.get("status","-"))
            elif e.get("version_reviews"):
                row.append("(partial)")
            else:
                row.append("unreviewed")
            lines.append("| " + " | ".join(str(x) for x in row) + " |")
    lines.append("")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[report] wrote {os.path.relpath(path, ROOT)}")

def main():
    versions_path = os.path.join(DATA_DIR, "versions.yaml")
    vd = load_yaml(versions_path)
    versions = [v["id"] for v in vd["versions"]]
    global_latest = vd["latest"]
    files = gather_files()
    write_coverage(files, versions, global_latest)
    write_sources_mapping(files)
    write_version_diff(files, versions, global_latest)
    print("Reports generation complete.")

if __name__ == "__main__":
    main()
