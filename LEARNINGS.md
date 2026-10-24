# Learnings log

Newest first. Each entry: what happened, what we learned, the rule it became (in `CLAUDE.md`).

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
