# Daily automation (target: up to 50 new previews a day)

Bailey approved fully automatic outreach (28 Nov 2026): send first emails/SMS, follow-ups and replies yourself, then report to him. **Ask him first (in the report, then wait) before anything involving money, refunds, or a customer's domain/DNS.** Follow CLAUDE.md and studio-kit/ throughout. Quality beats volume: a thin or wrong site is worse than none.

## 1. Morning: coordinator (this persistent session, ~7:47am, has Gmail)
1. `git pull --rebase origin main`.
2. **Inbox** (Gmail, `to:hello@onesightstudio.au newer_than:2d` + `from:stripe.com newer_than:2d` + ClickSend SMS-reply emails): read threads in full.
   - Owner reply: answer it (Gmail `reply`, Bailey's voice, signed "Bailey · One Sight Studio"), then `python3 tools/send.py mark <slug> replied`.
   - Unsubscribe / no / STOP: `mark <slug> unsubscribed`, STATUS `archived`, one-line confirmation, never contact again.
   - Change request: make it (facts from the owner or brief.md), rebuild, check, push, email or text the new link.
   - Keep form / Stripe payment: `mark <slug> kept`, welcome email asking for enquiry email, domain (or register one in their name at $21.95/yr, **they pay**), photos, and Google Business Profile access (add hello@onesightstudio.au as manager). Domain/DNS steps wait for Bailey's OK.
3. `python3 tools/send.py followups`; archive previews past `preview_until` with no yes.
4. Commit and push.
5. **Start 5 builder sessions** with `create_session` (environment site-previews, repo bailzbright1-ui/site-previews), titled "One Sight builder K/5 <date>", prompt: *"Read CLAUDE.md and DAILY.md, then do section 2 (Builder session) as shard K of 5, day number D."* (D = days since 2026-11-29.)

## 2. Builder session (one of 5, no Gmail needed)
1. `git pull --rebase origin main`, then `LEADS_FILE=leads.d/shard-K.json python3 tools/auto_batch.py --shard K --shards 5 --n 12 --day D`.
2. For **each** DRAFT:
   - Look at every `img/g-*` photo. Remove any that are stock-looking, blurry, people-focused stock or not their work; if fewer than 3 good ones remain, `rm -rf src/<slug>` and move on.
   - Check the address: if it looks like a home (no shop/unit, residential street), set `address` and `map_query` to null (suburb only).
   - Rewrite `headline`, `sub`, `kicker`, `gallery_title` in the spirit of the business (from their name, category, photos and Google data), with no invented facts. Add `services` only if their photos or Google category clearly show them. Add `faq`, `steps`, `band` only when there's something real to say (see CLAUDE.md). Pick a layout, palette and fonts that suit them; vary from the last few sites.
   - Delete the `_DRAFT` key, `python3 tools/gen_site.py <slug>`, `PREVIEW_DRAFTS=1 python3 tools/build.py`, then screenshot `docs/<slug>/index.html` at 1440 and 390 (`node tools/shots.js <slug>`) and look at both. Fix and repeat until it's genuinely good.
   - Set `src/<slug>/STATUS` to `ready`.
3. `git checkout -- docs qa`, then `git add src leads.d` and commit "Builder K: N drafts ready". Run `git pull --rebase` and push, retrying up to 3 times. If a rebase conflicts on a slug another builder also took, drop yours (`git rm -r src/<slug>`), then continue.
4. Finish with a short final message listing ready slugs and skipped leads with reasons.

## 3. Evening: publisher + report (this persistent session, ~5:47pm)
1. `git pull --rebase origin main`, then `python3 tools/publish.py` (merges builder sites, `ready` → `preview`, builds).
2. `node tools/check.js`. Any FAIL: set that slug back to `ready`, rebuild, and note it in the report.
3. Commit and push, wait about 90 seconds, then confirm each promoted URL returns 200 on https://onesightstudio.au/<slug>/.
4. `python3 tools/outreach.py && python3 tools/send.py first $(python3 tools/publish.py --list)` (email if a published email is recorded, else SMS to the published mobile).
5. Check Gmail again for replies since the morning and handle them as in 1.2.
6. Commit the logs and push.
7. **Report to Bailey** (Resend → bailzbright1@gmail.com, subject "One Sight daily: <date>"): new previews with links, who was emailed or texted, replies and how they were handled, change requests done, sign-ups and payments, follow-ups sent, take-downs, skipped leads count, anything waiting on his OK, and running totals (previews live, contacted, replied, kept).
