# Monty's Plumbing: design spec

## Direction Card
Lead **12 CoolFix** (Soft Atmospheric Service) · Donor **13 Trade** · Palette **Warm sand + action** · Accent **cobalt (hue ~218)** · Type **Plus Jakarta Sans 600/400 + 200 for stats** · Signature **Ghost watermark word** (from #01) · Layout **Full-bleed hero → split editorial → index list → strip → quiet footer** · Motion **Slow marquee, pauses on hover**

## Concept
"Coastal morning, calm hands": a sun-warmed sand palette says local and relaxed, and a single cobalt button says "call now". It should feel calm and dependable, not like a shouty emergency ad.

## Tokens
- `--bg #FAF6EF` · `--sand #EFE4D3` · `--surface #F4EDE2` · `--ink #15130F` · `--muted #6A6258` · `--line #E3D8C7`
- `--accent #1F5BD8` (cobalt) for call/quote actions + stat numerals only · `--accent-ink #fff`
- Display 600 `clamp(2.75rem,6.6vw,6.25rem)` lh .98 tracking −.035em · h2 600 `clamp(2rem,4vw,3.5rem)` · body 400 17px/1.6 · label 600 12px caps +.1em · stats 200 `clamp(56px,7vw,96px)`
- Radius 20px tiles, 999px pills · no shadows · hairlines

## Signature move
**"Peregian"** in huge italic, about 6% ink opacity, cropped off the bottom edge of the hero. Local pride, shown once.

## Sections
1. Hero (full-bleed sand): headline, sub-copy, Call + Quote, licence line; quote form card on the right
2. KPI tiles (donor idea): 21 yrs / 24/7 / ~1 hr / QBCC
3. Split editorial: why Monty's (focal point: headline)
4. Index list: 6 services as numbered rows
5. Marquee strip: slow slogan band
6. Service area + map
7. Final call CTA → quiet footer

## Borrowing from donor
KPI tiles row as social proof (Trade). Nothing else.

## NOT doing
- No sky/atmosphere-photo hero or clay 3D diagram (lead's signature)
- No floating UI-card orbit (donor's signature)
- No emoji, no second accent, no invented reviews, suburbs or phone numbers
