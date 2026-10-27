# Look: Tabloid / Newsprint

Hard-news energy. For `/cte-explainer` by default (reach, outrage, "is this real?").

- **Ground:** `assets/textures/Paper002.jpg` (newsprint grey), slow 1.00→1.05 push.
- **Masthead (every frame):** black bar 150 px, "Catch the Error" League Gothic 96 px white + "Extra · DD Mon YYYY"
  Libre Franklin 700 26 px caps; 14 px red rule `#d4231c` under it.
- **Type:** headlines League Gothic caps, 220–300 px, leading 0.86, `white-space: nowrap` per line (measure: 4 lines max,
  ≤ 12 characters a line). Kickers/credits Libre Franklin 700 caps 26–32 px, tracking .06em. Quotes Libre Franklin 800,
  96–118 px, tracking −.03em, key words underlined with a 28% red highlighter band.
- **Colour:** black, newsprint, red `#d4231c` for: the last headline word, banners, the stamp. Nothing else.
- **Parts:** red banner (`.banner`), real clipping (real screenshot, white card, −2° tilt, soft drop shadow), reaction
  cut-in (halftone-torn PD art + black caption bar), big numeral (League Gothic 1000 px) + side label, red stamp
  (12 px border, −7°, slams from 1.7×), "The catch" banner + quote.
- **Motion:** slams only: scale 1.12–1.25 → 1, y 18 → 0, 0.12 s `power4.out`, one per beat on the voice. Hard cuts.
  SFX: thud per headline line, punch per banner, impact on the reaction, stamp on the stamp.
- **Slop flags (stop and fix):** glow, gradients other than the highlighter band, 3D text, shaking camera, more than 3
  red things on screen, fake newspaper front pages of real outlets (we show their *real* headline as a clipping, never
  a mock-up with their name), AI-generated photos.
