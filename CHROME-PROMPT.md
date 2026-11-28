# Paste this into Claude in Chrome

Help me finish setting up One Sight Studio. **Ask me before any click that creates, saves, buys or sends something.** Never paste an API key into a chat, a document or your summary: copy it straight from where it's created into where it's stored. At the end, give me a short summary of the ⟶ items.

## 1. Resend API key → Claude Code environment

1. At resend.com → API Keys → Create API key. Name: `one-sight-claude-code`. Permission: **Sending access**. Domain: **onesightstudio.au**.
2. Copy the key (it's only shown once).
3. Open claude.ai/code. In the session titled with my One Sight work, open the **cloud environment menu in the session's title bar** (environment name **site-previews**) → **Edit** → **Network secrets** (may be called "API credentials") → Add:
   - Host: `api.resend.com`
   - Header: `Authorization`
   - Value: `Bearer ` followed by the key
   - Name: `Resend (One Sight)`
4. Save (ask me first).

⟶ Resend key stored in site-previews (yes/no)

## 2. Google Places API key → Claude Code environment

1. At console.cloud.google.com, create a project called `one-sight-studio` (or use an existing one if I have it).
2. APIs & Services → Library → enable **Places API (New)**. Billing must be on. Google gives a free monthly allowance, which our usage should stay within. Tell me if it asks for a card.
3. APIs & Services → Credentials → Create credentials → API key. Then **Edit API key** → API restrictions → Restrict key → only **Places API (New)**. Save.
4. Add it to the same **site-previews** environment → Network secrets:
   - Host: `places.googleapis.com`
   - Header: `X-Goog-Api-Key`
   - Value: the key (no "Bearer")
   - Name: `Google Places (One Sight)`

⟶ Places key stored (yes/no) · Did Google ask for billing? (yes/no)

## 3. Send as hello@onesightstudio.au from Gmail (so replies look right)

1. Create a **second** Resend API key: name `gmail-smtp`, Sending access, domain onesightstudio.au. Copy it.
2. Gmail (bailzbright1@gmail.com) → Settings → See all settings → Accounts and Import → **Send mail as** → Add another email address:
   - Name: `Bailey Bright | One Sight Studio`, email: `hello@onesightstudio.au`, untick "Treat as an alias"
   - SMTP server `smtp.resend.com`, port `465`, username `resend`, password: the gmail-smtp key, SSL
3. Gmail sends a confirmation code to hello@, which forwards back to this Gmail. Enter it.
4. Set "When replying to a message": reply from the same address it was sent to.

⟶ Gmail can send as hello@ (yes/no)

## 4. Find each business's published contact email

For each business below, find an email address **the business itself publishes for customers**: their website contact page, their Facebook page's About/Intro section, their Instagram bio, their Google Business Profile or their Fresha page. Only addresses they publish publicly. Note the exact URL where you saw it, and note it if the listing says "no marketing" or similar.

Also answer the question in brackets.

1. Beauty In A Box Co, Moffat Beach (their site beautyinaboxcocaloundra.com shows carla@beautyinaboxco.com.au. Confirm that's still current.)
2. Kozmetika, 31 Osprey St, Caloundra (facebook.com/k0zmetika, instagram.com/kozmetika__)
3. Wink Worthy Lashes & Brows, Maroochydore, 0400 781 552 (Are they still trading? Their Fresha page is gone.)
4. Luminous Nails Sunshine Coast, Palmview, 0439 929 210 (Their website luminous-nails.com.au doesn't load. Are they still trading?)
5. Wow Wow Nails, Shop 2a, 1794 David Low Way, Coolum Beach, (07) 5324 0059
6. Two Sisters Nails & Spa, Shop 4/708 David Low Way, Pacific Paradise, (07) 5326 1262 (Is this shop now called "ÚT Nails and Spa"?)
7. Monty's Plumbing, Peregian Beach, QBCC 1065201 (Also find their phone number.)
8. Mount Coolum Plumbing: already have pete@mtcplumbing.com.au, so skip
9. Hutcheson Plumbing & Roofing Maintenance, Coolum Beach, owner Bill (Also find their phone number.)
10. Homestyle Roof Painters, Bellmere, Geoff O'Hara, QBCC 1179124 (Also find their phone number.)

⟶ One line per business: email — URL where found — any "no marketing" note — answer to the bracketed question
