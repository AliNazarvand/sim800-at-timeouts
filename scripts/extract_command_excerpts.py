#!/usr/bin/env python3
"""Extract per-command PDF excerpts for manual / AI review.

For every AT command in data/*.yaml whose version_specific list is still
empty, this script pulls the relevant pages out of the cached
V1.01 / V1.10 / V1.12 PDFs and writes:

    build/pdf_excerpts/<slug>/<version>.txt     per-version excerpt
    build/pdf_excerpts/<slug>.md                combined, AI-friendly
    build/pdf_excerpts/INDEX.md                 summary of all commands

The excerpts are wide enough to include the surrounding context
(table, notes, etc.) so a human or an AI can read the Max Response Time
value with confidence.

Usage:
    python scripts/extract_command_excerpts.py
    python scripts/extract_command_excerpts.py --max-pages 3
"""
import argparse
import os
import re
import sys

try:
    import fitz
except ImportError:
    try:
        import pymupdf as fitz
    except ImportError:
        print("PyMuPDF is required: pip install PyMuPDF", file=sys.stderr)
        sys.exit(1)

try:
    import yaml
except ImportError:
    print("PyYAML is required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR  = os.path.join(ROOT, "data")
CACHE_DIR = os.path.join(ROOT, ".cache", "sources")
OUT_DIR   = os.path.join(ROOT, "build", "pdf_excerpts")

SKIP_FILES = {
    "versions.yaml","chapter_mapping.yaml","category_mapping.yaml",
    "command_inventory.yaml","module_compatibility.yaml",
}

PDFS = {
    "V1.01": "SIM800 Series_AT Command Manual_V1.01.pdf",
    "V1.10": "SIM800 Series_AT Command Manual_V1.10.pdf",
    "V1.12": "SIM800 Series_AT Command Manual_V1.12.pdf",
}

# characters of context to include before / after the match
PAD_BEFORE = 400
PAD_AFTER  = 2600


def slugify(cmd: str) -> str:
    """AT+CSQ -> AT_CSQ ; AT+HTTPACTION -> AT_HTTPACTION."""
    s = cmd.strip()
    s = s.replace("+", "_")
    s = re.sub(r"[^A-Za-z0-9_]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "UNKNOWN"


def load_yaml(p):
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_pdf(path):
    """Return list of (page_number, text)."""
    doc = fitz.open(path)
    pages = [(i + 1, doc.load_page(i).get_text("text"))
             for i in range(doc.page_count)]
    doc.close()
    return pages


def pages_for_command(cmd, pages, max_pages=None):
    """Return list of (page_number, excerpt_string) around cmd.

    Uses word-boundary matching, avoids the table-of-contents by
    preferring pages where the command appears near the word
    'Response' or 'Timeout' (which is where the actual spec lives).
    Falls back to first plain occurrence if no such page exists.
    """
    cmd_re = re.compile(r"\b" + re.escape(cmd) + r"\b")
    hits   = []
    for pno, text in pages:
        for m in cmd_re.finditer(text):
            start = max(0, m.start() - PAD_BEFORE)
            end   = min(len(text), m.end() + PAD_AFTER)
            excerpt = text[start:end]
            score = 0
            if re.search(r"Response\s+Time", excerpt, re.I):
                score += 10
            if re.search(r"Timeout", excerpt, re.I):
                score += 5
            if re.search(r"Table", excerpt, re.I):
                score += 2
            hits.append((score, pno, m.start(), excerpt))
    if not hits:
        return []

    # Group by page, keep the best (highest score, then earliest offset)
    by_page = {}
    for score, pno, off, ex in hits:
        cur = by_page.get(pno)
        if cur is None or score > cur[0]:
            by_page[pno] = (score, off, ex)

    # Order pages: highest score first, then page number ascending
    ordered = sorted(by_page.items(), key=lambda kv: (-kv[1][0], kv[0]))
    if max_pages is not None:
        ordered = ordered[:max_pages]
    # Re-sort by page number for readability
    ordered = sorted(ordered, key=lambda kv: kv[0])
    return [(pno, v[2]) for pno, v in ordered]


def collect_targets():
    """Yield (fname, command, entry) for entries with empty version_specific."""
    for fname in sorted(os.listdir(DATA_DIR)):
        if not fname.endswith(".yaml") or fname in SKIP_FILES:
            continue
        data = load_yaml(os.path.join(DATA_DIR, fname))
        for e in data.get("entries") or []:
            cmd = e.get("command") or ""
            if not cmd.startswith("AT+"):
                continue
            if e.get("version_specific"):
                continue
            yield fname, cmd, e


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-pages", type=int, default=2,
                    help="maximum excerpt pages per PDF per command "
                         "(default: 2)")
    args = ap.parse_args()

    if not os.path.isdir(CACHE_DIR):
        print(f"Cache dir not found: {CACHE_DIR}", file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)

    # Load PDFs once
    pdf_cache = {}
    for ver, fname in PDFS.items():
        path = os.path.join(CACHE_DIR, fname)
        if not os.path.exists(path):
            print(f"[warn] missing PDF: {path}", file=sys.stderr)
            continue
        print(f"[load] {ver}: {path}")
        pdf_cache[ver] = load_pdf(path)

    if not pdf_cache:
        print("No PDFs loaded; aborting.", file=sys.stderr)
        sys.exit(1)

    index_rows = []
    written = 0

    for fname, cmd, entry in collect_targets():
        slug = slugify(cmd)
        slug_dir = os.path.join(OUT_DIR, slug)
        os.makedirs(slug_dir, exist_ok=True)

        per_version_text = {}
        found_versions = []

        for ver in PDFS.keys():
            if ver not in pdf_cache:
                continue
            pages = pdf_cache[ver]
            excerpts = pages_for_command(cmd, pages, max_pages=args.max_pages)
            if not excerpts:
                txt = f"[No occurrence of {cmd} found in {ver}]\n"
                per_version_text[ver] = (txt, [])
                continue
            found_versions.append(ver)
            chunks = []
            used_pages = []
            for pno, ex in excerpts:
                chunks.append(f"----- page {pno} -----\n{ex}")
                used_pages.append(pno)
            per_version_text[ver] = ("\n\n".join(chunks), used_pages)

            with open(os.path.join(slug_dir, f"{ver}.txt"),
                      "w", encoding="utf-8", newline="\n") as f:
                f.write(f"# {cmd}  --  {ver}\n")
                f.write(f"# source: {PDFS[ver]}\n")
                f.write(f"# pages: {used_pages}\n\n")
                f.write(per_version_text[ver][0])

        # Combined markdown
        md_path = os.path.join(OUT_DIR, f"{slug}.md")
        md = []
        md.append(f"# {cmd}")
        md.append("")
        md.append(f"- file: `{fname}`")
        md.append(f"- representative_version: "
                  f"`{entry.get('representative_version','?')}`")
        rep_tv = (entry.get("timeouts") or [{}])[0]
        md.append(f"- representative_timeout_kind: "
                  f"`{rep_tv.get('timeout_kind','?')}`")
        md.append(f"- representative_max_value_ms: "
                  f"`{rep_tv.get('max_value_ms')}`")
        md.append(f"- available_in_versions: "
                  f"`{entry.get('available_in_versions')}`")
        md.append("")
        md.append("> Ask the AI to fill `version_specific` / `version_reviews` "
                  "for each non-representative version, using ONLY the "
                  "excerpts below.")
        md.append("")
        for ver in PDFS.keys():
            if ver not in per_version_text:
                continue
            txt, used_pages = per_version_text[ver]
            md.append(f"## {ver}")
            md.append("")
            if used_pages:
                md.append(f"Pages: {used_pages}")
            else:
                md.append(f"_No occurrence of {cmd} found in {ver}._")
            md.append("")
            md.append("```text")
            md.append(txt)
            md.append("```")
            md.append("")

        with open(md_path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(md))
        written += 1

        index_rows.append({
            "command": cmd,
            "file": fname,
            "slug": slug,
            "found_in": found_versions,
            "combined_md": os.path.relpath(md_path, ROOT),
        })

    # Index
    idx = ["# PDF Excerpts Index", ""]
    idx.append(f"Commands with empty `version_specific`: {len(index_rows)}")
    idx.append("")
    idx.append("| command | source yaml | found in | combined |")
    idx.append("|---------|-------------|----------|----------|")
    for r in index_rows:
        idx.append(f"| {r['command']} | {r['file']} "
                   f"| {','.join(r['found_in']) or '-'} "
                   f"| [{r['slug']}.md]({r['slug']}.md) |")
    idx.append("")
    with open(os.path.join(OUT_DIR, "INDEX.md"),
              "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(idx))

    print(f"[excerpts] commands processed: {len(index_rows)}")
    print(f"[excerpts] combined files written: {written}")
    print(f"[excerpts] output: {os.path.relpath(OUT_DIR, ROOT)}")
    print(f"[excerpts] index : "
          f"{os.path.relpath(os.path.join(OUT_DIR, 'INDEX.md'), ROOT)}")


if __name__ == "__main__":
    main()