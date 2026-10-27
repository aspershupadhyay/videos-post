# SPEC — Case 021: "One photo. One sentence. This toy.*" (GPT-6.1 Terra launch, read the line under the demo)

SPINE:   OpenAI's new GPT-6.1 Terra turned one photo into a die-cast toy model by driving a 3D app itself, and it's half
         the price, but the demo's own footnote says "Shown at actual speed. Some sections omitted." and the
         "3× faster" is OpenAI's own number that no one outside has checked yet.
TAKE:    "A demo is an ad. Read the line under it."
SCORE:   stakes 1 (price, apps you'll use) · twist 2 (the footnote) · real media 2 (OpenAI's own film) · fresh 2 (out Oct 26) · spine 2 = 9/10.
OUTPUT:  HyperFrames 1080×1920, 30 fps, 50.4 s; cuts derived from assets/vo/timing.json (scripts/build_scenes.py).
LOOK:    v4 "paper" (brand/README.md): paper ground from the logo, Courier Prime Bold ink type, OpenAI footage in rounded
         cards, red #DD483F only for the pen (and the asterisk), logo sting on the end card.
VOICE:   VoiceBox `sparsh` (myvoice), 13 takes in one job (3 hooks + 2 GPT spellings), takes 2, temp 0.6, lexicon off,
         subtitles off; every line match 1.0 (vo-03 0.997, "Terra" heard as "Tera"). Whisper word times via `transcribe`.
         "GPT" A/B: plain "GPT" 0.52 s vs "G.P.T." 0.58 s, both clean → plain. GPU stopped right after (~4 min used).
MUSIC:   "Ethernight Club" (Kevin MacLeod, CC BY 4.0) at −26 LUFS; drops out under the payoff (vo-06), lifts after the CTA.

| Film s | Scene | Voice | Screen |
|---|---|---|---|
| 0–4.27 | s1 hook | "One photo. One sentence. And an A.I. designed this toy." | Frame 0 = the toy in hand + "This toy.*" (cover). Photo + typed prompt (real clip) → zoom-through → the toy |
| 4.27–8.71 | s2 loop | "But OpenAI put one tiny line under this demo. Keep your eye on it." | The 3D-app demo in a card; the logo's pen circle draws round the tiny footnote |
| 8.71–14.14 | s3 what | "This is GPT 6.1 Terra. It's not built to chat. It's built to use your computer." | OpenAI's earth → Lisbon zoom, 9:16; typed prompt pills; "built to chat" struck; the world shrinks into a card |
| 14.14–18.67 | s4 how | "Here, it opens a 3D app and builds the tram, piece by piece." | Viewport crop of the build → carry into ChatGPT → push to the model |
| 18.67–26.14 | s5 numbers | "It's half the price of the last Terra. And OpenAI says it finishes tasks three times faster than its bigger models." | "Half the price." · the tram rolls in · "OpenAI says" · "3× faster*" · the tram drives off on "faster" |
| 26.14–30.91 | s6 payoff | "Now, that tiny line: shown at actual speed, some sections omitted." | Zoom into the real footnote, through it; typed in full; pen under "Some sections omitted."; demo keeps playing below |
| 30.91–34.0 | s7 | "Actual speed, with the slow parts cut out." | "Slow parts: cut." — the word is sliced by the pen |
| 34.0–40.57 | s8 catch | "And three times faster? That's OpenAI's own test. No one outside OpenAI has confirmed it yet." | dev.to screenshot; camera zooms to "three times faster", pans to "these are OpenAI's claims, not independent results"; "Not yet." circled |
| 40.57–43.67 | s9 line | "A demo is an ad. Read the line under it." | Pen draws the line under it |
| 43.67–50.41 | s10 end | "Seen a demo like this? Send it our way. We'll check it." | Logo sting (dot → e, c/t drop, pen circle, tagline types); handle underlined |

Hook variants kept for A/B (assets/vo/raw): **A (used)** "One photo. One sentence. And an A.I. designed this toy." ·
B "An A.I. looked at one photo, and designed this toy." · C "This toy was designed by an A.I. that saw one photo."

## Facts → source (checked 2026-10-27)
- Launch Oct 26 2026; "a fast, efficient model that combines detailed visual reasoning and precise computer use"; API
  `gpt-6.1-terra`; Plus/Pro/Enterprise/Edu in ChatGPT Work and Codex. — BleepingComputer (Oct 26), Simon Willison (Oct 26).
  openai.com returned 403 to our fetcher; its post is cited by both.
- Price $1 in / $5 out per 1M tokens vs GPT-5.6 Terra $2 / $12 → "half the price" (input exactly half, output 42%). — dev.to, Simon Willison.
- "completing tasks over three times faster than both GPT-6 Astra and GPT-6.1 Sol" — OpenAI's claim via BleepingComputer;
  dev.to: "these are OpenAI's claims, not independent results" and "have not been independently verified yet".
- Footnote under the demo, verbatim: "Shown at actual speed. Some sections omitted." — OpenAI's launch film, 0:12–0:17.
- The prompt in the film: "Create a detailed 3D model of this tram for die-cast toy manufacturing."
- Framing: we don't say the demo is fake. Real-time playback with cuts is normal for ads; the point is the clock.
