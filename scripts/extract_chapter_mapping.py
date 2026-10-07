#!/usr/bin/env python3
"""Extract chapter numbering from PDF TOC (requires PyMuPDF)."""
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
CHAPTER_RE = re.compile(r"^\s*Chapter\s+(\d+)\s*[:\.]?\s*(.+?)\s*$", re.M)

def extract(path):
    doc = fitz.open(path)
    toc = doc.get_toc() or []
    chapters = []
    for lvl, title, page in toc:
        m = CHAPTER_RE.match(title)
        if m:
            chapters.append({"number": int(m.group(1)),
                             "title": m.group(2).strip(),
                             "page": page})
    doc.close()
    return chapters

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=CACHE_DIR)
    ap.add_argument("--out", default=OUT_DIR)
    args = ap.parse_args()
    if not os.path.isdir(args.cache):
        print(f"Cache dir not found: {args.cache}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(args.out, exist_ok=True)
    for f in sorted(os.listdir(args.cache)):
        if not f.lower().endswith(".pdf"):
            continue
        chapters = extract(os.path.join(args.cache, f))
        base = os.path.splitext(f)[0]
        out_path = os.path.join(args.out, base + ".chapters.json")
        with open(out_path, "w", encoding="utf-8") as fo:
            json.dump({"file": f, "chapters": chapters}, fo,
                      ensure_ascii=False, indent=2)
        print(f"[toc] {f}: {len(chapters)} chapters -> {out_path}")

if __name__ == "__main__":
    main()
