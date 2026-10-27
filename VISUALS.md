# CatchTheError visual language v1 — "the evidence look"

Style frames: `brand/lookbook/` (`lookbook.html` → `frame-a..d.png`, `lookbook-sheet.jpg`), built from Case 020 assets.
We look like an investigation desk, not an AI product launch. Every visual is either **real evidence** or **a mark we
made on it** (the red pen, a measurement line, a number). Nothing decorative.

## The four looks (one video uses all four, in this order = our series format)

| # | Look | Job in the story | Built from | In the spirit of |
|---|---|---|---|---|
| A | **Forensic** | Show the claim, frozen and annotated | Freeze-frame of the real clip, 42% black scrim, 2 px white boxes + leader lines, numbered callouts ①②, timecode/frame stamp, red pen on the one thing that's wrong | NYT Visual Investigations |
| B | **Paper trail** | Show the source in its own words | The real page on a white card (soft shadow) on paper #F2F0EB, crop marks, the key phrase as a huge Instrument Serif pull quote, pen under it | print editorial, Vox explainers |
| C | **Split verdict** | The reveal: claim vs reality, as two numbers | Black top / white bottom, one number each (Geist 800 vs Instrument Serif), a to-scale bar, mono labels | Swiss grid, Bloomberg data graphics |
| D | **Screen proof** | "We looked" — the search, the paper, the real thing | A neutral browser window with the real page (live-scrolled Playwright recording when possible), cursor, pen box | creators who research on screen |

Sequence = **Exhibit → Source → Verdict → Proof**, then the natural CTA. A viewer should recognise us from any frame.

## How we make it (HyperFrames)
- Freeze-frames: `ffmpeg -ss T -frames:v 1` from the source; the scrim is a plain `rgba(10,10,10,.42)` div; callouts and boxes
  are SVG strokes drawn with `stroke-dashoffset` (0.3 s, `power2.inOut`), one per spoken phrase.
- Paper trail: screenshot the page (Playwright, 2× scale, cookies rejected), crop to the sentence, measure the phrase's
  box from the full-res capture before placing the pen (LEARNINGS 2026-10-27).
- Screen proof: record a real scroll with Playwright `recordVideo` (1080 wide) instead of a static screenshot — it's
  motion for free in the 25–40 s stretch that sagged in Case 020.
- Split verdict: the bar is to scale, always; if a ratio can't be shown honestly, don't draw a bar.

## Motion grammar
- Hard cuts on the voice. One slow push per shot (1.00 → 1.08). Freeze → annotate → release.
- Type blurs in per line (10 → 0 px, 0.18 s). Numbers count up once, never loop.
- No bounce/elastic eases, no spins, no glitch transitions, no Ken Burns on stills that don't matter.
- Sound follows the picture: a tick per callout, a scratch per pen stroke, one impact per scene change at most.

## AI-slop tells we never use
Neon cyan/purple glow · mesh gradients · glowing brains, robots, circuit boards, holograms · particles, lens flares,
light leaks · AI-generated images or stock 3D · typewriter text · glitch on every cut · emoji on screen · ALL-CAPS
shouting headlines · more than 3 typefaces · "revolutionary / game-changer" copy · HUD overlays of our own (the viral
clip's HUD is the *evidence*, never our style).

## Type & colour (unchanged, from STRATEGY.md §5)
Geist 800 display · Instrument Serif Italic for the one word that matters · Geist Mono for labels and credits.
Black #0A0A0A, white #FAFAFA, paper #F2F0EB (look B only), dim #8C8A86. Red #E0502B = the pen and the logo bug only.
