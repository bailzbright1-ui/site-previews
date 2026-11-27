# Beauty In A Box Co: design spec

## Direction Card
Lead **16 Luxe Escape** (Quiet Luxury) · Donor **12 CoolFix** · Palette **Atmospheric gradient** · Accent **signal orange (hue 15–30)** · Type **Onest 300/600 + Geist Mono** · Signature **Hub-and-spoke diagram** (from #07) · Layout **Sticky side rail + long content column** · Motion **Headline line reveal only**

## Concept
"Late-afternoon light at Moffat Beach": a soft dusk gradient (shell pink, then peach, then sea haze) sets the mood. Everything on top is quiet, white and precise, like a good salon: calm, clean, unhurried.

## Tokens
- `--bg #FBFAF8` · `--surface #EFEBE5` (warm stone) · `--ink #1A1714` · `--muted #6B635B` · `--line #E2DCD4`
- `--accent #E2602D` (signal orange, hue ~17) for book actions only · `--accent-ink #FFFFFF`
- Atmosphere gradient: `#F6D9CB → #F3C3A6 → #DCC9C0 → #B9CBCF`
- Type: display Onest 300, key word 600, `clamp(2.6rem, 6.4vw, 6rem)`, lh 0.98, tracking −0.035em · h2 `clamp(2rem,4vw,3.5rem)` 300 · body 16–17px/1.6 · label Geist Mono 12px uppercase +0.08em · prices and numbers Geist Mono
- Radius 28px panels, 999px pills · no shadows · hairline borders

## Signature move
**Treatment hub.** A central accent tile with the BIAB monogram inside a thin ring, with 4 spokes to white tiles: Waxing, Brows & Lashes, Spray Tans, Facials. Each tile has a line icon and caption. It's placed in the first scroll, once.

## Sections
1. Hero: atmospheric gradient panel, headline + 1 sentence + Book pill (focal point: headline)
2. Treatment hub: what we do, at a glance (focal point: diagram)
3. Menu: the 3 known prices in mono, then "60+ treatments" (focal point: price list)
4. Carla: story + 3 light mono stats (focal point: 15+ years)
5. How booking works: 3 numbered step cards, first filled (donor idea)
6. Visit: address, known hours, map
7. Closing CTA + footer

## Borrowing from donor
Only the numbered process step cards with the first step filled (CoolFix).

## NOT doing
- No staggered indented headline (lead's own signature)
- No hotel or wood photography, no photo bento
- No emoji icons, no drop shadows, no second accent colour
- No invented reviews, prices or hours. Only verified facts.
