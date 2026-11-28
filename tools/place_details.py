#!/usr/bin/env python3
"""Fetch full Google details + the business's OWN uploaded photos for a lead.

  python3 tools/place_details.py <slug> "<exact business name>"     (name must be in leads.json)

Writes src/<slug>/google.json and src/<slug>/img/g-N.webp. Only photos whose author is the
business itself are kept, and only if they're at least 1200px wide (the quality rule).
"""
import json, sys, io, urllib.request, datetime, re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
FIELDS = ("id,displayName,formattedAddress,addressComponents,nationalPhoneNumber,internationalPhoneNumber,websiteUri,rating,"
          "userRatingCount,googleMapsUri,regularOpeningHours.weekdayDescriptions,primaryTypeDisplayName,types,"
          "editorialSummary,photos,location,businessStatus")


def api(url, fields=None, binary=False):
    h = {"X-Goog-FieldMask": fields} if fields else {}
    with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=40) as r:
        d = r.read()
        return d if binary else json.loads(d)


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def run(slug, name):
    leads = json.loads((ROOT / "leads.json").read_text())
    pid = next(k for k, v in leads.items() if v["name"] == name)
    d = api(f"https://places.googleapis.com/v1/places/{pid}", FIELDS)
    out = ROOT / "src" / slug / "img"; out.mkdir(parents=True, exist_ok=True)
    biz = norm(d["displayName"]["text"])
    kept = []
    for ph in d.get("photos", []):
        authors = [a.get("displayName", "") for a in ph.get("authorAttributions", [])]
        own = any(norm(a) and (norm(a) in biz or biz in norm(a) or norm(a)[:10] == biz[:10]) for a in authors)
        if not own or ph.get("widthPx", 0) < 1200:
            continue
        try:
            img = Image.open(io.BytesIO(api(f"https://places.googleapis.com/v1/{ph['name']}/media?maxWidthPx=1600", binary=True))).convert("RGB")
        except Exception as e:
            print("photo failed", e); continue
        n = len(kept) + 1
        img.save(out / f"g-{n}.webp", "WEBP", quality=78, method=6)
        kept.append({"file": f"img/g-{n}.webp", "size": img.size, "author": authors})
    d.pop("photos", None)
    d["own_photos"] = kept
    d["fetched"] = datetime.date.today().isoformat()
    d["source"] = d.get("googleMapsUri")
    (ROOT / "src" / slug / "google.json").write_text(json.dumps(d, indent=2, ensure_ascii=False))
    print(f"{slug}: {len(kept)} own HD photos · {d.get('editorialSummary', {}).get('text', '')[:80]}")


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2])
