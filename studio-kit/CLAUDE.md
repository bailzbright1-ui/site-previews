# One Sight Studio — client preview builder

This folder is One Sight Studio's workshop. One Sight builds a website for a local business before they ask, sends the owner a private preview link, and makes it live for a flat monthly fee if they want to keep it. Your job here is to build those preview sites, and draft the message that goes with each one.

## Settings (fill these in once)

| Key | Value |
| --- | --- |
| YOUR_NAME | {your name} |
| EMAIL | {studio email} |
| MOBILE | {mobile} |
| ABN | {ABN} |
| PREVIEW_BASE | {e.g. https://onesight.studio/p} (no trailing slash) |
| CLAIM_LINK | {claim page URL, or mailto:EMAIL?subject=Keep%20my%20site} |
| STUDIO_SITE | {One Sight website URL} |

If a setting is still in `{braces}` when you need it, stop and ask me for it.

## Read before building

- `brand/CLIENT-SITES.md`: how every client site is built. Follow it exactly.
- `brand/BRAND.md`: One Sight's own brand (voice, colours, logo). Applies to One Sight's pages and outreach, NOT to client sites.
- `brand/PRICING.md`: the plans. The only prices you may ever write.
- `brand/OUTREACH.md`: message templates and the Spam Act rules.

Names used in those docs map to files here: **PreviewBar** = `brand/snippets/preview-bar.html`, **BuiltBy** = `brand/snippets/built-by.html`, the **Logos** group = `brand/logos/`, `fonts/` = `brand/fonts/`. `brand/one-sight.css` is the stylesheet for One Sight's own pages (tokens + components, classes start with `os-`).

## New client: the workflow

1. Copy `clients/_template/` to `clients/{slug}/` (slug = business name, lowercase, hyphens).
2. Fill `brief.md` from what the business has published. Ask me for their links if you don't have them. Every fact gets a source link. Download their logo and work photos into `assets/` and compress them (WebP, max 1600px wide).
3. Build `index.html` as `brand/CLIENT-SITES.md` describes: one static page, in the client's brand, mobile first.
4. In `<head>`: `<meta name="robots" content="noindex, nofollow">`. First thing in `<body>`: the contents of `brand/snippets/preview-bar.html` with `{BUSINESS_NAME}` and `{CLAIM_LINK}` filled in.
5. Check it before telling me it's done:
   - Render at 390px and 1440px wide and look at both.
   - Text contrast at least 4.5:1 against its background.
   - **Fact check:** list every factual claim on the page (name, services, phone, hours, areas, licence, anything) and point each one to a line in `brief.md`. Remove anything that doesn't have one.
   - No placeholder text left anywhere. No `{braces}`.
6. Draft the first email from `brand/OUTREACH.md` into `clients/{slug}/outreach.md`, with the preview link `PREVIEW_BASE/{slug}/` and my details from Settings.
7. Set `STATUS` to `preview`.

## Hard rules

- **Never invent facts** about a client: no made-up reviews, ratings, years in business, licence numbers, awards, staff names, prices or guarantees. Missing fact = leave that part out.
- **Their brand, not ours.** Client sites use the client's logo and colours and never Schibsted Grotesk, `teal` or our mark, except the preview bar and (once live) the footer credit.
- **Honest prices.** Only the prices in `brand/PRICING.md`. No strikethrough "was" prices, "valued at", countdowns or "only 2 spots left".
- **Outreach** only to an email or mobile the business publishes for customers, always with my name, ABN, contact details and an unsubscribe line. One follow-up at most.
- Don't describe sites as AI-made or quick to make; don't claim hand-crafted hours either. "We built this for you" is the line.

## Going live

Follow the checklist at the end of `brand/CLIENT-SITES.md`: remove the preview bar and `noindex`, connect their domain, point the form at their email and test it, add `brand/snippets/built-by.html` to the footer, set `STATUS` to `live`.
