# One Sight Studio: preview sites

One Sight Studio builds a website for a local business before they ask, sends the owner a private preview link, and makes it live for a flat monthly fee if they keep it. Brand rules, pricing and outreach rules live in `studio-kit/` (read `studio-kit/CLAUDE.md` and `studio-kit/brand/*.md` before building). This file maps those rules onto this repo.

## Layout

| Path | What |
|---|---|
| `src/<slug>/index.html` | Client preview source (one page, client's brand). Tokens like `{{NAME}}` are filled by the build. |
| `src/<slug>/brief.md` | Every fact on the site, each with a source link. **Not published.** |
| `src/<slug>/outreach.md` | First email, follow-up and SMS drafts. **Not published.** |
| `src/<slug>/STATUS` | `preview` / `live` / `archived` |
| `src/<slug>/img/` | Compressed WebP photos (max 2000px hero, 1200px others) |
| `studio/` | One Sight Studio's own pages: `index.html` (home) and `keep/` (the 3-click "keep this site" flow) |
| `sites.json` | Per-client name/phone/booking link, plus `agency` settings (your name, email, mobile, ABN, Stripe links, prices) |
| `docs/` | Build output, served by GitHub Pages at https://bailzbright1-ui.github.io/site-previews/ |
| `tools/build.py` | `python3 tools/build.py` builds everything into docs/. `--live <slug> --email … --domain …` makes a go-live package in live/ |
| `tools/check.js` | `node tools/check.js`: QA every preview (report in qa/REPORT.md) |
| `tools/motion.py` | Shared scroll animations injected into client sites (not studio pages) |
| `CHROME-REPORT.md` | **Read first.** What Claude in Chrome set up (domain, email, Resend, Places, Stripe, Gmail send-as), lead contact research, and the repo to-do list it left |

## Hard rules (from the kit, plus what we've learned)

- **Never invent facts.** If it isn't in `brief.md` with a source, it isn't on the site. No made-up reviews, review quotes, ratings, years, licences, staff, prices, guarantees, suburbs lists or services. Ratings only as "Rated X on <platform>" with a link.
- **Photos:** no stock photos of people (no faces, no full bodies). The owner's own published photos are best. Otherwise use people-free stock (objects, materials, hands at most), never presented as the business's own work or premises. Look at every photo before using it. **Owner photos must be sharp and high-res:** at least 2× the size they're displayed at, and never blurry video stills. If they aren't, use good-quality stock of the same subject instead, and ask the owner for originals later.
- **Their brand, not ours:** One Sight appears only in the preview bar (`tools/snippet_previewbar.html`, injected via `{{PREVIEW_BAR}}`) and, once live, the footer credit (added automatically by the live build).
- **Prices:** only those in `studio-kit/brand/PRICING.md` (Keep $29/mo, Grow $59/mo, Custom quoted). No fake discounts or urgency.
- **Each new site gets a fresh design direction** from the `web-design-inspiration` skill (history in `tools/design-history.json`).
- Before saying a site is done: build, run `node tools/check.js`, look at 1440px and 390px screenshots, and fact-check every claim against `brief.md`.
- Outreach follows `studio-kit/brand/OUTREACH.md` (Spam Act: identify yourself, ABN, unsubscribe line, one follow-up max).
