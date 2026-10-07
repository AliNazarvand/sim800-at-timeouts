#!/usr/bin/env python3
"""Fetch PDF sources and verify SHA-256 checksums (TOFU).

On first run, the SHA-256 of each downloaded PDF is recorded in
.cache/sources.sha256.json and reflected into docs/sources.md.
On later runs, the recorded hashes are verified.
"""
import argparse
import hashlib
import json
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CACHE = os.path.join(ROOT, ".cache", "sources")
MANIFEST_REL = os.path.join(".cache", "sources.sha256.json")
SOURCES_MD_REL = os.path.join("docs", "sources.md")

SOURCES = {
    "SIM800 Series_AT Command Manual_V1.01.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800%20Series_AT%20Command%20Manual_V1.01.pdf",
    "SIM800 Series_AT Command Manual_V1.10.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800%20Series_AT%20Command%20Manual_V1.10.pdf",
    "SIM800 Series_AT Command Manual_V1.12.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800%20Series_AT%20Command%20Manual_V1.12.pdf",
    "SIM800A_Hardware Design_V1.02.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800A_Hardware%20Design_V1.02.pdf",
    "SIM800C-DS_Hardware_Design_V1.01.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800C-DS_Hardware_Design_V1.01.pdf",
    "SIM800C_Hardware_Design_V1.02.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800C_Hardware_Design_V1.02.pdf",
    "SIM800F_Hardware Design_V1.05.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800F_Hardware%20Design_V1.05.pdf",
    "SIM800H&SIM800L_Hardware Design_V2.02.PDF": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800H%26SIM800L_Hardware%20Design_V2.02.PDF",
    "SIM800H_Hardware Design_V2.03.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800H_Hardware%20Design_V2.03.pdf",
    "SIM800L_Hardware Design_V1.00.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800L_Hardware%20Design_V1.00.pdf",
    "SIM800_Hardware Design_V1.09.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM800_Hardware%20Design_V1.09.pdf",
    "SIM808_Hardware Design_V1.03.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM808_Hardware%20Design_V1.03.pdf",
    "SIM868_Hardware_Design_V1.00.pdf": "https://raw.githubusercontent.com/AliNazarvand/Package-Datasheet/main/SIM868_Hardware_Design_V1.00.pdf",
}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def page_count(path):
    try:
        import fitz
        doc = fitz.open(path)
        n = doc.page_count
        doc.close()
        return n
    except Exception:
        return None

def load_manifest(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_manifest(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)

def write_sources_md(path, rows):
    lines = [
        "# Sources",
        "",
        "| Document | URL | SHA-256 | Pages |",
        "|----------|-----|---------|------:|",
    ]
    for name, url, sha, pages in rows:
        pg = str(pages) if pages is not None else "?"
        lines.append(f"| {name} | {url} | `{sha}` | {pg} |")
    lines.append("")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))

def fetch_all(cache_dir, manifest_path, sources_md_path):
    os.makedirs(cache_dir, exist_ok=True)
    manifest = load_manifest(manifest_path)
    rows = []
    changed = False
    for name, url in SOURCES.items():
        dest = os.path.join(cache_dir, name)
        if not os.path.exists(dest):
            print(f"[fetch] {name} ...")
            try:
                urllib.request.urlretrieve(url, dest)
            except Exception as e:
                print(f"[error] {name}: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"[skip]  {name}")
        actual = sha256_file(dest)
        expected = manifest.get(name)
        if expected is None:
            manifest[name] = actual
            changed = True
            print(f"[hash]  {name} -> {actual[:12]}")
        elif expected != actual:
            print(f"[error] checksum mismatch for {name}", file=sys.stderr)
            print(f"        expected {expected}", file=sys.stderr)
            print(f"        actual   {actual}", file=sys.stderr)
            sys.exit(1)
        rows.append((name, url, actual, page_count(dest)))
    if changed:
        save_manifest(manifest_path, manifest)
    write_sources_md(sources_md_path, rows)
    print("All sources fetched and verified.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=DEFAULT_CACHE)
    ap.add_argument("--manifest", default=os.path.join(ROOT, MANIFEST_REL))
    ap.add_argument("--sources-md", default=os.path.join(ROOT, SOURCES_MD_REL))
    args = ap.parse_args()
    fetch_all(args.cache, args.manifest, args.sources_md)

if __name__ == "__main__":
    main()
