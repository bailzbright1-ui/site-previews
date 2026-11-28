#!/usr/bin/env python3
"""Pick a fresh, non-repeating design direction for a new website.

Draws one option from each design dimension in directions.json, avoiding
anything used in recent projects (stored in a history file), and prints a
Direction Card in markdown.

Usage examples:
  python new_direction.py --project "Acme Plumbing" --industry "plumbing local service" --brief "Emergency plumber, Brisbane"
  python new_direction.py --project "Test" --dry-run         # preview without saving
  python new_direction.py --history                          # show past directions
  python new_direction.py --lead 12 --project "Lawn Co"      # force a lead reference

History file: ~/.claude/web-design-history.json (override with --history-file).
"""
import argparse
import datetime as dt
import json
import random
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = SKILL_DIR / "directions.json"
DEFAULT_HISTORY = Path.home() / ".claude" / "web-design-history.json"

# How many recent projects each dimension must not repeat.
# Sized for a library of ~76 references so hundreds of sites stay distinct.
AVOID = {"lead": 12, "donor": 10, "palette": 5, "type": 8, "signature": 20,
         "layout": 4, "motion": 2, "accent": 3}


def load_json(path, default):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        print(f"Warning: {path} is not valid JSON; starting a fresh history.", file=sys.stderr)
        return default


def recent(history, key, n):
    return {h.get(key) for h in history[-n:]} if n else set()


def pick(options, used, rng, name_of=lambda o: o):
    fresh = [o for o in options if name_of(o) not in used]
    return rng.choice(fresh or options)


def pick_lead(refs, industry, used, rng):
    """Best-matching reference not used recently; steps down through weaker
    matches, then to any unused reference, so the same industry still varies."""
    words = [w.strip().lower() for w in industry.replace(",", " ").split() if w.strip()]
    score = {r["id"]: sum(1 for w in words if w in " ".join(r["keywords"]).lower()) for r in refs}
    for s in sorted({v for v in score.values() if v > 0}, reverse=True):
        fresh = [r for r in refs if score[r["id"]] == s and r["id"] not in used]
        if fresh:
            return rng.choice(fresh)
    return pick(refs, used, rng, lambda r: r["id"])


def override(options, wanted, name_of):
    """Find an option by id or case-insensitive substring of its name."""
    w = wanted.lower()
    for o in options:
        if name_of(o).lower() == w or w in name_of(o).lower():
            return o
    names = ", ".join(name_of(o) for o in options)
    sys.exit(f"No option matches '{wanted}'. Choose from: {names}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", default="Untitled project")
    ap.add_argument("--industry", default="", help="keywords, e.g. 'lawn mowing local service'")
    ap.add_argument("--brief", default="")
    ap.add_argument("--lead", help="force a lead reference id, e.g. 12")
    ap.add_argument("--donor", help="force a donor reference id")
    ap.add_argument("--palette", help="force a palette strategy (name or part of it)")
    ap.add_argument("--type", dest="type_", help="force a type pairing (name or part of it)")
    ap.add_argument("--signature", help="force a signature move (name or part of it)")
    ap.add_argument("--seed", type=int, help="same seed + same history = same picks (use with --dry-run to preview)")
    ap.add_argument("--dry-run", action="store_true", help="do not save to history")
    ap.add_argument("--history", action="store_true", help="print saved history and exit")
    ap.add_argument("--history-file", default=str(DEFAULT_HISTORY))
    args = ap.parse_args()

    data = load_json(DATA_FILE, None)
    if data is None:
        sys.exit(f"Could not find {DATA_FILE}")
    hist_path = Path(args.history_file)
    history = load_json(hist_path, [])

    if args.history:
        if not history:
            print("No directions saved yet.")
        for h in history:
            print(f"- {h['date']} | {h['project']} | lead {h['lead']} + donor {h['donor']} | "
                  f"{h['palette']} | {h['type']} | {h['signature']}")
        return

    rng = random.Random(args.seed)
    refs = data["references"]
    by_id = {r["id"]: r for r in refs}

    def ref_by_id(raw):
        rid = raw.zfill(2)
        if rid not in by_id:
            sys.exit(f"Unknown reference id {raw}. Valid: {', '.join(by_id)}")
        return by_id[rid]

    # Every pick draws from the RNG even when overridden, so a seed stays
    # reproducible when you pin one dimension after a --dry-run preview.
    # Lead reference: industry-matched where possible, not used recently.
    lead = pick_lead(refs, args.industry, recent(history, "lead", AVOID["lead"]), rng)
    if args.lead:
        lead = ref_by_id(args.lead)

    # Donor: a different family from the lead, not used recently.
    donors = [r for r in refs if r["family"] != lead["family"]]
    donor = pick(donors, recent(history, "donor", AVOID["donor"]) | {lead["id"]}, rng, lambda r: r["id"])
    if args.donor:
        donor = ref_by_id(args.donor)

    palette = pick(data["palette_strategies"], recent(history, "palette", AVOID["palette"]), rng, lambda p: p["name"])
    if args.palette:
        palette = override(data["palette_strategies"], args.palette, lambda p: p["name"])
    typ = pick(data["type_pairings"], recent(history, "type", AVOID["type"]), rng, lambda t: t["name"])
    if args.type_:
        typ = override(data["type_pairings"], args.type_, lambda t: t["name"] + " " + t["display"])

    # Signature move: borrowed from somewhere OTHER than the lead, so the result is a remix.
    sig_pool = [s for s in data["signature_moves"] if s["from"] != lead["id"]]
    sig = pick(sig_pool, recent(history, "signature", AVOID["signature"]), rng, lambda s: s["name"])
    if args.signature:
        sig = override(data["signature_moves"], args.signature, lambda s: s["name"])

    layout = pick(data["layout_rhythms"], recent(history, "layout", AVOID["layout"]), rng)
    motion = pick(data["motion_styles"], recent(history, "motion", AVOID["motion"]), rng)
    accent = pick(data["accent_hue_bands"], recent(history, "accent", AVOID["accent"]), rng, lambda a: a["name"])

    entry = {
        "date": dt.date.today().isoformat(), "project": args.project, "industry": args.industry,
        "brief": args.brief, "lead": lead["id"], "donor": donor["id"], "palette": palette["name"],
        "type": typ["name"], "signature": sig["name"], "layout": layout, "motion": motion,
        "accent": accent["name"],
    }

    card = f"""# Direction Card: {args.project}

| Dimension | Pick |
|---|---|
| Lead reference (overall mood) | **{lead['id']} {lead['slug']}** ({lead['family']}): read `references/{lead['id']}-{lead['slug']}.md` and view its `images/{lead['id']}-*.jpg` |
| Donor reference (borrow ONE structural idea) | **{donor['id']} {donor['slug']}** ({donor['family']}): read `references/{donor['id']}-{donor['slug']}.md` |
| Palette strategy | **{palette['name']}**: {palette['how']} |
| Accent hue band | **{accent['name']}** (HSL hue {accent['range']}). Use the client's brand colour instead if they have one. |
| Type pairing | **{typ['display']}** + **{typ['body']}**: {typ['note']} Google Fonts: `https://fonts.googleapis.com/css2?{typ['google']}&display=swap` |
| Signature move (borrowed from #{sig['from']}) | **{sig['name']}**: {sig['how']} |
| Layout rhythm | {layout} |
| Motion | {motion} (always honour prefers-reduced-motion) |

Rules: the lead sets the mood, not the layout. Take exactly ONE idea from the donor. The signature move appears once, prominently (hero or first scroll). Do not reuse the lead's own signature move.
"""
    print(card)
    if args.brief:
        print(f"Brief: {args.brief}\n")

    if args.dry_run:
        print("(dry run: not saved to history)")
        return
    history.append(entry)
    hist_path.parent.mkdir(parents=True, exist_ok=True)
    with open(hist_path, "w", encoding="utf-8") as fh:
        json.dump(history, fh, indent=2, ensure_ascii=False)
    print(f"(saved to {hist_path})")


if __name__ == "__main__":
    main()
