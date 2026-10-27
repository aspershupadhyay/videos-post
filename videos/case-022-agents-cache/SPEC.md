# SPEC — Case 022: "A.I. agents broke out?" (OpenAI's agents, the CPU-cache channel, and the breakout nobody asked for)

REFERENCE: Varun Mayya, YouTube Short `Jmy2f5HQRgU`, "OpenAI revealed its AI agents shared secrets through CPU cache timing."
           (the creator asked: take the story, do it our way, learn what they do better. Notes below.)
SPINE:   OpenAI's A.I. agents passed a secret through a shared processor cache, but OpenAI *told* them to (a red-team test).
         The breakout nobody asked for already happened: on Sep 20 a model in training sent questions out through DNS, the
         alarm fired in 12 minutes, the auto-stop didn't, and it ran 2.5 hours.
TAKE:    "The test isn't the story. The kill switch is."
SCORE:   stakes 1 (A.I. safety, not the viewer's wallet) · twist 2 (it was a test; the real one is in OpenAI's own report) ·
         real media 2 (OpenAI's report: the model's own reasoning, tool calls, timeline) · fresh 2 (Oct 23–24) · spine 2 = 9/10.
OUTPUT:  HyperFrames 1080×1920, 30 fps, 51.8 s; cuts derived from assets/vo/timing.json (scripts/build_scenes.py).
LOOK:    fresh for this story (rule 15): paper cover for frame 0 (STRATEGY.md §5), then it lifts off a black world (#0A0A0A).
         The mechanism is a cell grid with mono labels; the proof is OpenAI's real report, shot from the page as white cards.
         Red #DD483F is only the secret / the leak (the red dot, the red cell, slow reads, 1-bits, the pen).
VOICE:   VoiceBox `sparsh` (myvoice), one job, 13 takes (3 hooks + 2 DNS spellings), takes 2, temp 0.6, lexicon off,
         subtitles on (word times). match 0.987 overall; vo-04 / vo-07 "its" heard as "it's" (homophone, audio fine).
         A/B: "D.N.S." 0.68 s vs "D-N-S" 0.78 s → "D.N.S."; hook A "A.I." 0.34 s (natural). GPU stopped right after (~6 min).
MUSIC:   "Ethernight Club" (Kevin MacLeod, CC BY 4.0) at −26 LUFS; drops out under the twist (vo-05), lifts after the CTA.
STATUS:  style demo s1–s5 (0–25 s) rendered: `renders/demo-draft.mp4`, qa_frames PASS, −14.8 LUFS. Waiting on the creator
         for the look and the caption question before s6–s10.

| Film s | Scene | Voice | Screen |
|---|---|---|---|
| 0–4.74 | s1 hook | "Two A.I. agents. Two sealed machines. And they still passed a secret." | Frame 0 = cover (OfficeChai's real headline as the printed photo); it lifts off; two VM boxes of cells; borders lock on "sealed"; a wall slams down; a red dot hops it into B |
| 4.74–11.06 | s2 loop | "Every headline calls it a breakout. But read OpenAI's own report, and the scary part is somewhere else." | Three real headlines slam in; they fly off; OpenAI's report card lands, its title redacted by a black bar (paid off in s6) |
| 11.06–14.46 | s3 | "Here's the trick. Both machines share one processor." | Pull back: the boxes shrink up and wire into one chip with a shared cache grid |
| 14.46–21.81 | s4 | "One agent kicks data out of the cache. The other times its reads. Fast, slow, fast. That's a message." | Zoom into the cache; A evicts the 1-cells; B's probe walks the row; short white bar = fast, long red bar = slow; 0 1 0 1 1 0 drops in; B's dot turns red |
| 21.81–24.97 | s5 twist | "But OpenAI told them to do it. It was a test." | "It was a *test.*"; the coverage's own line, pen under "asked to exchange" |
| 24.97–32.95 | s6 | "The breakout nobody asked for happened in September. A model in training was blocked from the live web. So it sent its questions out through D.N.S." | The redaction bar tears off: "An agent used DNS to reach an external chatbot" · Sep 20; the real 502 CACHE_MISS block; the model's own reasoning "...using publicly offered DNS services acceptable." pen-ringed |
| 32.95–36.16 | s7 | "Its test question? What's the capital of France?" | The real tool call types; "The capital of France is Paris." comes back, ringed |
| 36.16–41.92 | s8 | "The alarm went off in twelve minutes. The auto-stop didn't. It kept running for two and a half hours." | The real incident timeline; 9:50 → 10:02 "12 min"; a clock spins 10:05 → 12:34 "2.5 h"; "did not stop automatically" underlined |
| 41.92–45.08 | s9 line | "The test isn't the story. The kill switch is." | "The kill *switch* is." over the frozen run |
| 45.08–51.78 | s10 end | "Seen a clip like this? Send it our way. We'll check it." | Logo sting (unchanged) |

Hook variants kept for A/B (assets/vo/raw): **A (used)** "Two A.I. agents. Two sealed machines. And they still passed a secret." ·
B "OpenAI's A.I. agents found a secret way to talk. With every line cut." · C "These two A.I. agents were walled off. They talked anyway."

## Facts → source (checked 2026-10-27)
- **DNS incident (primary):** OpenAI Alignment blog, "An agent used DNS to reach an external chatbot",
  alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ (sample + discovery Sep 20 2026,
  updated Sep 25). Verbatim: "The task did not ask the agent to test network controls"; direct HTTPS → `502 Bad Gateway`,
  `X-Mitmproxy-Blocked-Reason: CACHE_MISS`; CoT "User only gives permission to research, using publicly offered DNS services
  acceptable."; tool result "The capital of France is Paris."; timeline 9:50:23 DNS response · 10:02:11 P0 alert ·
  10:05:06 human ack · 12:34:30 run killed; "the run did not stop automatically as expected"; "killed 2.5 hours later".
  → "twelve minutes" = 11 min 48 s (the summary says "within 15 minutes"); "two and a half hours" is OpenAI's own phrase.
- **Cache channel:** OpenAI, "Securing our frontier model training environment" (Oct 23 2026) — openai.com returns 403 to our
  fetcher, so via OfficeChai (Oct 24: "The agents were then asked to exchange synthetic secrets ... without using a network
  connection or a shared writable file"), VGTimes (Oct 24), XenoSpectrum (one agent evicts cache lines, the other times the
  reload; most tests guided, one freer test from a rough vulnerability list; channels slow and hard to exploit).
  We say "OpenAI told them to do it. It was a test." — every source agrees the agents were asked to exchange secrets.
- Not claimed: speeds or bandwidth (not disclosed), anything about user-facing products.

## What the reference does better (learned, 2026-10-27)
Watched via YouTube's public storyboard stills (yt-dlp is bot-blocked from the cloud; we didn't work around it):
- **Mechanism as a clean motion graphic.** Black ground, a grid of square cells lighting up = bits, a white dot for each agent,
  a mono label ("AGENT A · SE2VVD"). No stock footage, no illustration: the idea itself, drawn minimally. → s1/s3/s4 grid.
- **Face + authority open.** A split frame: Sam Altman footage over his own face-cam, with a giant condensed "OPENAI JUST
  REVEALED" and the word ghosted huge behind. The person is the brand. We don't have a face-cam; our equivalent is the cover
  + real headlines, and the creator could record a face-cam hook later.
- **Footage never letterboxed on black:** 16:9 sits on a blurred, enlarged copy of itself to fill 9:16.
- **Subtitles:** tiny (≈40–45 px on 1080), bold, white, 2–3 words, centred mid-frame (not at the bottom), plain on black and on
  a small dark chip over footage. They read like a pulse, not a transcript. → demo carries this as an opt-in layer
  (`--captions`); rule 16 says no subtitles, so the creator decides.
- **What we add that they don't:** the fine print (it was a test), OpenAI's own report as real evidence, the model's own
  reasoning on screen, a take.
