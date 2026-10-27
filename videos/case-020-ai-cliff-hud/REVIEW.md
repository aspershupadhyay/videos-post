# REVIEW — Case 020

**Delivered:** `renders/case-020-ai-cliff-hud-9x16.mp4` (1080×1920, 30 fps, 49.3 s) + `renders/cover.png`.

## Verified
- Facts: every on-screen claim traced to Apple Newsroom, the two papers, or the clip's own overlay (SPEC.md).
- Voice: 13/13 lines Whisper match ≥ 0.995, 0 re-voices; subtitles and polish off.
- Frames: `hyperframes check` ok; snapshots at every scene; cuts pulled from the render; `tools/qa_frames.py` PASS
  on draft and delivery (Case 018 had 6 empty gaps).
- Sound (measured): −13.7 LUFS integrated, −1.0 dBTP.
- Cover: claim readable in the 3:4 grid crop at 270 px wide.

## Kept on purpose
- Short `line_unread` holds: each is said aloud at the same moment; credits are secondary.
- No captions (creator's call): the panel type carries the key line in each clip scene.

## Weakest moment / next time
- s3 (the scale) opens on a near-empty middle for ~0.1 s before the bar grows; start the bar at 30%.
- The X post screenshot is low-res (588 px); ask for a 2× screenshot or capture the post directly.
- Cover has no `CASE 020` tag (template asks for it); add it as a separate cover layer next time.
