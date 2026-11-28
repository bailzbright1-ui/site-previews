#!/usr/bin/env python3
"""Generate a preview site from src/<slug>/spec.json.

  python3 tools/gen_site.py <slug>

spec.json holds ONLY facts from brief.md / google.json plus design choices:
{
 "name": "...", "kicker": "Barber shop · Maroochydore", "headline": ["Line one", "line *two*"],
 "sub": "...", "layout": "split|fullbleed|editorial|poster|collage",
 "palette": {"bg":"#..","surface":"#..","ink":"#..","muted":"#..","line":"#..","accent":"#..","accent_ink":"#.."},
 "fonts": {"display":"Family","body":"Family","google":"family=...&family=...", "display_weight":700, "display_case":"none|uppercase", "italic": false},
 "hero": "img/g-1.webp", "gallery": ["img/g-2.webp", ...], "gallery_title": "...",
 "services_title": "...", "services": [["Name","one line"], ...],
 "hours": ["Monday: Closed", ...] | null, "address": "..." | null, "area": "Suburb QLD",
 "map_query": "..." | null, "rating": {"value":4.8,"count":301,"url":"https://maps..."} | null,
 "book_url": "..." | null, "cta_label": "Book a cut", "form_subject": "New enquiry", "notes": ["walk-ins welcome"]
}
Then `python3 tools/build.py` fills the tokens ({{PHONE_HREF}} etc.) from sites.json.
"""
import json, sys, html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
e = html.escape


def rich(t):  # *word* -> accent/italic span
    out, on = "", False
    for part in e(t).split("*"):
        out += (f"<em>{part}</em>" if on else part); on = not on
    return out


def gen(slug):
    S = json.loads((ROOT / "src" / slug / "spec.json").read_text())
    p, f, L = S["palette"], S["fonts"], S["layout"]
    book = S.get("book_url")
    primary = (f'<a class="btn pri" href="{{{{BOOK_URL}}}}" target="_blank" rel="noopener">{e(S.get("cta_label","Book online"))} ↗</a>' if book
               else '<a class="btn pri" href="{{PHONE_HREF}}">{{CALL_LABEL}}</a>')
    secondary = ('<a class="btn sec" href="{{PHONE_HREF}}">{{CALL_LABEL}}</a>' if book else '<a class="btn sec" href="#contact">Send an enquiry</a>')
    h1 = "".join(f'<span class="ln"><span>{rich(l)}</span></span>' for l in S["headline"])
    gal = S.get("gallery", [])
    gal = gal if len(gal) <= 4 else gal[:9] if len(gal) >= 9 else gal[:5]
    services = "".join(f'<li data-r data-d="{i*70}"><b>{e(a)}</b><span>{e(b)}</span></li>' for i, (a, b) in enumerate(S.get("services", [])))
    hours = "".join(f'<div><span>{e(h.split(":",1)[0])}</span><span>{e(h.split(":",1)[1].strip())}</span></div>' for h in (S.get("hours") or []))
    r = S.get("rating")
    rating = (f'<a class="rate" href="{e(r["url"])}" target="_blank" rel="noopener"><b>{r["value"]}</b><span>★★★★★</span><small>{r["count"]} Google reviews ↗</small></a>' if r else "")
    notes = "".join(f"<span>{e(n)}</span>" for n in S.get("notes", []))
    gallery_html = "".join(f'<figure class="g{i%5}" data-r="clip" data-d="{(i%4)*90}"><img src="{g}" alt="{e(S["name"])}: photo {i+1}" loading="lazy"></figure>' for i, g in enumerate(gal))
    case = f.get("display_case", "none")
    css = f"""
:root{{--bg:{p['bg']};--surface:{p['surface']};--ink:{p['ink']};--muted:{p['muted']};--line:{p['line']};--accent:{p['accent']};--accent-ink:{p['accent_ink']};
--d:"{f['display']}",system-ui,sans-serif;--b:"{f['body']}",system-ui,sans-serif}}
*{{box-sizing:border-box;margin:0;padding:0}}html{{scroll-behavior:smooth}}
body{{font-family:var(--b);background:var(--bg);color:var(--ink);font-size:17px;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:clip}}
a{{color:inherit}}img{{display:block;width:100%;height:100%;object-fit:cover}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 clamp(18px,3.4vw,40px)}}
h1,h2,h3{{font-family:var(--d);font-weight:{f.get('display_weight',700)};letter-spacing:-.02em;line-height:.98;text-transform:{case};text-wrap:balance}}
h1 em,h2 em{{font-style:{'italic' if f.get('italic') else 'normal'};color:var(--accent)}}
.k{{font-size:12.5px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
:focus-visible{{outline:2px solid var(--accent);outline-offset:3px;border-radius:6px}}
.btn{{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:52px;padding:0 26px;border-radius:999px;font:600 16px var(--b);text-decoration:none;border:0;cursor:pointer;transition:filter .2s,transform .15s}}
.btn:hover{{filter:brightness(.93)}}.btn:active{{transform:translateY(1px)}}
.pri{{background:var(--accent);color:var(--accent-ink)}}.sec{{box-shadow:inset 0 0 0 1.5px currentColor}}
header .wrap{{display:flex;justify-content:space-between;align-items:center;height:74px;gap:16px}}
.logo{{font-family:var(--d);font-weight:{f.get('display_weight',700)};font-size:21px;text-decoration:none;text-transform:{case};letter-spacing:-.01em}}
header nav{{display:flex;gap:26px;font-size:15px}}header nav a{{text-decoration:none;opacity:.8}}header nav a:hover{{opacity:1}}
header .btn{{min-height:44px;padding:0 18px;font-size:15px}}
@media(max-width:820px){{header nav{{display:none}}}}
.ln{{display:block;overflow:hidden;padding-bottom:.05em}}.ln>span{{display:block;animation:up 1s cubic-bezier(.2,.7,.2,1) both}}
.ln:nth-child(2)>span{{animation-delay:.1s}}.ln:nth-child(3)>span{{animation-delay:.2s}}@keyframes up{{from{{transform:translateY(105%)}}}}
@media(prefers-reduced-motion:reduce){{.ln>span{{animation:none}}}}
.hero h1{{font-size:clamp(3rem,7.6vw,7.4rem)}}
.hero .sub{{font-size:19px;max-width:44ch;margin:24px 0 30px;color:var(--muted)}}
.ctas{{display:flex;gap:10px;flex-wrap:wrap}}
.notes{{display:flex;gap:8px;flex-wrap:wrap;margin-top:26px}}.notes span{{border:1px solid var(--line);border-radius:999px;padding:7px 14px;font-size:14px}}
.rate{{display:inline-flex;align-items:center;gap:10px;text-decoration:none;margin-top:22px;font-size:15px}}
.rate b{{font-family:var(--d);font-size:30px;line-height:1}}.rate span{{color:var(--accent);letter-spacing:2px}}.rate small{{color:var(--muted);font-size:14px}}
.hp{{overflow:hidden;border-radius:26px;position:relative}}.hp img{{position:absolute;inset:-6% 0;height:112%}}
/* layouts */
.L-split .hero .wrap{{display:grid;grid-template-columns:1.05fr .95fr;gap:clamp(24px,4vw,64px);align-items:center;padding-top:clamp(28px,5vw,64px);padding-bottom:clamp(56px,8vw,110px)}}
.L-split .hp{{aspect-ratio:4/5}}
.L-fullbleed .hero{{position:relative;min-height:min(92vh,900px);display:flex;align-items:flex-end;color:#fff;overflow:hidden}}
.L-fullbleed .hero .bg{{position:absolute;inset:0}}.L-fullbleed .hero .bg img{{height:112%}}
.L-fullbleed .hero .bg::after{{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.78),rgba(0,0,0,.25) 55%,rgba(0,0,0,.35))}}
.L-fullbleed .hero .wrap{{position:relative;padding-top:130px;padding-bottom:clamp(40px,7vw,90px);width:100%}}.L-fullbleed .hero .sub,.L-fullbleed .rate small{{color:rgba(255,255,255,.85)}}
.L-fullbleed header{{position:absolute;left:0;right:0;z-index:5;color:#fff}}.L-fullbleed .hero h1 em{{color:inherit;text-decoration:underline;text-decoration-color:var(--accent);text-decoration-thickness:6px;text-underline-offset:8px}}.L-fullbleed .hero .k{{color:rgba(255,255,255,.85)}}
.L-editorial .hero .wrap{{padding-top:clamp(36px,6vw,80px)}}.L-editorial .hero h1{{font-size:clamp(2.5rem,10vw,10rem);max-width:12ch;overflow-wrap:anywhere}}
.L-editorial .hero .row{{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap}}
.L-editorial .hp{{aspect-ratio:21/9;margin-top:clamp(28px,4vw,48px);border-radius:18px}}
.L-poster{{--bg:{p['ink']};--ink:{p['bg']};--surface:rgba(255,255,255,.06);--line:rgba(255,255,255,.14);--muted:rgba(255,255,255,.7)}}
.L-poster .hero .wrap{{padding-top:clamp(30px,5vw,70px);text-align:center}}.L-poster .hero h1{{font-size:clamp(3.4rem,12vw,12rem);line-height:.86}}
.L-poster .hero .sub{{margin-left:auto;margin-right:auto}}.L-poster .ctas,.L-poster .notes{{justify-content:center}}
.L-poster .strip{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:clamp(30px,5vw,60px)}}.L-poster .strip div{{aspect-ratio:auto;height:clamp(260px,38vw,520px);border-radius:16px;overflow:hidden}}
.L-collage .hero .wrap{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,60px);align-items:center;padding-top:clamp(28px,5vw,64px);padding-bottom:clamp(56px,8vw,110px)}}
.L-collage .stack{{position:relative;aspect-ratio:1}}.L-collage .stack div{{position:absolute;border-radius:22px;overflow:hidden;box-shadow:0 30px 60px -30px rgba(0,0,0,.4)}}
.L-collage .stack div:nth-child(1){{inset:0 18% 18% 0}}.L-collage .stack div:nth-child(2){{inset:45% 0 0 42%;border:6px solid var(--bg)}}
@media(max-width:900px){{.L-split .hero .wrap,.L-collage .hero .wrap{{grid-template-columns:1fr}}.L-split .hp{{aspect-ratio:4/3.4;order:-1}}.L-poster .strip{{grid-template-columns:1fr 1fr}}.L-poster .strip div:nth-child(3){{display:none}}}}
section.s{{padding:clamp(72px,10vw,140px) 0;border-top:1px solid var(--line)}}
.sh{{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;flex-wrap:wrap;margin-bottom:clamp(30px,4vw,52px)}}
.sh h2{{font-size:clamp(2.3rem,5vw,4.4rem);max-width:15ch}}.sh p{{color:var(--muted);max-width:42ch}}
.svc{{list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}}
.svc li{{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:26px;display:flex;flex-direction:column;gap:8px}}
.svc b{{font-family:var(--d);font-size:22px;font-weight:{f.get('display_weight',700)};text-transform:{case};letter-spacing:-.01em}}.svc span{{color:var(--muted);font-size:15px}}
.gal{{display:grid;grid-template-columns:repeat(4,1fr);grid-auto-rows:clamp(150px,18vw,250px);gap:10px}}
.gal figure{{overflow:hidden;border-radius:16px}}.gal .g0{{grid-column:span 2;grid-row:span 2}}
.gal.few{{grid-template-columns:repeat({max(len(gal),1)},1fr);grid-auto-rows:clamp(220px,30vw,420px)}}.gal.few figure{{grid-column:auto!important;grid-row:auto!important}}
.gal img{{transition:transform 1.2s cubic-bezier(.2,.7,.2,1)}}.gal figure:hover img{{transform:scale(1.04)}}
@media(max-width:760px){{.gal{{grid-template-columns:1fr 1fr}}}}
.info{{display:grid;grid-template-columns:1fr 1fr;gap:clamp(24px,4vw,56px)}}
.hours{{border-top:1px solid var(--ink)}}.hours div{{display:flex;justify-content:space-between;padding:13px 0;border-bottom:1px solid var(--line)}}
.map{{border-radius:20px;overflow:hidden;min-height:340px;background:var(--surface)}}.map iframe{{width:100%;height:100%;min-height:340px;border:0}}
@media(max-width:860px){{.info{{grid-template-columns:1fr}}}}
.contact{{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(24px,4vw,64px)}}
.contact h2{{font-size:clamp(2.3rem,5vw,4.2rem)}}
.form{{background:var(--surface);border:1px solid var(--line);border-radius:22px;padding:clamp(22px,3vw,34px)}}
.form label{{display:block;font-size:14px;font-weight:600;margin:14px 0 6px}}
.form input,.form textarea{{width:100%;min-height:48px;padding:12px 14px;border:1.5px solid var(--line);border-radius:12px;background:var(--bg);font:400 16px var(--b);color:var(--ink)}}
.form textarea{{min-height:96px}}.form input:focus,.form textarea:focus{{outline:none;border-color:var(--accent)}}
.form .btn{{width:100%;margin-top:20px}}.form .done{{display:none}}.form.sent .done{{display:block}}.form.sent .f{{display:none}}
@media(max-width:860px){{.contact{{grid-template-columns:1fr}}}}
footer{{border-top:1px solid var(--line);padding:30px 0 40px;color:var(--muted);font-size:14px}}footer .wrap{{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}}
.trust{{display:grid;grid-template-columns:repeat(4,1fr);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}}
.trust div{{padding:22px clamp(14px,2vw,28px);border-right:1px solid var(--line)}}.trust div:last-child{{border-right:0}}
.trust b{{display:block;font-family:var(--d);font-size:clamp(22px,2.4vw,32px);line-height:1.05;text-transform:{case}}}.trust span{{color:var(--muted);font-size:14px}}
@media(max-width:760px){{.trust{{grid-template-columns:1fr 1fr}}.trust div:nth-child(2){{border-right:0}}.trust div:nth-child(-n+2){{border-bottom:1px solid var(--line)}}}}
.about{{display:grid;grid-template-columns:.8fr 1.2fr;gap:clamp(24px,5vw,80px)}}.about p{{color:var(--muted);font-size:18px;margin-bottom:16px;max-width:62ch}}
@media(max-width:860px){{.about{{grid-template-columns:1fr}}}}
.steps{{list-style:none;display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.steps li{{background:var(--surface);border:1px solid var(--line);border-radius:20px;padding:28px;min-height:200px;display:flex;flex-direction:column;gap:10px}}
.steps li:first-child{{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}}.steps li:first-child p{{color:inherit;opacity:.85}}
.steps .n{{font-family:var(--d);font-size:40px;line-height:1;opacity:.5}}.steps b{{font-family:var(--d);font-size:24px;text-transform:{case}}}.steps p{{color:var(--muted);font-size:15px}}
@media(max-width:760px){{.steps{{grid-template-columns:1fr}}.steps li{{min-height:0}}}}
.band{{position:relative;border-radius:28px;overflow:hidden;margin:0 clamp(8px,1.4vw,18px);min-height:420px;display:flex;align-items:flex-end;color:#fff}}
.band img{{position:absolute;inset:0;height:100%}}.band h2 em{{color:inherit;text-decoration:underline;text-decoration-thickness:4px;text-underline-offset:6px;text-decoration-color:var(--accent)}}.band::after{{content:"";position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.75),rgba(0,0,0,.15))}}
.band .wrap{{position:relative;z-index:1;padding-bottom:clamp(32px,5vw,64px);width:100%}}.band h2{{font-size:clamp(2.4rem,5.6vw,5rem);max-width:14ch}}
.band .btn.sec{{color:#fff}}
.faq details{{border-bottom:1px solid var(--line);padding:18px 0}}.faq summary{{cursor:pointer;font-weight:600;font-size:18px;list-style:none;display:flex;justify-content:space-between;gap:16px}}
.faq summary::after{{content:"+";color:var(--accent);font-weight:700}}.faq details[open] summary::after{{content:"–"}}.faq p{{color:var(--muted);margin-top:10px;max-width:70ch}}
.fcols{{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:28px;padding:48px 0 28px}}.fcols b{{display:block;color:var(--ink);font-family:var(--d);font-size:20px;margin-bottom:10px;text-transform:{case}}}
.fcols a{{display:block;text-decoration:none;padding:3px 0}}.fcols a:hover{{text-decoration:underline}}.fhrs div{{display:flex;justify-content:space-between;gap:12px;font-size:13.5px;padding:2px 0}}
@media(max-width:760px){{.fcols{{grid-template-columns:1fr}}}}
.dock{{display:none}}@media(max-width:760px){{.dock{{display:grid;grid-template-columns:1fr 1fr;gap:8px;position:fixed;left:10px;right:10px;bottom:10px;z-index:40}}.dock .btn{{box-shadow:0 10px 24px -10px rgba(0,0,0,.45)}}.dock .sec{{background:var(--bg);color:var(--ink)}}footer{{padding-bottom:96px}}}}
"""
    hero_img = f'<img src="{S["hero"]}" alt="{e(S["name"])}" fetchpriority="high" data-px="0.05">'
    copy = f"""<p class="k">{e(S['kicker'])}</p>
      <h1 id="h1" style="margin-top:18px">{h1}</h1>
      <p class="sub" data-r data-d="250">{e(S['sub'])}</p>
      <div class="ctas" data-r data-d="350">{primary}{secondary}</div>
      {rating}
      {f'<div class="notes">{notes}</div>' if notes else ''}"""
    if L == "split":
        hero = f'<section class="hero"><div class="wrap"><div>{copy}</div><div class="hp" data-r="clip">{hero_img}</div></div></section>'
    elif L == "fullbleed":
        hero = f'<section class="hero"><div class="bg">{hero_img}</div><div class="wrap"><div style="max-width:760px">{copy}</div></div></section>'
    elif L == "editorial":
        hero = f'<section class="hero"><div class="wrap"><p class="k">{e(S["kicker"])}</p><h1 id="h1" style="margin-top:18px">{h1}</h1><div class="row"><p class="sub" data-r data-d="250">{e(S["sub"])}</p><div><div class="ctas" data-r data-d="350">{primary}{secondary}</div>{rating}</div></div><div class="hp" data-r="clip">{hero_img}</div></div></section>'
    elif L == "poster":
        strip = "".join(f'<div data-r="clip" data-d="{i*120}"><img src="{g}" alt="" loading="lazy"></div>' for i, g in enumerate(([S["hero"]] + gal)[:3]))
        hero = f'<section class="hero"><div class="wrap">{copy}<div class="strip" style="grid-template-columns:repeat({len(([S["hero"]] + gal)[:3])},1fr)">{strip}</div></div></section>'
    else:
        second = gal[0] if gal else S["hero"]
        hero = f'<section class="hero"><div class="wrap"><div>{copy}</div><div class="stack"><div data-r="clip">{hero_img}</div><div data-r="scale" data-d="300"><img src="{second}" alt="" loading="lazy"></div></div></div></section>'
    nav = '<nav aria-label="Main">' + ('<a href="#services">Services</a>' if services else '') + ('<a href="#work">Our work</a>' if gal else '') + ('<a href="#visit">Hours</a>' if hours else '') + '<a href="#contact">Contact</a></nav>'
    sec_services = f'<section class="s" id="services"><div class="wrap"><div class="sh"><h2 data-r>{rich(S.get("services_title","What we do"))}</h2></div><ul class="svc">{services}</ul></div></section>' if services else ""
    sec_gal = f'<section class="s" id="work"><div class="wrap"><div class="sh"><h2 data-r>{rich(S.get("gallery_title","Our work"))}</h2><p data-r>Photos from {e(S["name"])}.</p></div><div class="gal{" few" if len(gal) <= 3 else ""}">{gallery_html}</div></div></section>' if gal else ""
    mapq = S.get("map_query")
    sec_info = ""
    if hours or mapq:
        left = f'<div><p class="k">Hours</p><h2 style="font-size:clamp(2rem,4vw,3.4rem);margin:12px 0 22px" data-r>When we\'re open</h2><div class="hours" data-r>{hours}</div></div>' if hours else f'<div><p class="k">Where</p><h2 style="font-size:clamp(2rem,4vw,3.4rem);margin:12px 0 22px" data-r>{e(S["area"])}</h2><p style="color:var(--muted)">{e(S.get("address") or "Call for details.")}</p></div>'
        right = f'<div class="map" data-r><iframe title="Map of {e(S["area"])}" loading="lazy" src="https://www.google.com/maps?q={e(mapq)}&output=embed"></iframe></div>' if mapq else ""
        sec_info = f'<section class="s" id="visit"><div class="wrap info">{left}{right}</div></section>'
    addr_line = e(S.get("address") or S["area"])
    # --- richer sections, built only from facts in the spec ---
    def open_days(hs):
        if not hs: return None
        days = [h.split(":", 1)[0][:3] for h in hs if "Closed" not in h]
        return f"Open {len(days)} days" if len(days) >= 5 else "Open " + ", ".join(days)
    trust = []
    if r: trust.append((f'{r["value"]}★', f'{r["count"]} Google reviews'))
    if S.get("hours"): trust.append((open_days(S["hours"]).replace("Open ", ""), "open each week" if "days" in open_days(S["hours"]) else "open"))
    trust.append((S["area"].replace(" QLD", ""), "local to you"))
    trust.append(("Online" if book else "Call", "to book" if book else "or text to book"))
    trust_html = "".join(f'<div data-r data-d="{i*80}"><b>{e(a)}</b><span>{e(b)}</span></div>' for i, (a, b) in enumerate(trust))
    steps = S.get("steps") or []
    steps_html = "".join(f'<li data-r data-d="{i*100}"><span class="n">0{i+1}</span><b>{e(a)}</b><p>{e(b)}</p></li>' for i, (a, b) in enumerate(steps))
    faq = [tuple(x) for x in S.get("faq", [])]
    faq_html = "".join(f'<details data-r><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    about = "".join(f"<p data-r>{e(x)}</p>" for x in S.get("about", []))
    band_img = S.get("band_img") or S["hero"]

    page = f"""<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><!-- PREVIEW-ONLY -->
<title>{e(S['name'])} · {e(S['kicker'])}</title>
<meta name="description" content="{e(S['sub'])}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?{f['google']}&display=swap" rel="stylesheet">
<link rel="preload" as="image" href="{S['hero']}">
<style>{css}</style>
</head>
<body class="L-{L}">
<!--PREVIEW-->{{{{PREVIEW_BAR}}}}<!--/PREVIEW-->
<header><div class="wrap"><a class="logo" href="#top">{e(S['name'])}</a>{nav}<a class="btn pri" href="{'{{BOOK_URL}}' if book else '{{PHONE_HREF}}'}"{' target="_blank" rel="noopener"' if book else ''}>{'Book' if book else '{{PHONE_DISPLAY}}'}</a></div></header>
<main id="top">
{hero}
<div class="wrap"><div class="trust">{trust_html}</div></div>
{f'<section class="s" id="about"><div class="wrap about"><div><p class="k">About</p><h2 style="font-size:clamp(2.2rem,4.6vw,4rem);margin-top:12px" data-r>{rich(S.get("about_title","Who we *are*"))}</h2></div><div>{about}</div></div></section>' if about else ''}
{sec_services}
{sec_gal}
{f'''<section class="s" id="how"><div class="wrap"><div class="sh"><h2 data-r>{rich("How it *works*")}</h2><p data-r>Simple from start to finish.</p></div><ol class="steps">{steps_html}</ol></div></section>''' if steps else ""}
{f'''<section class="band" aria-label="Book"><img src="{band_img}" alt="" loading="lazy"><div class="wrap"><h2 data-r>{rich(S.get("band_title","Ready when *you* are."))}</h2><div class="ctas" style="margin-top:24px" data-r data-d="150">{primary}{secondary}</div></div></section>''' if S.get("band") else ""}
{sec_info}
{f'''<section class="s" id="faq"><div class="wrap info"><div><p class="k">Questions</p><h2 style="font-size:clamp(2.2rem,4.6vw,4rem);margin-top:12px" data-r>{rich("Good to *know*")}</h2></div><div class="faq">{faq_html}</div></div></section>''' if faq else ""}
<section class="s" id="contact"><div class="wrap contact">
  <div><p class="k">Get in touch</p><h2 style="margin-top:12px" data-r>{rich(S.get('contact_title','Let\'s *talk*.'))}</h2><p style="color:var(--muted);margin-top:16px;max-width:40ch">{addr_line}</p><div class="ctas" style="margin-top:24px">{primary}</div></div>
  <form class="form" id="quote" data-lead novalidate aria-label="Enquiry">
    <input type="hidden" name="_subject" value="{e(S.get('form_subject','New enquiry from your website'))}"><input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">
    <div class="f"><label for="n">Name</label><input id="n" name="name" required autocomplete="name"><label for="p">Phone</label><input id="p" name="phone" type="tel" required autocomplete="tel" inputmode="tel" pattern="[0-9 +\\(\\)]{{8,}}"><label for="m">How can we help?</label><textarea id="m" name="message"></textarea><button class="btn pri" type="submit">Send</button></div>
    <div class="done" role="status"><h3 style="font-size:28px">Thanks, we'll be in touch.</h3><!--PREVIEW--><p style="font-size:13px;opacity:.7;margin-top:10px">This is a preview. Once your site is live, enquiries go straight to your inbox.</p><!--/PREVIEW--></div>
  </form>
</div></section>
</main>
<footer><div class="wrap" style="display:block"><div class="fcols"><div><b>{e(S['name'])}</b><span>{addr_line}</span><a href="{{{{PHONE_HREF}}}}" style="margin-top:8px">{{{{PHONE_DISPLAY}}}}</a>{f'<a href="{{{{BOOK_URL}}}}" target="_blank" rel="noopener">Book online ↗</a>' if book else ''}{f'<a href="{e(r["url"])}" target="_blank" rel="noopener">Google reviews ↗</a>' if r else ''}</div><div><b>Hours</b><div class="fhrs">{''.join(f'<div><span>{e(h.split(":",1)[0][:3])}</span><span>{e(h.split(":",1)[1].strip())}</span></div>' for h in (S.get("hours") or [])) or '<span>Call for times</span>'}</div></div><div><b>Explore</b>{'<a href="#services">Services</a>' if services else ''}{'<a href="#work">Our work</a>' if gal else ''}{"<a href=#how>How it works</a>" if steps else ""}{"<a href=#faq>Questions</a>" if faq else ""}<a href="#contact">Contact</a></div></div><div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;border-top:1px solid var(--line);padding-top:18px"><span>© {{{{YEAR}}}} {e(S['name'])} · {e(S['area'])}</span></div></div></footer>
<div class="dock">{('<a class="btn pri" href="{{BOOK_URL}}" target="_blank" rel="noopener">Book online</a><a class="btn sec" href="{{PHONE_HREF}}">Call</a>' if book else '<a class="btn pri" href="{{PHONE_HREF}}">Call now</a><a class="btn sec" href="#contact">Enquire</a>')}</div>
<script>
document.querySelectorAll('form[data-lead]').forEach(function(f){{f.addEventListener('submit',function(e){{e.preventDefault();if(!f.checkValidity()){{f.reportValidity();return}}var ep='{{{{FORM_ENDPOINT}}}}',b=f.querySelector('[type=submit]');if(!ep){{f.classList.add('sent');return}}b.disabled=true;b.textContent='Sending\\u2026';fetch(ep,{{method:'POST',headers:{{Accept:'application/json'}},body:new FormData(f)}}).then(function(r){{if(!r.ok)throw 0;f.classList.add('sent')}}).catch(function(){{b.disabled=false;b.textContent='Try again';alert('Sorry, that did not send. Please call us instead.')}})}})}});
</script>
</body>
</html>"""
    (ROOT / "src" / slug / "index.html").write_text(page)
    print("generated", slug)


if __name__ == "__main__":
    for s in sys.argv[1:]:
        gen(s)
