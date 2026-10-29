# Case 024 — Mixture of Experts (Instagram carousel)

First carousel. Built in Figma: https://www.figma.com/design/s5Jo8NJjpLQsqPFvufq1Ew (team CatchTheError, page 1,
frames `Slide 01 … Slide 09`, 1080×1350 / 4:5). Exports in `renders/` (git-ignored; delivered to VoiceBox, see RENDERS.md).

**Spine:** Meta's Llama 4 runs only 17B of its 400B parameters per token (Mixture of Experts), which is why it's cheap
to run, but all 400B still sit in memory, and the "experts" don't specialise by topic.

**Hook device (creator's ask):** The Social Network. Cover = Mark (Jesse Eisenberg) in the hoodie at the whiteboard;
slide 4 = the Facemash ranking formula on the dorm window → "every MoE has one too: the router".

## Slides
| # | Headline (red serif word) | Visual | Source |
|---|---|---|---|
| 1 | Zuckerberg's AI ignores 96% of *itself.* · "On every word. On purpose. Here's the trick →" | printed still, hoodie | TMDB backdrop of *The Social Network* (2010) |
| 2 | A normal AI wakes its whole brain for *every word.* | 8×8 grid, all on | — |
| 3 | Meta cut Llama 4 into *128 experts.* | shared bar + 128 cells, 1 red | Meta blog |
| 4 | Facemash ran on one formula, scribbled on a dorm window. / Every MoE has one too. It's called the *router.* | printed still, window formula | TMDB backdrop |
| 5 | How the router picks, for every single word: 01–04 … The other 127 *sleep.* | type only | Meta blog ("one of the 128 routed experts") |
| 6 | 400B parameters. *Only 17B work.* | bar to scale (17/400) + Meta screenshot, pen under "17 billion active parameters" | Meta blog |
| 7 | Cheap to run. Not cheap to *store.* | Meta screenshot, pen under "all parameters are stored in memory" | Meta blog |
| 8 | And the "experts"? Not really *experts.* | Mixtral paper crop, pen under "we do not observe obvious patterns" | arXiv 2401.04088 §5 |
| 9 | Not 128 geniuses. One very fast *traffic cop.* · save ask | ct(e) logo v3 | — |

## Fact checks (primary sources, checked 2026-10-28)
- Maverick: "17 billion active parameters, 128 experts, and 400 billion total parameters"; "MoE layers use 128 routed
  experts and a shared expert. Each token is sent to the shared expert and also to one of the 128 routed experts. As a
  result, while all parameters are stored in memory, only a subset … are activated"; "can be run on a single NVIDIA H100
  DGX host". — ai.meta.com/blog/llama-4-multimodal-intelligence/
- 96% = 1 − 17/400 = 95.75%, rounded. Per token (slides say "word" in headlines, "token" in labels). Llama 4
  alternates dense and MoE layers; the 17B active figure is Meta's own and already accounts for that.
- Mixtral §5: "Surprisingly, we do not observe obvious patterns in the assignment of experts based on the topic";
  "words such as 'self' in Python … routed through the same expert"; "indentation tokens are always assigned to the
  same experts". — arxiv.org/abs/2401.04088. This is Mixtral 8x7B, not Llama 4 (slide 8 names Mixtral).
- Facemash/window formula: a scene in the film (Elo rating written on the dorm window), not a documentary claim.

## Design
Paper ground (`brand/logo-v3/paper-1080x1920.png`, centre-cropped), Inter Extra Bold headlines (−4.5 %), one Instrument
Serif Italic red word + pen underline per slide, Courier Prime kicker `CASE 024 / MIXTURE OF EXPERTS` + `n/9`, real
stills as printed photos, real source screenshots on white cards. Red #DD483F only on the pen word, the picked expert,
the 17B bar and the logo.
