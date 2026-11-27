# Website previews (Sunshine Coast)

| Folder | What |
|---|---|
| `src/<slug>/index.html` | Site source (edit these). Each has a `design.md` with its design direction. |
| `sites.json` | Per-site details: name, phone, booking link, and your agency name for the preview banner |
| `docs/` | **Built previews**, served by GitHub Pages at `https://<you>.github.io/<repo>/<slug>/` |
| `tools/build.py` | `python3 tools/build.py` rebuilds all previews · `--live <slug> …` makes a go-live package (see GO-LIVE.md) |
| `tools/check.js` | `node tools/check.js` runs QA on every preview (report + screenshots in `qa/`) |

Every preview shows a "Website concept … not the official site yet" bar and is hidden from Google (`noindex` + `robots.txt`), so nobody mistakes it for the business's real site.
