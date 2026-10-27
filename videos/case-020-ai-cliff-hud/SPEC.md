# SPEC — Case 020: "AI picks every safe step down a cliff?" (viral HUD clip check)

SPINE:   568K people watched an "AI" pick safe footsteps down a cliff, but its readout claims a 300 m drop that
         Apple's LiDAR (5 m) couldn't measure, it labels the view "Wonderful", and the post names no source.
         The real AI for rock slopes exists: fixed cameras and LiDAR drones, not your boots.
TAKE:    "If the AI looks like a movie, it's probably an edit."
SCORE:   stakes 1 · twist 2 · real media 2 · fresh 2 (post < 24 h) · spine 2 = 9/10.
OUTPUT:  HyperFrames 1080×1920, 30 fps, 49.3 s. Type v3 (Geist 800 / Instrument Serif Italic / Geist Mono).
VOICE:   VoiceBox `sparsh` (myvoice), 13 lines, takes 2, temperature 0.6, subtitles OFF, polish OFF; all lines
         match ≥ 0.995, 0 re-voices. Levelled to −14 LUFS per line in `scripts/prep_audio.py`; phrase cues from pauses.
MUSIC:   "Ethernight Club" (Kevin MacLeod, CC BY 4.0) at −26 LUFS; dips under the twist; +5 dB after the last word.
FRAMING: we don't say "fake". We say what the frame shows, what a real sensor can do, and that no source is named.

| Film s | Scene | Voice | Screen |
|---|---|---|---|
| 0–7.4 | s1 hook | "An AI, picking every safe step down a cliff. 568,000 views. Nobody checked the readout." | The viral clip full-bleed; panel: claim → 568,000 counting up → "Nobody checked the *readout.*" |
| 7.4–10.6 | s2 | "Look. Drop: over three hundred meters." | Clip's drop counter; punch-in; red pen circles ">300 METER" |
| 10.6–13.75 | s3 | "Apple's LiDAR scanner measures up to five meters." | Apple Newsroom sentence, pen under "up to 5 meters away"; 300 m bar vs 5 m tick, to scale |
| 13.75–16.7 | s4 | "And no sensor on Earth writes… wonderful." | Frame from the clip; pen under WONDERFUL |
| 16.7–22.1 | s5 | "The post names no company. No paper. No device. We looked. Nothing." | The X post; rows company/paper/device/our search; pen circles "nothing" |
| 22.1–27.0 | s6 | "Here's the twist. The real AI exists. It just doesn't walk with you." | White ground, type only; music dips |
| 27.0–32.55 | s7 | "In Chongqing, fixed cameras watch rock faces, and a model tracks falling rocks in real time." | Sci. Rep. paper header + Fig. 9 (PTZ frames with rock tracks) |
| 32.55–37.6 | s8 | "In Hong Kong, a LiDAR drone flies under the trees to inspect landslide barriers." | Nat. Commun. header + Fig. 2 (drone, LiDAR maps) → Fig. 1 (landslide, barriers) |
| 37.6–39.95 | s9 | "Less cinematic. Actually real." | Viral clip vs Fig. 9, stacked |
| 39.95–43.45 | s10 | "If the AI looks like a movie, it's probably an edit." | White ground; pen under *edit.* |
| 43.45–49.33 | s11 | "We read the fine print. Catch the Error." | End card, mark builds |

## Facts → source (checked 2026-10-27)
- Post: @CodeByPoonam on X, "AI uses Cameras and Lidars to spot dangerous rock slopes.", 568K views, 5.2K likes,
  637 reposts at 22 h (creator's screenshot). Original maker of the clip: not found (3 searches).
- Overlay text in the clip: "ANALYSING TERRAIN", "DROP SIM" counting 133 → 284 → ">300 METER", "WONDERFUL", "DANGER".
- Apple: "The LiDAR Scanner measures the distance to surrounding objects up to 5 meters away" — Apple Newsroom, Mar 18 2020
  (iPad Pro). Survey-grade LiDAR reaches much further; we only claim Apple's consumer scanner.
- Huang et al., "Real-time dynamic monitoring of rockfalls with PTZ cameras", Sci. Rep. 16, 19993 (2026), Chongqing;
  YOLOv8 + tracking, deployed on NVIDIA Orin. CC BY-NC-ND 4.0, figures shown whole and credited.
- Liu et al., "Slope inspection under dense vegetation using LiDAR-based quadrotors", Nat. Commun. 16, 7411 (2025),
  with Hong Kong's Civil Engineering and Development Department. CC BY-NC-ND 4.0, figures shown whole and credited.
