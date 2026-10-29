# SPEC — Case 023: "13× faster than what?" (Apple's M6 MacBook Pro ad, read to its last frame)

REFERENCE: Apple's M6 MacBook Pro film, as posted by Greg Joswiak ("Everyday tasks. No sweat. Faster graphics. Nailed it.
           On-device AI…"), 48.4 s, 1920×1080, 23.976 fps; the creator dropped the MP4 and asked to learn its transitions.
SPINE:   Apple says the new MacBook Pro is 13× faster at A.I. — measured against a 2020 M1 laptop — and against last year's
         M5, Apple's own number is 1.3×. The 13× is time to first token: how fast the answer starts, not the whole answer.
TAKE:    "Still on an M1? Real upgrade. Bought an M5 last year? Keep your money."
LINE:    "Thirteen times faster than what? The answer is always in the last frame."
SCORE:   stakes 2 (a $1,999 buying decision) · twist 2 (the comparison is in the ad's own fine print) · real media 2 (Apple's
         film, Apple's newsroom footnote, Apple's 2020 M1 press photo) · fresh 2 (announced Oct 27 2026, pre-orders Oct 28) ·
         spine 2 = 10/10.
OUTPUT:  HyperFrames 1080×1920, 30 fps, 46.0 s; cuts derived from assets/vo/timing.json (scripts/build_scenes.py).
LOOK:    fresh for this story (rule 15), borrowed from the source: real footage in angled shards on black that morph from
         cut to cut; the cover breaks into two shards and falls away; the ad's last frame as a white-bordered printed frame.
         Ours on top: #0A0A0A ground, Inter 800, the red pen #DD483F as the one accent (asterisk, rings, underlines, the dot
         that turns 13 into 1.3 — the logo's falling dot). Captions on (rule 16).
VOICE:   VoiceBox `sparsh` (myvoice), one job: 13 takes (3 hooks + "M one"/"M1" A/B), takes 2, temp 0.6, lexicon off.
         All lines match 0.99–1.0 except vo-04/04b at 0.83: Whisper wrote "twenty twenty" as "2020" (digits, not a mishear).
         "M one" (vo-04, 0.74 s with a beat after it) picked over "M1" (vo-04b, 0.66 s). GPU stopped after the job.
MUSIC:   "Voxel Revolution" (Kevin MacLeod, CC BY 4.0) at −26 LUFS; drops out under the fine print (vo-03), lifts after the CTA.
QA:      qa_layout PASS; draft qa_frames PASS (first draft FAIL: the ad's last frame read as EMPTY → framed as a printed frame).

| Film s | Scene | Voice | Screen |
|---|---|---|---|
| 0–4.11 | s1 hook | "Apple says its new MacBook Pro is thirteen times faster at A.I." | Frame 0 = cover; it cracks diagonally and the halves fall away from Apple's own "UP TO 13X FASTER AI PERFORMANCE" shot (slowed 1.75×); a red asterisk lands after 13X on "A.I." |
| 4.11–8.95 | s2 loop | "The answer is in tiny grey text, on the last frame of Apple's own ad." | The ad flashes past in a morphing shard (title, carry); hard cut to the ad's last frame in a white printed frame; the pen rings the grey fine print; zoom through it |
| 8.95–12.14 | s3 | "Performance testing against MacBook Pro with M one." | The fine print itself, enlarged from the ad (1.9×), lifted from grey to white as it's read; pen under "with M1." (music out) |
| 12.14–15.30 | s4 | "M one. That's a laptop from twenty twenty." | "M1" big; Apple's own Nov 2020 photo of the 13-inch M1 MacBook Pro lands as a printed photo; red italic "2020" + pen |
| 15.30–20.44 | s5 | "Against last year's M five? Apple's own number is one point three times." | "13×" over Apple's newsroom footnote (shot at 400 css px ×3); the card dims to "14-inch MacBook Pro with M5"; the digits part and a red dot falls in: "1.3×"; pen under "up to 1.3x faster" |
| 20.44–25.05 | s6 | "And what got thirteen times faster? The wait before the A.I. starts answering." | Apple's words "Up to 13x faster time to first token" (pen under "time to first token"); Apple's own Autopilot UI in a shard; a red bar runs from "wait" and stops as Apple's A.I. shows "Here are some suggestions of what to do next…" |
| 25.05–28.58 | s7 | "Not the whole answer. Just how fast it starts." | An answer streams in as token pills ("The whole answer: not timed"); the first token turns red, ringed; "First token: the 13× part" |
| 28.58–34.05 | s8 take | "Still on an M one? It's a real upgrade. Bought an M five last year? Keep your money." | Two shards: the 2020 M1 photo ("M1 → M6", "Real upgrade.") then the new laptop from Apple's film ("M5 → M6", "Keep your *money.*") |
| 34.05–38.97 | s9 line | "Thirteen times faster than what? The answer is always in the last frame." | Four ad shots race past in morphing shards; the last frame again, pushed in; the pen rings the fine print |
| 38.97–46.01 | s10 end | "Seen an ad like this? Send it our way. We'll check it." | Paper end card + logo sting |

Hook variants kept for A/B (assets/vo/raw): **A (used)** "Apple says its new MacBook Pro is thirteen times faster at A.I." ·
B "Thirteen times faster at A.I. That's Apple's new MacBook Pro." · C "…faster at A.I. Faster than what?"

## Facts → source (checked 2026-10-28)
- **Primary:** Apple Newsroom, "Apple introduces the new 14-inch MacBook Pro with M6" (Oct 27 2026),
  apple.com/newsroom/2026/10/apple-introduces-the-new-14-inch-macbook-pro-with-m6/. Verbatim: "For those upgrading from M1,
  … up to 11x faster graphics and up to 13x faster AI performance." Bullet: "Up to 13x faster time to first token performance
  for LLM prompt processing compared to the 13-inch MacBook Pro with M1, and up to 1.3x faster than the 14-inch MacBook Pro
  with M5." Footnote 3: testing by Apple, September 2026. Also: GPU up to 30% / AI workloads up to 25% faster than M5;
  $1,999; pre-orders Oct 28, available Nov 6.
- **The ad's own fine print** (last frame, 0:40–0:48): "Performance testing against specific MacBook Pro systems with M1.
  Results reflect approximate performance; visit apple.com/macbook-pro. Battery life varies by use and configuration.
  Additional software shown."
- **"A laptop from 2020":** Apple Newsroom, "Introducing the next generation of Mac" (Nov 10 2020) — the 13-inch MacBook Pro
  with M1; the s4/s8 photo is that release's press image (Apple_new-macbookpro-photographer-photo_11102020).
- Cross-checks: TechCrunch and 9to5Mac (Oct 27 2026) report the same 13× / 1.3× figures.
- **There is no M6 Pro chip.** The new machine is the 14-inch MacBook Pro *with M6*; the M5 Pro / M5 Max models stay on sale
  (9to5Mac). We say "new MacBook Pro", never "M6 Pro".
- Not claimed: the 11× graphics (it's Blender ray tracing vs an M1, which has no hardware ray tracing — a good second catch,
  but a 4th number; kept for the caption), battery, or anything Apple didn't publish.

## What we learned from Apple's film (→ brand/MOTION.md)
- **Shards, not frames.** Footage lives in angled 4-point polygons on black; the polygon itself morphs between cuts, so a cut
  is also a shape change. The black between shards is the brand's negative space.
- **Type rides the shard.** "NEW MACBOOK PRO WITH M6" and "24 HOURS OF BATTERY LIFE" are set on the diagonal of the
  shard's edge and rotate with it; "UP TO 13X FASTER AI PERFORMANCE" sits under a funnel-shaped shard.
- **The product enters through the shape.** A funnel (inverted trapezoid) frames the person and the laptop sits in its neck.
- **One number per shot, giant and condensed**, with the qualifier ("UP TO") small beside it.
- **The last frame is the logo + fine print, held 8 s.** That's where the comparison lives — our story.
