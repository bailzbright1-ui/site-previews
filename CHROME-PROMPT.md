# Paste this into Claude in Chrome

I'm setting up One Sight Studio's payments, domain and email. Help me through each part in my browser. **Ask me before any click that buys something, creates something, or saves a setting.** Don't send any emails. At the end, give me a short summary with every value marked ⟶ below, so I can paste it back to Claude Code.

## 1. Stripe payment links

In my Stripe dashboard, create two **new** products. Don't reuse the "Trim" products.

| | Link 1 | Link 2 |
|---|---|---|
| Product name | Website – Keep plan | Website – Grow plan |
| Price | A$29.00, recurring, monthly | A$59.00, recurring, monthly |
| Description | Your website live on your domain. Hosting, SSL, backups, 1 change a month. Month to month. | Everything in Keep, plus up to 3 changes a month, Google Business Profile tidy-up and a new section each quarter. Month to month. |

For each payment link:
- Free trial: **30 days**
- Tick: Collect customer names, Collect business names, Require phone number
- Leave Managed Payments and automatic tax **off**
- After payment → Redirect to `https://bailzbright1-ui.github.io/site-previews/keep/thanks/`
- Show me the summary before clicking Create link

Then in Settings → Billing → Subscriptions and emails, turn on (ask me first):
- the email that reminds customers before a free trial ends
- the customer portal, so customers can cancel themselves

⟶ Keep link URL · Grow link URL

## 2. Domain

If I haven't bought it yet, help me register the studio domain (e.g. onesightstudio.com.au; .com.au needs my ABN 88 359 529 731). Then, in the domain's DNS settings, add these records so the website runs on it (ask before saving):

| Type | Name | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | bailzbright1-ui.github.io |

Remove any existing "parking" A records on @ that point elsewhere.

⟶ The exact domain · the registrar used · the price I paid for 1 year of the .com.au (we quote this to customers)

## 3. Email on the domain

Set up a mailbox like `hello@<domain>` (Google Workspace, Zoho Mail free plan, or the registrar's own email, whichever I choose). Add the MX/TXT records it asks for.

Then create a free **Resend** account (resend.com), add the same domain under Domains, and add the DNS records Resend shows (they're separate from the mailbox records, usually on a `send` or `resend._domainkey` name). Wait until Resend shows the domain as **Verified**. Then create an API key with "Sending access" only. **Don't paste the key anywhere.** Just tell me it's been created.

⟶ Studio email address · Resend domain verified (yes/no) · Resend API key created (yes/no)

## 4. GitHub Pages custom domain (do this after DNS is saved)

Open https://github.com/bailzbright1-ui/site-previews/settings/pages. Under **Custom domain**, enter the domain, click Save, wait for the DNS check to pass, then tick **Enforce HTTPS** (it can take up to an hour to become available).

⟶ Custom domain check passed (yes/no) · Enforce HTTPS ticked (yes/no)
