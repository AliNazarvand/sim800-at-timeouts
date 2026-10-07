#!/usr/bin/env python3
"""Phase-10: populate version_reviews + remove unverifiable placeholders.

Reads build/version_analysis/corrections.json produced by Phase-9.

Two actions per entry:
  A) If the representative version's extracted status is "present" and the
     extracted ms equals the current YAML ms, then for every non-representative
     version whose extracted status is also "present" with the same ms, add
     an "approved_present_equivalent" VersionReview with evidence page taken
     from the extraction.

  B) If a version is not extractable from any PDF (all three show
     section_not_found), the entry is treated as an unverifiable placeholder
     and removed from data/*.yaml and from command_inventory.yaml.

After the changes, metadata.review_scope and metadata.pending_versions are
recomputed so that validate.py stays happy.
"""
import argparse, copy, json, os, shutil, sys
try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr); sys.exit(1)

ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR  = os.path.join(ROOT, "data")
BUILD_DIR = os.path.join(ROOT, "build", "version_analysis")
DOCS_DIR  = os.path.join(ROOT, "docs")

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

    corr_path = os.path.join(BUILD_DIR, "corrections.json")
    if not os.path.exists(corr_path):
        print(f"Missing {corr_path}; run Phase-9 first.", file=sys.stderr)
        sys.exit(1)
    with open(corr_path, encoding="utf-8") as f:
        corrections = json.load(f)

    versions_path = os.path.join(DATA_DIR, "versions.yaml")
    vd = load_yaml(versions_path)
    versions = [v["id"] for v in vd["versions"]]
    order = {v: i for i, v in enumerate(versions)}

    corr_index = {}
    for c in corrections["entries"]:
        corr_index.setdefault(c["file"], {})[c["command"]] = c

    report = {"reviews_added": [], "removed": [], "files_touched": []}

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

        by_cmd = corr_index.get(fname, {})
        new_entries = []
        file_reviews = 0
        file_removed = 0

        for e in entries:
            cmd = e.get("command")
            c = by_cmd.get(cmd)
            if not c:
                new_entries.append(e)
                continue

            rep = e.get("representative_version")
            rep_res = c["per_version"].get(rep, {})

            # ---- Action B: removal ----
            all_ns = all(
                c["per_version"].get(v, {}).get("status") == "section_not_found"
                for v in c["per_version"]
            )
            if rep_res.get("status") == "section_not_found" and all_ns:
                report["removed"].append({
                    "file": fname, "command": cmd,
                    "reason": "section header not found in any PDF"})
                file_removed += 1
                continue

            # ---- Action A: reviews ----
            if rep_res.get("status") != "present":
                new_entries.append(e)
                continue

            cur_ms = None
            for tv in (e.get("timeouts") or []):
                if tv.get("timeout_kind") == "max_response_time":
                    cur_ms = tv.get("max_value_ms")
                    break
            if cur_ms is None or rep_res.get("ms") != cur_ms:
                new_entries.append(e)
                continue

            existing = {r.get("version") for r in (e.get("version_reviews") or [])}
            new_reviews = list(e.get("version_reviews") or [])
            for v in (e.get("available_in_versions") or []):
                if v == rep or v in existing:
                    continue
                vres = c["per_version"].get(v, {})
                if vres.get("status") == "present" and vres.get("ms") == cur_ms:
                    page = vres.get("page") or 1
                    new_reviews.append({
                        "version": v,
                        "status": "approved_present_equivalent",
                        "evidence": {
                            "section": f"Page {page}",
                            "page": int(page),
                            "note": "Auto-verified from PDF; MRT matches representative.",
                            "compared_to_version": rep,
                        },
                    })
                    file_reviews += 1

            new_reviews.sort(key=lambda r: order.get(r.get("version"), 999))
            e["version_reviews"] = new_reviews
            new_entries.append(e)

        if not (file_reviews or file_removed):
            continue

        report["files_touched"].append(fname)
        data["entries"] = new_entries

        # ---- Recompute metadata ----
        pending = compute_pending_union(new_entries, versions)
        md = data.setdefault("metadata", {})
        if not pending:
            md["review_scope"] = "complete"
            md["pending_versions"] = []
        else:
            md["review_scope"] = "partial"
            md["pending_versions"] = sorted(pending)

        report["reviews_added"].append({"file": fname, "count": file_reviews})

        if args.apply:
            bak = path + ".pre_phase10.bak"
            if not os.path.exists(bak):
                shutil.copy2(path, bak)
            dump_yaml(path, data)

    # ---- Update command_inventory.yaml for removals ----
    removed_cmds = {r["command"] for r in report["removed"]}
    if removed_cmds:
        inv_path = os.path.join(DATA_DIR, "command_inventory.yaml")
        inv = load_yaml(inv_path)
        changed_inv = False
        for chap in inv.get("chapters") or []:
            cmds = chap.get("commands") or []
            filtered = [c for c in cmds if c not in removed_cmds]
            if filtered != cmds:
                chap["commands"] = filtered
                changed_inv = True
        if changed_inv and args.apply:
            bak = inv_path + ".pre_phase10.bak"
            if not os.path.exists(bak):
                shutil.copy2(inv_path, bak)
            dump_yaml(inv_path, inv)
            report["command_inventory_updated"] = True

    # ---- Write reports ----
    with open(os.path.join(BUILD_DIR, "phase10_report.json"),
              "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    lines = ["# Phase-10 Report", ""]
    lines.append(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    lines.append("")
    lines.append("## Reviews added")
    lines.append("")
    if report["reviews_added"]:
        lines.append("| file | new approved_present_equivalent reviews |")
        lines.append("|------|----------------------------------------:|")
        for r in report["reviews_added"]:
            lines.append(f"| {r['file']} | {r['count']} |")
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("## Entries removed (unverifiable placeholders)")
    lines.append("")
    if report["removed"]:
        lines.append("| file | command | reason |")
        lines.append("|------|---------|--------|")
        for r in report["removed"]:
            lines.append(f"| {r['file']} | {r['command']} | {r['reason']} |")
    else:
        lines.append("(none)")
    lines.append("")

    with open(os.path.join(DOCS_DIR, "review_population.md"),
              "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

    total_reviews = sum(r["count"] for r in report["reviews_added"])
    print(f"[phase10] reviews added: {total_reviews}")
    print(f"[phase10] entries removed: {len(report['removed'])}")
    print(f"[phase10] files touched: {len(report['files_touched'])}")
    print(f"[phase10] wrote docs\\review_population.md")


if __name__ == "__main__":
    main()