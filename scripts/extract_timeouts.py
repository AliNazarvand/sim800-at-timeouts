#!/usr/bin/env python3
"""Extract timeouts from PDFs (requires PyMuPDF only)."""
import argparse
import json
import os
import re
import sys

try:
    import fitz
except ImportError:
    print("PyMuPDF is required: pip install PyMuPDF", file=sys.stderr)
    sys.exit(1)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(ROOT, ".cache", "sources")
OUT_DIR   = os.path.join(ROOT, "build", "extracted")

RESPONSE_TITLE_RE = re.compile(r"(Max(?:imum)?\s+Response\s+Time|Response\s+Time)", re.I)

# Patterns are applied to each page that contains a Response Time title.
# Each pattern MUST have two groups: (value, unit).
PHRASE_RES = [
    # Existing patterns
    re.compile(r"within\s+(\d+)\s*(s|seconds?)", re.I),
    re.compile(r"after\s+(\d+)\s*(s|seconds?)", re.I),
    re.compile(r"maximum\s+(?:of\s+)?(\d+)\s*(ms|s)", re.I),
    re.compile(r"the module returns .* in\s+(\d+)\s*(s|seconds?)", re.I),
    re.compile(r"default\s+(?:is\s+)?(\d+)\s*(ms|s)", re.I),
    # Extended coverage
    re.compile(r"at\s+least\s+(\d+)\s*(ms|s|seconds?)", re.I),
    re.compile(r"no\s+more\s+than\s+(\d+)\s*(ms|s|seconds?)", re.I),
    re.compile(r"timeout\s+(?:of\s+|is\s+)?(\d+)\s*(ms|s|seconds?)", re.I),
    re.compile(r"(\d+)\s*(ms|s|seconds?)\s+timeout", re.I),
    re.compile(r"about\s+(\d+)\s*(ms|s|seconds?)", re.I),
    re.compile(r"approximately\s+(\d+)\s*(ms|s|seconds?)", re.I),
    re.compile(r"takes\s+(\d+)\s*(ms|s|seconds?|min|minutes?)", re.I),
    re.compile(r"wait\s+(\d+)\s*(ms|s|seconds?|min|minutes?)", re.I),
    re.compile(r"delay\s+(?:of\s+)?(\d+)\s*(ms|s|seconds?|min|minutes?)", re.I),
    re.compile(r"ready\s+after\s+(\d+)\s*(ms|s|seconds?)", re.I),
    re.compile(r"(\d+)\s*(min|minutes?)", re.I),
    re.compile(r"(\d+)\s*ms", re.I),
    re.compile(r"(\d+)\s*seconds?", re.I),
]

def to_ms(value, unit):
    u = unit.lower()
    if u.startswith("ms") or u.startswith("millisecond"):
        return int(value)
    if u.startswith("s") or u.startswith("sec"):
        return int(value) * 1000
    if u.startswith("min"):
        return int(value) * 60000
    return None

def scan_phrase_timeouts(text):
    out = []
    seen = set()
    for rx in PHRASE_RES:
        for m in rx.finditer(text):
            ms = to_ms(m.group(1), m.group(2))
            if ms is None:
                continue
            key = (ms, m.group(0).strip().lower())
            if key in seen:
                continue
            seen.add(key)
            out.append({"pattern": rx.pattern, "ms": ms, "raw": m.group(0)})
    return out

def extract_pdf(path, out_dir):
    doc = fitz.open(path)
    base = os.path.splitext(os.path.basename(path))[0]
    results = {"file": os.path.basename(path), "pages": doc.page_count, "hits": []}
    for pno in range(doc.page_count):
        page = doc.load_page(pno)
        text = page.get_text("text")
        if not RESPONSE_TITLE_RE.search(text):
            continue
        entry = {"page": pno + 1, "phrase_hits": scan_phrase_timeouts(text)}
        try:
            tabs = page.find_tables()
            # Use extract() to avoid a pandas dependency.
            entry["tables"] = [t.extract() for t in tabs.tables]
        except Exception as ex:
            entry["table_error"] = str(ex)
        results["hits"].append(entry)
    doc.close()
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, base + ".json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[extract] {os.path.basename(path)} -> {out_path} ({len(results['hits'])} pages)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=CACHE_DIR)
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--pdf", default=None)
    args = ap.parse_args()
    targets = []
    if args.pdf:
        targets = [args.pdf]
    else:
        if not os.path.isdir(args.cache):
            print(f"Cache dir not found: {args.cache}. Run fetch_sources.py first.",
                  file=sys.stderr)
            sys.exit(1)
        for f in sorted(os.listdir(args.cache)):
            if f.lower().endswith(".pdf"):
                targets.append(os.path.join(args.cache, f))
    if not targets:
        print("No PDFs to process.", file=sys.stderr)
        sys.exit(1)
    for p in targets:
        extract_pdf(p, args.out)
    print("Extraction complete (review artifacts under build/extracted/).")

if __name__ == "__main__":
    main()