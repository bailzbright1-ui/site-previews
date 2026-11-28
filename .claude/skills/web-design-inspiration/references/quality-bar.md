# Quality bar: check before calling a site done

Work through this list after building. Fix anything that fails. Screenshot the result (see "Visual check" below) and compare it side by side with the lead reference's screenshots.

## Visual check (required)
1. Run the site locally.
2. Capture full-page screenshots at **1440px** and **390px** wide. Use Playwright if it's available:
   ```bash
   npx playwright screenshot --full-page --viewport-size=1440,900 http://localhost:3000 shot-desktop.png
   npx playwright screenshot --full-page --viewport-size=390,844 http://localhost:3000 shot-mobile.png
   ```
   If the Playwright browsers aren't installed, run `npx playwright install chromium` first. For a static HTML file, use a `file:///` URL.
3. Open both screenshots with the Read tool and look at them next to `images/<lead-id>-*.jpg`. Ask:
   - Does it have the same level of polish and restraint?
   - Is the signature move obvious within the first screen?
   - Would someone mistake it for the reference? It shouldn't be confusable. If it is, push the remix further.

## Typography
- [ ] Two families at most (three only if one is a mono for labels).
- [ ] Display size uses `clamp()` (e.g. `clamp(2.75rem, 7vw, 7.5rem)`). Body text is 15–18px on desktop and at least 15px on mobile.
- [ ] Display line-height 0.9–1.05 with tight tracking. Body line-height 1.5–1.65.
- [ ] Body line length is 55–75 characters (`max-width: 65ch`).
- [ ] No orphan single words on headline last lines (use `text-wrap: balance` on headings).
- [ ] Fonts load with `display=swap` and are preconnected.

## Colour
- [ ] Palette defined once as CSS custom properties with roles (`--bg`, `--ink`, `--muted`, `--accent`, `--surface`, `--line`).
- [ ] The accent is used only for actions and key highlights.
- [ ] Text contrast meets WCAG AA: 4.5:1 for body, 3:1 for large text. Check grey-on-colour and white-on-photo especially. Add a scrim or gradient behind text on images.
- [ ] No unearned gradients, and no default blue-purple "AI" gradient unless the direction calls for it.

## Layout & spacing
- [ ] 4/8px spacing scale only. Section padding uses `clamp(4rem, 10vw, 9rem)`.
- [ ] A 12-column grid on desktop, intentionally broken in 1–2 places for the signature move.
- [ ] Each section has one job and one focal point.
- [ ] Mobile isn't just stacked desktop: reorder, resize the display type, and keep the signature move working (or adapt it).
- [ ] No horizontal scroll at 360px.

## Components & UX
- [ ] One primary CTA per viewport. The secondary CTA is visibly secondary.
- [ ] The primary action (quote, book, buy, call) is reachable within one tap on mobile (sticky header or bottom bar).
- [ ] Every interactive element has hover, focus-visible and active states. Focus rings are visible.
- [ ] Touch targets are at least 44×44px.
- [ ] Forms have real labels, helpful placeholders, inline validation and a clear success state.
- [ ] Nav works with a keyboard. The mobile menu traps focus and closes on Esc.
- [ ] Images have meaningful `alt` text, with `loading="lazy"` below the fold and explicit `width`/`height` to prevent layout shift.

## Motion
- [ ] Every animation respects `@media (prefers-reduced-motion: reduce)`.
- [ ] Enter animations are 300–700ms and ease-out, run once and are subtle.
- [ ] Nothing moves that the user didn't cause, except one hero moment or a slow marquee.

## Content
- [ ] Real, specific copy: numbers, place names, prices, steps. No lorem ipsum and no "Lorem Company".
- [ ] Headlines say what the business does in plain words within the first screen.
- [ ] Trust signals near CTAs: reviews, guarantees, licences, "no lock-in" and similar.
- [ ] Footer has contact details, service area, legal links and the brand sign-off.

## Performance & build
- [ ] Hero image is at most about 250KB (AVIF/WebP), with `fetchpriority="high"` on the LCP image.
- [ ] No unused libraries. Plain CSS or Tailwind is fine, but don't add a heavy animation library for one fade.
- [ ] Lighthouse: Performance 90+, Accessibility 95+ (run `npx lighthouse http://localhost:3000 --view` if available).
- [ ] Semantic HTML: one `h1`, ordered headings, and `header` / `main` / `section` / `footer` landmarks.
