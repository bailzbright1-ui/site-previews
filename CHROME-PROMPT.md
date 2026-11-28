# Paste this into Claude in Chrome

I'm setting up One Sight Studio's payments, domain and email. Help me through each part in my browser. **Ask me before any click that buys something, creates something, or saves a setting.** Don't send any emails. At the end, give me a short summary with every value marked ⟶ below, so I can paste it back to Claude Code.

## 1. Stripe (the Keep link is already done)

Create one more payment link the same way as the existing Keep link: new product **Website – Grow plan**, A$59.00 recurring monthly, description "Everything in Keep, plus up to 3 changes a month, Google Business Profile tidy-up and a new section each quarter. Month to month." No free trial. Tick collect customer names, business names, and require phone number. After payment, redirect to `https://bailzbright1-ui.github.io/site-previews/keep/thanks/`. Show me before clicking Create.

⟶ Grow link URL

## 2. Domain

If I haven't bought it yet, the studio domain is **onesightstudio.au**. Then, in the domain's DNS settings, add these records so the website runs on it (ask before saving):

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | bailzbright1-ui.github.io |

Remove any existing "parking" A records on @ that point elsewhere.

⟶ Registrar used · the current price for 1 year of a **.com.au** at that registrar (we quote this to customers as their domain cost)

## 3. Email on the domain

The mailbox hello@onesightstudio.au already exists. Create a free **Resend** account (resend.com), add the same domain under Domains, and add the DNS records Resend shows (they're separate from the mailbox records, usually on a `send` or `resend._domainkey` name). Wait until Resend shows the domain as **Verified**. Then create an API key with "Sending access" only. **Don't paste the key anywhere.** Just tell me it's been created.

⟶ Resend domain verified (yes/no) · Resend API key created (yes/no)

## 4. GitHub Pages custom domain (do this after DNS is saved)

Open https://github.com/bailzbright1-ui/site-previews/settings/pages. Under **Custom domain**, enter the domain, click Save, wait for the DNS check to pass, then tick **Enforce HTTPS** (it can take up to an hour to become available).

⟶ Custom domain check passed (yes/no) · Enforce HTTPS ticked (yes/no)
