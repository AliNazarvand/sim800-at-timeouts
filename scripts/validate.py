#!/usr/bin/env python3
"""Validate the SIM800 AT timeouts database (extended implementation)."""
import json
import os
import re
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator = None

try:
    from referencing import Registry, Resource
except ImportError:
    Registry = None
    Resource = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
SCHEMA_DIR = os.path.join(ROOT, "schema")
INCLUDE_DIR = os.path.join(ROOT, "include", "sim800_at_timeouts")
SKIP_FILES = {
    "versions.yaml","chapter_mapping.yaml","category_mapping.yaml",
    "command_inventory.yaml","module_compatibility.yaml"
}
MS_MAX = 4294967294
PAGE_MAX = 4294967294

ALL_TIMEOUT_KINDS = {
    "max_response_time","prompt_timeout","send_timeout","max_timeout",
    "min_delay","max_wait","boot_time","retry_interval",
    "urc_report_timeout","init_delay","hardware_settle_time",
}
PRESENCE_VALUES = {"present","explicitly_removed","not_mentioned"}
EXTRACTION_VALUES = {"extracted_from_table","extracted_from_text","not_specified"}
REVIEW_VALUES = {
    "approved_present_equivalent","approved_present_different",
    "approved_present_not_mentioned","approved_present_explicitly_removed",
    "approved_absent_command","approved_removed_command",
    "pending_review","rejected_pdf_unavailable","rejected_uncertain",
}
REVIEW_SCOPES = {"absent","partial","complete"}
SECTION_RE = re.compile(r"^(Table|Section|Chapter|Page|Figure)\s")

# §10.6 — primary field(s) per timeout_kind
PRIMARY_FIELD = {
    "max_response_time": ["max_value_ms"],
    "prompt_timeout": ["max_value_ms"],
    "send_timeout": ["max_value_ms"],
    "max_timeout": ["min_value_ms","max_value_ms"],
    "min_delay": ["min_value_ms"],
    "max_wait": ["max_value_ms"],
    "boot_time": ["max_value_ms"],
    "retry_interval": ["nominal_value_ms"],
    "urc_report_timeout": ["max_value_ms"],
    "init_delay": ["min_value_ms"],
    "hardware_settle_time": ["min_value_ms"],
}
NUM_FIELDS = ("min_value_ms","max_value_ms","nominal_value_ms",
              "recommended_value_ms","default_value_ms")

def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def check_database_version(errors):
    hpp = os.path.join(INCLUDE_DIR, "database_version.hpp")
    if not os.path.exists(hpp):
        errors.append("database_version.hpp not found")
        return None
    with open(hpp, encoding="utf-8") as f:
        content = f.read()
    m = re.search(r'DATABASE_VERSION\s*=\s*"([^"]+)"', content)
    if not m:
        errors.append("DATABASE_VERSION not found in database_version.hpp")
        return None
    return m.group(1)

def validate_timeouts(timeouts, cmd, extraction_status, errors):
    if extraction_status == "not_specified":
        for tv in timeouts:
            for k in NUM_FIELDS:
                if tv.get(k) is not None:
                    errors.append(f"{cmd}: {k} must be null when not_specified")
        return
    kinds = [tv.get("timeout_kind") for tv in timeouts]
    if len(set(kinds)) != len(kinds):
        errors.append(f"{cmd}: duplicate timeout_kind in timeouts")
    for tv in timeouts:
        k = tv.get("timeout_kind")
        if k not in ALL_TIMEOUT_KINDS:
            errors.append(f"{cmd}: invalid timeout_kind '{k}'")
            continue
        for num_key in NUM_FIELDS:
            v = tv.get(num_key)
            if v is not None and (not isinstance(v, int) or v < 0 or v > MS_MAX):
                errors.append(f"{cmd}: {num_key}={v} out of range [0,{MS_MAX}]")
        # §10.6: if this TimeoutValue has any numeric value, it must sit
        # in a primary field for its kind.
        has_value = any(tv.get(f) is not None for f in NUM_FIELDS)
        if has_value:
            prim = PRIMARY_FIELD.get(k, [])
            if prim and all(tv.get(p) is None for p in prim):
                errors.append(f"{cmd}: timeout_kind={k} has a value but no "
                              f"primary field ({'/'.join(prim)}) is set")

def timeouts_equal(a, b):
    def key(tv):
        return (tv.get("timeout_kind"),) + tuple(tv.get(f) for f in NUM_FIELDS)
    return sorted(map(key, a)) == sorted(map(key, b))

def validate_entry(e, version_order, versions, global_latest, errors):
    cmd = e.get("command","<no-command>")
    rv = e.get("representative_version")
    if not rv:
        errors.append(f"{cmd}: representative_version is null")
    avail = e.get("available_in_versions") or []
    if not avail:
        errors.append(f"{cmd}: available_in_versions is empty")
    elif rv and rv not in avail:
        errors.append(f"{cmd}: representative_version '{rv}' not in available_in_versions")
    if avail:
        newest = max(avail, key=lambda v: version_order.get(v, -1))
        if rv and rv != newest:
            errors.append(f"{cmd}: representative_version must be newest "
                          f"('{newest}') of available_in_versions (got '{rv}')")
    ext = e.get("extraction_status_latest")
    if ext not in EXTRACTION_VALUES:
        errors.append(f"{cmd}: invalid extraction_status_latest '{ext}'")
    pres = e.get("presence_status_latest")
    if pres not in PRESENCE_VALUES:
        errors.append(f"{cmd}: invalid presence_status_latest '{pres}'")
    if pres in ("explicitly_removed","not_mentioned"):
        if e.get("timeouts"):
            errors.append(f"{cmd}: presence_status_latest={pres} requires empty timeouts")
        if ext != "not_specified":
            errors.append(f"{cmd}: presence_status_latest={pres} requires "
                          "extraction_status=not_specified")
    validate_timeouts(e.get("timeouts", []) or [], cmd, ext, errors)

    vspec = e.get("version_specific", []) or []
    seen = []
    for ve in vspec:
        v = ve.get("version")
        if v in seen:
            errors.append(f"{cmd}: duplicate version '{v}' in version_specific")
        seen.append(v)
        if v not in avail:
            errors.append(f"{cmd}: version_specific '{v}' not in available_in_versions")
        ve_ext = ve.get("extraction_status")
        ve_pres = ve.get("presence_status")
        validate_timeouts(ve.get("timeouts", []) or [], f"{cmd}/{v}", ve_ext, errors)
        # §10.8.5: not_mentioned / explicitly_removed require empty timeouts
        if ve_pres in ("explicitly_removed","not_mentioned"):
            if ve.get("timeouts"):
                errors.append(f"{cmd}/{v}: presence_status={ve_pres} requires empty timeouts")
            if ve_ext != "not_specified":
                errors.append(f"{cmd}/{v}: presence_status={ve_pres} requires "
                              "extraction_status=not_specified")
        ssame = ve.get("source_same_as_representative")
        if ssame is True:
            if ve.get("source_document") is not None:
                errors.append(f"{cmd}/{v}: source_same_as_representative=true requires null source_document")
            if ve.get("source_section") is not None:
                errors.append(f"{cmd}/{v}: source_same_as_representative=true requires null source_section")
            if ve.get("page_hint_same_as_representative") is not True:
                errors.append(f"{cmd}/{v}: source_same_as_representative=true requires "
                              "page_hint_same_as_representative=true")
        else:
            if not ve.get("source_document"):
                errors.append(f"{cmd}/{v}: source_same_as_representative=false requires source_document")
            if not ve.get("source_section"):
                errors.append(f"{cmd}/{v}: source_same_as_representative=false requires source_section")
        ph_same = ve.get("page_hint_same_as_representative")
        if ph_same is True and ve.get("page_hint") is not None:
            errors.append(f"{cmd}/{v}: page_hint_same_as_representative=true requires null page_hint")
        ph = ve.get("page_hint")
        if ph is not None and (not isinstance(ph, int) or ph < 1 or ph > PAGE_MAX):
            errors.append(f"{cmd}/{v}: page_hint={ph} out of range")
        # §10.8.4: version_specific present must differ from top-level
        if ve_pres == "present" and ve_ext != "not_specified":
            if timeouts_equal(ve.get("timeouts", []) or [], e.get("timeouts", []) or []):
                errors.append(f"{cmd}/{v}: version_specific present with identical "
                              "timeouts as top-level")
    # §10.10: sorted ascending
    orders = [version_order.get(v, -1) for v in seen]
    if orders != sorted(orders):
        errors.append(f"{cmd}: version_specific not sorted by version order")
    # §13: not_specified representative must not appear in version_specific
    if ext == "not_specified" and rv in seen:
        errors.append(f"{cmd}: representative_version must not appear in "
                      "version_specific when extraction_status_latest=not_specified")

    reviews = e.get("version_reviews", []) or []
    for vr in reviews:
        st = vr.get("status")
        v = vr.get("version")
        if st not in REVIEW_VALUES:
            errors.append(f"{cmd}: invalid review_status '{st}'")
            continue
        if st.startswith("approved_"):
            ev = vr.get("evidence")
            if ev is None:
                errors.append(f"{cmd}/{v}: evidence is mandatory for {st}")
            else:
                sec = ev.get("section")
                if not sec or not SECTION_RE.match(sec):
                    errors.append(f"{cmd}/{v}: evidence.section pattern mismatch for {st}")
                if st == "approved_present_equivalent" and ev.get("compared_to_version") != rv:
                    errors.append(f"{cmd}/{v}: approved_present_equivalent requires "
                                  f"compared_to_version == '{rv}'")
        in_spec = next((ve for ve in vspec if ve.get("version") == v), None)
        if v in avail and in_spec is not None:
            ps = in_spec.get("presence_status")
            if ps == "present" and st != "approved_present_different":
                errors.append(f"{cmd}/{v}: version_specific present requires "
                              "status=approved_present_different")
            if ps == "not_mentioned" and st != "approved_present_not_mentioned":
                errors.append(f"{cmd}/{v}: version_specific not_mentioned requires "
                              "status=approved_present_not_mentioned")
            if ps == "explicitly_removed" and st != "approved_present_explicitly_removed":
                errors.append(f"{cmd}/{v}: version_specific explicitly_removed requires "
                              "status=approved_present_explicitly_removed")
        if v in avail and in_spec is None and v != rv:
            if st not in ("approved_present_equivalent","pending_review") \
                    and not st.startswith("rejected_"):
                errors.append(f"{cmd}/{v}: in available_in_versions but absent from "
                              "version_specific must be approved_present_equivalent/pending_review")
        if v not in avail:
            if st not in ("approved_absent_command","approved_removed_command",
                          "pending_review") and not st.startswith("rejected_"):
                errors.append(f"{cmd}/{v}: version not in available_in_versions "
                              "requires approved_absent_command/approved_removed_command")
    if rv and rv != global_latest:
        gl_review = [vr for vr in reviews if vr.get("version") == global_latest]
        if gl_review:
            st = gl_review[0].get("status")
            if st not in ("approved_absent_command","approved_removed_command","pending_review") \
                    and not (st or "").startswith("rejected_"):
                errors.append(f"{cmd}: global_latest review status must be "
                              "approved_absent_command/approved_removed_command")

    ph = e.get("page_hint")
    if ph is not None and (not isinstance(ph, int) or ph < 1 or ph > PAGE_MAX):
        errors.append(f"{cmd}: page_hint={ph} out of range")

def compute_pending_union(data, versions):
    """Versions not yet approved for at least one entry (excludes rv).

    Only reviews whose status starts with "approved_" count as reviewed.
    pending_review and rejected_* are treated as not-reviewed.
    """
    pending = set()
    for e in data.get("entries", []) or []:
        rv = e.get("representative_version")
        reviewed = {
            vr.get("version")
            for vr in (e.get("version_reviews") or [])
            if (vr.get("status") or "").startswith("approved_")
        }
        unreviewed = set(versions) - reviewed - ({rv} if rv else set())
        pending.update(unreviewed)
    return pending

def validate_file_metadata(fname, data, versions, errors):
    md = data.get("metadata", {}) or {}
    scope = md.get("review_scope")
    if scope not in REVIEW_SCOPES:
        errors.append(f"{fname}: invalid review_scope '{scope}'")
        return
    pending = set(md.get("pending_versions") or [])
    if scope == "absent":
        if pending != set(versions):
            errors.append(f"{fname}: review_scope=absent requires pending_versions={versions}")
        for e in data.get("entries", []) or []:
            if e.get("version_reviews"):
                errors.append(f"{fname}: absent but {e.get('command')} has version_reviews")
    elif scope == "partial":
        if not pending:
            errors.append(f"{fname}: partial requires non-empty pending_versions")
        expected = compute_pending_union(data, versions)
        if pending != expected:
            errors.append(f"{fname}: partial pending_versions mismatch. "
                          f"Expected {sorted(expected)}, got {sorted(pending)}")
    elif scope == "complete":
        if pending:
            errors.append(f"{fname}: complete requires empty pending_versions")

def validate_command_inventory(inv_path, data_by_chapter, errors):
    """Two-way check: every inventory command must be in data files, and
    every data-file command must be in the inventory."""
    if not os.path.exists(inv_path):
        return
    inv = load_yaml(inv_path)
    inv_cmds = set()
    for chap in inv.get("chapters", []) or []:
        for cmd in chap.get("commands", []) or []:
            inv_cmds.add(cmd)
    data_cmds = set()
    for _, d in data_by_chapter.items():
        for e in d.get("entries", []) or []:
            data_cmds.add(e.get("command"))
    for cmd in sorted(inv_cmds - data_cmds):
        errors.append(f"command_inventory: '{cmd}' in inventory but not in any data file")
    for cmd in sorted(data_cmds - inv_cmds):
        errors.append(f"command_inventory: '{cmd}' in data files but not in inventory")

def build_registry(schema_dir):
    if Registry is None or Resource is None:
        return None
    resources = []
    for fname in os.listdir(schema_dir):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(schema_dir, fname)
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        uri = "file://" + path.replace(os.sep, "/")
        resources.append((uri, Resource.from_contents(data)))
        if isinstance(data, dict) and "$id" in data:
            resources.append((data["$id"], Resource.from_contents(data)))
    return Registry().with_resources(resources)

def main():
    errors = []
    versions_path = os.path.join(DATA_DIR, "versions.yaml")
    if not os.path.exists(versions_path):
        print("versions.yaml not found", file=sys.stderr)
        sys.exit(1)
    versions_data = load_yaml(versions_path)
    versions = [v["id"] for v in versions_data["versions"]]
    version_order = {v["id"]: v["order"] for v in versions_data["versions"]}
    global_latest = versions_data["latest"]
    if global_latest not in versions:
        errors.append("latest must be in versions")

    db_version = check_database_version(errors)
    print(f"Versions: {versions}, latest={global_latest}, db_version={db_version}")

    registry = build_registry(SCHEMA_DIR) if Draft202012Validator and Registry else None

    data_by_chapter = {}
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".yaml") or fname in SKIP_FILES:
            continue
        path = os.path.join(DATA_DIR, fname)
        data = load_yaml(path)
        data_by_chapter[fname] = data

        md = data.get("metadata", {}) or {}
        if db_version and md.get("database_version") and md.get("database_version") != db_version:
            errors.append(f"{fname}: metadata.database_version "
                          f"'{md.get('database_version')}' != '{db_version}'")

        if Draft202012Validator is not None:
            cat_schema = fname.replace(".yaml", ".schema.json")
            cat_schema_path = os.path.join(SCHEMA_DIR, cat_schema)
            if os.path.exists(cat_schema_path):
                try:
                    cat_schema_data = load_json(cat_schema_path)
                    if registry is not None:
                        Draft202012Validator(cat_schema_data, registry=registry).validate(data)
                    else:
                        Draft202012Validator(cat_schema_data).validate(data)
                except Exception as ex:
                    errors.append(f"{fname}: schema validation failed: {ex}")

        validate_file_metadata(fname, data, versions, errors)
        for entry in data.get("entries", []) or []:
            validate_entry(entry, version_order, versions, global_latest, errors)

    validate_command_inventory(
        os.path.join(DATA_DIR, "command_inventory.yaml"),
        data_by_chapter, errors)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    print("Validation passed.")

if __name__ == "__main__":
    main()
