# Case 018 v2 storyboard: "They made it worse on purpose" (~45 s)

Spine: *Moonshot made its own AI worse at hacking, because open weights can't be recalled, but the scores are its own.*
Built from the v1 post-mortem (LEARNINGS.md, 2026-10-27). Reuses v1's footage, charts, SFX and music.

| Time | Voice | Screen |
|---|---|---|
| 0–2.5 | "An AI lab just made its own model *worse*. On purpose." | Real xdev-bench-hard table full frame; red pen strikes 90 → 81. Frame 0 = cover. |
| 2.5–5 | "And the reason should worry you more than the model." | The table pushes in and dims; *"Why?"* in Instrument Serif Italic rides over it (no bare black). |
| 5–12 | "This is Kimi K3.1 Pro. It found 36 bugs in a physics simulator and taught this body to walk." | Fall → walk, one cut, cropped tight on the figure with the labels masked so it fills the frame; pen circles 36. |
| 12–17 | "On the hardest coding test, it's less than one point behind the #1 model." | Real Terminal-Bench chart, push to the two rows; red bracket 0.7. |
| 17–27 | "So it got *too* good at hacking. Ninety percent of their hardest tests. They cut its training until it hit 81." | Back to the table, slow push, 90 → 81 with context. |
| 27–33 | "Because on November 4th, they give it away. And open weights can't be recalled." | "Nov 4", then *"can't be recalled"* with the pen underline over a dimmed weights/download still. Music drops out. |
| 33–39 | "The fine print: those scores are Moonshot's own. Independent testers rank it fourth." | "VENDOR-REPORTED" in mono over the chart, then the Artificial Analysis ranking, #4 underlined. |
| 39–44 | "When you can't take it back, you decide what to give away." | Big type on #FAFAFA, music swells. |
| 44–47 | "We read the fine print. Catch the Error." | Logo end card ≥ 3 s; last frame dissolves to the table so it loops. |

Numbers on screen: 36, 0.7, 90 → 81 (plus #4 as a rank).
Cover: "Made worse. *On purpose.*" over the table crop, `CASE 018` top-left.
Gate: `python3 tools/qa_frames.py renders/<draft>.mp4` must PASS before the delivery render.
