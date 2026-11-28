#!/usr/bin/env python3
"""Evening publish step (single writer). Merges builder drafts, publishes, verifies, sends.

  python3 tools/publish.py            merge src/*/site.json -> sites.json; STATUS ready -> preview; build
  python3 tools/publish.py --list     print slugs that were just promoted (from .promoted)
After this: node tools/check.js, git push, wait ~90s, confirm each URL is 200, then
python3 tools/outreach.py && python3 tools/send.py first $(cat .promoted)
"""
import json, sys, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
if "--list" in sys.argv:
    print((ROOT / ".promoted").read_text() if (ROOT / ".promoted").exists() else ""); sys.exit()
c = json.loads((ROOT / "sites.json").read_text())
have = {s["slug"] for s in c["sites"]}
promoted = []
for f in sorted((ROOT / "src").glob("*/site.json")):
    d = json.loads(f.read_text()); slug = d["slug"]
    st = (f.parent / "STATUS").read_text().strip() if (f.parent / "STATUS").exists() else "draft"
    if st == "ready":
        (f.parent / "STATUS").write_text("preview\n"); d["lead_status"] = "ready"; promoted.append(slug)
    if slug in have:
        c["sites"] = [d if s["slug"] == slug else s for s in c["sites"]]
    else:
        c["sites"].append(d)
    f.unlink()
(ROOT / "sites.json").write_text(json.dumps(c, indent=2))
(ROOT / ".promoted").write_text(" ".join(promoted))
subprocess.run([sys.executable, str(ROOT / "tools/build.py")], check=True)
print(f"promoted {len(promoted)}: {' '.join(promoted)}")
