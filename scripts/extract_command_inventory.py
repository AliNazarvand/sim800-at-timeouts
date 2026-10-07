#!/usr/bin/env python3
"""Extract AT command names from PDF text (requires PyMuPDF)."""
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
CMD_RE = re.compile(r"\bAT\+([A-Z][A-Z0-9]{1,15})\b")

def extract(path):
    doc = fitz.open(path)
    found = {}
    for pno in range(doc.page_count):
        txt = doc.load_page(pno).get_text("text")
        for m in CMD_RE.finditer(txt):
            name = "AT+" + m.group(1)
            found.setdefault(name, pno + 1)
    doc.close()
    return sorted(found.items())

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
            print(f"Cache dir not found: {args.cache}", file=sys.stderr)
            sys.exit(1)
        for f in sorted(os.listdir(args.cache)):
            if f.lower().endswith(".pdf"):
                targets.append(os.path.join(args.cache, f))

    os.makedirs(args.out, exist_ok=True)
    for p in targets:
        cmds = extract(p)
        base = os.path.splitext(os.path.basename(p))[0]
        out_path = os.path.join(args.out, base + ".commands.json")
        with open(out_path, "w", encoding="utf-8") as fo:
            json.dump({"file": os.path.basename(p),
                       "commands": [{"name": n, "first_page": pg} for n, pg in cmds]},
                      fo, ensure_ascii=False, indent=2)
        print(f"[inv] {os.path.basename(p)}: {len(cmds)} commands -> {out_path}")

if __name__ == "__main__":
    main()
