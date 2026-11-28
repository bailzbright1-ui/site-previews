One Sight Studio builds a website for a local business before they ask, sends the owner a private preview link, and makes it live for a flat monthly fee if they want to keep it. Everything in this system serves that first look: it should feel like a real studio went out of its way for them, because one did.

**Tagline:** We build it first. You decide.
**Name:** "One Sight" = one look. The pitch only works if the owner opens the link, so every touchpoint leads to the preview.

Read these sections before building anything:

- **This page**: voice, colour, type, logo, layout.
- **Pricing and offers**: the plans and the rules for showing prices.
- **Outreach**: the email and SMS templates and the rules for sending them.
- **Building client previews**: how Claude Code builds each client's site, the preview bar, and what must never be invented.

## Two brands, never mixed

One Sight's brand appears in exactly four places: the One Sight website, outreach messages, the preview bar on top of a client preview, and the small "Site by One Sight Studio" credit in a live client site's footer. A client's site is in **the client's** brand (their logo, their colours). Never put `teal`, the spotlight mark or One Sight type on a client's pages beyond the preview bar and the credit.

## Voice

- Write like a local tradie who's good with computers: plain, warm, confident. Australian English (colour, organise, enquiry).
- "We" is the studio. "You" is the owner. Talk about their business, not about us.
- Sentence case everywhere: headings, buttons, plan names. No exclamation marks. No emoji.
- Short sentences. Numerals for numbers ("3 changes a month"). Prices as `$29/month` or `$29/mo` in tight UI.
- Talk about what they get, never how it's made. Don't call the build AI-made, quick or effortless, and don't claim hours of hand-crafting either. "We built this for you" is true and enough.
- Never say: cheap, affordable, cutting-edge, world-class, revolutionary, guaranteed results, #1, "limited time".

Real copy to copy:

| Where | Copy |
| --- | --- |
| Hero | **We built your website.** Have a look first. If you like it, it goes live for $29 a month. |
| Sub | No setup fee. No lock-in. Your domain stays yours. |
| Primary button | Keep this site |
| Secondary button | See how it works |
| Preview bar | PREVIEW · Built for **Joe's Plumbing** by One Sight Studio. Not live yet. |
| Footer credit | Site by One Sight Studio |
| Decline line | Not for you? No worries. The preview comes down in 14 days and you'll never hear from us again. |

## Colour

- Build every page on `paper` with `ink` text. Use `paper-sunk` for alternate bands instead of borders.
- `teal` is a **fill**: primary buttons, the featured plan border, lens-dot bullets, the mark. Put `on-teal` text on it, never white.
- Never set text in `teal` on light `paper` (2.2:1). Use `teal-text` for links and teal words.
- `teal-soft` is the quiet highlight ground. Text on it is `ink` or `teal-text`.
- `spot` (amber) means **preview / not live yet** and nothing else. Use it for the PREVIEW tag and draft dots only, with `on-spot` text.
- `chrome` is for One Sight UI that sits on top of a client's site (the preview bar). It doesn't change with the theme.
- `danger` is for form errors only, always with words.
- One `teal` primary button per view. Everything else is the ink or ghost button.

## Type

- One family: **Schibsted Grotesk** (Google Fonts, 400–900) for everything. Labels and URLs in **JetBrains Mono**.
- The font files are in `fonts/` (both are free, SIL Open Font Licence). On a web page you can load them from Google Fonts instead: `https://fonts.googleapis.com/css2?family=Schibsted+Grotesk:wght@400..900&family=JetBrains+Mono:wght@400;500&display=swap`.
- Set the hero in `display`, page titles in `h1`, sections in `h2`, cards in `h3`, running copy in `body`, intros in `body-lg`, footnotes in `small`.
- Prices: the numeral in `price`, the "/month" beside it in `small` + `teal-text`.
- Eyebrows and tags in `label`, uppercase. URLs as text in `url`.
- Headings are tight and heavy (negative letter-spacing, built into the styles); body copy is never bolder than 500.

## Layout and shape

- Max content width 1120px; text columns max 640px. Gutters `space-4` on mobile, `space-6` on desktop.
- Section padding `space-8` on mobile, `space-9` on desktop. Heading-to-content gap `space-7`.
- Cards: `paper` fill, 1px `line` border, `radius-lg`, `space-6` padding. Only the featured plan and browser-frame mockups get `shadow-card`.
- Buttons and tags are pills (`radius-pill`). Images and screenshots use `radius-md`.
- Show client work inside a simple browser frame (`radius-md`, `line` border, `shadow-card`) so it reads as a real site, not a stock photo.
- Lens dots: list bullets are 8px `teal` discs, a nod to the two lenses in the mark. Use them for feature lists only.

## States, motion, focus

- Hover: buttons darken slightly (an inset shade), links underline. 150ms ease, nothing else moves.
- Keyboard focus: 2px solid `focus`, 2px offset, on every link, button and field. Never remove it.
- No parallax, no scroll-jacking, no autoplay.

## Logo

Files are in the **Logos** asset group.

- On `paper` or any light ground, use `one-sight-studio-logo.png`. On `chrome` or dark grounds, use `one-sight-studio-logo-reversed.png`.
- Use the mark alone (`one-sight-studio-mark.png`) for the favicon, social avatar, the preview bar and the footer credit. Not below 16px tall.
- Clear space on every side: at least the width of one lens circle (about a quarter of the mark's width).
- Never recolour, stretch, outline or rotate it. Never put it on a `teal` fill (the mark disappears). Never rebuild it in SVG by eye; ask for a vector file from the original designer.
- The logo is a raster file. Display the lockup at 240px wide or less, the mark at 64px or less, to stay sharp on retina screens.

## Imagery and icons

- Show real work: screenshots of real client previews (with permission once live). No stock photos of people pointing at laptops.
- On client sites, use the client's own published photos of their work. No stock people.
- Icons: the brand has no icon set of its own. Use **Lucide** at 20px, 1.75 stroke, in `ink` or `teal-text`, sparingly (flagged: a stand-in, not part of the original identity).

## Honesty rules (they protect the business)

- Every price shown is a price we actually charge. No strikethrough "was" prices, no fake discounts, no countdown timers. See **Pricing and offers**.
- No made-up testimonials, client counts, star ratings or "as seen in" logos. Until there are real ones, show the work.
- Preview sites never invent facts about the client (licences, years in business, awards, reviews, prices). See **Building client previews**.
