# The pipeline (run from Claude Code, site-previews environment)

| Stage | Tool | Notes |
|---|---|---|
| 1. Find leads | `python3 tools/find_leads.py "<trade>" "<suburb>"` → `leads.json` (scored) | Google Places key is in the environment. Best leads: open, well reviewed, no real website. |
| 2. Facts + own photos | `python3 tools/fresha.py <slug> <url>`, the business's own website, Google data from leads.json | Every fact goes in `src/<slug>/brief.md` with its source. Photos must pass the quality rule in CLAUDE.md. |
| 3. Build | New `src/<slug>/`, fresh direction from `.claude/skills/web-design-inspiration`, `python3 tools/build.py`, `node tools/check.js`, push → https://onesightstudio.au/<slug>/ | |
| 4. Contact | Find an email the business publishes (website, Facebook About, Google). Record it in `sites.json` (`outreach_email`, `outreach_source`), then `python3 tools/outreach.py` | No published email → SMS draft in outreach.md (Bailey sends from his phone; no SMS API yet). |
| 5. Send | `python3 tools/send.py first <slug>…` (Resend, from hello@onesightstudio.au), `python3 tools/send.py followups` daily, `python3 tools/send.py status` | One email + one follow-up max, logged in `outreach-log.json`. |
| 6. Replies, change requests, sign-ups | Gmail connector (hello@ forwards to Gmail): FormSubmit change requests, keep forms, Stripe payment emails, owner replies | **Gmail connector must be connected** in claude.ai → Settings → Connectors. Mark outcomes with `tools/send.py mark <slug> replied|unsubscribed|kept|declined`. |
| 7. Go live | `python3 tools/build.py --live <slug> --email <owner> --domain <domain>` and GO-LIVE.md. Domains are paid by the customer ($21.95/yr .com.au). | DNS changes on the customer's domain need the owner (or their login) |
| 8. Google | Submit the live site to Google; add the website to their Google Business Profile once they add hello@onesightstudio.au as a manager | |
| 9. Take down | 14 days after the first email with no yes: set STATUS to `archived`, rebuild | Automatic: archived sites are skipped by the build |
