# How this runs (all from one Claude Code chat)

| Step | Command / how | Status |
|---|---|---|
| Find leads | Google Places API search by trade + suburb | Needs **Google Places API key** (Network secret for `places.googleapis.com`, header `X-Goog-Api-Key`) |
| Pull facts + own photos (beauty) | `python3 tools/fresha.py --all` (or `<slug>`) → `src/<slug>/fresha.json` + `img/fresha-N.webp`, only the business's own uploads | Working |
| Pull facts + own photos (business website) | Fetch their site, read footer/contact/services, download their photos | Working (each new domain needs adding to the environment's allowed hosts) |
| Build + publish previews | `python3 tools/build.py`, `node tools/check.js`, git push → GitHub Pages | Working |
| Emails | `python3 tools/outreach.py` → `src/<slug>/outreach.md` | Working; sending needs **Resend API key** + your domain |
| Payments | Stripe Payment Links (Keep $29 / Grow $59, 30-day trial) | Needs **Stripe restricted key** (Network secret for `api.stripe.com`) or the two link URLs |
| Change requests + keep form | FormSubmit to your studio email | Needs your **studio email** |

Add keys in: session title bar → cloud environment **site-previews** → Edit → Network secrets. Then start a new session in that environment.
