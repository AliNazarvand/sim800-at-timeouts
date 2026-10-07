#!/usr/bin/env python3
"""Validate documentation examples in docs/examples/.

Reuses the validation rules from scripts/validate.py so that the same
rule set is applied to both data/ and docs/examples/.
"""
import os
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import validate as V  # noqa: E402

EX_DIR = os.path.join(ROOT, "docs", "examples")
REQUIRED_METADATA = {
    "description","schema_version","database_version",
    "review_scope","pending_versions","extracted_from",
}

def check_yaml(path, versions, version_order, global_latest, errors):
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except Exception as ex:
        errors.append(f"{path}: failed to parse YAML: {ex}")
        return
    if not isinstance(data, dict):
        errors.append(f"{path}: top-level must be a mapping")
        return
    md = data.get("metadata")
    if not isinstance(md, dict):
        errors.append(f"{path}: missing metadata block")
    else:
        missing = REQUIRED_METADATA - set(md.keys())
        if missing:
            errors.append(f"{path}: metadata missing {sorted(missing)}")
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append(f"{path}: entries must be a non-empty list")
        return
    for e in entries:
        for k in ("command","category","description","timeouts",
                  "representative_version","available_in_versions"):
            if k not in e:
                errors.append(f"{path}: entry missing '{k}'")
        # Reuse the data-file validation rules
        V.validate_entry(e, version_order, versions, global_latest, errors)

def check_cpp(path, errors):
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    if "#include" not in txt:
        errors.append(f"{path}: no #include directives")
    if "int run_" not in txt:
        errors.append(f"{path}: no 'int run_*' function found")

def main():
    errors = []
    if not os.path.isdir(EX_DIR):
        print(f"{EX_DIR} not found", file=sys.stderr)
        sys.exit(1)

    versions_path = os.path.join(ROOT, "data", "versions.yaml")
    versions_data = V.load_yaml(versions_path)
    versions = [v["id"] for v in versions_data["versions"]]
    version_order = {v["id"]: v["order"] for v in versions_data["versions"]}
    global_latest = versions_data["latest"]

    for fname in sorted(os.listdir(EX_DIR)):
        p = os.path.join(EX_DIR, fname)
        if fname.endswith((".yaml",".yml")):
            check_yaml(p, versions, version_order, global_latest, errors)
        elif fname.endswith(".cpp"):
            check_cpp(p, errors)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    print("Doc examples OK.")

if __name__ == "__main__":
    main()
