# videos-post

Short-form research videos for **CatchTheError** (Instagram Reels, YouTube Shorts, X), built with
[HyperFrames](https://hyperframes.heygen.com) (HTML → MP4) and voiced with the VoiceBox MCP (trained voice `sparsh`).

- **Start every session by reading `STRATEGY.md`** (topic scoring, hook method, structure, covers, no-dead-frames gate,
  scoreboard) and `TOPICS.md` (the scored topic bank). Then `PLAYBOOK.md` for production: research, voice, sound, motion.
- `LEARNINGS.md` is the dated feedback log; `tools/qa_frames.py <render>` is the blank/frozen-frame gate.
- HyperFrames skills are vendored in `.claude/skills/` (`/hyperframes` first). Pinned CLI: `npx hyperframes@0.8.192`.
- Brand: **logo v3 "ct(e)"** — read `brand/README.md` (layers, paper ground, colours) and `brand/MOTION.md` (transitions
  learned from reference films). Every end card uses the reusable sting `brand/motion/logo-sting.html`. Logo 2.0 is retired.
- One folder per video in `videos/`; each has `SPEC.md`, `scripts/` (audio prep, captions, SFX cues) and a local, git-ignored
  `renders/`. Finished renders live on VoiceBox only; `RENDERS.md` says where each one is.

## Taste rules — from the creator's feedback (read before every video; these override the playbook)

Log every new piece of feedback in `LEARNINGS.md` with the date, and promote it here once it's a rule.

1. **Restraint over palette.** Case 017 used every brand colour as a whole-frame world (teal, mustard, rust) — too much,
   it reads as a template. Default ground is **black (#0A0A0A) or white (#FAFAFA)** (since Case 021: the logo's paper, rule 15). The brand appears as **one signature
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
9. **Every video ships a cover** (`renders/cover.png`, series template in `STRATEGY.md` §5) that reads in the 3:4 grid crop
   and at 120 px wide. The printed-photo still shows whole lines only (crop off any half-cut line).
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
15. **Match the logo's feel; design each video fresh (creator, 2026-10-27).** Fixed: every end card is
    `brand/motion/logo-sting.html` ("amazing" — keep it), red #DD483F stays the brand's one accent. Open: the look, layout,
    motion graphics and animation of each video. Pick what serves that story; don't copy the last case. Case 021's
    paper + printed-photo look is one good reference (`videos/case-021-gpt-6-1-terra`), not a template. Show a short style
    demo before building a whole video in a new look.
16. **Captions yes (reference style), no on-screen credits (creator, 2026-10-27, Case 022).** Captions in the Varun Mayya
    reference style: 2–3 words, Inter 700 44 px, white on a small dark chip, centred at y 1400 (`build_scenes.py --captions`
    in case-022). Don't otherwise put the voice on screen as text, and no source / credit lines in the frame (sources go in `POST.md`). Text appears only as short expressive lines on some beats
    (Case 021: Inter 800 + one red Instrument Serif italic word underlined by the pen). Show it, don't read it: turn each claim into a
    visual (the pen slices the tram = half price; the pen cuts the demo = "slow parts cut out"; an AD stamp on the demo).
    Real footage big (Case 021 framed it as printed photos; any treatment that keeps it real works). Cover = the creator's
    template (`STRATEGY.md` §5).
17. **Safe zones (Shorts + Reels).** Key content lives in y 240–1480 on 1080×1920; no text under the right button rail
    (x > 940) below y 950. Rearrange to fit, never shrink. Check with the overlay in `brand/README.md` before delivery.
18. **Sanity gate before any render (creator, 2026-10-27).** Nothing may cover text (a moving block over "CPU" failed
    Case 022), no text overlapping text, ≥ 16 px between text and any box border (inside or out), and every screenshot
    must be clearly readable on a phone (its text ≥ 26 px tall in the frame: shoot pages at ~400 css px wide ×3, crop to
    the lines that matter, declare `data-text-px` on the `<img>`). Run `node tools/qa_layout.mjs <project>` on the live
    preview; it must PASS, then look at a snapshot of every scene, then the draft render + `qa_frames.py`.
19. **Explain a mechanism one cause per line (creator, Case 022).** When a story has a "how it works", give each step
    its own short line and its own on-screen action (cache = a shelf → on-shelf fast / off-shelf slow → kick = 1 /
    leave = 0 → time the read → bit by bit). One sentence carrying the whole mechanism over an abstract graphic failed.
20. **Deliver to VoiceBox only (creator, 2026-10-27).** The final MP4 and cover go to VoiceBox Files (`add_media`;
    Videos / Images), named `case-0NN-<slug>-9x16.mp4` and `case-0NN-<slug>-cover.png`; check the copy's md5 against
    the local file, then keep them out of git (`renders/` is ignored). Files over ~3 MB need a public link for
    `add_media`; the repo is public, so push the file, copy it, then `git rm --cached` it in the next commit.
21. **Upload with the key, not MCP (creator, 2026-10-28).** The creator saved the VoiceBox upload key in this cloud
    environment's variables as `VOICEBOX_UPLOAD_TOKEN`; every new session has it (check: `[ -n "$VOICEBOX_UPLOAD_TOKEN" ]
    && echo set`; never print the value). Upload with `tools/vb_upload.sh <folder id or path> <files…>` (2 GB/file);
    `VB_CAROUSEL="<post name>"` groups slides as one carousel in argument order (`VB_POSITION_START` to append). Raw API,
    if needed: `POST https://voiceboxstudio.vercel.app/api/files/upload` with `Authorization: Bearer $VOICEBOX_UPLOAD_TOKEN`
    and `{"name","folder","carousel","position"}` → `curl -T <file> <upload_url>` → `POST …/api/files/complete
    {"ticket"}`. If the variable is missing, the script falls back to a git-ignored `.env` at the repo root. Never write
    the key into a tracked file (public repo), and never start an upload you won't finish (it can lock the carousel).
    File each post under `Images / 30 Days Post Challenge / <post name>`, then attach the files to the post's `ig_post`
    target with `publish_post` (go: save) so the board has the carousel too.
22. **Someone else's video (YouTube) as the source (Case 025).** Ask the creator for the link first; never hunt a
    paraphrased quote across the web. From the cloud, YouTube gives captions (`yt-dlp --skip-download --write-auto-subs`:
    word times in `<c>` tags) and oEmbed/stills, but refuses the media (bot check / 403) in every permission mode, and
    trying other clients is blocked as bot-check circumvention. So straight away ask the creator to upload the MP4 to
    VoiceBox Files (on a phone: screen-record the part; on a computer: `yt-dlp`), then pull it with `get_file`.
    Name speakers from the video's own name supers, never by guess.
23. **Insight clips (sharing someone's argument, not checking it).** No voice-over over them and nothing against them:
    our cover + a cold open on their best line, their exchange uncut, captions, a few expressive lines, the logo sting and
    a text ask ("Do you agree with her?"). Credit the source and the speakers in the caption (`POST.md`). Template:
    `videos/case-025-veliz-tech-not-neutral` (`cut_clips.py` per-shot 9:16 crops, `build.py` from the word times).
24. **Publishing to Instagram: check the caption before anything goes live (Case 025).** Save the plan with our
    caption (`publish_post` go: save), confirm `ig.caption` in the reply, then go: now and read the log: a line
    "…from the post package" means the caption was rewritten → `publish_status` stop at once (it cancels while Instagram
    is still processing). VoiceBox fixed that override on 2026-10-29 (it rewrote our caption twice before the fix);
    keep the check anyway.
