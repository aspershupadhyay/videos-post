# Learnings log

Newest first. Each entry: what happened, what we learned, the rule it became (in `CLAUDE.md`).

## 2026-10-28 — Renders moved to VoiceBox; purged from git history
- Creator: upload the old renders to VoiceBox and purge them from history. Four finals were already on VoiceBox under the
  creator's own names (md5-matched); uploaded the 020/021 covers and 4 demo/lab renders (md5-verified), then rewrote all
  5 branches without any `renders/` file (only renders changed; commit counts equal) and force-pushed with leases.
  → `RENDERS.md` maps every render to its VoiceBox file.
- Could've done better: a `'videos/*/renders'` glob pathspec silently matched nothing inside `filter-branch`; I caught it
  only because I counted reachable render objects after the rewrite. → Always verify a history rewrite by counting what
  should be gone, never by the tool's "rewritten" message.

## 2026-10-27 — Case 022 delivered: cover + VoiceBox-only delivery
- Cover: frame 0 per the template; my own rule 18 caught a half-cut text line at the bottom of the printed photo →
  cropped to headline + date. Passes the 3:4 grid crop and the 120 px test. → Rule 9 now says "whole lines only".
- Creator: deliver the video and cover to VoiceBox, renamed, and keep them only there. → Rule 20; `renders/` ignored.
  The old commits on this public branch still hold earlier renders in history (purging needs a force-push; not done).
- Promoted from this case: rule 18 (layout gate), rule 19 (one cause per line for a mechanism), rule 20 (VoiceBox only).
- Could've done better: I exported the cover from frame 0 without applying the same legibility check to it as to the
  scenes. → The cover is a scene too: it goes through qa_layout (the gate checks t = 0 with the cover exempt only from
  safe-zone/crowding, not from SMALL/COVERED).

## 2026-10-27 — Case 022 v3: creator review of the full cut → a layout gate
- **Creator:** keep the captions; fix 0:38–0:46 (three report cards stacked, too dense); the "CPU" text sat cramped in its
  box and a data block flew over it; the cache label touched the CPU box. **Make a sanity check part of the repo: spacing,
  text overlapping, nothing covering text, screenshots clearly visible, before every render.** → Rules 16 (captions) + 18.
- Built `tools/qa_layout.mjs`: seeks the live preview (`window.__player.renderSeek`) every 0.2 s and checks the DOM for
  OVERLAP / COVERED / CROWDED (< 16 px) / SAFE / OFFFRAME / SMALL (screenshot text < 26 px via `data-text-px`). Verified it
  fails on the old layout (label 4 px from the CPU box, block over "CPU", "Agent B" pushed under the right rail) and
  passes the fix. HyperFrames' own `check` only catches text-on-text overlap.
- Fixes: CPU box 270 px with its label at the top, blocks land under it; the cache label on a dark backing so blocks pass
  behind it; s6 = one full-width card per beat with a mono label; VGTimes cropped to its headline; short agent labels.
- The gate also caught my own fix (a camera pan pushed labels off-frame) before the render. That's the point of it.
- Could've done better: every one of these was visible in my own contact sheets; I looked for "does it work", not for
  spacing. → The gate now does the looking; still eyeball one frame per scene for taste.

## 2026-10-27 — Case 022 v2: creator feedback on the style demo
- **Creator:** make it ~1 minute; explain the mechanism the exact way the reference does; the screenshots had visual
  issues; the visual explanation wasn't good.
- My read of what failed: the abstract cell grid showed *that* bits move, not *why* (no cache vs memory, no notion of a
  slow read), and one 7 s line carried the whole mechanism. Report screenshots were shot at 668 css px wide, so text was
  ~20 px on a phone; the VGTimes crop carried the site's nav bar; the redaction bar overhung its card.
- Fixed: one idea per line (cache = a shelf by the CPU → on-shelf fast / off-shelf slow → A kicks = 1, leaves = 0 →
  B times reads → bit by bit), each line its own visible action; screenshots re-shot at 400 css px ×3 with measured
  phrase boxes driving every pen mark; padded cards. → Rule candidate: **explain a mechanism one cause per line, each with
  its own on-screen action; shoot any text screenshot at the width it'll be read at (≥ 32 px text in the frame).**
- Could've done better: I should have checked screenshot text size at phone scale before the demo (it was visible in the
  first contact sheet), and storyboarded the explainer as steps before drawing a diagram.

## 2026-10-27 — Case 022: learning from a reference Short (Varun Mayya, OpenAI agents + CPU cache)
- **Creator asked:** make a video on the same story, our way, and learn how they explain visuals and use subtitles.
- **What they do better:** the mechanism as a clean black motion graphic (cell grid = bits, dot = agent, mono labels);
  a face + authority open (Altman footage split with their face-cam, giant condensed headline ghosted behind); 16:9 footage
  filled with a blurred copy of itself, never letterboxed; tiny 2–3 word bold captions mid-frame, on a dark chip over
  footage. → Case 022 uses the grid idea in our language; captions built as an opt-in layer for the creator to judge.
- **Our edge:** they told the headline; OpenAI's own report says the agents were *asked* to, and has a better story (Sep 20:
  a model sent questions out through DNS; the auto-stop failed for 2.5 h). The fine print beat the reference's whole video.
- Could've done better: yt-dlp is bot-blocked from the cloud; I tried it twice before falling back to oEmbed + the public
  storyboard stills (hq1–3). → For a YouTube reference, start with oEmbed + `i.ytimg.com/vi/<id>/hq{1,2,3}.jpg`, and ask the
  creator to drop the MP4 in the repo if we need the full cut. First demo render failed STATIC once (2.3–4.4 s, boxes
  holding still) — rule 8's lesson again: plan a moving real area every 2 s in the storyboard, not after the render.

## 2026-10-27 — Case 021: v3 "dense" look demo rejected, v2 stays
- The creator said v2 "feels empty" and asked what Varun Mayya's AEOS would do better. I demoed the first 19 s in a
  dense, AEOS-style look: footage full-bleed in every shot, a cut every 1.5–2 s, paper-strip keyword labels, the red pen
  in every shot, the footnote redacted as the open loop. **Verdict for this video: "the first one is better", keep v2.**
- The creator on what to take from it: **don't hard-code a look.** v2 suited this story; the next video can be any design,
  motion graphics or animation. Stay open, pick the treatment per story. → Rule 15 rewritten (fixed: logo sting, red
  accent, no subtitles, safe zones, cover template; open: everything else).
- Learned: "feels empty" is a note on that cut, not a request to swap in someone else's style. Try the fix in the
  video's own language first.
- Did right: a 19 s demo plus a side-by-side before building 50 s, so the "no" cost one render, not a full video.
  Keep doing that for any change of look.

## 2026-10-27 — Case 021 v2: creator feedback on v1
- **Disliked:** the aesthetic (typewriter text everywhere), the subtitle-like headlines repeating the voice, the source
  credits on screen, the cover ("pretty shit"). **Liked:** the script, the logo CTA sting ("amazing").
- **Asked for:** cover like their reference (paper, big Inter headline with a red serif-italic word + pen, real still in a
  frame, CATCH · THE · (E)RROR), `CASE 0NN / topic` on top, no subtitles, clean and visually expressive, everything inside
  the Shorts/Reels safe zone without shrinking. → Rules 15–17, `STRATEGY.md` §5.
- My own review of v1: footage small in cards with the lower 40% of the frame empty; every line typed on screen; 3 scenes
  of type only; cover was just frame 0. v2: footage 1000 px wide or full-bleed, one line of type per beat at most, the
  numbers become objects (the pen slices the tram; the pen cuts the demo; AD stamp; the 3× fades to a ghost when "no one
  has confirmed it").
- Checked before claiming: the demo looked like it had 4 jump cuts (frame-diff spikes) — the frames show camera moves, not
  edits, so we didn't say it.
- Could've done better: I treated "match the logo" as "use the logo's font for everything". → Match the logo's *feel*
  (paper, red pen, restraint), take type from the creator's references; show one style frame before building 10 scenes.

## 2026-10-27 — Case 021 (GPT-6.1 Terra) + new logo v3 "ct(e)"
- **Creator:** new logo (red "ct" on a rule, the "e" dropped below and circled in red pen, CATCH · THE · ERROR, paper
  ground). Asked to save it for future sessions, match the video's look to it, use it creatively in motion, and learn the
  zooms and transitions of OpenAI's Terra film. → `brand/README.md`, `brand/MOTION.md`, `brand/motion/logo-sting.html`,
  rule 15 (look v4 "paper").
- Logo layers were cut from the PNG by colour (red = R−G), an opening (min/max filter) to split letters from the thin pen
  stroke, and largest-blob per letter; checked side by side against the source.
- The story came from the source's own fine print: "Shown at actual speed. Some sections omitted." under the demo.
  → Always read every caption/footnote in a launch film frame by frame; that's where our beat is.
- One voice job (13 takes incl. 3 hooks + 2 GPT spellings, ~1 min on L4) + one transcribe for word times; 0 re-voices.
- Could've done better: the first draft failed the STATIC gate twice because pen marks and mono text don't count as
  motion. → Plan one beat that moves a real area every ~2 s *in the storyboard*, before building. Also: BleepingComputer
  and openai.com block our fetcher (403 / Cloudflare); dev.to and simonwillison.net work for screenshots.


## 2026-10-27 — Creator: undo the format/look experiments; stick to the Case 020 routine
- Removed `/cte-explainer`, `/cte-demo`, `cte-kit`, `videos/_lab`, `VISUALS.md`, `EDITING.md`, `brand/lookbook`,
  `brand/fonts` and the "Catch it yourself" topic entry (all still in git history before this commit).
  Kept: rules 1–14 and this log. Production goes back to the Case 020 routine (`PLAYBOOK.md`, `STRATEGY.md`).
- Could've done better: I built two full skills + a kit before the creator had approved even one direction. → Show one
  small test, get a yes, and only then turn it into reusable tooling.

## 2026-10-27 — /cte-explainer + /cte-demo skills; Tabloid + Zine lab tests
- Built 10 s lab tests (`videos/_lab/`): Tabloid explainer (OpenAI agents story, Tech Times clipping, Courbet PD
  reaction) and Zine demo (real Content Credentials Verify recording, zoom-follow, step cards). Both PASS qa_frames.
- Facts: AFP/Tech Xplore had no severity rating → dropped that claim; used OpenAI's own quote instead.
- Memes: public-domain art only (Courbet, *Le Désespéré*, PD-Art), treated offline (halftone/photocopy, torn edge).
- Could've done better: headline wrapped and a stat overflowed on first snapshot; two pen marks missed until I computed
  them from the camera formula. → The kit README now states the formula; measure every mark, every time.
  Tech Xplore blocks bots — keep a list of outlets that allow screenshots.

## 2026-10-27 — Creator rejected Newsroom/Broadsheet type + 3 logo concepts; shortlisted Tabloid + Zine
- Feedback: "neither looks good, think outside the box, don't stay biased to what we already did".
  → Inspiration comes from real outside work first (Fonts In Use, Dribbble, foundries), shown as a curated board,
  *before* I build anything of my own. Shortlist kept: Tabloid/Newsprint, Zine/Photocopy (review later).
- Could've done better: I iterated inside our own style instead of looking outward; the first raw board was noisy
  site screenshots — curate 4 directions × 4 real works from the start.

## 2026-10-27 — Type, logo and editing taste (creator: fonts and logo look like AI slop)
- **Confirmed:** Geist + Instrument Serif is the AI-startup default (named in a 2026 "design slop" round-up), so it
  signals "AI product". Proposed newsroom type (Schibsted Grotesk / Newsreader / IBM Plex Mono) and 3 logo concepts
  built from editing marks (circle, [sic], strike) instead of a magnifier + bug icon. `EDITING.md` holds the cutting rules.
- Could've done better: two specimen frames wrapped on the first render, and the logo circle sat off-centre;
  measure text boxes before placing hand-drawn marks (same lesson as Case 020; make it a habit, not a fix).

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
