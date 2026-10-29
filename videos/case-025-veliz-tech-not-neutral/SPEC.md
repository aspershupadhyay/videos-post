# Case 025 — "Technology is never neutral" (Prof. Carissa Véliz, Nexus Institute)

**Not a fact-check.** An insight clip: we share her argument as she made it, no voice-over against her, nothing
said against her in our text. Creator's ask (2026-10-29): a glimpse of the conversation, the other speaker
included, captions, elite presentation.

## Source
- "Is technology neutral?" — Nexus Institute, https://www.youtube.com/watch?v=AhED5V1TcC0 (6:38).
  Credit in `POST.md` (rule 16). Timed transcript from YouTube's English captions: `scripts/source-transcript.txt`.
- The line the creator remembered is, verbatim: "it would **never** occur to you to cook with a gun."
- Speaker names other than Véliz: read them from the video itself (name supers / Nexus page). Don't guess.

## Status — delivered 2026-10-29
- Source MP4 uploaded by the creator to VoiceBox (Videos / veliz-nexus.mp4, 1920x1080 50 fps AV1, 6:38); YouTube itself
  refused this sandbox (bot check / 403) even with permission.
- Built: `scripts/cut_clips.py <source>` (per-shot 9:16 crops, wide shot over a blurred copy, dialogue -15 LUFS) →
  `scripts/build.py` (captions from YouTube's word times, name tags, 3 expressive lines, SFX, music bed) →
  `scripts/make_cover.mjs`. Clips/audio are git-ignored; rebuild from the VoiceBox source.
- Gates: `check` clean · qa_layout PASS · qa_frames PASS (draft + delivery) · mix -15.2 LUFS integrated.
- Delivered (md5-checked): VoiceBox Videos `case-025-veliz-tech-never-neutral-9x16.mp4` (59.4 s) and Images
  `case-025-veliz-tech-never-neutral-cover.png`.
- **Live on Instagram 2026-10-29:** https://www.instagram.com/reel/DfEtGQejPYw/ (board post `6ae310935b4d2f43c22f`,
  ig_reel, POST.md caption + cover; published after VoiceBox fixed its caption override, see LEARNINGS 2026-10-29).

## The cut (as built)
Cold open 82.90–87.00 (her gun line), then 59.85 → 109.60: AlQama's "…neutrally" to his "I agree." (the creator's
end point; the second "I agree", at 1:49), applause running on under the end card. Speakers from the video's own name
supers: Khalifa AlQama, Carissa Véliz (Javier Cercas comes in later, not in this cut).
| src | who | line |
|---|---|---|
| 0:59 | first speaker | "…I think you have to look at technology neutrally. I think what we do with technology —" "You can jump in now." |
| 1:15 | Véliz | "But technology is never neutral because it's not God given. We designed it and we designed it to do something." |
| 1:21 | other | "I agree." |
| 1:22 | Véliz | "So for example, it would never occur to you to cook with a gun. It's not made for that. [It's made] to threaten or kill." |
| 1:28 | Véliz | "And there might be a function in that, but it's not neutral. And when you design A.I. to extract all value without consent, to surveil on a mass scale, that is not neutral." |
| 1:39 | Véliz | "And every surveillance tool is not neutral. Surveillance is made to control. And we're social beings. So what do we control? We control other human beings." |
| 1:49 | AlQama | "I agree." (end here; applause runs on under the end card) |

Alternatives offered: B 0:59–1:22 (stops at the first "I agree", loses the gun line); C 0:59–6:26 (to "I agree
with that"; knife / Plato / Gutenberg / "personal landmine"; ~5.5 min, YouTube not Reels).

## Presentation
- Frame 0 = cover (STRATEGY §5 template adapted: no "Fact check" line): "Is technology *neutral*?" (or "Is a gun just a
  *tool*?"), red serif italic word + pen, a real still of her in the printed-photo frame.
- 9:16 reframe of the 16:9 stage footage (crop off the Nexus side bar), hard-cut to whoever speaks; slow push on her
  key lines; split (her top / him bottom) where they overlap.
- Captions: rule 16 chip style, her one key word per beat in red (#DD483F): "never neutral", "gun", "control".
- One expressive line where the gun line lands. Name tag on her first frame: "Prof. Carissa Véliz · Oxford".
- End: `brand/motion/logo-sting.html` + a natural ask (text, or one short `sparsh` line: "Do you agree with her?
  Tell us below."). No voice-over over her words.
- Gates: qa_layout, snapshots, draft + qa_frames, style demo to the creator before the full render, then VoiceBox.
