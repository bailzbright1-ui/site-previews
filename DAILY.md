# Daily run (scheduled task)

Bailey approved fully automatic outreach on 28 Nov 2026: send first emails, follow-ups and replies yourself, then email him a summary. **Always ask him first (in the summary, then wait) before anything involving money, refunds, or a customer's domain or DNS.** Follow CLAUDE.md, AUTOMATION.md and studio-kit/ throughout.

1. **Sync:** `git pull --rebase origin main`.
2. **Inbox (Gmail connector):** search `to:hello@onesightstudio.au newer_than:2d` plus `from:stripe.com newer_than:2d`, and read each thread in full.
   - **Reply from a lead:** answer it with Gmail `reply` (friendly, short, Bailey's voice from studio-kit/brand/BRAND.md, signed Bailey · One Sight Studio). Then `python3 tools/send.py mark <slug> replied`.
   - **"unsubscribe" / "no thanks":** `mark <slug> unsubscribed` (or `declined`), set `src/<slug>/STATUS` to `archived`, and send a one-line confirmation. Never contact them again.
   - **Change request (FormSubmit "Change request: …"):** make the changes (facts must still come from the owner or brief.md), rebuild, QA, push, then email them the updated link.
   - **Keep form / Stripe payment:** `mark <slug> kept`. Email the owner to welcome them and ask for: the email for enquiries, their domain (or whether to register one in their name at $21.95/yr, paid by them), photos they'd like used, and whether to add the site to their Google Business Profile (they add hello@onesightstudio.au as a manager). **Add a line to Bailey's summary before any DNS change or domain purchase.**
3. **Follow-ups:** `python3 tools/send.py followups`.
4. **Take-downs:** any log entry still `sent` after its `preview_until` date: set STATUS `archived` (the build removes the preview).
5. **New leads (2 per day):** take the next trade/area pair from `tools/lead-rotation.json` (create it from TRADES × AREAS in find_leads.py if missing, then advance it) and run `python3 tools/find_leads.py`. Pick up to 2 leads with score ≥ 6 that aren't in sites.json. For each:
   - Gather facts only from what the business publishes: Google data in leads.json, their Fresha/Facebook/own site (add hosts to the environment if needed). Write `brief.md` with a source for every fact.
   - Roll a fresh design direction from `.claude/skills/web-design-inspiration`, then build `src/<slug>/index.html` following the existing sites' pattern (tokens, data-lead forms, data-r motion). Photos must pass CLAUDE.md's quality rule.
   - Add the site to sites.json. Find an email the business publishes for customers and record `outreach_email` and `outreach_source`; with none, leave it blank: `tools/send.py first` then texts their published **mobile** via ClickSend (once `SMS_FROM` is set in tools/send.py and the ClickSend secret is in the environment). SMS replies arrive in the hello@ inbox via ClickSend's email forwarding. With no email and no mobile, list it in the summary for Bailey.
   - `python3 tools/build.py`, `node tools/check.js` (must PASS), look at the 1440/390 screenshots, fact-check against brief.md, push, confirm the live URL returns 200, `python3 tools/outreach.py`, then `python3 tools/send.py first <slug>`.
6. **Save:** commit and push (including outreach-log.json and leads.json).
7. **Summary to Bailey:** send with Resend (same as tools/send.py) to bailzbright1@gmail.com, subject "One Sight daily: <date>". Include: replies handled, sign-ups, change requests done, follow-ups sent, new previews and emails sent (with links), SMS drafts for him to send, and anything waiting on his OK.
