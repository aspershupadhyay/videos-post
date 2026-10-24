# videos-post

Short-form research videos for **CatchTheError** (Instagram Reels, YouTube Shorts, X), built with
[HyperFrames](https://hyperframes.heygen.com) (HTML → MP4) and voiced with the VoiceBox MCP (trained voice `sparsh`).

- Read `PLAYBOOK.md` before making or editing a video: research, script, voice, sound and motion rules.
- HyperFrames skills are vendored in `.claude/skills/` (`/hyperframes` first). Pinned CLI: `npx hyperframes@0.8.192`.
- Brand: `brand/` (logo SVGs from `brand/build_logo.py`) and each video's `DESIGN.md`.
- One folder per video in `videos/`; each has `SPEC.md`, `scripts/` (audio prep, captions, SFX cues) and `renders/`.

## Taste rules — from the creator's feedback (read before every video; these override the playbook)

Log every new piece of feedback in `LEARNINGS.md` with the date, and promote it here once it's a rule.

1. **Restraint over palette.** Case 017 used every brand colour as a whole-frame world (teal, mustard, rust) — too much,
   it reads as a template. Default ground is **black (#0A0A0A) or white (#FAFAFA)**. The brand appears as **one signature
   element** only (e.g. the red-pen mark / rust accent on the single word that matters, and the logo on the end card).
   The palette is for consistency, not decoration.
2. **It must look real, not generated.** Real footage, real screenshots and real UI from the source beat drawn
   illustrations. Fewer elements per frame, more space, one idea per shot. "Anyone with a subscription can make a
   video — we're building taste."
3. **Script like a million-follower creator.** Tight, conversational, opinionated, no filler; a hook that creates a
   question in the first 1–2 s, open loops, payoff, and a line people want to repeat.
4. **Use real source media.** For a product/model video, fetch the company's own launch video, demos and benchmark
   charts and cut them in (credited), instead of recreating them.
5. **Always verify:** facts against primary sources, frames by snapshot, sound by measurement — before delivering.
6. Kept from Case 017 (liked): the SFX design, the music bed under the voice, the trained `sparsh` voice.
