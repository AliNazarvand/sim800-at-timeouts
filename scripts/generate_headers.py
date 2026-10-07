#!/usr/bin/env python3
"""Generate C++ headers from YAML data.

Naming: for array AT_BASIC_TIMEOUTS the finder is find_at_basic_entry;
for SMS_TIMEOUTS the finder is find_sms_entry. Rule: lowercase the array
name and strip a trailing "_timeouts".
"""
import argparse
import hashlib
import json
import os
import sys

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
DEFAULT_INCLUDE = os.path.join(ROOT, "include", "sim800_at_timeouts")

CATEGORY_ENUM = {
    "at_basic": "Category::AtBasic",
    "at_3gpp_27007": "Category::At3gpp27007",
    "at_3gpp_27005": "Category::At3gpp27005",
    "sms": "Category::Sms",
    "gprs": "Category::Gprs",
    "tcpip": "Category::Tcpip",
    "http": "Category::Http",
    "ftp": "Category::Ftp",
    "audio": "Category::Audio",
    "stk": "Category::Stk",
    "init": "Category::Init",
}
TIMEOUT_KIND_ENUM = {
    "max_response_time": "TimeoutKind::MaxResponseTime",
    "prompt_timeout": "TimeoutKind::PromptTimeout",
    "send_timeout": "TimeoutKind::SendTimeout",
    "max_timeout": "TimeoutKind::MaxTimeout",
    "min_delay": "TimeoutKind::MinDelay",
    "max_wait": "TimeoutKind::MaxWait",
    "boot_time": "TimeoutKind::BootTime",
    "retry_interval": "TimeoutKind::RetryInterval",
    "urc_report_timeout": "TimeoutKind::UrcReportTimeout",
    "init_delay": "TimeoutKind::InitDelay",
    "hardware_settle_time": "TimeoutKind::HardwareSettleTime",
}
EXTRACTION_ENUM = {
    "extracted_from_table": "ExtractionStatus::ExtractedFromTable",
    "extracted_from_text": "ExtractionStatus::ExtractedFromText",
    "not_specified": "ExtractionStatus::NotSpecified",
}
PRESENCE_ENUM = {
    "present": "PresenceStatus::Present",
    "explicitly_removed": "PresenceStatus::ExplicitlyRemoved",
    "not_mentioned": "PresenceStatus::NotMentioned",
}
REVIEW_ENUM = {
    "approved_present_equivalent": "ReviewStatus::ApprovedPresentEquivalent",
    "approved_present_different": "ReviewStatus::ApprovedPresentDifferent",
    "approved_present_not_mentioned": "ReviewStatus::ApprovedPresentNotMentioned",
    "approved_present_explicitly_removed": "ReviewStatus::ApprovedPresentExplicitlyRemoved",
    "approved_absent_command": "ReviewStatus::ApprovedAbsentCommand",
    "approved_removed_command": "ReviewStatus::ApprovedRemovedCommand",
    "pending_review": "ReviewStatus::PendingReview",
    "rejected_pdf_unavailable": "ReviewStatus::RejectedPdfUnavailable",
    "rejected_uncertain": "ReviewStatus::RejectedUncertain",
}
MAX_TIME, MAX_AVAIL, MAX_VREV = 8, 8, 8

HEADER_ORDER = [
    ("at_basic.hpp", "at_basic.yaml", "sim800::timeouts::at_basic", "AT_BASIC_TIMEOUTS"),
    ("at_3gpp.hpp",  "at_3gpp.yaml",  "sim800::timeouts::at_3gpp",  "AT_3GPP_TIMEOUTS"),
    ("sms.hpp",      "sms.yaml",      "sim800::timeouts::sms",      "SMS_TIMEOUTS"),
    ("gprs.hpp",     "gprs.yaml",     "sim800::timeouts::gprs",     "GPRS_TIMEOUTS"),
    ("tcpip.hpp",    "tcpip.yaml",    "sim800::timeouts::tcpip",    "TCPIP_TIMEOUTS"),
    ("http.hpp",     "http.yaml",     "sim800::timeouts::http",     "HTTP_TIMEOUTS"),
    ("ftp.hpp",      "ftp.yaml",      "sim800::timeouts::ftp",      "FTP_TIMEOUTS"),
    ("audio.hpp",    "audio.yaml",    "sim800::timeouts::audio",    "AUDIO_TIMEOUTS"),
    ("stk.hpp",      "stk.yaml",      "sim800::timeouts::stk",      "STK_TIMEOUTS"),
    ("init.hpp",     "init.yaml",     "sim800::timeouts::init",     "INIT_TIMEOUTS"),
]
HEADER_TO_CATS = {
    "at_basic.hpp": ["at_basic"],
    "at_3gpp.hpp":  ["at_3gpp_27007", "at_3gpp_27005"],
    "sms.hpp":      ["sms"],
    "gprs.hpp":     ["gprs"],
    "tcpip.hpp":    ["tcpip"],
    "http.hpp":     ["http"],
    "ftp.hpp":      ["ftp"],
    "audio.hpp":    ["audio"],
    "stk.hpp":      ["stk"],
    "init.hpp":     ["init"],
}

def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def ms_val(v):
    return "MS_UNSET" if v is None else f"{int(v)}u"

def page_val(v):
    return "PAGE_UNSET" if v is None else f"{int(v)}u"

def cpp_string(s):
    if s is None:
        s = ""
    s = str(s)
    out = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "")
    return f'"{out}"'

def emit_timeout(tv):
    kind = TIMEOUT_KIND_ENUM.get(tv.get("timeout_kind", ""), "TimeoutKind::MaxResponseTime")
    return "{ " + ", ".join([
        kind,
        ms_val(tv.get("min_value_ms")),
        ms_val(tv.get("max_value_ms")),
        ms_val(tv.get("nominal_value_ms")),
        ms_val(tv.get("recommended_value_ms")),
        ms_val(tv.get("default_value_ms")),
    ]) + " }"

def emit_timeout_array(t):
    lines = ["            " + emit_timeout(x) for x in t]
    lines += ["            TIMEOUT_VALUE_PAD"] * (MAX_TIME - len(t))
    return "{{\n" + ",\n".join(lines) + "\n        }}"

def emit_avail(vs):
    parts = [cpp_string(v) for v in vs] + ["{}"] * (MAX_AVAIL - len(vs))
    return "{{ " + ", ".join(parts) + " }}"

def emit_evidence(ev):
    if ev is None:
        return ("ReviewEvidence{ std::string_view{}, PAGE_UNSET, "
                "std::string_view{}, std::string_view{} }")
    return ("ReviewEvidence{ " + cpp_string(ev.get("section")) + ", "
            + page_val(ev.get("page")) + ", "
            + cpp_string(ev.get("note") or "") + ", "
            + cpp_string(ev.get("compared_to_version") or "") + " }")

def emit_version_entry(ve):
    t = ve.get("timeouts", []) or []
    return "\n".join([
        "            {",
        f"                {cpp_string(ve.get('version'))},",
        "                " + emit_timeout_array(t) + ",",
        f"                {len(t)},",
        f"                {PRESENCE_ENUM.get(ve.get('presence_status',''), 'PresenceStatus::NotMentioned')},",
        f"                {EXTRACTION_ENUM.get(ve.get('extraction_status',''), 'ExtractionStatus::NotSpecified')},",
        f"                {'true' if ve.get('source_same_as_representative') else 'false'},",
        f"                {cpp_string(ve.get('source_document') or '')},",
        f"                {cpp_string(ve.get('source_section') or '')},",
        f"                {'true' if ve.get('page_hint_same_as_representative') else 'false'},",
        f"                {page_val(ve.get('page_hint'))}",
        "            }",
    ])

def emit_vspec(vs):
    if not vs:
        return "{{}}"
    return "{{\n" + ",\n".join(emit_version_entry(v) for v in vs) + "\n        }}"

def emit_version_review(vr):
    ev = vr.get("evidence")
    has = ev is not None
    return "\n".join([
        "            {",
        f"                {cpp_string(vr.get('version'))},",
        f"                {REVIEW_ENUM.get(vr.get('status',''), 'ReviewStatus::PendingReview')},",
        f"                {'true' if has else 'false'},",
        "                " + emit_evidence(ev),
        "            }",
    ])

def emit_vrevs(vs):
    if not vs:
        return "{{}}"
    items = [emit_version_review(v) for v in vs]
    items += ["            VERSION_REVIEW_PAD"] * (MAX_VREV - len(items))
    return "{{\n" + ",\n".join(items) + "\n        }}"

def emit_command_entry(e):
    t = e.get("timeouts", []) or []
    a = e.get("available_in_versions", []) or []
    vs = e.get("version_specific", []) or []
    vr = e.get("version_reviews", []) or []
    return "\n".join([
        "    {",
        f"        {cpp_string(e.get('command'))},",
        f"        {CATEGORY_ENUM.get(e.get('category',''), 'Category::AtBasic')},",
        f"        {cpp_string(e.get('description'))},",
        "        " + emit_timeout_array(t) + ",",
        f"        {len(t)},",
        f"        {cpp_string(e.get('source_document'))},",
        f"        {cpp_string(e.get('source_section'))},",
        f"        {EXTRACTION_ENUM.get(e.get('extraction_status_latest',''), 'ExtractionStatus::NotSpecified')},",
        f"        {PRESENCE_ENUM.get(e.get('presence_status_latest',''), 'PresenceStatus::Present')},",
        f"        {cpp_string(e.get('representative_version'))},",
        "        " + emit_avail(a) + ",",
        f"        {len(a)},",
        "        " + emit_vspec(vs) + ",",
        f"        {len(vs)},",
        "        " + emit_vrevs(vr) + ",",
        f"        {len(vr)},",
        f"        {page_val(e.get('page_hint'))},",
        f"        {cpp_string(e.get('notes') or '')}",
        "    }",
    ])

def hash_entries(entries):
    blob = json.dumps(entries, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()

def gather(yaml_source, cats):
    merged = []
    yaml_path = os.path.join(DATA_DIR, yaml_source)
    if not os.path.exists(yaml_path):
        return merged
    data = load_yaml(yaml_path)
    for e in data.get("entries", []) or []:
        if e.get("category") in cats:
            merged.append(e)
    merged.sort(key=lambda x: x.get("command", ""))
    return merged

def finder_name(array_name):
    n = array_name.lower()
    if n.endswith("_timeouts"):
        n = n[:-len("_timeouts")]
    return f"find_{n}_entry"

def generate_header(yaml_source, ns, array_name, entries, hash_hex):
    count = len(entries)
    body = ",\n".join(emit_command_entry(e) for e in entries) if entries else ""
    idx = ",\n".join("    " + cpp_string(e.get("command", "")) for e in entries) if entries else ""
    fn = finder_name(array_name)
    L = [
        "// ============================================================",
        "// AUTO-GENERATED FILE — DO NOT EDIT MANUALLY",
        f"// Generated from: data/{yaml_source}",
        f"// Content hash (SHA-256 of entries section only): {hash_hex}",
        "// Generator: scripts/generate_headers.py",
        "// Database version: 1.0.0",
        "// To regenerate: cmake --build . --target generate",
        "// ============================================================",
        "",
        "#pragma once",
        '#include "timeout_types.hpp"',
        '#include "database_version.hpp"',
        "#include <array>",
        "#include <cstddef>",
        "#include <string_view>",
        "#include <algorithm>",
        "",
        f"namespace {ns} {{",
        "",
        f"inline constexpr std::array<CommandEntry, {count}> {array_name} = {{{{",
    ]
    if body:
        L.append(body)
    L += [
        "}};",
        "",
        f"inline constexpr std::size_t {array_name}_COUNT = {array_name}.size();",
        f"static_assert({array_name}_COUNT <= MAX_ENTRIES_PER_HEADER,",
        f'              "{array_name} entry count exceeds MAX_ENTRIES_PER_HEADER");',
        "",
        f"inline constexpr std::array<std::string_view, {array_name}_COUNT> "
        f"{array_name}_COMMAND_INDEX = {{{{",
    ]
    if idx:
        L.append(idx)
    L += [
        "}};",
        "",
        f"inline const CommandEntry* {fn}(std::string_view cmd) noexcept {{",
        f"    auto it = std::lower_bound({array_name}_COMMAND_INDEX.begin(), "
        f"{array_name}_COMMAND_INDEX.end(), cmd);",
        f"    if (it == {array_name}_COMMAND_INDEX.end() || *it != cmd) return nullptr;",
        f"    return &{array_name}[static_cast<std::size_t>(it - "
        f"{array_name}_COMMAND_INDEX.begin())];",
        "}",
        "",
        f"}} // namespace {ns}",
        "",
    ]
    return "\n".join(L)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default=DEFAULT_INCLUDE)
    args = ap.parse_args()
    os.makedirs(args.output, exist_ok=True)
    for hdr, yml, ns, arr in HEADER_ORDER:
        entries = gather(yml, HEADER_TO_CATS[hdr])
        h = hash_entries(entries)
        content = generate_header(yml, ns, arr, entries, h)
        with open(os.path.join(args.output, hdr), "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        print(f"[gen] {hdr}: {len(entries)} entries, hash={h[:12]}")
    print("Header generation complete.")

if __name__ == "__main__":
    main()
