#!/usr/bin/env python3
"""Pull a business's published facts and own photos from its Fresha page.

  python3 tools/fresha.py <slug>            uses book_url from sites.json
  python3 tools/fresha.py <slug> <url>
  python3 tools/fresha.py --all             every site with a Fresha book_url

Writes src/<slug>/fresha.json (facts + source URL + fetch date) and downloads the
business's own gallery photos to src/<slug>/img/fresha-N.webp (max 1600px).
Nothing is invented: every value comes from the page's structured data.
"""
import json, re, sys, datetime, io, urllib.request, html as H
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"}


def get(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        data = r.read()
        return data if binary else data.decode("utf-8", "replace")


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


def extract(url):
    page = get(url)
    out = {"source": url, "fetched": datetime.date.today().isoformat()}
    for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', page, re.S):
        try:
            d = json.loads(m.group(1))
        except Exception:
            continue
        for node in walk(d):
            t = node.get("@type")
            types = t if isinstance(t, list) else [t]
            if any(x and ("Business" in x or "Salon" in x or "Spa" in x or "Store" in x) for x in types):
                out["name"] = H.unescape(re.sub(r"\s*\|\s*Fresha$", "", node.get("name", "")))
                out["telephone"] = node.get("telephone")
                out["summary"] = H.unescape(node.get("description", ""))
                out["price_range"] = node.get("priceRange")
                out["categories"] = [H.unescape(x) for x in node.get("knowsAbout", [])]
                out["socials"] = node.get("sameAs", [])
                a = node.get("address") or {}
                out["address"] = ", ".join(x for x in [a.get("streetAddress"), a.get("addressLocality"), a.get("addressRegion"), a.get("postalCode")] if x)
                ar = node.get("aggregateRating") or {}
                if ar:
                    out["rating"] = {"value": ar.get("ratingValue"), "count": ar.get("reviewCount") or ar.get("ratingCount")}
                if node.get("openingHours"):
                    out["opening_hours"] = node["openingHours"]
                if node.get("geo"):
                    out["geo"] = node["geo"]
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', page, re.S)
    nd = json.loads(m.group(1)) if m else {}
    # long description, socials and website as the business wrote them
    for node in walk(nd):
        if "openingHours" in node and isinstance(node.get("openingHours"), list) and "opening_hours" not in out:
            out["opening_hours"] = node["openingHours"]
        if isinstance(node.get("description"), str) and node.get("description", "").startswith(("At ", "We ", "Welcome")) and "about" not in out:
            out["about"] = node["description"]
        if "websiteUrl" in node:
            out["website"] = node.get("websiteUrl")
            out["instagram"] = node.get("instagramUrl")
            out["facebook"] = node.get("facebookUrl")
    # services with prices (their wording)
    services = []
    for node in walk(nd):
        if node.get("__typename") in ("Service", "ServiceItem", "Package") and node.get("name"):
            price = None
            for k in ("retailPrice", "price", "priceFrom"):
                p = node.get(k)
                if isinstance(p, dict) and "value" in p:
                    price = p["value"]; break
            services.append({"name": H.unescape(node["name"]), "caption": node.get("caption"), "price_aud": price, "type": node["__typename"]})
    seen, uniq = set(), []
    for s in services:
        if s["name"] not in seen:
            seen.add(s["name"]); uniq.append(s)
    out["services"] = uniq
    # the business's own gallery photos (uploaded by the business to its Fresha profile)
    imgs, seen = [], set()
    for node in walk(nd):
        for k in ("url", "src", "imageUrl"):
            u = node.get(k)
            if isinstance(u, str) and "images.fresha.com/locations/location-profile-images" in u:
                base = u.split("?")[0]
                if base not in seen:
                    seen.add(base); imgs.append({"url": base, "description": H.unescape(node.get("description") or node.get("alt") or "")})
    if not imgs:
        for u in sorted(set(re.findall(r'https://images\.fresha\.com/locations/location-profile-images/[^"?\\ ]+', page))):
            imgs.append({"url": u, "description": ""})
    # Fresha also shows OTHER nearby businesses' photos as recommendations. Keep only photos
    # uploaded by this business: the file name carries the business name, and the folder its location id.
    token = re.sub(r"[^A-Za-z0-9]", "", (out.get("name") or "").split(" - ")[0])
    own_dirs = {u["url"].split("/")[-2] for u in imgs if token and token.lower() in u["url"].split("/")[-1].replace("-", "").lower()}
    out["photos"] = [u for u in imgs if u["url"].split("/")[-2] in own_dirs]
    out["photos_skipped_other_businesses"] = len(imgs) - len(out["photos"])
    return out


def save_photos(slug, info, limit=10):
    out = ROOT / "src" / slug / "img"; out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("fresha-*.webp"):
        old.unlink()
    for i, p in enumerate(info["photos"][:limit], 1):
        try:
            im = Image.open(io.BytesIO(get(p["url"] + "?f_width=1600&f_quality=80", binary=True))).convert("RGB")
        except Exception as e:
            p["error"] = str(e); continue
        if im.width > 1600:
            im = im.resize((1600, round(im.height * 1600 / im.width)), Image.LANCZOS)
        name = f"fresha-{i}.webp"
        im.save(out / name, "WEBP", quality=78, method=6)
        p["file"] = f"img/{name}"; p["size"] = list(im.size)


def run(slug, url):
    info = extract(url)
    save_photos(slug, info)
    (ROOT / "src" / slug / "fresha.json").write_text(json.dumps(info, indent=2, ensure_ascii=False))
    print(f"{slug}: {info.get('name')} · {info.get('telephone')} · rating {info.get('rating')} · {len(info['services'])} services · {len([p for p in info['photos'] if p.get('file')])} photos")


if __name__ == "__main__":
    sites = json.loads((ROOT / "sites.json").read_text())["sites"]
    if sys.argv[1:] == ["--all"]:
        for s in sites:
            if "fresha.com" in (s.get("book_url") or ""):
                try:
                    run(s["slug"], s["book_url"])
                except Exception as e:
                    print(s["slug"], "FAILED", e)
    else:
        slug = sys.argv[1]
        url = sys.argv[2] if len(sys.argv) > 2 else next(s["book_url"] for s in sites if s["slug"] == slug)
        run(slug, url)
