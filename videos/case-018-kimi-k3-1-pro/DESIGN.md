---
name: CatchTheError — restrained (v2, from Case 018 on)
colors:
  ground: "#0A0A0A"
  ink: "#F4F2EE"
  dim: "#8C8A86"
  hairline: "#2A2A2A"
  signature: "#E0502B"
typography:
  display: { family: "Bricolage Grotesque", weight: 650, stretch: "92%", case: sentence, tracking: "-0.025em", leading: 0.98 }
  caption: { family: "Bricolage Grotesque", weight: 600, stretch: "100%", size: 60px }
  credit: { family: "JetBrains Mono", weight: 500, size: 26px, color: dim, case: upper, tracking: "0.06em" }
---

# CatchTheError v2: restraint

Black ground, white type, the source's own footage and charts. The brand is **one** thing: the red pen,
a hand-drawn signature-red stroke that circles or underlines the single fact that matters in a beat. The
red appears nowhere else except the mark on the end card.

## Do

- Real media first: the company's footage full-bleed (cinematic demos) or framed 16:9 on black (research
  clips, keep their labels), real charts as clean screenshots on black with a 20 px radius.
- One idea per frame. If a frame needs a second line of type, cut words.
- Sentence case. No all-caps headlines. Tracking slightly negative on display.
- Credit footage in mono, dim, small: "Footage: Moonshot AI".
- Motion: hard cuts on the voice; footage punch-in 1.00 → 1.06 only on an emphasis word; titles blur in per
  word (8 → 0 px, 0.16 s); the red pen draws in 0.35 s with `power2.inOut` and holds.
- Captions: white, sentence case, active word full white, other words 55% white. No boxes or chips.

## Don't

- No coloured worlds, paper texture, grain, stamps, hard shadows, pills or cards-with-borders.
- No glow, gradients, particles, floating loops.
- Red on more than one thing per frame.
- Re-drawing a chart that exists as a real image.
