# CatchTheError growth strategy

How we pick, hook, build and judge a video. `PLAYBOOK.md` is the production manual; this file is the creative
and growth system, and it changes after every video (see "The loop" at the bottom).

## Scoreboard (update after every post — 48 h numbers)

| Case | Topic | Length | Views (48 h) | Follows | Notes |
|---|---|---|---|---|---|
| 017 | ArtCraft fact-check | ~70 s | — | — | colour worlds; too busy |
| 018 | Kimi K3.1 Pro | 74 s | 3,253 (account, as of 2026-10-27) | +12 | best story at 0:42; 6 blank gaps |
| 020 | Viral cliff "AI" HUD check | 49 s | — | — | first v3 type; qa_frames PASS; no captions |

Target per video: beat the previous one on **3-s hold** and **avg % watched**, not raw views. Ask the creator for
these two numbers from Insights / YouTube Studio; log them here.

## 1. Pick the topic (score before you research deeply)

Score 0–2 on each; make it only if the total is ≥ 7 of 10.

| Test | 2 = | 0 = |
|---|---|---|
| **Stakes for the viewer** | affects their money, job, safety, privacy, or the apps they use | insider/industry-only |
| **A twist** | the fine print contradicts the headline ("worse on purpose", "vendor-reported", "cheated the test") | straight announcement |
| **Real media exists** | official demo video, real chart, real UI/screenshot we can show | we'd have to draw it |
| **Freshness** | < 72 h old, or an evergreen myth people still repeat | stale and already covered by everyone |
| **One-sentence spine** | the whole video fits in one sentence | needs three ideas |

What our niche rewards (fine print + AI): benchmarks that lie, safety incidents, "free" products with a catch,
hidden pricing/ads, security bugs people must patch, and viral claims we can check. Avoid pure spec-sheet launches
unless they have a twist.

## 2. The spine (write this before anything else)

> **[Surprising true fact]** — because **[reason]** — but **[the fine print]**.

Example (Case 018 redo): *Moonshot made its own AI worse at hacking — because open weights can't be recalled — but the
scores are Moonshot's own.* Everything that doesn't serve the spine is cut, however good the footage is.

## 3. Hook method (0–3 s decides everything)

1. **Lead with the strongest fact**, never the warm-up. If the best line is at 40 s, move it to 0 s.
2. **Frame 0 = the payoff image + a claim that opens a question** (and it doubles as the cover). Never a logo,
   black, or a letterboxed strip.
3. **Line 1 ≤ 8 words**, a contradiction or a stake: "An AI lab just made its own model worse. On purpose."
4. **Line 2 opens the loop** with a specific question ("And the reason should worry you more than the model.").
   Pay the loop off at 55–65 % of the runtime, not earlier.
5. **Banned openers and re-hooks:** "here's the part nobody's talking about", "you won't believe", "let's dive in",
   "in today's video", naming the product first.
6. Write **3 hook variants**, voice all three (cheap: one `voice_lines` call), pick by ear and by which frame-0 reads
   best at phone size. Keep the losers in `SPEC.md` for A/B on another platform.

## 4. Structure (target 40–50 s, ≤ 120 words)

| % | Beat | Rule |
|---|---|---|
| 0–6 | Hook | strongest fact + frame-0 image |
| 6–12 | Open loop | one specific question |
| 12–35 | Proof | real footage/chart, the one number that makes it credible |
| 35–60 | Payoff | answer the loop; the twist |
| 60–80 | The catch | our brand beat: vendor-reported vs independent, what isn't out yet |
| 80–92 | Repeatable line | ≤ 10 words, a take people would quote |
| 92–100 | End card | a natural spoken ask ("Seen a clip like this? Send it our way. We'll check it.") over the logo, ≥ 3 s |

- **Max 3 numbers on screen** per video. Each one gets a red-pen moment; the rest stay in the caption.
- **Have a take.** Say what we think, then show why. Neutral recaps don't get shared.
- Every scene must change something on screen at least every 2 s (a cut, a push, a build, the pen).

## 5. Look v3 — type and covers

**Type (v3, trial on Case 019; compare by snapshot against v2 Bricolage before switching for good):**
- Display: **Geist** 800, tracking −0.04em, leading 0.95, sentence case.
- Emphasis: **Instrument Serif Italic** for the *one* word that carries the twist (alongside the red pen). One word per
  scene at most — this is the editorial signature, not decoration.
- Credits/data: **Geist Mono** 500, uppercase, +0.06em.
- All three are OFL on Google Fonts; vendor the woff2 files into `assets/fonts/` (no network at render time).
- Grounds stay #0A0A0A / #FAFAFA; red #E0502B only on the pen and the mark (CLAUDE.md rule 1).

**Covers (the profile grid is our storefront):**
- Every video ships `renders/cover.png` (1080×1920) and frame 0 matches it.
- Instagram's grid shows the **centre 1080×1440 (3:4)**: everything that matters sits inside it.
- Fixed template so the grid reads as one series: black ground · one real image (product footage still, chart crop,
  screenshot) in the top two-thirds · **2–4 word claim** in Geist 800 at ≥ 150 px · the one twist word in Instrument
  Serif Italic with the red pen · `CASE 0NN` in Geist Mono top-left · no logo (the profile picture already says it).
- Test: shrink the cover to 120 px wide; if the claim isn't readable, it's too long.

## 6. No dead frames (hard gate)

Case 018 had 6 empty gaps (0.6–1.1 s of bare black at scene starts, while type waited to animate in).
- Each scene's first element is **visible on its first frame** (animate in from 0.85 opacity/scale or a mask, never from 0).
- Hard cuts land on content, not on ground. Silence in the music is fine; emptiness on screen is not.
- `python3 tools/qa_frames.py <render>` must **PASS** (no EMPTY ≥ 0.3 s, no STATIC > 2 s) before delivery.
  Run it on a draft render (`-q draft`), fix, then render delivery once.

## 7. Work efficiently (limited compute and credits)

- Order: spine → script → 3 hook voicings → full voice → build → `check` → snapshots at the QA times →
  **one draft render → qa_frames → one delivery render**. No delivery render before the draft passes.
- Re-voice only the lines that fail (`match` < 0.95 or a misheard name), never the whole script.
- Reuse the previous case's `scripts/`, SFX and fonts; only new footage gets downloaded.
- Research: primary source first, then at most 2 checks. Don't do open-ended browsing.

## 8. The loop (how this file gets better on its own)

After every video, in the same session that delivers it:
1. Run `qa_frames.py` and write the weakest moment in the case's `REVIEW.md`.
2. When the creator shares numbers or feedback, add a dated entry to `LEARNINGS.md` and a row to the scoreboard above.
3. If a learning holds for two videos, promote it into a rule here or in `CLAUDE.md`, and delete what it replaces.
4. Refresh `TOPICS.md`: drop stale topics, re-score the rest, add what's new this week.
