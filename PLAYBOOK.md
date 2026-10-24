# CatchTheError video playbook

How a CatchTheError video gets made in this repo: research → script → voice → sound → motion → check → render.
The rules come from the HyperFrames skills (`.claude/skills/hyperframes`, measured on HeyGen's own films),
the brand in `brand/`, and what worked on Case 017. Start a new video with:

```bash
cd videos && npx hyperframes@0.8.192 init case-0NN-<slug> --example blank --resolution portrait --non-interactive
```

Then copy `DESIGN.md`, `assets/fonts/`, `assets/sfx/` and `scripts/` from `videos/case-017-artcraft`.

## 1. Research (the brand is the fact-check)

- Every claim on screen traces to a named source. Read at least three, and prefer primary sources (the
  project's own site or repo, the person's own post) over write-ups. Note the source in small mono
  type on the frame that uses it.
- Never derive a number the sources don't give. "43,000 stars by Oct 11" is fine. "20× faster" is not
  fine unless someone measured it.
- Show the claim being checked as text, not as a fake screenshot of a real person's account.
- The format: **viral claim → what's real → errors (1–3) → verdict stamp → follow.**

## 2. Script (hook in the first second)

- Frame 0 is the thumbnail: the claim itself, readable, with a question ("Cloned in a week?").
  Never a logo or black.
- Line 1 restates the claim in its most shareable form. Line 2 promises the payoff ("so let's catch the error").
- Then open loops: number the errors ("Error one… two… three") so viewers stay for the count.
- Short sentences, about 19 words per scene, 2.2 words a second. A 60–70 s video is about 150 words.
- End on the verdict in one line, then the call to action: "Follow CatchTheError. We check the post before you share it."
- Banned words: unlock, seamless, supercharge, game-changer, revolutionize, effortless.

## 3. Voice (VoiceBox MCP, trained model `sparsh`)

- `preview_pronunciation` first; add `pronounce` fixes (e.g. `CatchTheError → "Catch The Error"`, `ArtCraft → "Art Craft"`).
- `voice_lines` with `engine: myvoice`, `voice: sparsh`, `style: tech`, `platform: reels`, `takes: 3`,
  `subtitles: true`, one line id per sentence group (`vo-01` …). Takes 3 = best of three per sentence.
- Keep the per-word timings (`*.subs.json`): they drive captions and every on-screen cue.
- Check each result's `match` (≥0.95). Whisper mishearing a word ("parity" → "parody") is fine if the
  audio is right; fix the caption text in `scripts/build_captions.py`.

## 4. Sound: the voice is the clock

| Layer | Level | Rule |
| --- | --- | --- |
| Voice | −14 LUFS (VoiceBox mastering) | Everything is timed to its words |
| Music bed | −26 LUFS (about 12 dB under the voice) | Human-composed, CC BY or better; skip the quiet intro; drop it out for one beat before the verdict; lift it after the last word |
| SFX | 0.2–0.6 volume, peaks 3–6 dB over the bed | Only on a visible action: stamp → impact, red pen → scratch, card → whoosh, count → ticks |

- Music used so far: Kevin MacLeod / incompetech.com (CC BY 4.0, credit in the caption). Freesound and
  Pixabay are blocked from the cloud sandbox; Kenney.nl packs (CC0) and the HyperFrames bundled SFX work.
- `scripts/build_sfx.py` places each SFX so its measured peak lands one frame after its picture. Edit
  `scripts/sfx_cues.json`, not the HTML.
- Rotate takes (`stamp-a/b/c`, `scratch-a/b/c`); the same whoosh on every cut is the clearest tell of
  a template.

## 5. Motion: the case-file medium

- Grounds are whole-frame worlds: paper (home), teal, mustard, rust. Change world on each beat, through
  an object on screen: zoom through the lens, flood out of a stamp, a whip, an iris, a sheet covering the frame.
- Stamps: scale 1.5 → 1 in 0.12 s with `power4.in`, then dead still, with a sound on contact.
- Red pen: an SVG stroke drawn with `stroke-dashoffset`, or a background band growing left to right.
- Highlighter: `background-size` on an inline span, swept in on the spoken word.
- Arrivals use `expo.out` / `power4.out` at 0.35–0.6 s. Exits are 40% shorter with `power3.in`.
  Per-word titles blur 8 → 0 px in 0.13–0.18 s.
- Something new every 2–4 s. Nothing breathes, floats or drifts after it lands.
- Vertical safe zone: words between y 168 and 1150 px. Captions sit at 1196 px. Below 1330 px is
  platform UI (caption, buttons).

## 6. HyperFrames gotchas we hit

- A `fromTo` tween that starts later renders its *from* state at t=0 (immediateRender). For anything
  hidden until later: hide it in CSS (`opacity: 0`), give the tween `immediateRender: false`, and put
  `opacity: 1` in **both** from and to.
- Don't `tl.set()` initial hidden states at 0 (lint `gsap_timeline_set_initial_hide`); use CSS.
- Give every `<audio>` a `data-duration` and layered SFX different `data-track-index` lanes.
- Rotating an SVG `<g>` with `svgOrigin` can shift it: animate a plain `y` when you only need a drop.
- Run `npx hyperframes check --json`, then `snapshot --at …` and *look* before rendering.

## 7. Ship

```bash
npx hyperframes check --json
npx hyperframes snapshot --at 0,5,10,...
npx hyperframes render -q delivery -o renders/<name>-9x16.mp4
npx hyperframes audio renders/<name>-9x16.mp4 --json   # loudness and hits, measured
```

Post copy goes in the video folder's `POST.md`: a hook caption, three hashtags at most, and the music credit.
