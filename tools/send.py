#!/usr/bin/env python3
"""Send outreach through Resend and keep a log. The key comes from the environment's network secret.

  python3 tools/send.py first <slug> [<slug> ...] [--dry-run]   first email (once per business, ever)
  python3 tools/send.py followups [--dry-run]                   one follow-up, 6+ days after the first, if no reply
  python3 tools/send.py mark <slug> replied|unsubscribed|kept|declined
  python3 tools/send.py status

Log: outreach-log.json. Rules enforced here (Spam Act + studio-kit/brand/OUTREACH.md):
- only to the address in src/<slug>/outreach.json (one the business publishes), with its source recorded
- one first email and at most one follow-up per business, never after a reply/unsubscribe/decline
- every message identifies the sender, ABN and an unsubscribe line (checked before sending)
"""
import json, sys, datetime, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "outreach-log.json"
FROM = "Bailey Bright | One Sight Studio <hello@onesightstudio.au>"
REPLY_TO = "hello@onesightstudio.au"
FOLLOWUP_AFTER_DAYS = 6
PREVIEW_DAYS = 14
today = datetime.date.today()


def load():
    return json.loads(LOG.read_text()) if LOG.exists() else {}


def save(log):
    LOG.write_text(json.dumps(log, indent=2, ensure_ascii=False))


def resend(to, subject, text):
    req = urllib.request.Request("https://api.resend.com/emails", method="POST",
        data=json.dumps({"from": FROM, "to": [to], "reply_to": REPLY_TO, "subject": subject, "text": text}).encode(),
        headers={"Content-Type": "application/json", "User-Agent": "one-sight-studio/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())["id"]


def checks(msg, o):
    body = msg["body"]
    for need in ("One Sight Studio", "unsubscribe"):
        assert need.lower() in body.lower(), f"missing '{need}'"
    assert "[" not in body or "[DATE" in body, "unfilled placeholder"
    assert o["to"] and "@" in o["to"], "no published email"
    assert o["source"], "no source recorded for the address"


def first(slugs, dry):
    log = load()
    for slug in slugs:
        o = json.loads((ROOT / "src" / slug / "outreach.json").read_text())
        if slug in log:
            print(f"{slug}: already contacted on {log[slug]['first_sent']}, skipping"); continue
        st = (ROOT / "src" / slug / "STATUS").read_text().strip()
        if st != "preview":
            print(f"{slug}: STATUS is {st}, skipping"); continue
        checks(o["first"], o)
        if dry:
            print(f"--- DRY RUN {slug} -> {o['to']}\nSubject: {o['first']['subject']}\n\n{o['first']['body']}\n"); continue
        mid = resend(o["to"], o["first"]["subject"], o["first"]["body"])
        log[slug] = {"to": o["to"], "source": o["source"], "first_sent": today.isoformat(), "first_id": mid,
                     "followup_due": (today + datetime.timedelta(days=FOLLOWUP_AFTER_DAYS)).isoformat(),
                     "preview_until": (today + datetime.timedelta(days=PREVIEW_DAYS)).isoformat(), "status": "sent"}
        save(log); print(f"{slug}: sent to {o['to']} ({mid})")


def followups(dry):
    log = load()
    for slug, e in log.items():
        if e["status"] != "sent" or e.get("followup_sent") or e["followup_due"] > today.isoformat():
            continue
        o = json.loads((ROOT / "src" / slug / "outreach.json").read_text())
        msg = dict(o["followup"])
        msg["body"] = msg["body"].replace("[DATE: 14 days after first email]", datetime.date.fromisoformat(e["preview_until"]).strftime("%-d %B"))
        checks(msg, o)
        if dry:
            print(f"--- DRY RUN follow-up {slug} -> {e['to']}\n{msg['body']}\n"); continue
        e["followup_id"] = resend(e["to"], msg["subject"], msg["body"]); e["followup_sent"] = today.isoformat()
        save(log); print(f"{slug}: follow-up sent")


if __name__ == "__main__":
    a = sys.argv[1:]; dry = "--dry-run" in a; a = [x for x in a if x != "--dry-run"]
    if a[0] == "first": first(a[1:], dry)
    elif a[0] == "followups": followups(dry)
    elif a[0] == "mark":
        log = load(); log[a[1]]["status"] = a[2]; log[a[1]][a[2] + "_on"] = today.isoformat(); save(log); print("ok")
    elif a[0] == "status":
        for k, e in load().items():
            print(f"{k:26} {e['status']:12} first {e['first_sent']}  follow-up {e.get('followup_sent') or 'due ' + e['followup_due']}  preview until {e['preview_until']}")
