#!/usr/bin/env python3
"""Import a business's own photos (from Chrome / the owner) into its site.
Usage:  python3 tools/import_photos.py photos.zip     (zip with one folder per slug, e.g. kozmetika/1.jpg)
        python3 tools/import_photos.py <folder>
Each image becomes src/<slug>/img/own-N.webp (max 1600px), and is listed in that site's brief.md.
Then add the photos to the page (a "Our work" gallery) and check every one by eye."""
import sys, zipfile, tempfile, shutil
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1])
tmp = Path(tempfile.mkdtemp())
if src.suffix == ".zip":
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    src = tmp
slugs = {p.name for p in (ROOT / "src").iterdir() if p.is_dir()}
for d in sorted(p for p in src.rglob("*") if p.is_dir() and p.name in slugs):
    out = ROOT / "src" / d.name / "img"; out.mkdir(exist_ok=True)
    n = len(list(out.glob("own-*.webp")))
    added = []
    for f in sorted(d.iterdir()):
        if f.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".heic"):
            continue
        try:
            im = Image.open(f).convert("RGB")
        except Exception as e:
            print("skip", f, e); continue
        if im.width > 1600:
            im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        n += 1; name = f"own-{n}.webp"
        im.save(out / name, "WEBP", quality=78, method=6); added.append((name, f.name, im.size))
    if added:
        b = ROOT / "src" / d.name / "brief.md"
        b.write_text(b.read_text() + "\n### Owner's own photos (imported)\n" + "".join(f"- `img/{a}` ({s[0]}×{s[1]}) from `{o}`: source link in chrome-results.md\n" for a, o, s in added))
        print(d.name, "->", [a for a, _, _ in added])
shutil.rmtree(tmp, ignore_errors=True)
