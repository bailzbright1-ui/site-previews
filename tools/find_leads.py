#!/usr/bin/env python3
"""Find Sunshine Coast businesses worth building a preview for, via Google Places (New).

  python3 tools/find_leads.py "plumber" "Caloundra" [--max 20]
  python3 tools/find_leads.py --batch            runs TRADES x AREAS below (watch your Places quota)

Writes/updates leads.json: one entry per Google place, with the published facts Google holds
(name, address, phone, website, hours, rating, review count, Maps link) and a score.
Best leads: open, well reviewed, and either no website or one that's down.
"""
import json, sys, urllib.request, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "leads.json"
FIELDS = ("places.id,places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.websiteUri,"
          "places.rating,places.userRatingCount,places.googleMapsUri,places.businessStatus,places.primaryTypeDisplayName,"
          "places.regularOpeningHours.weekdayDescriptions")
TRADES = ["plumber", "electrician", "roofer", "pest control", "lawn mowing", "pressure cleaning", "nail salon",
          "lash and brow studio", "beauty salon", "dog grooming", "mobile mechanic", "pool cleaning", "painter", "barber"]
AREAS = ["Caloundra", "Kawana Waters", "Maroochydore", "Buderim", "Nambour", "Coolum Beach", "Noosaville", "Beerwah"]


def search(q, maxn=20):
    req = urllib.request.Request("https://places.googleapis.com/v1/places:searchText", method="POST",
        data=json.dumps({"textQuery": q, "regionCode": "AU", "pageSize": min(maxn, 20)}).encode(),
        headers={"Content-Type": "application/json", "X-Goog-FieldMask": FIELDS})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read()).get("places", [])


def site_ok(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=12) as r:
            return r.status < 400
    except Exception:
        return False   # down, or not reachable from this environment (domain not on the allow-list)


def score(p):
    if p.get("businessStatus") != "OPERATIONAL":
        return -99
    s = 0
    w = (p.get("websiteUri") or "").lower()
    s += 3 if (not w or any(x in w for x in ("facebook.com", "instagram.com", "fresha.com", "square.site", "linktr.ee", "as.me", "timely", "wixsite", "business.site"))) else 0
    r, n = p.get("rating", 0), p.get("userRatingCount", 0)
    s += 2 if r >= 4.7 else 1 if r >= 4.3 else 0
    s += 2 if n >= 50 else 1 if n >= 15 else 0
    s += 1 if p.get("nationalPhoneNumber") else -2
    return s


def run(trade, area, maxn):
    leads = json.loads(OUT.read_text()) if OUT.exists() else {}
    known = {s["name"].lower() for s in json.loads((ROOT / "sites.json").read_text())["sites"]}
    for p in search(f"{trade} in {area} QLD", maxn):
        name = p["displayName"]["text"]
        if p["id"] in leads or name.lower() in known:
            continue
        leads[p["id"]] = {
            "name": name, "trade": trade, "area": area, "address": p.get("formattedAddress"),
            "phone": p.get("nationalPhoneNumber"), "website": p.get("websiteUri"),
            "rating": p.get("rating"), "reviews": p.get("userRatingCount"), "maps": p.get("googleMapsUri"),
            "hours": (p.get("regularOpeningHours") or {}).get("weekdayDescriptions"),
            "type": (p.get("primaryTypeDisplayName") or {}).get("text"), "status": p.get("businessStatus"),
            "score": score(p), "found": datetime.date.today().isoformat(), "source": "Google Places API", "stage": "new"}
    OUT.write_text(json.dumps(leads, indent=2, ensure_ascii=False))
    top = sorted((l for l in leads.values() if l["area"] == area and l["trade"] == trade), key=lambda l: -l["score"])
    for l in top[:8]:
        print(f'{l["score"]:>3}  {l["name"][:40]:40} {l["rating"]}★ ({l["reviews"]})  {l["phone"] or "-":14} {l["website"] or "NO WEBSITE"}')


if __name__ == "__main__":
    a = sys.argv[1:]
    maxn = int(a[a.index("--max") + 1]) if "--max" in a else 20
    if "--batch" in a:
        for t in TRADES:
            for ar in AREAS:
                run(t, ar, maxn)
    else:
        run(a[0], a[1], maxn)
