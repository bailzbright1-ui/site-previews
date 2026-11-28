#!/usr/bin/env python3
"""Download the original Dribbble images for every reference (optional).

The skill already ships with screenshots in images/. Run this only if you
want the designers' full shot images too. They are saved to
images/originals/<id>-<slug>/ and are for private reference only.

Usage:
  python fetch_originals.py                # all references, resized to 1600px wide (recommended)
  python fetch_originals.py --only 12 15   # just some references
  python fetch_originals.py --full         # full-resolution originals (large: several MB each)
  python fetch_originals.py --videos       # also download the shot videos (.mp4/.mov)
"""
import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SOURCES = SKILL_DIR / "sources.json"
OUT = SKILL_DIR / "images" / "originals"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
    "Referer": "https://dribbble.com/",
    "Accept": "image/avif,image/webp,image/png,image/jpeg,*/*;q=0.8",
}
EXT = {"image/png": ".png", "image/jpeg": ".jpg", "image/webp": ".webp", "image/gif": ".gif",
       "image/avif": ".avif", "video/mp4": ".mp4", "video/quicktime": ".mov"}


def fetch(url, dest_stem):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as resp:
        ctype = resp.headers.get("Content-Type", "").split(";")[0].strip()
        ext = EXT.get(ctype) or Path(url.split("?")[0]).suffix or ".bin"
        dest = dest_stem.with_suffix(ext)
        if dest.exists() and dest.stat().st_size > 0:
            return dest, "exists"
        data = resp.read()
    dest.write_bytes(data)
    return dest, f"{len(data) // 1024} KB"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", help="reference ids, e.g. 01 12")
    ap.add_argument("--full", action="store_true", help="download full-resolution originals")
    ap.add_argument("--videos", action="store_true", help="also download videos")
    args = ap.parse_args()

    refs = json.loads(SOURCES.read_text(encoding="utf-8"))
    if args.only:
        wanted = {i.zfill(2) for i in args.only}
        refs = [r for r in refs if r["id"] in wanted]

    ok = fail = 0
    for r in refs:
        folder = OUT / f"{r['id']}-{r['slug']}"
        folder.mkdir(parents=True, exist_ok=True)
        items = [(u, "img") for u in r["images"]]
        if args.videos:
            items += [(u, "vid") for u in r["videos"]]
        if not items:
            print(f"{r['id']} {r['slug']}: video-only shot, use --videos (screenshots already in images/)")
            continue
        for n, (url, kind) in enumerate(items, 1):
            src = url if (args.full or kind == "vid") else url + "?resize=1600x1200&vertical=center"
            stem = folder / f"{n:02d}-{kind}"
            try:
                dest, info = fetch(src, stem)
                ok += 1
                print(f"{r['id']} {r['slug']}: {dest.name} ({info})")
            except Exception as exc:  # network errors, 403s, timeouts
                fail += 1
                print(f"{r['id']} {r['slug']}: FAILED {src} ({exc})", file=sys.stderr)
            time.sleep(0.3)
    print(f"\nDone: {ok} downloaded, {fail} failed. Files are in {OUT}")
    if fail:
        print("Failures are usually network or CDN blocks. The bundled screenshots in images/ are enough to work from.")


if __name__ == "__main__":
    main()
