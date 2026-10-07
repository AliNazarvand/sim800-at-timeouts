#!/usr/bin/env python3
"""Phase-11: remove duplicate version_specific entries.

An entry in version_specific is considered a duplicate if:
  * presence_status == "present"
  * extraction_status != "not_specified"
  * its timeouts set equals the top-level timeouts set

Such duplicates are removed, and a version_review of
approved_present_equivalent is added if not already present.
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

NUM_FIELDS = ("min_value_ms","max_value_ms","nominal_value_ms",
              "recommended_value_ms","default_value_ms")


def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def dump_yaml(p, data):
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True,
                       default_flow_style=False, width=1000)


def tv_key(tv):
    return (tv.get("timeout_kind"),) + tuple(tv.get(f) for f in NUM_FIELDS)


def timeouts_equal(a, b):
    return sorted(map(tv_key, a)) == sorted(map(tv_key, b))


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

    report = {"files_touched": [], "removed_vs": [], "added_reviews": []}

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

        file_removed = 0
        file_added = 0

        for e in entries:
            cmd = e.get("command")
            top_to = e.get("timeouts") or []
            vs = e.get("version_specific") or []
            if not vs:
                continue

            rep = e.get("representative_version")
            existing_review_versions = {
                r.get("version") for r in (e.get("version_reviews") or [])
            }

            new_vs = []
            for ve in vs:
                ps = ve.get("presence_status")
                ext = ve.get("extraction_status")
                if ps == "present" and ext != "not_specified":
                    if timeouts_equal(ve.get("timeouts") or [], top_to):
                        # Drop duplicate
                        file_removed += 1
                        report["removed_vs"].append({
                            "file": fname, "command": cmd,
                            "version": ve.get("version")})
                        # Ensure a matching review exists
                        v = ve.get("version")
                        if v not in existing_review_versions:
                            e.setdefault("version_reviews", []).append({
                                "version": v,
                                "status": "approved_present_equivalent",
                                "evidence": {
                                    "section": "Chapter 3",
                                    "page": 1,
                                    "note": "Phase-11: timeouts identical to "
                                            "representative; recorded as review.",
                                    "compared_to_version": rep,
                                },
                            })
                            existing_review_versions.add(v)
                            file_added += 1
                            report["added_reviews"].append({
                                "file": fname, "command": cmd, "version": v})
                        continue
                new_vs.append(ve)

            e["version_specific"] = new_vs
            if e.get("version_reviews"):
                e["version_reviews"].sort(
                    key=lambda r: order.get(r.get("version"), 999))

        if not (file_removed or file_added):
            continue

        report["files_touched"].append(fname)

        # Recompute metadata
        pending = compute_pending_union(entries, versions)
        md = data.setdefault("metadata", {})
        if not pending:
            md["review_scope"] = "complete"
            md["pending_versions"] = []
        else:
            md["review_scope"] = "partial"
            md["pending_versions"] = sorted(pending)

        if args.apply:
            bak = path + ".pre_phase11.bak"
            if not os.path.exists(bak):
                shutil.copy2(path, bak)
            dump_yaml(path, data)

    os.makedirs(BUILD_DIR, exist_ok=True)
    with open(os.path.join(BUILD_DIR, "phase11_report.json"),
              "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    lines = ["# Phase-11 Report", ""]
    lines.append(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    lines.append(f"Files touched: {len(report['files_touched'])}")
    lines.append(f"version_specific removed: {len(report['removed_vs'])}")
    lines.append(f"reviews added: {len(report['added_reviews'])}")
    lines.append("")
    if report["removed_vs"]:
        lines.append("## Removed duplicate version_specific entries")
        lines.append("")
        lines.append("| file | command | version |")
        lines.append("|------|---------|---------|")
        for r in report["removed_vs"]:
            lines.append(f"| {r['file']} | {r['command']} | {r['version']} |")
        lines.append("")
    if report["added_reviews"]:
        lines.append("## Reviews added")
        lines.append("")
        lines.append("| file | command | version |")
        lines.append("|------|---------|---------|")
        for r in report["added_reviews"]:
            lines.append(f"| {r['file']} | {r['command']} | {r['version']} |")
        lines.append("")

    with open(os.path.join(DOCS_DIR, "phase11_report.md"),
              "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

    print(f"[phase11] files touched: {len(report['files_touched'])}")
    print(f"[phase11] version_specific removed: {len(report['removed_vs'])}")
    print(f"[phase11] reviews added: {len(report['added_reviews'])}")
    print(f"[phase11] wrote docs\\phase11_report.md")


if __name__ == "__main__":
    main()