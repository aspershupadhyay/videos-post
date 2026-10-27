# cte-kit — shared parts for /cte-explainer and /cte-demo

Not a skill on its own. Both format skills build from these parts so an improvement here lands in every future video.

| Path | What |
|---|---|
| `looks/tabloid/LOOK.md`, `looks/zine/LOOK.md` | The two looks: tokens, fonts, textures, do / don't, slop flags |
| `templates/tabloid-explainer/` | Proven 10 s opening (lab test 2026-10-27): masthead, headline slam, real clipping, reaction cut-in, number + stamp, "The catch" quote |
| `templates/zine-demo/` | Proven 10 s demo: result-first torn print, step cards 1-2-3, zoom-follow camera on a real recording, marker pen, chip |
| `assets/fonts/` | League Gothic, Libre Franklin, Permanent Marker, Courier Prime (+ `SOURCES.md`) |
| `assets/textures/` | ambientCG CC0 paper: `Paper001` white, `Paper002` newsprint grey, `Paper003` crumpled |
| `assets/reactions/` | Public-domain reaction images, pre-treated (`*-halftone-torn.png` tabloid, `*-photocopy-torn.png` zine) + `SOURCES.md` |
| `assets/sfx/` | Kenney CC0 SFX (thud, punch, stamp, scratch, pop, tick, whoosh…) |
| `scripts/print_fx.py` | Offline halftone / photocopy / torn-edge treatments (never fake these with CSS filters) |
| `scripts/record_demo.cjs` | Playwright recording of a real site with a visible cursor + `demo-log.json` (time + box of every action) |
| `scripts/qa_frames.py` | Blank / frozen frame gate (`--ground light` for paper looks) |
| `scripts/build_sfx.py`, `scripts/prep_audio_case020.py` | SFX placement from cues; voice levelling + phrase onsets (adapt per case) |

## Reaction images ("memes") — the clean rule
Only public-domain or CC0 art/photos (Wikimedia Commons "Public domain" / PD-Art; NASA; Library of Congress no-known-
restrictions). Log every one in `assets/reactions/SOURCES.md`. Never movie stills, TV screenshots, other creators'
memes, or AI-generated faces. Treat with `print_fx.py` so they belong to the look. A caption makes the joke, the art
just reacts.

## Zoom-follow camera (demo)
Page is recorded at W×H (default 1200×1000), shown in a window (default 960×800). For each logged action:
`scale s` (1.25–1.6), `x = clamp(winW/2 − cx·s, winW − W·s, 0)`, `y = clamp(winH/2 − cy·s, winH − H·s, 0)`;
tween 0.6–0.7 s `power2.inOut`, starting ~0.6 s *before* the action. Pen marks over the recording: compute their
window position from the same formula — never place them by eye.
