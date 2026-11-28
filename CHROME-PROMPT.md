# Paste this into Claude in Chrome

Set up SMS for One Sight Studio so Claude Code can text businesses that have no published email. **Ask me before any click that buys, creates, saves or sends.** Never paste an API key into a chat, document or your summary.

1. Sign up at **clicksend.com** (Australia) with hello@onesightstudio.au, business name One Sight Studio, ABN 88 359 529 731.
2. Buy a **dedicated Australian mobile number** (Numbers → Buy number; usually a small monthly fee). Show me the price first. This gives two-way SMS, so replies come back to us.
3. Under **Inbound rules**: forward all inbound SMS to **hello@onesightstudio.au** (email), so replies land in the inbox Claude Code reads.
4. Add credit (start small, e.g. $20), but show me first.
5. Get the API credentials: Account → API Credentials (username + API key). Then, in claude.ai/code, open the **site-previews** environment (session title bar → environment → Edit → Network secrets) and add:
   - Host: `rest.clicksend.com`
   - Header: `Authorization`
   - Value: `Basic ` followed by base64 of `username:apikey`. Work it out on a scratch page in the browser with `btoa("username:apikey")` and don't show it to me.
   - Name: `ClickSend (One Sight)`
6. Check that **Sender ID** shows the dedicated number (not alphanumeric), so people can reply.

⟶ Summary for Claude Code: the dedicated number (e.g. +614xxxxxxxx) · monthly number fee · cost per SMS · inbound forwarding to hello@ on (yes/no) · secret saved (yes/no)
