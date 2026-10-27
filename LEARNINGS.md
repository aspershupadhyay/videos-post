# Learnings log

Newest first. Each entry: what happened, what we learned, the rule it became (in `CLAUDE.md`).

## 2026-10-27 — Visual language v1 (creator asked for creative visuals that don't look like AI hype)
- Proposed 4 looks built only from real evidence + our marks: Forensic, Paper trail, Split verdict, Screen proof
  (`VISUALS.md`, style frames in `brand/lookbook/`). Not yet tested in a video — judge on Case 021.
- Could've done better: the first Split-verdict frame had "300 m" wrapping at 380 px; check every style frame at
  full size before showing it.

## 2026-10-27 — Self-review of Case 020 (after the creator's fix request)
- **Whisper "match" is not a pronunciation check.** "ay-eye" scored 0.995 and still sounded like "AAAI". → For any
  acronym or name, voice 2–3 spellings in the *first* job and compare word length; never trust match alone.
- **I broke my own rule 3** with a slogan CTA. → Read the CTA aloud against rule 13 before voicing.
- **One GPU session, not two.** The A/B spelling test belonged in the first voice job (cost: one extra boot + load).
- **27–37 s is the weakest stretch:** two research scenes of paper headers + still figures read academic. → Next time
  use moving real media there (the papers' supplementary videos, a drone clip) and keep a paper header ≤ 1 s.
- **Hook could be sharper:** frame 0 restates the viral claim; the doubt ("nobody checked the readout") arrives at 6 s.
  → Put a hint of the catch on frame 0 (e.g. the red pen already on ">300 m").
- Smaller: X post screenshot low-res; cover lacks `CASE 020`; first-pass pen positions guessed from thumbnails.

## 2026-10-27 — Case 020 fix: "AI" pronunciation + a natural CTA (creator feedback)
- **Heard by the creator:** "AI" came out stretched ("AAAI ai ai") with `pronounce {"AI": "ay-eye"}`.
  Tested three spellings on 3 lines (myvoice `sparsh`, lexicon off): **"A.I." → clean "AI" in all 3, word 0.26–0.34 s**;
  "A-I" also clean; **"Ay Eye" fails** (heard "and I.I.", "A.I.I."). → Rule: write **A.I.** in the script text,
  `lexicon: false`, no pronounce entry for AI. Measure the word's length (natural ≈ 0.3–0.45 s) when in doubt.
- **CTA:** "We read the fine print. Catch the Error." sounded like a slogan (AI slop). Replaced with a person talking:
  "Seen a clip like this? Send it our way. We'll check it." — also asks for DMs (free topic sourcing).
  → Rule: the CTA is a natural ask a creator would say out loud, never a tagline read aloud.
- Scene cuts were hard-coded seconds and drifted when lines were re-voiced. → `build_scenes.py` now derives every
  cut from `timing.json` (0.2 s before the line). Never hard-code cut times.
- Cost: one L4 job with 10 lines (~6 min incl. model load), GPU stopped straight after.

## 2026-10-27 — Review: Case 020 (viral cliff "AI" HUD) — could've done better
- **Worked:** blank-frame gate PASS first try (rule 8 paid off); voice with subtitles/polish OFF took ~2 min on an L4
  and 0 re-voices; GPU stopped right after (≈0.15 units). Phrase cues from the voice's own pauses replaced Whisper.
- I deleted the full Apple screenshot before the crop was verified and had to re-shoot it. → Keep raw captures in the
  scratchpad until the frame is checked by snapshot.
- PubMed Central served a captcha; nature.com worked after rejecting cookies. → For Springer Nature papers, shoot
  nature.com and pull figures from media.springernature.com/lw1200/... directly.
- The source clip opens on a 0.8 s white fade; frame 0 came out white. → Always measure a source's first second
  (signalstats YAVG) before cutting the hook.
- Pen positions guessed from thumbnails missed twice (Apple underline, "edit."). → Measure text boxes from a
  full-res snapshot before placing the pen; one snapshot per pen.
- Cover still lacks the `CASE 0NN` tag from the template. → Build the cover as its own layer next time.

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
- "AI" via the lexicon became "A I" with a pause ("an A, I took over"). Fix then: `lexicon: false` + `pronounce {"AI": "ay-eye"}` — **superseded 2026-10-27: write "A.I." instead (ay-eye stretches).**
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
