#!/usr/bin/env python3
"""Daily batch: find leads, pull Google facts + owner photos, draft a site spec, generate.

  python3 tools/auto_batch.py --shard K --shards 5 --n 10     (each builder session runs one shard)

For each shard it walks its own slice of TRADES x AREAS, searches Google Places, and drafts sites for
leads that pass the gate. Then it STOPS for a human-quality pass by the Claude session running it:
that session must look at every draft's photos and screenshots, rewrite the headline/sub in the
business's own terms, fix anything off, then build, check, push and send (see DAILY.md, "Builder session").

Gate (skip the lead if any fail):
  - open business, rating >= 4.5 with >= 20 reviews, Australian mobile (04..) or a published email
  - no real website (social / booking pages are fine), or a website that's down
  - at least 3 photos uploaded to Google BY THE BUSINESS, each >= 1200px wide
  - not already in sites.json or src/
Outputs drafts in src/<slug>/ with STATUS=draft and prints a summary line per draft.
"""
import argparse, json, re, subprocess, sys, hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import find_leads  # noqa: E402

AREAS = ["Caloundra", "Kawana Waters", "Maroochydore", "Buderim", "Nambour", "Coolum Beach", "Noosaville", "Beerwah",
         "Sippy Downs", "Mooloolaba", "Tewantin", "Pelican Waters", "Caboolture", "Redcliffe", "North Lakes", "Strathpine",
         "Chermside", "Aspley", "Morayfield", "Bribie Island", "Gympie", "Noosa Heads", "Peregian Springs", "Maleny"]
TRADES = ["barber", "nail salon", "hair salon", "lash and brow studio", "beauty salon", "dog grooming", "mobile dog grooming",
          "pressure cleaning", "window cleaning", "lawn mowing", "landscaping", "electrician", "plumber", "handyman",
          "tiler", "painter", "pest control", "pool cleaning", "mobile mechanic", "massage", "personal trainer",
          "cafe", "florist", "tattoo studio", "car detailing", "removalist", "carpet cleaning", "fencing"]
SOCIAL = ("facebook.com", "instagram.com", "fresha.com", "square.site", "linktr.ee", "as.me", "gettimely", "timely",
          "wixsite", "business.site", "bookings.", "setmore", "booksy")

FONTS = [
    {"display": "Archivo", "body": "Inter", "google": "family=Archivo:wght@500;800&family=Inter:wght@400;500;600", "display_weight": 800, "display_case": "uppercase"},
    {"display": "Fraunces", "body": "Manrope", "google": "family=Fraunces:ital,opsz,wght@0,9..144,500;1,9..144,500&family=Manrope:wght@400;500;600", "display_weight": 500, "italic": True},
    {"display": "Oswald", "body": "Inter", "google": "family=Oswald:wght@500;700&family=Inter:wght@400;500;600", "display_weight": 700, "display_case": "uppercase"},
    {"display": "DM Serif Display", "body": "DM Sans", "google": "family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@400;500;700", "display_weight": 400, "italic": True},
    {"display": "Bricolage Grotesque", "body": "DM Sans", "google": "family=Bricolage+Grotesque:opsz,wght@12..96,700;12..96,800&family=DM+Sans:wght@400;500;700", "display_weight": 800},
    {"display": "Syne", "body": "Work Sans", "google": "family=Syne:wght@700;800&family=Work+Sans:wght@400;500;600", "display_weight": 800},
    {"display": "Young Serif", "body": "Figtree", "google": "family=Young+Serif&family=Figtree:wght@400;500;600", "display_weight": 400},
    {"display": "Space Grotesk", "body": "Space Grotesk", "google": "family=Space+Grotesk:wght@400;500;700", "display_weight": 700},
    {"display": "Gloock", "body": "Instrument Sans", "google": "family=Gloock&family=Instrument+Sans:wght@400;500;600", "display_weight": 400},
    {"display": "Anton", "body": "Inter", "google": "family=Anton&family=Inter:wght@400;500;600", "display_weight": 400, "display_case": "uppercase"},
    {"display": "Instrument Serif", "body": "Inter", "google": "family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600", "display_weight": 400, "italic": True},
    {"display": "Plus Jakarta Sans", "body": "Plus Jakarta Sans", "google": "family=Plus+Jakarta+Sans:wght@400;500;700;800", "display_weight": 800},
]
P = lambda bg, sf, ink, mu, ln, ac, ai: {"bg": bg, "surface": sf, "ink": ink, "muted": mu, "line": ln, "accent": ac, "accent_ink": ai}
PALETTES = [
    P("#F4F1EC", "#FFFFFF", "#121417", "#5E6166", "#E2DED7", "#C4202A", "#FFFFFF"),
    P("#0F0F10", "#19191B", "#F3F1EC", "#A7A39B", "#2A2A2D", "#E8B04B", "#111111"),
    P("#FFF6F3", "#FFFFFF", "#2B1A1E", "#7A6166", "#F1DDD8", "#C42D63", "#FFFFFF"),
    P("#F3F8F2", "#FFFFFF", "#17301F", "#5C6F61", "#DCE8DB", "#22783F", "#FFFFFF"),
    P("#FBF7EF", "#FFFFFF", "#231F1A", "#6F675C", "#EDE4D3", "#9C6B12", "#FFFFFF"),
    P("#EFEAE2", "#F8F5F0", "#1F2A33", "#5D6670", "#DAD3C8", "#B4232A", "#FFFFFF"),
    P("#F2F6F9", "#FFFFFF", "#0E2233", "#5A6B7A", "#D9E3EA", "#1463BF", "#FFFFFF"),
    P("#0E1116", "#161B22", "#F1F3F5", "#9AA4AF", "#26303B", "#F5C518", "#111111"),
    P("#F7F2EC", "#FFFFFF", "#2A211C", "#76695F", "#E8DED3", "#8E5634", "#FFFFFF"),
    P("#FFF8F0", "#FFFFFF", "#1E2B3A", "#6B7684", "#EADFD2", "#C25E12", "#FFFFFF"),
    P("#F1EDE3", "#FBF8F1", "#16302B", "#5E6B66", "#DDD6C6", "#1F5E4E", "#FFFFFF"),
    P("#101317", "#171C22", "#EEF1F4", "#9AA3AD", "#27303A", "#3FA7F5", "#0A0A0A"),
]
LAYOUTS = ["split", "fullbleed", "editorial", "poster", "collage"]


def slugify(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:40]


def suburb(addr):
    m = re.search(r",\s*([A-Za-z .'-]+?)\s+QLD", addr or "")
    return m.group(1).strip() if m else ""


def gate(l, known):
    w = (l.get("website") or "").lower()
    ph = re.sub(r"\s", "", l.get("phone") or "")
    return (l.get("status") == "OPERATIONAL" and (l.get("rating") or 0) >= 4.5 and (l.get("reviews") or 0) >= 20
            and ph.startswith("04") and (not w or any(x in w for x in SOCIAL))
            and l["name"].lower() not in known)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shard", type=int, required=True); ap.add_argument("--shards", type=int, default=5)
    ap.add_argument("--n", type=int, default=10); ap.add_argument("--day", type=int, default=0, help="rotation offset (day number)")
    a = ap.parse_args()
    sites = json.loads((ROOT / "sites.json").read_text())["sites"]
    known = {s["name"].lower() for s in sites} | {json.loads(p.read_text())["name"].lower() for p in (ROOT / "src").glob("*/site.json")}
    pairs = [(t, ar) for ar in AREAS for t in TRADES]
    start = (a.day * a.shards + a.shard) * 7 % len(pairs)
    mine = [pairs[(start + i * a.shards) % len(pairs)] for i in range(len(pairs) // a.shards)]
    drafts = []
    for trade, area in mine:
        if len(drafts) >= a.n:
            break
        try:
            find_leads.run(trade, area, 20)
        except Exception as e:
            print("search failed", trade, area, e); continue
        leads = json.loads(find_leads.OUT.read_text())
        for pid, l in sorted(leads.items(), key=lambda kv: -(kv[1].get("reviews") or 0)):
            if len(drafts) >= a.n:
                break
            if l.get("stage") != "new" or l["trade"] != trade or l["area"] != area or not gate(l, known):
                continue
            slug = slugify(l["name"])
            if (ROOT / "src" / slug).exists():
                continue
            r = subprocess.run([sys.executable, str(ROOT / "tools/place_details.py"), slug, l["name"]], capture_output=True, text=True)
            g = json.loads((ROOT / "src" / slug / "google.json").read_text()) if (ROOT / "src" / slug / "google.json").exists() else {}
            own = [p["file"] for p in g.get("own_photos", [])]
            leads[pid]["stage"] = "checked"
            if len(own) < 3:
                leads[pid]["stage"] = "skipped: <3 own HD photos"
                subprocess.run(["rm", "-rf", str(ROOT / "src" / slug)]); continue
            known.add(l["name"].lower())
            h = int(hashlib.md5(slug.encode()).hexdigest(), 16)
            hours = [x.replace(" ", " ").replace(" ", " ") for x in (g.get("regularOpeningHours") or {}).get("weekdayDescriptions", [])] or None
            if hours and all("24 hours" in x for x in hours):
                hours = None   # usually a listing error
            sub = suburb(g.get("formattedAddress")) or area
            cat = (g.get("primaryTypeDisplayName") or {}).get("text") or trade.title()
            spec = {
                "name": g["displayName"]["text"], "kicker": f"{cat} · {sub}",
                "headline": [f"{sub}'s", f"*{trade}*."], "sub": f"{cat} in {sub}. Call or text to book.",
                "layout": LAYOUTS[h % len(LAYOUTS)], "palette": PALETTES[(h // 7) % len(PALETTES)], "fonts": FONTS[(h // 11) % len(FONTS)],
                "hero": own[0], "gallery": own[1:9], "gallery_title": "Recent *work*",
                "hours": hours, "address": g.get("formattedAddress", "").replace(", Australia", ""), "area": f"{sub} QLD",
                "map_query": g.get("formattedAddress"), "rating": {"value": g.get("rating"), "count": g.get("userRatingCount"), "url": g.get("googleMapsUri")},
                "book_url": None, "cta_label": "Call to book", "_DRAFT": "rewrite headline/sub, check photos, check address isn't a home, then delete this key",
            }
            (ROOT / "src" / slug / "spec.json").write_text(json.dumps(spec, indent=1, ensure_ascii=False))
            (ROOT / "src" / slug / "STATUS").write_text("draft\n")
            (ROOT / "src" / slug / "brief.md").write_text(
                f"# Brief: {spec['name']}\n\nSource: Google Business Profile via Places API ({g.get('googleMapsUri')}), fetched {g.get('fetched')}.\n\n"
                f"| Fact | Value |\n|---|---|\n| Name | {spec['name']} |\n| Address | {g.get('formattedAddress')} |\n| Phone | {g.get('nationalPhoneNumber')} |\n"
                f"| Website now | {g.get('websiteUri') or 'none'} |\n| Rating | {g.get('rating')} from {g.get('userRatingCount')} Google reviews |\n| Category | {cat} |\n"
                f"| Hours | {'; '.join(hours or ['not listed'])} |\n\n## Photos\n`img/g-*` uploaded to Google by the business itself (>=1200px). Check each by eye.\n")
            (ROOT / "src" / slug / "site.json").write_text(json.dumps({"slug": slug, "name": spec["name"], "phone": g.get("nationalPhoneNumber", ""), "book_url": "", "owner_email": "", "domain": "",
                          "found_on": "Google", "existing_domain": "", "outreach_email": "", "outreach_source": "", "lead_status": "draft"}, indent=2))
            subprocess.run([sys.executable, str(ROOT / "tools/gen_site.py"), slug], capture_output=True)
            drafts.append(slug)
            print(f"DRAFT {slug}: {spec['name']} · {l['rating']}★ ({l['reviews']}) · {len(own)} own photos · {spec['layout']}")
        find_leads.OUT.write_text(json.dumps(leads, indent=2, ensure_ascii=False))
    print(f"{len(drafts)} drafts: {' '.join(drafts)}")


if __name__ == "__main__":
    main()
