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
        "PREVIEW_BAR": (ROOT / "tools/snippet_previewbar.html").read_text(encoding="utf-8"),
        "CLAIM_LINK": f"../keep/?site={site['slug']}",
        "STUDIO_EMAIL": agency.get("email", ""), "STUDIO_MOBILE": agency.get("mobile", ""),
        "STUDIO_MOBILE_HREF": re.sub(r"[^0-9+]", "", agency.get("mobile", "")),
        "YOUR_FIRST": (agency.get("your_name") or "us").split()[0],
        "BAR_OFFER": "1st month free" if agency.get("trial_days") else agency.get("price_keep", "$29") + "/mo",
        "STUDIO_SITE": agency.get("studio_site") or "../",
        "NAME": site["name"], "AGENCY": agency["name"], "BOOK_URL": site.get("book_url") or "#contact",
        "FORM_ENDPOINT": endpoint, "YEAR": str(datetime.date.today().year),
        **phone_tokens(site.get("phone", "")),
    }
    for k in ("PREVIEW_BAR",):  # snippets first, they contain tokens
        html = html.replace("{{" + k + "}}", toks.pop(k))
    if live:
        credit = (ROOT / "tools/snippet_builtby.html").read_text(encoding="utf-8")
        html = html.replace("</footer>", '<div style="padding:8px 0">' + credit + "</div></footer>", 1)
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
    for s in data["sites"]:
        src = SRC / s["slug"] / "index.html"
        if not src.exists():
            print(f"skip {s['slug']} (no source yet)")
            continue
        out = DOCS / s["slug"]
        out.mkdir(parents=True)
        out.joinpath("index.html").write_text(render(src.read_text(encoding="utf-8"), s, data["agency"]), encoding="utf-8")
        for extra in (SRC / s["slug"]).iterdir():  # copy any images/assets
            if extra.name not in ("index.html", "design.md", "src-img", "brief.md", "STATUS", "outreach.md"):
                (shutil.copytree if extra.is_dir() else shutil.copy2)(extra, out / extra.name)
        print(f"built docs/{s['slug']}/")


def build_studio(data):
    """One Sight Studio's own pages (home + keep/claim flow) into docs/ root."""
    a = data["agency"]
    sites = {s["slug"]: {"name": s["name"]} for s in data["sites"] if (SRC / s["slug"] / "index.html").exists()}
    dl = ""
    for label, key, href in (("Name", "your_name", None), ("Email", "email", "mailto:"), ("Mobile", "mobile", "tel:")):
        if a.get(key):
            v = a[key]
            val = f'<a href="{href}{re.sub(r"[^0-9+@a-zA-Z._-]", "", v)}">{v}</a>' if href else v
            dl += f"<div><dt class=\"small\">{label}</dt><dd>{val}</dd></div>"
    if not dl:
        dl = '<div><dd class="small" style="color:var(--ink-muted)">Contact details coming soon.</dd></div>'
    toks = {
        "PRICE_KEEP": a.get("price_keep", "$29"), "PRICE_GROW": a.get("price_grow", "$59"),
        "YEAR": str(datetime.date.today().year), "CONTACT_DL": dl,
        "YOUR_FIRST": (a.get("your_name") or "us").split()[0], "MOBILE": a.get("mobile", ""),
        "MOBILE_HREF": re.sub(r"[^0-9+]", "", a.get("mobile", "")),
        "ABN_LINE": f" · ABN {a['abn']}" if a.get("abn") else "",
        "STUDIO_ROBOTS": "" if a.get("email") and a.get("abn") else '<meta name="robots" content="noindex, nofollow">',
        "SITES_JSON": json.dumps(sites),
        **(lambda t, pk: {
            "OFFER_LINE": f"your first month is free, then it's {pk} a month." if t else f"it goes live for {pk} a month.",
            "COMPARE_LINE": f"First month free, then {pk} a month." if t else f"then {pk} a month.",
            "TRIAL_NOTE": " Your first month is free on Keep and Grow. We remind you before your first payment." if t else "",
            "TRIAL_FAQ": f'<details><summary>How does the free month work?</summary><p>Your site goes live and you pay nothing for the first {t} days. We email you before your first payment. If you cancel before then, you are not charged.</p></details>' if t else "",
            "KEEP_FINE": f"Your first month is free. You enter your card on a secure Stripe page, and you are not charged until day {t + 1}. We remind you before then, and you can cancel before then at no cost." if t else "You'll pay by card on a secure Stripe page.",
            "TODAY_ROW": '<div><span>Due today</span><span>$0</span></div>' if t else "",
            "MONTHLY_LABEL": f"Monthly, after {t} days free" if t else "Monthly",
            "GO_LABEL": "Start my free month" if t else "Continue to secure payment",
        })(a.get("trial_days"), a.get("price_keep", "$29")),
        "KEEP_CFG": json.dumps({"email": a.get("email", ""), "stripe_keep": a.get("stripe_keep_link", ""), "stripe_grow": a.get("stripe_grow_link", "")}),
    }
    studio = ROOT / "studio"
    for page in studio.rglob("index.html"):
        html = page.read_text(encoding="utf-8")
        for k, v in toks.items():
            html = html.replace("{{" + k + "}}", v)
        left = re.findall(r"\{\{[A-Z_]+\}\}", html)
        if left:
            sys.exit(f"studio {page}: unresolved tokens {sorted(set(left))}")
        out = DOCS / page.relative_to(studio)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8")
    shutil.copytree(studio / "assets", DOCS / "assets", dirs_exist_ok=True)
    if (studio / "keep" / "shots").exists():
        shutil.copytree(studio / "keep" / "shots", DOCS / "keep" / "shots", dirs_exist_ok=True)
    print("built studio pages (docs/index.html, docs/keep/)")


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
        if extra.name not in ("index.html", "design.md", "src-img", "brief.md", "STATUS", "outreach.md"):
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
        build_studio(d)
