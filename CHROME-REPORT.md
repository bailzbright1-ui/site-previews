# Report from Claude in Chrome (28 Nov 2026)

Every step in `CHROME-PROMPT.md` is done. This file is the current state of the accounts and settings, plus the contact research. No key values are written anywhere. They sit only in the services and the environment secrets.

Bailey's standing rules: ask him before anything that creates, saves, buys or sends something, and don't send any emails without his OK.

## Accounts and settings (all working)

| Thing | State |
|---|---|
| Domain | `onesightstudio.au`, registered at GoDaddy. DNS on Cloudflare (nameservers bryce / nia.ns.cloudflare.com). |
| Website | GitHub Pages serves `docs/` at https://onesightstudio.au with HTTPS. `www` → CNAME to bailzbright1-ui.github.io. `tools/build.py` keeps `docs/CNAME` across rebuilds; don't remove that. |
| Inbox | `hello@onesightstudio.au` forwards to Bailey's Gmail through Cloudflare Email Routing. |
| Sending from Gmail | Gmail can **send as** `Bailey Bright \| One Sight Studio <hello@onesightstudio.au>` through Resend SMTP (smtp.resend.com, 465, SSL, user `resend`, its own `gmail-smtp` key). Replies go out from the address the message was sent to. Bailey can send outreach by hand from Gmail as hello@. |
| Resend | Domain `onesightstudio.au` verified. Keys: `one-sight-claude-code` (sending only, this domain only) and `gmail-smtp`. |
| Environment secrets | In the **site-previews** cloud environment: `api.resend.com` → `Authorization: Bearer …` and `places.googleapis.com` → `X-Goog-Api-Key`. They only apply to sessions started after they were added, so start a new session in site-previews if a call isn't authorised. |
| Google Places | Project `one-sight-studio`, **Places API (New)** enabled. The key is restricted to that API only. It's linked to Bailey's existing Google billing account, and Google didn't ask for a card. |
| Stripe | Separate account "One Sight Studio" (statement descriptor ONE SIGHT STUDIO). Keep plan: $29/month payment link, **no trial**, no Grow link yet. Customer portal is on. Both links are in `sites.json`. There's no Stripe API key; we use links only. |
| Keep sign-up | Works end to end on onesightstudio.au (no real payment made). FormSubmit is activated for both onesightstudio.au and bailzbright1-ui.github.io. |

`AUTOMATION.md` still lists the Resend and Places keys as needed, a Stripe key and a 30-day trial. Those lines are out of date. Update them from the table above.

## Published contact emails (part 4)

None of these listings say "no marketing" or anything like it. I filled `outreach_email` and `outreach_source` in `sites.json` for the six rows marked ✓. I left the others blank because they need a decision first.

| Site | Email | Where it's published | Notes |
|---|---|---|---|
| beauty-in-a-box-co ✓ | carla@beautyinaboxco.com.au | https://www.beautyinaboxcocaloundra.com/contact | Still current. The phone there (+61 406 034 321) matches. |
| kozmetika ✓ | kozmetika_@outlook.com | https://www.facebook.com/K0zmetika (About → Contact info) | The Facebook phone (0432 124 207) matches. |
| wink-worthy ✓ | info@winkworthylashes.com | https://www.facebook.com/winkworthylashesandbrows (About → Contact info) | **Still trading.** Booking has moved to Acuity: https://winkworthylashesandbrows.as.me/ (it shows Christmas 2026 hours; "Lashes & brows with Jordan, Sunshine Cove, Maroochydore"). The Fresha `book_url` in sites.json is dead, so swap it. Google now lists **44 Serenity Cct, Maroochydore**, not 22 Eton Ln. Fix the brief and site. |
| luminous-nails ✓ | info@luminous-nails.com.au | https://www.luminous-nails.com.au/ | **Still trading.** The Google profile is active and the website loads now (about, services, booking, gift cards). There's a second location in Strathpine. They already have a site, so probably low priority. |
| wow-wow-nails ✓ | wowwownailscoolum@gmail.com | https://www.facebook.com/wowwownailscoolum (About → Contact info) | Their Facebook intro says "Under New Management". |
| two-sisters-nails | staff@luminailsandbeauty.com.au | https://www.facebook.com/Luminailsandbeauty (About → Contact info) | The shop at Shop 4/708 David Low Way, same phone (07) 5326 1262, now trades as **Lumi Nails & Beauty** and has its own website, https://luminailsandbeauty.com.au/. Fresha still calls it "ÚT Nails and Spa". The preview carries an old name, and the business already has a site. Rename and rework it, or drop it. |
| montys-plumbing | (craigmontysplumbing@gmail.com) | Only in the contact details of https://www.localsearch.com.au/profile/monty-s-plumbing/peregian-beach-qld/D9rX, not shown as text on the page | Localsearch isn't on the allowed-source list, so Bailey decides. **Phone: 0428 196 916** (Localsearch "Show Number"; Google shows the same). An older (07) 5448 3114 appears on Yelp. ⚠ montysplumbing.com.au is a *different* Monty's in Sydney. Don't use it. |
| hutcheson-roofing | none published | Their site https://www.hutchesonmaintenance.com.au/contact has only a contact form | Localsearch contact data has tbhutcheson@westnet.com.au (same caveat as Monty's). **Phone: 0412 453 464** (own site and Localsearch). They already have a website, so probably low priority. |
| homestyle-roof-painters ✓ | admin@hrproofing.com.au | https://hrproofing.com.au/contact/ (homestyleroofpainters.com.au redirects there) | **Phone: 07 5495 2200.** The site shows **QBCC Licence No 15438263**, not 1179124, so fix the brief. Offices: Caboolture head office and Tewantin Sunshine Coast office. They already have a full website, so probably low priority. |

## Still to do in the repo

1. Add the new phone numbers above to `sites.json` **and** each `brief.md` with their sources before they appear on a site (Monty's, Hutcheson, Homestyle). Also apply the Wink Worthy and Homestyle corrections.
2. Regenerate `outreach.md` for every site. The current drafts still link to the old github.io preview addresses; previews now live at https://onesightstudio.au/<slug>/.
3. Re-rank the leads now that Luminous, Lumi (ex Two Sisters), Hutcheson and Homestyle are known to have their own websites.
4. Rebuild, run `node tools/check.js`, and push.
