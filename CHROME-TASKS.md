# Tasks for Claude in Chrome

Paste everything below the line into Claude in Chrome. When it's finished, upload the file it produces (`chrome-results.md`) back into this Claude Code session.

---

I run One Sight Studio. We build websites for local Sunshine Coast businesses before they ask, then offer to make them live. Another Claude (in Claude Code) built 10 preview sites but can't open most websites from its environment. I need you to check things in the browser and report back. **Don't send any emails or messages, don't buy anything, and ask me before clicking any final "Create", "Save" or "Pay" button.**

Put everything you find into one markdown file called `chrome-results.md`, using the template at the bottom, and give it to me to download.

## Task 1: Check the 10 preview sites work

Open each link on desktop, then use your phone-sized view if you can:

1. https://bailzbright1-ui.github.io/site-previews/beauty-in-a-box-co/
2. https://bailzbright1-ui.github.io/site-previews/kozmetika/
3. https://bailzbright1-ui.github.io/site-previews/wink-worthy/
4. https://bailzbright1-ui.github.io/site-previews/luminous-nails/
5. https://bailzbright1-ui.github.io/site-previews/wow-wow-nails/
6. https://bailzbright1-ui.github.io/site-previews/two-sisters-nails/
7. https://bailzbright1-ui.github.io/site-previews/montys-plumbing/
8. https://bailzbright1-ui.github.io/site-previews/mount-coolum-plumbing/
9. https://bailzbright1-ui.github.io/site-previews/hutcheson-roofing/
10. https://bailzbright1-ui.github.io/site-previews/homestyle-roof-painters/

For each, report:
- Does the page load, with photos showing?
- Does the Google map show (where there is one)?
- Do the "Book online" buttons open the right business's Fresha page?
- Does "Request changes" (top bar) open a form? Don't submit it.
- Does "Keep this site" open a page with that business's name on it?
- Anything that looks broken, wrong or odd.

Also open https://bailzbright1-ui.github.io/site-previews/ (the studio homepage) and report anything broken.

## Task 2: Fact-check each business (most important)

For each business, find their **own published** information: Google Business Profile (search their name + suburb on Google Maps), their Facebook or Instagram page, their Fresha page, and any website they have. Then compare it with what's on the preview site and list:

- **Wrong:** anything on the preview that doesn't match what they publish (phone, address, hours, services, names, licence numbers, years in business). Quote both versions.
- **Missing:** useful facts they publish that the preview doesn't have, like hours or extra services.
- **Their website:** do they already have one? Give the URL and a one-line honest opinion: none, outdated, decent or good.
- **Outreach contact:** the email address and/or mobile number they publish **for customers**, and exactly where you found it (URL). Only include contacts they publish publicly. Note it if a listing says "no marketing" or similar.
- **Their own photos:** links to 3–6 photos of their own work or premises from their Google, Facebook or Instagram that we could use (with their permission later). Just the links; don't download anything.
- **Logo:** a link to their logo if they have one, and their brand colours if obvious.
- **Google reviews link:** the URL of their Google reviews.

The businesses:
1. Beauty In A Box Co, 15 Fairlie Crescent, Moffat Beach (Fresha: "Beauty In A Box Co Caloundra")
2. Kozmetika, 31 Osprey Street, Caloundra
3. Wink Worthy Lashes & Brows, Maroochydore (phone 0400 781 552; which street address is current?)
4. Luminous Nails Sunshine Coast, Palmview (phone 0439 929 210; which street address is current? Friday–Sunday hours?)
5. Wow Wow Nails, Shop 2a, 1794 David Low Way, Coolum Beach (hours?)
6. Two Sisters Nails & Spa, Shop 4/708 David Low Way, Pacific Paradise (hours? Do they really do fish pedicures?)
7. Monty's Plumbing, Peregian Beach (QBCC 1065201; **we have no phone number**)
8. Mount Coolum Plumbing (0493 027 027; they have mtcplumbing.com.au, so how good is it?)
9. Hutcheson Plumbing & Roofing Maintenance, Coolum Beach (owner Bill; **we have no phone number**)
10. Homestyle Roof Painters (Geoff O'Hara, QBCC 1179124; **we have no phone number**; is it "41 years" or more?)

## Task 3: Domain prices

Find the current price to register a **.com.au** domain for 1 year (and 2 years if 1 isn't offered) at **VentraIP**, **Crazy Domains** and **GoDaddy Australia**. Report the price, any first-year promo vs renewal price, and that .com.au needs an ABN.

For each business that **doesn't** already have a website, check whether an obvious `.com.au` name is available, e.g. `montysplumbing.com.au`. Use a registrar's search box. Report available or taken. Don't buy anything.

## Task 4: Stripe payment links (only if I'm logged in, and ask me before clicking Create)

In my Stripe dashboard, help me create **two Payment Links**. Don't reuse my existing "Trim" products.

| | Link 1 | Link 2 |
|---|---|---|
| New product name | Website – Keep plan | Website – Grow plan |
| Price | A$29.00, recurring, monthly | A$59.00, recurring, monthly |
| Description | Your website live on your domain. Hosting, SSL, backups, 1 change a month. Month to month. | Everything in Keep, plus up to 3 changes a month, Google Business Profile tidy-up and a new section each quarter. Month to month. |

For both:
- Include a free trial: **30 days**
- Options: tick Collect customer names, Collect business names, Require phone number. Leave Managed Payments **off**. Leave tax off.
- After payment tab: redirect to `https://bailzbright1-ui.github.io/site-previews/keep/thanks/`
- Stop and show me the summary before clicking **Create link**.

Then, in Settings → Billing → Subscriptions and emails, show me where to turn on (1) the reminder email before a free trial ends and (2) the customer portal, so customers can cancel themselves. Ask before saving.

Put both payment link URLs in the results file.

## Results template (`chrome-results.md`)

```
# Chrome results

## 1. Preview sites
| Site | Loads + photos | Map | Book buttons | Request changes | Keep page | Problems |
|---|---|---|---|---|---|---|

Studio homepage: …

## 2. Fact-check
### <Business name>
- Wrong on preview: …
- Missing from preview: …
- Their existing website: <url or "none"> — <none / outdated / decent / good>
- Outreach contact: <email / mobile> — found at <url> — marketing restrictions: <none / quote>
- Own photos: <links>
- Logo: <link> — colours: …
- Google reviews: <link>
(repeat for all 10)

## 3. Domains
| Registrar | .com.au 1 yr | Renewal | Notes |
|---|---|---|---|

| Business | Suggested domain | Available? |
|---|---|---|

## 4. Stripe
- Keep link: https://buy.stripe.com/…
- Grow link: https://buy.stripe.com/…
- Trial reminder email: on/off · Customer portal: on/off
```
