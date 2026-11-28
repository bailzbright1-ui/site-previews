# web-design-inspiration: a Claude Code skill

76 curated website designs (from Dribbble) with screenshots, design breakdowns, industry playbooks for local businesses, and a direction picker that makes every site Claude Code builds look different, even across hundreds of builds.

**Updating from the 17-reference version?** Delete the old `web-design-inspiration` folder first, then install this one. Your direction history (`~/.claude/web-design-history.json`) is kept separately and carries over.

## Install

### Windows (PowerShell)
```powershell
# 1. Make the skills folder if it doesn't exist
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
# 2. Unzip (adjust the path if your download went somewhere else)
Expand-Archive -Path "$HOME\Downloads\web-design-inspiration.zip" -DestinationPath "$HOME\.claude\skills" -Force
# 3. Check it's there: you should see SKILL.md
Get-ChildItem "$HOME\.claude\skills\web-design-inspiration"
```

### macOS / Linux (bash/zsh)
```bash
mkdir -p ~/.claude/skills
unzip -o ~/Downloads/web-design-inspiration.zip -d ~/.claude/skills
ls ~/.claude/skills/web-design-inspiration
```

Restart Claude Code (or open a new session). Ask it to build a website and it will load the skill automatically. You can also say "use the web-design-inspiration skill".

To use it in one project only, put the folder in `<project>/.claude/skills/` instead.

## Optional
- Download the designers' original shot images (needs internet). Run from the skill folder:
  `python scripts/fetch_originals.py` (Windows: `py scripts\fetch_originals.py`). About 230 images, roughly 1600px wide, so allow a few hundred MB
- See which directions you've already used: `python scripts/new_direction.py --history`
- Add more references later: put the screenshots in `images/` using the next number (e.g. `18-name-sheet.jpg`), write `references/18-name.md` in the same format, and add an entry to `directions.json` → `references`.

## Credits
Every design belongs to its designer or studio. `sources.json` lists the Dribbble link and designer for every reference. They are here for private inspiration only.
