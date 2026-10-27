---
name: cte-explainer
description: CatchTheError meme-paced explainer — a 40-50 s vertical Reel/Short that fact-checks or explains an AI/tech story with fast cuts, title slams, real screenshots, public-domain reaction cut-ins and our fine-print twist. Use when the creator says "/cte-explainer <topic> [tabloid|zine]" or asks for an explainer, fact-check or news video. Builds with HyperFrames + VoiceBox (sparsh).
---

# /cte-explainer — meme-paced explainer

Input: a topic (or a viral post/link) and optionally a look (`tabloid` default, `zine`). Output:
`videos/case-0NN-<slug>/renders/<slug>-9x16.mp4` + `renders/cover.png` + `POST.md`, merged to the default branch.

Read first, in this order: `CLAUDE.md` (rules 1-14), `STRATEGY.md`, `EDITING.md`, `.claude/skills/cte-kit/README.md`,
the chosen `looks/<look>/LOOK.md`, then `/hyperframes`. Fact rules beat style rules every time.

## 1. Frame it (no tools yet)
- Score the topic (STRATEGY §1) and write the **one-sentence spine**: surprising fact — because — the fine print.
- Pick the **3 numbers max** and the **one line people will repeat**.

## 2. Verify (primary sources)
- Primary source first (the company's post, the paper, the official page), max 2 confirming reports.
- Note every on-screen fact → source in `SPEC.md`. If a claim only exists in secondary coverage, say so or drop it.
- Pages that block bots: try another outlet that ran the *same* report; never paraphrase a headline into a fake one.

## 3. Script to the beat template (≈ 45 s, ≤ 120 words, one line per beat)
| Time | Beat | Screen (look parts) |
|---|---|---|
| 0–2 s | Hook: the strongest fact, ≤ 8 words | Headline slam, 3–4 lines (frame 0 = cover) |
| 2–6 s | Open loop: a specific question | Real clipping/screenshot + banner |
| 6–30 s | Proof beats, a cut every 1–1.5 s | Real media, big numeral + label, one reaction cut-in about every 5 s, red pen/stamp on the key fact |
| 30–38 s | The catch (our fine print) | "The catch" banner + quote/fact |
| 38–43 s | The line to repeat | Big type |
| 43–47 s | Natural CTA ("Seen a clip like this? Send it our way. We'll check it.") | End card |
Write **"A.I."**, never "AI". Have a take. Banned: "nobody's talking about", "let's dive in", "game-changer".

## 4. Voice (VoiceBox, `sparsh`)
`gpu start purpose voice` (L4) → `voice_lines` engine `myvoice`, voice `sparsh`, style `tech`, platform `reels`,
takes 2, `params.temperature 0.6`, `lexicon false`, **subtitles false, polish false**, one id per beat (`vo-01`…).
A/B every name/acronym spelling in this first job (rule 14). Download, then **`gpu stop` immediately**.
Level each line to −14 LUFS and get phrase onsets from pauses (`cte-kit/scripts/prep_audio_case020.py` pattern).

## 5. Media
Real screenshots/clips (Playwright 2× for pages; crop to the sentence that matters). Reactions only from
`cte-kit/assets/reactions/` or new public-domain/CC0 finds (log in `SOURCES.md`), treated with `print_fx.py`.

## 6. Build
Copy `cte-kit/templates/tabloid-explainer/` (or zine) into the case folder, plus fonts/textures/SFX from the kit.
One scene per beat group; every cut derived from `timing.json` (never hard-coded); scene's first frame always has
content. Pen/stamp positions measured, not guessed. Music bed −26 LUFS under voice; SFX from cues.

## 7. Gates (all must pass before delivery)
`hyperframes check` (0 errors) → snapshots at every beat, **look at them** → draft render → `qa_frames.py`
(`--ground light` for paper looks) → re-watch 25–40 s for retention → loudness −14 ±1 LUFS, ≤ −1 dBTP → delivery
render → `cover.png` (claim readable in the 3:4 crop at 120 px wide).
**Slop check:** run the look's slop flags against the snapshots; flag anything that looks generated to the creator.

## 8. Deliver + learn
Send the MP4 + cover, write `POST.md`, commit, PR + merge. Log a dated "could've done better" in `LEARNINGS.md`,
add the case to the `STRATEGY.md` scoreboard, update `TOPICS.md`.
