# Building client previews

Instructions for Claude Code (or anyone) building a client's preview site. The client's site wears **the client's** brand; One Sight only appears in the preview bar and, once live, the footer credit.

## Folder per client

```
clients/
  joes-plumbing/            # slug: lowercase business name, hyphens
    brief.md                # every fact used on the site, each with its source link
    index.html              # the site: one static page, no build step
    assets/                 # their logo and photos, compressed (WebP, max 1600px wide)
    STATUS                  # one word: preview | live | archived
```

The preview URL is `{PREVIEW_BASE}/{slug}/`. Replace `{PREVIEW_BASE}` with the real domain once it's registered.

## The brief comes first

Before writing any HTML, fill `brief.md` from what the business has **published** (website, Google Business Profile, Facebook, Instagram, signage photos):

- Business name exactly as they write it, trading suburb and service area
- Services they list, in their words
- Phone, email, hours, ABN, licence numbers: only if published
- Their logo and brand colours (sample from their logo or signage)
- Photos of their work they've posted publicly
- A link to their Google reviews

**Never invent anything.** If a fact isn't in `brief.md`, leave that part of the site out. No made-up reviews, star ratings, years in business, licence numbers, awards, team names, prices, guarantees or "serving since". A preview with a fake fact can embarrass the owner and lose the sale.

## Page structure

One page, in this order, dropping any section the brief can't support:

1. **Hero**: business name, one line on what they do and where, a click-to-call button (`tel:`) and a quote/enquiry button.
2. **Services**: cards or a list, their words.
3. **Work**: a gallery of their own photos.
4. **Reviews**: a "Read our reviews on Google" link. Quote reviews on the page only after the owner says yes, once live.
5. **Service area**: suburbs listed as text (a map embed is optional).
6. **Contact**: phone, email, hours, an enquiry form.
7. **Footer**: name, ABN and licence if published; once live, the One Sight credit.

## Their look, our standards

- Colours from the client's logo or signage. Check text contrast is at least 4.5:1; if their colour fails as text, use it only as a fill.
- Type: one clean Google Font that suits the trade (e.g. a sturdy grotesk for trades, a softer serif for beauty or food). Don't use Schibsted Grotesk: that's ours.
- Mobile first. Tap targets at least 44px. Phone number tappable everywhere it appears.
- Semantic HTML, real `alt` text, visible keyboard focus, no autoplay.
- Fast: one HTML file plus CSS, images lazy-loaded, no frameworks or trackers.

## On every preview

- Put this in `<head>` so Google never indexes a preview: `<meta name="robots" content="noindex, nofollow">`
- Put the **PreviewBar** component as the first element in `<body>`, with the business name filled in and the button linking to the claim page or a pre-filled email.
- The enquiry form posts nowhere real yet; on submit, show "This is a preview. Once your site is live, enquiries go straight to your inbox."

## Going live (checklist)

1. Remove the preview bar and the `noindex` tag.
2. Connect their domain (registered in their name) and check HTTPS.
3. Point the enquiry form at their email and send a test.
4. Add the **BuiltBy** credit to the footer.
5. Set `STATUS` to `live`; check the site on a phone.

If they decline or don't reply within 14 days, take the preview down and set `STATUS` to `archived`.
