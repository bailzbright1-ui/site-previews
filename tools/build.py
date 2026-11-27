#!/usr/bin/env python3
"""Build preview sites into docs/ (served by GitHub Pages) or a live site into live/.

Preview (all sites):   python3 tools/build.py
Go live (one site):    python3 tools/build.py --live <slug> --email owner@biz.com.au [--domain biz.com.au] [--phone "0400 000 000"]

Source pages in src/<slug>/index.html use these tokens:
  {{NAME}} {{AGENCY}} {{PHONE_DISPLAY}} {{PHONE_HREF}} {{CALL_LABEL}} {{BOOK_URL}} {{FORM_ENDPOINT}} {{YEAR}}
and these preview-only markers, which the live build strips:
  <!--PREVIEW--> ... <!--/PREVIEW-->      (blocks, e.g. the preview banner)
  any line containing PREVIEW-ONLY         (e.g. the noindex meta tag)
"""
import argparse, datetime, json, re, shutil, sys, zipfile
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, DOCS, LIVE = ROOT / "src", ROOT / "docs", ROOT / "live"


def load():
    return json.loads((ROOT / "sites.json").read_text(encoding="utf-8"))


def phone_tokens(phone):
    if phone:
        digits = re.sub(r"[^\d+]", "", phone)
        return {"PHONE_DISPLAY": phone, "PHONE_HREF": f"tel:{digits}", "CALL_LABEL": f"Call {phone}"}
    # No published number yet: call buttons become "request a call back" and scroll to the form.
    return {"PHONE_DISPLAY": "Request a call back", "PHONE_HREF": "#quote", "CALL_LABEL": "Request a call back"}


def render(html, site, agency, live=False, endpoint=""):
    toks = {
        "NAME": site["name"], "AGENCY": agency["name"], "BOOK_URL": site.get("book_url") or "#contact",
        "FORM_ENDPOINT": endpoint, "YEAR": str(datetime.date.today().year),
        **phone_tokens(site.get("phone", "")),
    }
    for k, v in toks.items():
        html = html.replace("{{" + k + "}}", v)
    if live:
        html = re.sub(r"<!--PREVIEW-->.*?<!--/PREVIEW-->", "", html, flags=re.S)
        html = "\n".join(l for l in html.splitlines() if "PREVIEW-ONLY" not in l)
    from motion import HEAD as MH, BODY as MB
    if "data-no-motion" not in html:
        html = html.replace("</head>", MH + "\n</head>", 1).replace("</body>", MB + "\n</body>", 1)
    left = re.findall(r"\{\{[A-Z_]+\}\}", html)
    if left:
        sys.exit(f"{site['slug']}: unresolved tokens {sorted(set(left))}")
    return html


def build_previews(data):
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir()
    (DOCS / ".nojekyll").write_text("")
    (DOCS / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    (DOCS / "index.html").write_text(
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><title>Website previews</title></head>'
        '<body style="font:16px system-ui;display:grid;place-items:center;min-height:100vh;margin:0;color:#555">'
        '<p>Private website previews. Use the link you were sent.</p></body></html>')
    for s in data["sites"]:
        src = SRC / s["slug"] / "index.html"
        if not src.exists():
            print(f"skip {s['slug']} (no source yet)")
            continue
        out = DOCS / s["slug"]
        out.mkdir(parents=True)
        out.joinpath("index.html").write_text(render(src.read_text(encoding="utf-8"), s, data["agency"]), encoding="utf-8")
        for extra in (SRC / s["slug"]).iterdir():  # copy any images/assets
            if extra.name not in ("index.html", "design.md", "src-img"):
                (shutil.copytree if extra.is_dir() else shutil.copy2)(extra, out / extra.name)
        print(f"built docs/{s['slug']}/")


def build_live(data, slug, email, domain, phone):
    site = next((s for s in data["sites"] if s["slug"] == slug), None)
    if not site:
        sys.exit(f"unknown slug {slug}")
    if phone:
        site["phone"] = phone
    out = LIVE / slug
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    endpoint = f"https://formsubmit.co/ajax/{email}"
    html = render((SRC / slug / "index.html").read_text(encoding="utf-8"), site, data["agency"], live=True, endpoint=endpoint)
    out.joinpath("index.html").write_text(html, encoding="utf-8")
    for extra in (SRC / slug).iterdir():
        if extra.name not in ("index.html", "design.md", "src-img"):
            (shutil.copytree if extra.is_dir() else shutil.copy2)(extra, out / extra.name)
    if domain:
        out.joinpath("CNAME").write_text(domain + "\n")
        out.joinpath("robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: https://{domain}/sitemap.xml\n")
        out.joinpath("sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f'<url><loc>https://{domain}/</loc></url></urlset>\n')
    zpath = LIVE / f"{slug}.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in out.rglob("*"):
            z.write(f, f.relative_to(out))
    print(f"live site ready: live/{slug}/  (zip: live/{slug}.zip)")
    print(f"form enquiries -> {email} (FormSubmit sends them a one-time 'activate' email on the first enquiry)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--live", metavar="SLUG")
    ap.add_argument("--email", help="owner's email for enquiry forms (required with --live)")
    ap.add_argument("--domain", default="")
    ap.add_argument("--phone", default="")
    a = ap.parse_args()
    d = load()
    if a.live:
        if not a.email:
            sys.exit("--email is required with --live")
        build_live(d, a.live, a.email, a.domain, a.phone)
    else:
        build_previews(d)
