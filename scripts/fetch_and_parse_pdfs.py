#!/usr/bin/env python3
"""Fetch SIM800 PDFs from GitHub raw URLs and extract text in memory.

No files are written to disk unless --save is given. Designed so the
extracted text can be handed to a human or an AI for version-diff review.

Requires:  pip install requests PyMuPDF

Examples
--------
    # List all known sources
    python scripts/fetch_and_parse_pdfs.py --list

    # Fetch one PDF, print to stdout (first 30 pages only)
    python scripts/fetch_and_parse_pdfs.py --fetch SIM800_AT_V1.01 --max-pages 30

    # Fetch all three AT Manual versions and dump to build/pdf_text/
    python scripts/fetch_and_parse_pdfs.py --dump-all --save

    # Extract just the pages that mention a command (per version)
    python scripts/fetch_and_parse_pdfs.py --cmd "AT+CSQ" --save

    # Compare a command across the three AT Manual versions
    python scripts/fetch_and_parse_pdfs.py --compare "AT+CSQ"
    python scripts/fetch_and_parse_pdfs.py --compare "AT+CIPSEND" --context 2
"""
import argparse
import io
import os
import re
import sys

try:
    import requests
except ImportError:
    print("requests is required: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF is required: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "build", "pdf_text")
GH_RAW = "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/"

# Keys are stable; do not rename.
SOURCES = {
    # AT Command Manuals (the ones that matter for version diffs)
    "SIM800_AT_V1.01":  GH_RAW + "SIM800%20Series_AT%20Command%20Manual_V1.01.pdf",
    "SIM800_AT_V1.10":  GH_RAW + "SIM800%20Series_AT%20Command%20Manual_V1.10.pdf",
    "SIM800_AT_V1.12":  GH_RAW + "SIM800%20Series_AT%20Command%20Manual_V1.12.pdf",
    # Hardware Design guides (used for INIT timeout entries)
    "SIM800_HW_V1.09":  GH_RAW + "SIM800_Hardware%20Design_V1.09.pdf",
    "SIM800L_HW_V1.00": GH_RAW + "SIM800L_Hardware%20Design_V1.00.pdf",
    "SIM800A_HW_V1.02": GH_RAW + "SIM800A_Hardware%20Design_V1.02.pdf",
    "SIM800C_HW_V1.02": GH_RAW + "SIM800C_Hardware_Design_V1.02.pdf",
    "SIM800C-DS_HW_V1.01": GH_RAW + "SIM800C-DS_Hardware_Design_V1.01.pdf",
    "SIM800F_HW_V1.05": GH_RAW + "SIM800F_Hardware%20Design_V1.05.pdf",
    "SIM800H_HW_V2.03": GH_RAW + "SIM800H_Hardware%20Design_V2.03.pdf",
    "SIM800H_L_HW_V2.02": GH_RAW + "SIM800H%26SIM800L_Hardware%20Design_V2.02.PDF",
    "SIM808_HW_V1.03":  GH_RAW + "SIM808_Hardware%20Design_V1.03.pdf",
    "SIM868_HW_V1.00":  GH_RAW + "SIM868_Hardware_Design_V1.00.pdf",
}

AT_MANUAL_KEYS = ["SIM800_AT_V1.01", "SIM800_AT_V1.10", "SIM800_AT_V1.12"]

# Any page containing this is relevant when extracting a command section.
RESPONSE_TITLE_RE = re.compile(
    r"(Max(?:imum)?\s+Response\s+Time|Response\s+Time)", re.I
)

def list_sources():
    width = max(len(k) for k in SOURCES)
    for k, v in SOURCES.items():
        print(f"{k.ljust(width)}  {v}")

def fetch_bytes(url):
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    return r.content

def open_doc(url):
    return fitz.open(stream=fetch_bytes(url), filetype="pdf")

def page_text(doc, idx):
    return doc.load_page(idx).get_text("text") or ""

def dump_full_text(key, doc, out_path):
    lines = [f"===== {key} =====", f"pages: {doc.page_count}", ""]
    for i in range(doc.page_count):
        lines.append(f"----- PAGE {i+1} -----")
        lines.append(page_text(doc, i))
        lines.append("")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"[dump] {key} -> {out_path} ({doc.page_count} pages)")

def find_command_pages(doc, command, context):
    """Return sorted set of page indices that mention `command` (case-insensitive)."""
    needle = command.upper()
    hits = []
    for i in range(doc.page_count):
        txt = page_text(doc, i).upper()
        if needle in txt:
            hits.append(i)
    keep = set()
    for h in hits:
        for c in range(h - context, h + context + 1):
            if 0 <= c < doc.page_count:
                keep.add(c)
    return sorted(keep), hits

def extract_command(doc, command, context=2, include_tables=True):
    pages, hits = find_command_pages(doc, command, context)
    out = []
    for i in pages:
        p = doc.load_page(i)
        out.append(f"----- PAGE {i+1} -----")
        out.append(p.get_text("text") or "")
        if include_tables and RESPONSE_TITLE_RE.search(out[-1]):
            try:
                tabs = p.find_tables()
                for j, t in enumerate(tabs.tables):
                    out.append(f"[TABLE {j+1} on page {i+1}]")
                    for row in t.extract():
                        out.append(" | ".join("" if c is None else str(c) for c in row))
            except Exception as ex:
                out.append(f"[table_error] {ex}")
        out.append("")
    return "\n".join(out), hits

def cmd_compare(args):
    cmd = args.compare.upper()
    results = {}
    for key in AT_MANUAL_KEYS:
        url = SOURCES[key]
        try:
            doc = open_doc(url)
        except Exception as ex:
            print(f"[error] {key}: {ex}", file=sys.stderr)
            continue
        body, hits = extract_command(doc, cmd, context=args.context)
        results[key] = (body, hits, doc.page_count)
        doc.close()

    out_path = os.path.join(OUT_DIR, f"compare_{cmd.replace('+','_')}.txt")
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# Version comparison for {cmd}\n")
        f.write(f"# context: {args.context} pages before/after each hit\n\n")
        for key in AT_MANUAL_KEYS:
            if key not in results:
                f.write(f"===== {key} : NOT FETCHED =====\n\n")
                continue
            body, hits, npages = results[key]
            f.write(f"===== {key}  (pages={npages}, hits={len(hits)}: {[h+1 for h in hits]}) =====\n")
            f.write(body)
            f.write("\n")
    print(f"[compare] {cmd} -> {out_path}")

def cmd_cmd(args):
    """Extract a single command from every AT manual, save per-version files."""
    cmd = args.cmd.upper()
    os.makedirs(OUT_DIR, exist_ok=True)
    for key in AT_MANUAL_KEYS:
        try:
            doc = open_doc(SOURCES[key])
        except Exception as ex:
            print(f"[error] {key}: {ex}", file=sys.stderr)
            continue
        body, hits = extract_command(doc, cmd, context=args.context)
        out_path = os.path.join(OUT_DIR, f"{key}__{cmd.replace('+','_')}.txt")
        with open(out_path, "w", encoding="utf-8", newline="\n") as f:
            f.write(f"# {key} : {cmd}  (hits={[h+1 for h in hits]})\n\n")
            f.write(body)
        doc.close()
        print(f"[cmd] {key} {cmd} -> {out_path} ({len(hits)} hits)")

def cmd_dump_all(args):
    os.makedirs(OUT_DIR, exist_ok=True)
    keys = list(SOURCES.keys()) if args.dump_all == "all" else AT_MANUAL_KEYS
    for key in keys:
        try:
            doc = open_doc(SOURCES[key])
        except Exception as ex:
            print(f"[error] {key}: {ex}", file=sys.stderr)
            continue
        out_path = os.path.join(OUT_DIR, f"{key}.txt")
        dump_full_text(key, doc, out_path)
        doc.close()

def cmd_fetch(args):
    key = args.fetch
    if key not in SOURCES:
        print(f"Unknown key: {key}", file=sys.stderr)
        sys.exit(1)
    doc = open_doc(SOURCES[key])
    limit = doc.page_count if args.max_pages is None else min(args.max_pages, doc.page_count)
    for i in range(limit):
        print(f"----- PAGE {i+1} -----")
        print(page_text(doc, i))
    doc.close()

def main():
    ap = argparse.ArgumentParser(
        description="Fetch & parse SIM800 PDFs from GitHub raw URLs."
    )
    ap.add_argument("--list", action="store_true",
                    help="List all known source keys and URLs.")
    ap.add_argument("--fetch", metavar="KEY",
                    help="Fetch one PDF by key and print to stdout.")
    ap.add_argument("--max-pages", type=int, default=None,
                    help="Limit pages when using --fetch.")
    ap.add_argument("--dump-all", nargs="?", const="at", choices=["at","all"],
                    help="Dump AT manuals (default) or ALL sources to build/pdf_text/.")
    ap.add_argument("--cmd", metavar="AT+XXX",
                    help="Extract pages mentioning a command in each AT manual.")
    ap.add_argument("--compare", metavar="AT+XXX",
                    help="Compare a command across the 3 AT manual versions.")
    ap.add_argument("--context", type=int, default=2,
                    help="Pages of context around each command hit (default 2).")
    ap.add_argument("--save", action="store_true",
                    help="Accepted for symmetry; --cmd/--compare always save.")
    args = ap.parse_args()

    if args.list:
        list_sources(); return
    if args.fetch:
        cmd_fetch(args); return
    if args.dump_all:
        cmd_dump_all(args); return
    if args.cmd:
        cmd_cmd(args); return
    if args.compare:
        cmd_compare(args); return
    ap.print_help()

if __name__ == "__main__":
    main()