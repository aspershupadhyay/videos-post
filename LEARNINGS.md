# Learnings log

Newest first. Each entry: what happened, what we learned, the rule it became (in `CLAUDE.md`).

## 2026-10-27 — Review: strategy setup + Case 019 topic pick (could've done better)
- I wrote "Kimi redo" as the top pick without asking whether the creator wanted to revisit a posted topic; they didn't.
  → Next time: offer new topics first; a redo only if asked.
- I used two extended searches before shortlisting; one standard roundup search plus targeted primary-source fetches
  would have been enough. → Shortlist from one roundup, then spend fetches only on the top 2 primary sources.
- Several primary pages (CNBC) block fetching; Fortune and php.net worked. → Prefer the vendor's own page and php.net-style
  official pages, and note any secondary-only fact in the spec as a to-do before voicing.
- The "70%" check paid off: Wiz's number had no method; W3Techs gave the real denominator. → Always look up where a
  headline number comes from; it's usually where our fine-print beat is.

## 2026-10-27 — Case 018 (Kimi K3.1 Pro): post-mortem, first numbers
- **Numbers:** account at 3,253 views and 12 followers after Case 018. Growing, but strategy has to change.
- **Story:** three videos glued together (walking sim → spec sheet → "worse on purpose"); the shareable angle came at
  0:42 and the 17–39 s spec-sheet middle sagged. ~11 numbers in 74 s. → Rule 7 + `STRATEGY.md` §2–4.
- **Re-hook:** "here's the part nobody's talking about" is a cliché → banned (`STRATEGY.md` §3).
- **Cover:** "It couldn't walk. Then the AI fixed the physics." answered its own question; 16:9 strip on black wastes the
  hook frame. → Cover template, `STRATEGY.md` §5, rule 9.
- **Blank visuals** (creator noticed): measured 6 empty gaps of 0.6–1.1 s at scene starts (9.8, 17.3, 39.2, 41.8,
  54.1, 62.8 s) where type faded in from 0 on black, plus a 2.2 s frozen end card. → `tools/qa_frames.py`, rule 8.
- **Ending:** CTA instead of a repeatable line; end card ~2 s. → structure in `STRATEGY.md` §4.
- **Asked for:** best fonts, a consistent thumbnail theme on the profile, optimised use of resources, self-improving
  process. → Type v3 trial (Geist / Instrument Serif Italic / Geist Mono), covers, rules 10–11.
- Redo storyboard: `videos/case-018-kimi-k3-1-pro/STORYBOARD-v2.md`.

## 2026-10-24 — Case 018 (Kimi K3.1 Pro): voice lessons
- The `sparsh` model's learned temperature drifted to 1.0 between sessions. At 1.0 it said the brand as
  "Catch the Air/Ur" three times. At **0.5–0.7** with the name written as plain words ("Catch the Error",
  not "CatchTheError" + a pronounce rule) it was heard correctly in 12 of 12 takes.
  → Rule: pin `params.temperature` 0.6 for brand names and numbers; always read each line's `heard` text.
- "AI" via the lexicon became "A I" with a pause ("an A, I took over"). Fix: `lexicon: false` + `pronounce {"AI": "ay-eye"}`.
- "Kimi" needed `Kee-mee` (with hyphen) for Whisper to hear "Kimi"; "Keemee" was heard as "Kami".
- Never end on two sentences that can run together ("…don't have to. Follow…" was heard as "don't have to follow").
- Moonshot's research footage has labels burned over the subject: show it 16:9 framed on black instead of
  cropping to vertical. Cinematic demos crop to 9:16 well.

## 2026-10-24 — Case 017 (ArtCraft fact-check) feedback
- **Liked:** sound effects, background music level under the voice, overall energy.
- **Too much:** colour. Teal / mustard / rust full-frame worlds plus paper grain felt busy and "AI-made".
  → Rule 1: black or white ground, one brand signature element.
- **Wanted:** taste and realism — real media from the source, fewer decorative objects.
  → Rules 2 and 4.
- **Wanted:** stronger scripting, "like a million-follower creator". → Rule 3.
- Technical: HyperFrames volume automation did not lift the bed above unity; bake envelopes into the music file
  (`scripts/prep_audio.py`). GSAP `fromTo` with a delayed start needs `immediateRender: false` and opacity in both vars.
