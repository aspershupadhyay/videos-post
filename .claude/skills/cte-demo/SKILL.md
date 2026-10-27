---
name: cte-demo
description: CatchTheError zoom-follow screen demo — a 35-45 s vertical tutorial that shows a real tool/website in use, result first, then numbered steps with the camera following each click, then the tool's honest limit. Use when the creator says "/cte-demo <tool or how-to> [zine|tabloid]" or asks for a tutorial, tool demo or "Catch it yourself" episode. Builds with Playwright recording + HyperFrames + VoiceBox (sparsh).
---

# /cte-demo — zoom-follow screen demo

Input: a tool + task ("check an image with Content Credentials") and optionally a look (`zine` default, `tabloid`).
Output: `videos/case-0NN-<slug>/renders/<slug>-9x16.mp4` + `cover.png` + `POST.md`, merged.

Read first: `CLAUDE.md`, `STRATEGY.md`, `EDITING.md`, `.claude/skills/cte-kit/README.md`, `looks/<look>/LOOK.md`,
`/hyperframes`.

## 1. Frame it
- The **result** the viewer gets (frame 0), **3 steps max**, the tool's **limit** (always said: e.g. "no label ≠ fake",
  "only detects Google's own watermark", "no public detector reliably catches the newest A.I. video").
- Verify what the tool claims to do on its official page/help doc; note sources in `SPEC.md`.

## 2. Capture (real, never mocked)
- **Public website:** write `steps.json` and run `node .claude/skills/cte-kit/scripts/record_demo.cjs steps.json <dir>`
  → `demo.webm` + `demo-log.json` (time + box of every action, visible cursor). Use a genuine sample file (e.g. C2PA
  test files from github.com/contentauth/c2pa-rs `sdk/tests/fixtures`). Trim to the actions with ffmpeg → mp4 30 fps.
- **Logged-in tools / phone apps:** ask the creator to screen-record (Screen Studio, QuickTime, phone recorder) and
  send it; log action times by watching it (snapshot every 0.5 s) — never fake a UI.
- Grab the result frame as a still for the hook.

## 3. Script to the beat template (35–45 s)
| Time | Beat | Screen |
|---|---|---|
| 0–3 s | Result first ("This photo's 'ID' doesn't check out.") | Result still in a torn mount, marker circle on the verdict |
| 3–6 s | Why care, one line | Same, slow push |
| 6–30 s | Steps 1 → 2 → 3, one action each | Recording in mount; step card pops per step; camera zooms to each logged action |
| 30–37 s | The limit (honest) | Black caption chip with the rule |
| 37–42 s | Natural CTA | End card |
"A.I." spelling, natural CTA, have a take (rule 13).

## 4. Voice
Same as `/cte-explainer` §4 (sparsh, subtitles/polish off, A/B names, GPU off straight after). Step cards land on the
phrase onset of each step's line; the camera move starts ~0.6 s before the logged click it frames.

## 5. Build
Copy `cte-kit/templates/zine-demo/`. Camera keyframes from `demo-log.json` with the kit's zoom formula (film time =
step offset + (log t − trim start)). Pen marks over the recording placed by the same formula. Captions on the chip
only (no subtitles).

## 6. Gates + deliver + learn
Exactly `/cte-explainer` §7–8, plus: every step must be readable at phone size (UI text ≥ ~22 px after zoom), and the
limit line must be present.
