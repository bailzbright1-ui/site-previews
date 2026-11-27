# Making a client's site live

When a business says yes:

## 1. Get 3 things from them
- **Email** for website enquiries (the contact form sends to this)
- **Phone** they want on the site (if it isn't already)
- **Domain**: do they own one (e.g. `montysplumbing.com.au`)? If not, buy one for them (~$15–25/yr for .com.au, needs their ABN) and add it to the monthly fee.

## 2. Build the live version (one command)
```bash
python3 tools/build.py --live montys-plumbing --email owner@theirbiz.com.au --domain montysplumbing.com.au --phone "0400 000 000"
```
This creates `live/montys-plumbing/` and `live/montys-plumbing.zip` with:
- the preview banner removed
- Google indexing switched on (noindex removed, robots.txt + sitemap added)
- the contact form wired to their email via FormSubmit (no account needed). **The first enquiry triggers a one-time "Activate form" email to the owner; ask them to click it.** Send a test enquiry yourself right after going live.
- call buttons pointing at the real phone number

## 3. Host it (pick one, all free for a single page)
**Netlify (easiest):** sign in at app.netlify.com → *Add new site → Deploy manually* → drag the `live/<slug>` folder in → *Domain settings → Add custom domain* → follow the DNS steps (point the domain's DNS at Netlify). HTTPS is automatic.

**Cloudflare Pages:** *Workers & Pages → Create → Pages → Upload assets* → upload the folder → *Custom domains*.

**GitHub Pages:** create a repo for the client, push the folder's contents, *Settings → Pages → Deploy from branch*. The `CNAME` file is already included.

## 4. After it's live
- Check it on your phone: tap Call, send a test enquiry, tap Book.
- Set up their **Google Business Profile** website link to the new domain.
- Start billing (a Stripe Payment Link for a monthly subscription is the simplest).
- Re-run the build any time you change their site, then re-upload the folder.
