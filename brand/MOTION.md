# Motion library — moves learned from reference films

Each move: what the reference does (measured from its frames), and how we build it in HyperFrames. Use 3–5 kinds per
film, each caused by something on screen. Working code for every move is in `videos/case-021-gpt-6-1-terra/scripts/build_scenes.py`.

## From OpenAI's "GPT-6.1 Terra" launch film (Oct 2026, 31.5 s, 24 fps, white ground)
| Move | In their film | Our build (Case 021) |
|---|---|---|
| **Continuous zoom-through** | 0:00–0:06 one unbroken push: earth → Iberia → Lisbon rooftops → street; no cuts, clouds hide the seams | s1: the photo card scales 1 → 2.6 with blur 0 → 14 px in 0.32 s `power3.in`; the next shot arrives at 1.25 → 1 with blur 12 → 0, `expo.out`. s6: zoom 2.6× into a real footnote, then through it (→ 14×, fade) onto the same words typed big |
| **The world shrinks into a card** | 0:08–0:09 the full-bleed street shot shrinks into a rounded card on white, and a prompt bar appears under it | s3: full-bleed wrapper `scale 0.62, borderRadius 48, y −140`, 0.6 s `power2.inOut`; the pills move with it |
| **Typed prompt pill** | 0:09–0:12 "Create a detailed 3D model of this tram…" types into a pill under the image | `.pill` (white, 80 px radius, soft shadow) + per-letter `.ch` spans revealed by a stagger (`type()`), 26–40 chars/s |
| **Card push to the subject** | 0:21–0:22 the render inside the app window grows to fill the frame | s4: inner wrapper of the card scales 1 → 1.55, `power2.inOut`, origin on the model |
| **Object inline in a sentence** | 0:22 "Sees it. [tram] Does it." — a cutout of the real object between two words | s5: "Half the price." / [tram cutout, `mix-blend-mode: multiply`, feathered mask] / "3× faster*" stacked for 9:16 |
| **The object becomes real** | 0:23–0:24 a hand sets the die-cast toy down on white | s1 frame 0 + the hook's payoff shot (slowed 2.5×) |
| **Dot → logo** | 0:27–0:31 a coloured dot pulses, the ChatGPT wordmark and sticker icons pop round it, it resolves into the logo | `brand/motion/logo-sting.html`: our red dot falls onto the rule, then through it, and becomes the circled e |

## Ours (brand signatures)
- **Printed photo**: real footage in a card with a 6 px #1B1B1B border, 26 px radius, offset shadow; lands from below with a
  small rotation that settles to 0 (`expo.out`).
- **Claim → object**: the pen slices the object (half the price), cuts the footage card in two (slow parts cut out), an
  AD stamp slams onto the demo (`power4.in`, lands rotated −9°), an unverified number fades to a grey ghost.
- **Red pen** (`pen()`): SVG path, `stroke-dasharray` draw-on in 0.3–0.45 s, under or through the one fact that matters.
- **Pen ring** (`ring_img()` + `ring()`): the logo's own hand-drawn circle, drawn on with a conic mask.
- **Red asterisk** = "there's fine print": appears on the claim, paid off when the fine print is shown.
- **Cut word**: the word is sliced along the pen line and the halves drift apart (s7, "cut.").

## Gate reminder
`tools/qa_frames.py --ground light` for paper videos. Small changes (a pen line, mono text) don't count as motion
for the STATIC gate (mean frame diff at 54×96); give every 2 s a beat that moves a real area (footage, a card, an object).
