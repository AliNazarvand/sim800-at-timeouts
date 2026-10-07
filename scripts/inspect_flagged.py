#!/usr/bin/env python3
"""Show raw PDF text around 'Max Response Time' for the 7 flagged cases.

For each case, prints every page containing the command together with
a 1500-char window around the first 'Max Response Time' or 'Response Time'
match, so a human reviewer can determine the correct value.
"""
import os
import re
import sys
import textwrap

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF_TEXT_DIR = os.path.join(ROOT, "build", "pdf_text")

AT_TXT = {
    "V1.01": "SIM800_AT_V1.01.txt",
    "V1.10": "SIM800_AT_V1.10.txt",
    "V1.12": "SIM800_AT_V1.12.txt",
}

PAGE_RE = re.compile(r"^----- PAGE (\d+) -----$")
MRT_RE = re.compile(r"Max(?:imum)?\s+Response\s+Time", re.I)
RT_RE = re.compile(r"(?:Max(?:imum)?\s+)?Response\s+Time", re.I)

CASES = [
    ("AT+CPIN", "V1.12"),
    ("AT+CMGD", "V1.12"),
    ("AT+CMGR", "V1.01"),
    ("AT+CMGR", "V1.10"),
    ("AT+CMGR", "V1.12"),
    ("AT+CMGS", "V1.10"),
    ("AT+CMGS", "V1.12"),
]


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


def collect_candidates(cmd, pages):
    """Return list of (page_no, kind, excerpt) for all pages that
    mention both the command and a 'Response Time' phrase."""
    cmd_upper = cmd.upper()
    out = []
    for pno, text in pages:
        up = text.upper()
        if cmd_upper not in up:
            continue
        m = MRT_RE.search(text)
        if not m:
            m = RT_RE.search(text)
        if not m:
            continue
        start = max(0, m.start() - 200)
        end = min(len(text), m.end() + 900)
        excerpt = text[start:end]
        kind = "Max Response Time" if MRT_RE.match(text, m.start()) else "Response Time"
        out.append((pno, kind, excerpt))
    return out


def report_case(cmd, ver):
    fname = AT_TXT.get(ver)
    if not fname:
        return
    path = os.path.join(PDF_TEXT_DIR, fname)
    if not os.path.exists(path):
        print(f"  [missing PDF text] {fname}")
        return
    pages = list(read_pages(path))
    cands = collect_candidates(cmd, pages)
    if not cands:
        print(f"  No 'Response Time' phrase found on pages containing {cmd}.")
        return
    print(f"  Found {len(cands)} candidate page(s):")
    for pno, kind, excerpt in cands:
        print(f"\n  --- page {pno} ({kind}) ---")
        wrapped = textwrap.indent(excerpt.strip(), "      ")
        print(wrapped)
    print()


def main():
    print("=" * 72)
    print(" RAW PDF TEXT INSPECTION — 7 flagged cases")
    print("=" * 72)
    print()
    print(" Review each excerpt and decide:")
    print("   (a) stored value in data/*.yaml is CORRECT")
    print("   (b) extracted value in timeouts.json is CORRECT")
    print("   (c) neither — a third value is correct")
    print()
    for cmd, ver in CASES:
        print(f"[{cmd}] {ver}")
        report_case(cmd, ver)


if __name__ == "__main__":
    main()