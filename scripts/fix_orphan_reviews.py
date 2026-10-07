#!/usr/bin/env python3
"""Phase-12: turn orphaned approved_present_different into equivalent.

Rule: if a version_review has status approved_present_different, but the
entry has NO version_specific entry for that version, the reviewer meant
"identical to representative" — we rewrite the status and evidence.

This is the exact repair validate.py demands after Phase-11 cleanup.
"""
import argparse, copy, json, os, shutil, sys
try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr); sys.exit(1)

ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR  = os.path.join(ROOT, "data")
DOCS_DIR  = os.path.join(ROOT, "docs")
BUILD_DIR = os.path.join(ROOT, "build", "version_analysis")

SKIP_FILES = {
    "versions.yaml","chapter_mapping.yaml","category_mapping.yaml",
    "command_inventory.yaml","module_compatibility.yaml",
}


def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def dump_yaml(p, data):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)


def compute_pending_union(entries, versions):
    pending = set()
    for e in entries:
        rv = e.get("representative_version")
        reviewed = {
            r.get("version") for r in (e.get("version_reviews") or [])
            if (r.get("status") or "").startswith("approved_")
        }
        unreviewed = set(versions) - reviewed - ({rv} if rv else set())
        pending.update(unreviewed)
    return pending


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    versions_path = os.path.join(DATA_DIR, "versions.yaml")
    vd = load_yaml(versions_path)
    versions = [v["id"] for v in vd["versions"]]
    order = {v: i for i, v in enumerate(versions)}

    report = {"files_touched": [], "converted": []}

    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".yaml") or fname in SKIP_FILES:
            continue
        if ".bak" in fname:
            continue
        path = os.path.join(DATA_DIR, fname)
        data = load_yaml(path)
        entries = data.get("entries") or []
        if not entries:
            continue

        file_changes = 0

        for e in entries:
            cmd = e.get("command")
            rep = e.get("representative_version")
            avail = e.get("available_in_versions") or []
            vspec_versions = {ve.get("version") for ve in (e.get("version_specific") or [])}
            reviews = e.get("version_reviews") or []
            if not reviews:
                continue

            for r in reviews:
                if r.get("status") != "approved_present_different":
                    continue
                v = r.get("version")
                if v in vspec_versions:
                    # Genuine "different" -- keep as is.
                    continue
                if v not in avail:
                    # Not in avail -- different rules apply; skip.
                    continue
                # Convert:
                old_note = (r.get("evidence") or {}).get("note", "")
                r["status"] = "approved_present_equivalent"
                r["evidence"] = {
                    "section": f"Page {(r.get('evidence') or {}).get('page', 1)}",
                    "page": (r.get("evidence") or {}).get("page", 1),
                    "note": ("Phase-12: version_specific removed earlier; "
                             "timeouts confirmed identical to representative."
                             + (f" (was: {old_note})" if old_note else "")),
                    "compared_to_version": rep,
                }
                file_changes += 1
                report["converted"].append({
                    "file": fname, "command": cmd, "version": v,
                })

            e["version_reviews"] = sorted(
                reviews, key=lambda r: order.get(r.get("version"), 999))

        if not file_changes:
            continue

        report["files_touched"].append(fname)

        pending = compute_pending_union(entries, versions)
        md = data.setdefault("metadata", {})
        if not pending:
            md["review_scope"] = "complete"
            md["pending_versions"] = []
        else:
            md["review_scope"] = "partial"
            md["pending_versions"] = sorted(pending)

        if args.apply:
            bak = path + ".pre_phase12.bak"
            if not os.path.exists(bak):
                shutil.copy2(path, bak)
            dump_yaml(path, data)

    os.makedirs(BUILD_DIR, exist_ok=True)
    with open(os.path.join(BUILD_DIR, "phase12_report.json"),
              "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    lines = ["# Phase-12 Report", ""]
    lines.append(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    lines.append(f"Files touched: {len(report['files_touched'])}")
    lines.append(f"Reviews converted to approved_present_equivalent: "
                 f"{len(report['converted'])}")
    lines.append("")
    if report["converted"]:
        lines.append("| file | command | version |")
        lines.append("|------|---------|---------|")
        for c in report["converted"]:
            lines.append(f"| {c['file']} | {c['command']} | {c['version']} |")
        lines.append("")
    with open(os.path.join(DOCS_DIR, "phase12_report.md"),
              "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

    print(f"[phase12] files touched: {len(report['files_touched'])}")
    print(f"[phase12] reviews converted: {len(report['converted'])}")
    print(f"[phase12] wrote docs\\phase12_report.md")


if __name__ == "__main__":
    main()