---
name: apple-film-moves
description: The editing and motion grammar of Apple's product films, measured from the MacBook Pro with PROLED XDR film (Oct 2026) and built as reusable HyperFrames moves - labels pinned to a tracked surface (planar tracking), labels fixed while the world moves past, port-style label rhythm, the lid bookend, full-bleed 9:16 crops of 4K masters, speed ramps and reversed shots. Use when cutting a premium product/launch video, an "ad-grade" short, or any video from a company's own launch film.
---

# Apple film moves

Learned frame by frame from Apple's touchscreen MacBook Pro film (1:56.7, 3840×2160, 23.976 fps, music only, no
narration) and shipped in `videos/case-026-touch-macbook-pro`. Use 3–5 of these per video, each caused by something on
screen. Code: `scripts/build_scenes.py` (`pin()`, `full()`, `ring_img()`), `scripts/cut_clips.py`, `tools/track_plane.py`.

## What the film does (measured)

| Move | In Apple's film | Why it works |
|---|---|---|
| **Pinned label** | "Up to 2000 nits peak brightness" lies flat on the desk in perspective and moves with it as the camera dollies (0:16–0:18); "PROLED XDR Display" rides the desk edge (0:13) | The spec belongs to the object; no overlay layer |
| **Fixed label, world passes** | "3 pounds light" holds dead still mid-frame while a walker carries the laptop past and through it (1:09–1:11) | Motion comes from the footage, the type stays calm |
| **Label rhythm** | Locked-off low angle; each cut swaps one word in the same slot: MagSafe → Headphone jack → HDMI → SDXC card slot (1:30–1:35), about 1 cut a second | A list becomes a beat |
| **One word, big, beside the product** | "Display" floats next to the screen at the screen's height (0:13) | Names the feature with one word |
| **Bookends** | Opens on the closed lid, its logo lighting up (0:03–0:06); ends on the lid closing, the logo glowing, then the logo + one line of fine print on black (1:47–1:56) | The product is the title card |
| **Camera always moving** | Slow dolly / push / orbit on every shot; FPV drone flights link locations (1:36–1:41); the spiral stair top-down (0:48) | No frame is ever static |
| **Hands on the screen** | Every touch shot is a hand mid-gesture: pinch, drag, spin, play | Show the verb, not the spec |
| **Fine print** | Only one line in the whole film: "Weight varies by configuration and manufacturing process." (under the "3 pounds" claim) | Read the last frame: that's where claims are qualified |

## Build them in HyperFrames

1. **Cut 9:16 from the 4K master** (`scripts/cut_clips.py`): crop 1215×2160 at `cx*2 ± 607` (cx in 1920-wide px), scale
   to 1080×1920. Speed: `setpts=(PTS-STARTPTS)/speed`. **Put `-t` before `-i`** (as an output option it silently cuts
   every slowed clip to its source length). Reverse in a second pass: `reverse,setpts=N/30/TB`. Check every clip's
   duration with ffprobe before building; check the shot list against a scene detect: Apple hides cuts inside camera
   whips (0.3 s of Finder, then the 3D model), so a "shot" can cross a cut.
2. **Pinned label** (`tools/track_plane.py`): pick a textured flat surface on the shot's first frame (screen UI, keys,
   desk), run `python3 tools/track_plane.py <master> <t0> <t1> "<quad>" assets/track/<shot>.json --show`, and look at the
   `.jpg` (quad on first/middle/last frame). In the scene, lay the label out in frame px on the t0 frame inside a full-frame
   `.pin` div (`transform-origin: 0 0`); `pin(sel, mats, fps, 0)` steps one `matrix3d` per source frame from the timeline
   (seek-safe). `track()` maps H from source px to frame px: `A·H·A⁻¹`, `A = scale(1080/607.5)` + crop offset; fps × speed.
   Surfaces near the bottom of a 9:16 crop (keyboard decks) fall under the caption area: pin to the screen glass instead.
3. **Fixed label**: `.lab` (Inter 600, 78 px, −0.03em, white, soft dark shadow), centred, y 600–760, rising in on its word;
   a small second line (46 px, 500) for the qualifier. Ticks or checks in the red pen, drawn on.
4. **Label rhythm**: 3–4 shots of ~0.5 s each in one slot, a tick SFX per cut (`tick-a/b` rotated).
5. **Bookends**: open on the lid's logo (it works as an underlay a falling shot reveals); close on the lid shutting
   (thud-wood on the frame it shuts) before the end card.
6. **The fine print** as the brand beat: the last frame as a white-bordered printed frame (bare black reads EMPTY to
   `qa_frames`), lift the grey line ×2.6 so it reads on a phone, push in to ≥ 26 px text, pen under the key words.

## Ours on top (CatchTheError)
- The cover's printed photo **becomes the film**: `clip-path: inset(photo rect round 26px)` → `inset(0)`, 0.55 s `expo.inOut`.
- **The claim acts it out**: "your arm would fall off" → the shot falls off its corner (`rotation 24, y 1500, power2.in`) onto
  the next shot; "you never have to lift it" → the arm shot plays backwards.
- **Strike the quote** with the pen when the story contradicts it ("It ~~doesn't~~ work.").

## Gates
`npx hyperframes check` → snapshots of every scene → `node tools/qa_layout.mjs` (labels vs captions vs the right rail) →
draft render → `python3 tools/qa_frames.py`. A pinned label can drift out of the safe zone as the camera moves: the layout
gate samples every 0.2 s, so it catches that.
