#!/usr/bin/env python3
"""Regenerate src/<slug>/outreach.md for every site from sites.json (studio-kit/brand/OUTREACH.md template).
Run after changing your details, domain price, preview base URL or a site's contact info:  python3 tools/outreach.py"""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
c = json.loads((ROOT / "sites.json").read_text())
a = c["agency"]
v = lambda k, ph: a.get(k) or ph
trial = a.get("trial_days")
offer = (f"free for the first month, then {a.get('price_keep','$29')} a month" if trial else f"for {a.get('price_keep','$29')} a month")
sms_offer = (f"First month free, then {a.get('price_keep','$29')}/mo if you keep it" if trial else f"Live for {a.get('price_keep','$29')}/mo if you like it")
sig = f"{v('your_name','[YOUR NAME]')}\nOne Sight Studio · ABN {v('abn','[ABN]')} · {v('mobile','[MOBILE]')} · {v('email','[EMAIL]')}"
first = v('your_name', '[YOUR NAME]').split()[0]
for s in c["sites"]:
    n, slug = s["name"], s["slug"]
    if not (ROOT / "src" / slug / "index.html").exists():
        continue
    link = f"{a['preview_base'].rstrip('/')}/{slug}/"
    dom = (f"We'd connect it to your existing domain, {s['existing_domain']}." if s.get("existing_domain") else
           f"If you don't have a domain yet, we can register one in your name. The registration fee is {a.get('domain_price') or '[DOMAIN PRICE]'} a year, paid by you and separate from the monthly fee.")
    to = s.get("outreach_email") or "(not found yet: only use an email or mobile they publish for customers)"
    src = s.get("outreach_source") or "(record where you found it)"
    t = f"""# Outreach: {n}

**Preview:** {link}
**Send to:** {to}
**Found at:** {src}

---

**Subject:** I built a website for {n}

Hi there,

I'm {v('your_name','[YOUR NAME]')} from One Sight Studio in {v('suburb','[YOUR SUBURB]')}. I came across {n} on {s.get('found_on') or '[WHERE]'} and put together a website for you. It's already built. Have a look:

{link}

If you like it, it can be live on your own domain this week, {offer}. No setup fee, no lock-in, and changes are included. Want something changed first? There's a "Request changes" button at the top of the preview.

{dom}

If it's not for you, no worries. The preview comes down in 14 days.

{sig}

Don't want emails from us? Reply "unsubscribe" and you won't hear from us again.

---

**Follow-up (once, 5–7 days later, only if no reply)**
**Subject:** Re: I built a website for {n}

Hi there, just checking the link came through: {link}. Happy to change anything: photos, wording, colours. The preview is up until [DATE: 14 days after first email].

{first} · One Sight Studio
Reply "unsubscribe" to stop these emails.
"""
    ph = re.sub(r"\s", "", s.get("phone", ""))
    if ph.startswith("04"):
        t += f"""
---

**SMS** (this mobile is published for customers: {s['phone']})

Hi, {first} from One Sight Studio here. I built a website for {n}, have a look: {link}. {sms_offer}, no setup fee. Reply STOP to opt out.
"""
    (ROOT / "src" / slug / "outreach.md").write_text(t)
    print("wrote", slug)
