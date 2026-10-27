# videos-post

Short-form research videos for **CatchTheError** (Instagram Reels, YouTube Shorts, X), built with
[HyperFrames](https://hyperframes.heygen.com) (HTML → MP4) and voiced with the VoiceBox MCP (trained voice `sparsh`).

- **Start every session by reading `STRATEGY.md`** (topic scoring, hook method, structure, covers, no-dead-frames gate,
  scoreboard) and `TOPICS.md` (the scored topic bank). Then `PLAYBOOK.md` for production: research, voice, sound, motion.
- `VISUALS.md` is the visual language (Exhibit → Source → Verdict → Proof; style frames in `brand/lookbook/`).
- `EDITING.md` is the cutting/sound taste guide and the type + logo v2 proposal (awaiting the creator's pick).
- `LEARNINGS.md` is the dated feedback log; `tools/qa_frames.py <render>` is the blank/frozen-frame gate.
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
7. **One spine, best fact first.** Case 018 glued three stories together and buried the shareable one at 0:42. Write
   the one-sentence spine first; the strongest fact is line 1 and frame 0. 40–50 s, max 3 numbers on screen, have a take.
8. **No dead frames.** Something real is on screen from the first frame of every scene; nothing frozen > 2 s.
   `python3 tools/qa_frames.py` must PASS on the draft render before the delivery render.
9. **Every video ships a cover** (`renders/cover.png`, series template in `STRATEGY.md` §5) that reads in the 3:4 grid crop.
10. **Spend resources once.** Draft render → QA → one delivery render; re-voice only the failing lines; reuse the last
    case's scripts, SFX and fonts.
11. **Learn every video.** Log the creator's numbers and feedback in `LEARNINGS.md` + the `STRATEGY.md` scoreboard; promote
    what holds twice into a rule here; refresh `TOPICS.md` each session.
12. **Review after every task.** End each task (a video, research, a fix) with a short "Could've done better" note in
    `LEARNINGS.md` (dated): what slowed us, what was weak, what to do differently. Don't redo the finished task for it;
    it's for the next one, so we never repeat a mistake.
13. **Voice: write "A.I." in the script** (`lexicon: false`, no pronounce rule for it); "ay-eye" stretches into "AAAI".
    The CTA is a natural ask said like a person ("Seen a clip like this? Send it our way. We'll check it."), never a slogan.
14. **A passing check is not quality.** Whisper match can't hear a stretched word and qa_frames can't see a boring stretch.
    Before delivery: A/B any acronym or name in the first voice job, re-watch the 25–40 s middle for retention, and ask the
    creator to listen once.
