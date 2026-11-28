---
name: web-design-inspiration
description: Use whenever building, redesigning or restyling a website, landing page or marketing web UI, especially sites for local businesses. Gives 76 curated Dribbble reference designs (screenshots + breakdowns), industry playbooks, and a direction picker so every new site looks distinct while keeping a premium UI/UX bar.
---

# Web design inspiration

This skill holds a curated library of 76 high-end website designs across 34 visual families and ~25 industries, plus a system for turning them into **new, original sites that never look like each other**, even across hundreds of builds. The goal is to match their quality, not their exact look.

`<skill-dir>` below means the folder that contains this SKILL.md.

## File map
- `references/industry-playbooks.md`: the best reference IDs, must-have sections and fresh-angle ideas for each kind of business, plus rules for spec/preview sites. **Read the entry for the client's industry first.**
- `references/INDEX.md`: table of all 76 references, their families and the shared DNA.
- `references/NN-slug.md`: deep breakdown of one reference (palette, type, layout, signature move, what to borrow, what not to copy).
- `images/NN-slug-*.jpg`: screenshots of each reference. **Look at them with the Read tool.** The words alone are not enough.
- `references/quality-bar.md`: the checklist every finished site must pass, including the screenshot comparison.
- `directions.json`: the menus of palette strategies, type pairings, signature moves, layouts and motion.
- `scripts/new_direction.py`: picks a fresh combination and logs it, so consecutive projects never repeat.
- `scripts/fetch_originals.py`: optional download of the original Dribbble images.
- `sources.json`: credits and original image URLs for every reference.

## Workflow (follow in order)

### 1. Understand the brief
Pin down: the business and what it sells, the audience, the single most important action (call, quote, book, buy, sign up), and any existing brand assets (logo, colours, fonts, photos). If the user gave brand colours or fonts, **those win** over anything the picker suggests. Keep the picker's *strategy* and apply it to their colours.

### 2. Roll a direction
```bash
python "<skill-dir>/scripts/new_direction.py" --project "<site name>" --industry "<3-6 keywords>" --brief "<one line>"
```
(On Windows, use `py` if `python` isn't found.) It prints a **Direction Card**: lead reference, donor reference, palette strategy, accent hue band, type pairing, signature move, layout rhythm and motion style. It also saves the card to `~/.claude/web-design-history.json` so the next project avoids the same choices.

- To preview without saving, add `--dry-run --seed 5`. To keep that roll but swap one pick that clearly fights the brief, rerun with the same seed plus `--palette "<name>"`, `--type "<name>"`, `--signature "<name>"`, `--donor <id>` or `--lead <id>`.
- If the user explicitly asks for a style ("make it like Lumen"), pass `--lead 08`. Still let the other dimensions roll.
- If Python is unavailable, choose by hand from `directions.json`, following the same rules, and append the choices to the history file yourself.

### 3. Study the references (don't skip)
1. Read the client's industry entry in `references/industry-playbooks.md` (must-have sections and primary action), and skim `references/INDEX.md`.
2. Read the lead and donor breakdown files. The lead often comes from a *different* industry on purpose: keep the industry's must-haves, and take the look from the lead.
3. **Open the lead's and donor's screenshots** (`images/<id>-*.jpg`) with the Read tool and study them: spacing, scale contrast, how few colours they use, how small the UI details are.
4. Optional: glance at one more reference from the same family for range.

### 4. Write a design spec before coding
Create `design.md` in the project with:
- **Direction Card** (paste it).
- **Concept**: one sentence describing the feeling, plus the metaphor (e.g. "freshly striped lawn seen from above").
- **Tokens**: the colour roles with hex values (`--bg`, `--surface`, `--ink`, `--muted`, `--line`, `--accent`, `--accent-ink`), the type scale (display, h2, h3, body, small, label), spacing scale, radius, shadow (usually none).
- **Signature move**: exactly how it will look and where it appears (hero or first scroll).
- **Section list**: each section's single job and focal point.
- **What we're borrowing**: the one structural idea from the donor.
- **What we're NOT doing**: list the lead's own signature move and any reference-specific elements you must not copy.

### 5. Build
- Put tokens in CSS custom properties (or the Tailwind theme) first. Never hard-code stray colours.
- Load the type pairing from Google Fonts with `display=swap` and preconnect.
- Build mobile and desktop together. Make the signature move work on both, or adapt it on purpose.
- Use real, specific copy for the business (prices, suburbs, steps, guarantees). If facts are unknown, use clearly marked placeholders like `[PRICE]`, not invented claims. **Never fabricate** testimonials, star ratings, review counts, licence numbers, awards or stats. Quote real public reviews accurately with their source, or leave a placeholder. For preview sites built before the business has hired anyone, follow "Spec sites for cold outreach" in `references/industry-playbooks.md`.
- Imagery: use the client's photos if provided. Otherwise use well-art-directed stock or CSS/SVG art that fits the palette strategy, with consistent light and temperature across the page.

### 6. Verify against the quality bar
Work through `references/quality-bar.md`. **Screenshot your build at 1440px and 390px and look at it next to the lead reference's screenshots.** Fix the gaps in polish. If your build could be mistaken for the reference, push the remix further.

## Uniqueness rules (hard)
1. **Never** reuse a recent project's lead reference, palette strategy, type pairing or signature move. The history file enforces this: no repeat lead within 12 projects, no repeat signature move within 20, no repeat type pairing within 8. Don't bypass it unless the user insists. When building many sites for the **same industry** (e.g. 20 plumbers), that matters most: the industry's must-haves stay constant, and everything visual rotates.
2. The lead sets the **mood and level of restraint**, not the layout. Don't trace its section order.
3. Take **exactly one** structural idea from the donor.
4. Use the signature move **once, prominently**. Repeating it everywhere cheapens it.
5. Don't use the lead reference's own signature move (the picker already excludes it).
6. Vary the hero composition between projects: centred, left-aligned, split, full-bleed, type-only, or object-led.

## Inspiration, not imitation
These are other designers' copyrighted works. Use them to learn principles (scale, restraint, palette discipline, rhythm). **Never** copy their brand names, logos, mascots, illustrations, 3D renders, photos, copywriting, or a pixel-for-pixel layout. Each breakdown file has a "Don't copy" line. Never put the reference images themselves into a client site.

## Avoid the generic "AI website" look
Unless the direction explicitly calls for it, don't default to:
- A purple-to-blue gradient hero, glassmorphism everywhere, or neon glows on white.
- A centred hero, then 3 identical feature cards with emoji icons, then a testimonial slider, then a pricing table, then FAQ, on autopilot.
- Inter for everything at weights 400/600 with no scale contrast.
- Rounded-2xl cards with drop shadows on every element.
- Stock "diverse team high-fiving" photos.
- More than one accent colour fighting for attention.
- Generic copy like "Elevate your business with cutting-edge solutions".

## Quick defaults when the brief is tiny
- Hero headline at 7–9 words or fewer. Sub-copy of 1–2 sentences. One primary CTA and one secondary.
- Sections: hero → proof → offer or services → how it works → social proof → CTA → footer. Then restyle and reorder these through the layout rhythm so it doesn't feel templated.
- Always include: sticky or easy-to-reach primary action on mobile, clear contact info, and a service area or location if the business is local.
