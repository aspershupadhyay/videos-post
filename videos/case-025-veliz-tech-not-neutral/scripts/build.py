"""Build the film from the source's word timings: index.html, compositions/{s1,s2,s3,captions}.html, assets/music/bed.wav.

    python3 scripts/build.py          (after scripts/cut_clips.py)

Word times: YouTube's own English captions for the video (scripts/source-words.json, [word, start, end] in source
seconds). They lead the audio by ~0.1 s (speech onset measured at 60.00 vs "I" at 59.88), so captions use them as is.
Timeline: s1 cold open (her gun line) 0-4.10 · s2 the exchange 4.10-53.80 · s3 end card + logo sting to END.
"""
import json
import re
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
COLD_IN, COLD_DUR = 82.90, 4.10
MAIN_IN, MAIN_VID, MAIN_AUD = 59.85, 49.70, 53.55
M = COLD_DUR                     # main starts here on the film clock
END_CARD = M + MAIN_VID          # 53.80
END = round(END_CARD + 5.6, 2)   # sting lands by +2.3 s, holds >= 3 s


def main_t(src):
    return round(M + src - MAIN_IN, 3)


def cold_t(src):
    return round(src - COLD_IN, 3)


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                                check=True, capture_output=True, text=True).stdout)


# ---------- words -> caption chips ----------
words = [w for w in json.loads((P / "scripts/source-words.json").read_text())]
words = [[re.sub(r"^>>\s*", "", w).strip(), s, e] for w, s, e in words]
words = [[w, s, min(e, s + 0.7)] for w, s, e in words if w and w != ">>"]   # YouTube's end = next word's start
words.append(["control.", 103.95, 104.70])     # YouTube's captions drop it; she says "Surveillance is made to control."
words.sort(key=lambda w: w[1])
CROSSTALK = (87.10, 87.66)                      # AlQama's "Very good." under her line: left out of the captions
ALQAMA = lambda t: t < 74.0 or t >= 108.9      # who is speaking
RED = {"neutral", "neutral.", "gun.", "kill.", "surveil", "control."}
RED_ONCE_SKIP = {"neutrally."}                  # his word, not hers


def chips(lo, hi, clock, stop):
    ws = [w for w in words if lo <= w[1] < hi and not (CROSSTALK[0] <= w[1] < CROSSTALK[1])]
    out, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        nxt = ws[i + 1] if i + 1 < len(ws) else None
        text = " ".join(x[0] for x in cur)
        brk = (nxt is None or len(cur) >= 3 or len(text) >= 15 or re.search(r"[.,?!]$", w[0])
               or nxt[1] - w[2] > 0.3 or ALQAMA(nxt[1]) != ALQAMA(w[1]) or len(text + " " + nxt[0]) > 18)
        if brk:
            out.append({"words": cur, "start": clock(cur[0][1]), "spk": "a" if ALQAMA(cur[0][1]) else "v"})
            cur = []
    for i, c in enumerate(out):
        last_end = clock(c["words"][-1][2])
        c["end"] = round(min(out[i + 1]["start"] if i + 1 < len(out) else stop, last_end + 0.5, stop), 3)
    return out


cold_chips = chips(COLD_IN, COLD_IN + COLD_DUR, cold_t, COLD_DUR - 0.02)
main_chips = chips(MAIN_IN, 109.45, main_t, END_CARD - 0.02)

# ---------- expressive lines (s2): Inter 800 + one red serif italic word + the pen ----------
# (trigger word in source s, held until source s, html). The caption chip holding the trigger word is suppressed.
LINES = [(76.36, 80.90, 'Never <span class="it">neutral.</span>'),
         (88.32, 91.40, 'Made to <span class="it">kill.</span>'),
         (103.95, 105.45, 'Made to <span class="it">control.</span>')]
suppressed = set()
for trig, _, _ in LINES:
    for i, c in enumerate(main_chips):
        if any(abs(w[1] - trig) < 0.01 for w in c["words"]):
            suppressed.add(i)


def chip_html(cid, c):
    parts = []
    for w, _, _ in c["words"]:
        cls = ' class="r"' if (w in RED and c["spk"] == "v") else ""
        parts.append(f"<b{cls}>{w}</b>" if cls else w)
    return f'<div id="{cid}" class="cap {c["spk"]}" style="opacity:0"><span>{" ".join(parts)}</span></div>'


caps_html, caps_js = [], []
allc = [("k", c) for c in cold_chips] + [("m", c) for i, c in enumerate(main_chips) if i not in suppressed]
for n, (_, c) in enumerate(allc):
    cid = f"c{n}"
    caps_html.append(chip_html(cid, c))
    caps_js.append(f'tl.set("#{cid}", {{ opacity: 1, visibility: "visible" }}, {c["start"]:.3f}); '
                   f'tl.set("#{cid}", {{ opacity: 0, visibility: "hidden" }}, {c["end"]:.3f});')

FONTS = """    @font-face { font-family: "Inter"; font-weight: 100 900; font-display: block; src: url("assets/fonts/Inter.ttf") format("truetype"); }
    @font-face { font-family: "Instrument Serif"; font-style: italic; font-weight: 400; font-display: block; src: url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2"); }
    @font-face { font-family: "Courier Prime"; font-weight: 700; font-display: block; src: url("assets/fonts/CourierPrime-Bold.ttf") format("truetype"); }"""

(P / "compositions/captions.html").write_text(f"""<template>
  <style>
{FONTS}
    #root {{ position: absolute; inset: 0; overflow: visible; background: transparent; }}
    .cap {{ position: absolute; left: 0; top: 1400px; width: 1080px; text-align: center; }}
    .cap span {{ display: inline-block; padding: 8px 18px 10px; border-radius: 12px; background: rgba(10, 10, 10, 0.72); color: #fff;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 44px; letter-spacing: -0.035em; }}
    .cap.a span {{ color: #d9d7d2; }}
    .cap b {{ font-weight: 800; }}
    .cap b.r {{ color: #ff6a5f; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{"".join(caps_html)}</div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(caps_js)}
      tl.set({{}}, {{}}, {END_CARD:.2f});
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
""")

# ---------- shared scene CSS ----------
SCENE_CSS = FONTS + """
    #root { position: absolute; inset: 0; overflow: hidden; background: #0a0a0a; color: #f4f2ee; font-family: "Inter", sans-serif; }
    .it { position: relative; display: inline-block; font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; color: #dd483f; letter-spacing: -0.01em; font-size: 1.14em; line-height: 0.8; padding-right: 0.06em; }
    .ul { position: absolute; left: -2%; bottom: -0.12em; width: 104%; height: 0.3em; overflow: visible; }
    .ul path { fill: none; stroke: #dd483f; stroke-width: 7; stroke-linecap: round; stroke-dasharray: 1400; stroke-dashoffset: 1400; }
    .cam { position: absolute; inset: 0; overflow: hidden; }
    .cam video { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; display: block; }
    .shade { position: absolute; left: 0; width: 1080px; pointer-events: none; }
    .tag { position: absolute; left: 64px; top: 262px; padding: 16px 26px 18px 30px; border-radius: 14px; background: rgba(10, 10, 10, 0.74); opacity: 0; }
    .tag::before { content: ""; position: absolute; left: 0; top: 18px; bottom: 18px; width: 6px; border-radius: 3px; background: #dd483f; }
    .tag .n { font-weight: 700; font-size: 40px; letter-spacing: -0.03em; color: #fff; white-space: nowrap; }
    .tag .r { margin-top: 6px; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.12em; text-transform: uppercase; color: #b9b7b2; white-space: nowrap; }
    .line { position: absolute; left: 0; top: 1176px; width: 1080px; text-align: center; font-weight: 800; font-size: 104px; letter-spacing: -0.05em; line-height: 1; color: #fff;
      text-shadow: 0 6px 40px rgba(0, 0, 0, 0.75), 0 2px 8px rgba(0, 0, 0, 0.6); opacity: 0; }
"""
UL = '<svg class="ul" viewBox="0 0 100 20" preserveAspectRatio="none"><path vector-effect="non-scaling-stroke" d="M2 12 C 30 7, 66 11, 98 5" /></svg>'


def with_pen(html):
    return html.replace("</span>", UL + "</span>", 1)


# ---------- s1: cold open (the gun line), frame 0 = the cover ----------
(P / "compositions/s1.html").write_text(f"""<template>
  <style>
{SCENE_CSS}
    #s1-cov {{ position: absolute; inset: 0; background: url("assets/shots/cover.png") 0 0 / 1080px 1920px; z-index: 5; }}
  </style>
  <div id="root" data-composition-id="s1" data-width="1080" data-height="1920">
    <div id="s1-cam" class="cam">
      <video id="s1-v" class="clip" src="assets/clips/coldopen.mp4" data-start="0" data-duration="{COLD_DUR}" muted playsinline></video>
    </div>
    <div class="shade" style="top:0;height:560px;background:linear-gradient(rgba(10,10,10,0.55),rgba(10,10,10,0))"></div>
    <div class="shade" style="top:1040px;height:880px;background:linear-gradient(rgba(10,10,10,0),rgba(10,10,10,0.6))"></div>
    <div id="s1-tag" class="tag"><div class="n">Prof. Carissa Véliz</div><div class="r">University of Oxford</div></div>
    <div id="s1-cov"></div>
  </div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      // frame 0 is the cover; it lifts away like a page as her line starts
      tl.to("#s1-cov", {{ y: -1920, rotation: -4, duration: 0.55, ease: "power3.in", transformOrigin: "0px 1920px" }}, 0.28);
      tl.fromTo("#s1-cam", {{ scale: 1.12 }}, {{ scale: 1.0, duration: 0.9, ease: "expo.out", transformOrigin: "540px 700px" }}, 0.5);
      tl.fromTo("#s1-cam", {{ scale: 1.0 }}, {{ scale: 1.07, duration: {COLD_DUR - 1.4:.2f}, ease: "sine.inOut", transformOrigin: "540px 700px", immediateRender: false }}, 1.4);
      tl.fromTo("#s1-tag", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "expo.out", immediateRender: false }}, 0.85);
      tl.to("#s1-tag", {{ opacity: 0, duration: 0.2 }}, {COLD_DUR - 0.25:.2f});
      tl.set({{}}, {{}}, {COLD_DUR});
      window.__timelines["s1"] = tl;
    }})();
  </script>
</template>
""")

# ---------- s2: the exchange ----------
CUTS = [60.08, 72.22, 74.32, 75.86, 89.30, 93.08, 105.66]          # source cuts (cut_clips.py)
line_divs, line_js = [], []
for i, (trig, hold, html) in enumerate(LINES):
    a, b = main_t(trig) - M - 0.05, main_t(hold) - M
    line_divs.append(f'<div id="s2-l{i}" class="line">{with_pen(html)}</div>')
    line_js.append(f'tl.fromTo("#s2-l{i}", {{ opacity: 0, y: 40, scale: 0.96 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "expo.out", immediateRender: false }}, {a:.3f});')
    line_js.append(f'tl.to("#s2-l{i} .ul path", {{ strokeDashoffset: 0, duration: 0.34, ease: "power2.inOut" }}, {a + 0.3:.3f});')
    line_js.append(f'tl.to("#s2-l{i}", {{ opacity: 0, duration: 0.18 }}, {b:.3f});')
loc = lambda src: round(main_t(src) - M, 3)
pushes = [  # (from src, to src) slow push on the shot while the key line lands; snaps back on the next cut
    (82.40, 89.30),    # "…cook with a gun. It's not made for that. To threaten or kill."
    (99.20, 105.66),   # "…that is not neutral … Surveillance is made to control."
]
push_js = []
for a, b in pushes:
    push_js.append(f'tl.fromTo("#s2-cam", {{ scale: 1 }}, {{ scale: 1.07, duration: {loc(b) - loc(a):.3f}, ease: "sine.inOut", transformOrigin: "540px 760px", immediateRender: false }}, {loc(a):.3f});')
    push_js.append(f'tl.set("#s2-cam", {{ scale: 1 }}, {loc(b):.3f});')

(P / "compositions/s2.html").write_text(f"""<template>
  <style>
{SCENE_CSS}
  </style>
  <div id="root" data-composition-id="s2" data-width="1080" data-height="1920">
    <div id="s2-cam" class="cam">
      <video id="s2-v" class="clip" src="assets/clips/main.mp4" data-start="0" data-duration="{MAIN_VID}" muted playsinline></video>
    </div>
    <div class="shade" style="top:0;height:560px;background:linear-gradient(rgba(10,10,10,0.55),rgba(10,10,10,0))"></div>
    <div class="shade" style="top:1040px;height:880px;background:linear-gradient(rgba(10,10,10,0),rgba(10,10,10,0.6))"></div>
    <div id="s2-tag-a" class="tag"><div class="n">Khalifa AlQama</div></div>
    <div id="s2-tag-v" class="tag"><div class="n">Prof. Carissa Véliz</div><div class="r">University of Oxford</div></div>
    {"".join(line_divs)}
  </div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      // who's talking: his tag as he starts, hers as she cuts in
      tl.fromTo("#s2-tag-a", {{ opacity: 0.85, x: -20 }}, {{ opacity: 1, x: 0, duration: 0.3, ease: "expo.out" }}, 0);
      tl.to("#s2-tag-a", {{ opacity: 0, duration: 0.2 }}, 3.2);
      tl.fromTo("#s2-tag-v", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.4, ease: "expo.out", immediateRender: false }}, {loc(75.86):.3f});
      tl.to("#s2-tag-v", {{ opacity: 0, duration: 0.2 }}, {loc(75.86) + 3.4:.3f});
      {(chr(10) + "      ").join(line_js)}
      {(chr(10) + "      ").join(push_js)}
      tl.set({{}}, {{}}, {MAIN_VID});
      window.__timelines["s2"] = tl;
    }})();
  </script>
</template>
""")

# ---------- s3: end card (paper) + the ask; the logo sting plays on top ----------
S3 = round(END - END_CARD, 2)
(P / "compositions/s3.html").write_text(f"""<template>
  <style>
{SCENE_CSS}
    #root {{ background: #e7e7e5 url("assets/logo/paper-1080x1920.png") 0 0 / 1080px 1920px; color: #141414; }}
    #s3-a {{ position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 72px; letter-spacing: -0.03em; }}
    #s3-b {{ position: absolute; left: 0; top: 1290px; width: 1080px; text-align: center; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.08em; text-transform: uppercase; color: #5f5f5c; opacity: 0; }}
  </style>
  <div id="root" data-composition-id="s3" data-width="1080" data-height="1920">
    <div id="s3-a">Do you agree with her?</div>
    <div id="s3-b">Tell us in the comments</div>
  </div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      tl.fromTo("#s3-a", {{ opacity: 0.85, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, 0);
      tl.fromTo("#s3-b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, immediateRender: false }}, 2.0);
      tl.set({{}}, {{}}, {S3});
      window.__timelines["s3"] = tl;
    }})();
  </script>
</template>
""")

# ---------- sound: dialogue, music bed, SFX ----------
SFX = [  # (file, film s, volume, note)
    ("whoosh", 0.30, 0.16, "the cover lifts away"),
    ("whoosh-short", M - 0.08, 0.12, "cut back to where it started"),
    ("scratch-a", main_t(LINES[0][0]) + 0.27, 0.32, "pen under 'neutral.'"),
    ("scratch-b", main_t(LINES[1][0]) + 0.27, 0.32, "pen under 'kill.'"),
    ("scratch-c", main_t(LINES[2][0]) + 0.27, 0.32, "pen under 'control.'"),
    ("drop", END_CARD + 0.05 + 0.32, 0.3, "the dot lands on the rule"),
    ("thud-wood", END_CARD + 0.05 + 0.85, 0.2, "c lands"),
    ("plate", END_CARD + 0.05 + 0.97, 0.16, "t lands"),
    ("pop", END_CARD + 0.05 + 0.80, 0.22, "the dot becomes the e"),
    ("scratch-c", END_CARD + 0.05 + 1.10, 0.4, "the pen circles the e"),
    ("typing", END_CARD + 0.05 + 1.75, 0.12, "CATCH · THE · ERROR"),
]
sfx_tags = []
for n, (f, t, v, note) in enumerate(SFX):
    d = dur(P / f"assets/sfx/{f}.mp3")
    sfx_tags.append(f'<audio id="sfx-{n + 1:02d}" class="clip" src="assets/sfx/{f}.mp3" data-start="{t:.3f}" data-duration="{d:.3f}" '
                    f'data-track-index="{12 + n % 5}" data-volume="{v}" data-audio-group="sfx"></audio><!-- {note} -->')

# Music: "Ossuary 6 - Air" (Kevin MacLeod, CC BY 4.0), from 14 s in (its slow swell is over by then), ~16 dB under the
# dialogue; lifts under the end card with the applause, fades out at the end.
lift = END_CARD
env = (f"volume='if(gt(t,{lift + 0.6:.2f}),2.2,if(gt(t,{lift:.2f}),1+1.2*(t-{lift:.2f})/0.6,1))':eval=frame")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "14", "-t", str(END + 0.5), "-i", str(P / "assets/music/ossuary-6-air-source.mp3"),
                "-af", "loudnorm=I=-31:TP=-3:LRA=11,afade=t=in:d=0.6," + env + f",afade=t=out:st={END - 1.8:.2f}:d=1.8",
                "-ar", "48000", str(P / "assets/music/bed.wav")], check=True)

index = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>CatchTheError — Case 025: Carissa Véliz, "technology is never neutral"</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0a0a0a; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <!-- Footage: "Is technology neutral?", Nexus Institute (youtube.com/watch?v=AhED5V1TcC0); reframed by scripts/cut_clips.py.
           Cold open (her gun line) -> the exchange from Khalifa AlQama's "technology … neutrally" to his "I agree." -> end card. -->
      <div id="s1" data-composition-id="s1" data-composition-src="compositions/s1.html" data-start="0" data-duration="{COLD_DUR}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 1"></div>
      <div id="s2" data-composition-id="s2" data-composition-src="compositions/s2.html" data-start="{M}" data-duration="{MAIN_VID}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 2"></div>
      <div id="s3" data-composition-id="s3" data-composition-src="compositions/s3.html" data-start="{END_CARD:.2f}" data-duration="{S3}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 3"></div>
      <div id="sting" data-composition-id="logo-sting" data-composition-src="compositions/logo-sting.html" data-start="{END_CARD + 0.05:.2f}" data-duration="{S3 - 0.05:.2f}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 50"></div>
      <div id="caps" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{END_CARD:.2f}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 60"></div>

      <!-- Dialogue: the source's own sound, levelled to -15 LUFS (cut_clips.py); it runs on into the applause under the end card. -->
      <audio id="dlg-cold" class="clip" src="assets/audio/coldopen.wav" data-start="0" data-duration="{dur(P / 'assets/audio/coldopen.wav'):.3f}" data-track-index="10" data-volume="1" data-audio-group="voiceover"></audio>
      <audio id="dlg-main" class="clip" src="assets/audio/main.wav" data-start="{M}" data-duration="{dur(P / 'assets/audio/main.wav'):.3f}" data-track-index="10" data-volume="1" data-audio-group="voiceover"></audio>

      <!-- Music bed: "Ossuary 6 - Air", Kevin MacLeod (incompetech.com), CC BY 4.0; envelope baked in. -->
      <audio id="music" class="clip" src="assets/music/bed.wav" data-start="0" data-duration="{END}" data-track-index="11" data-volume="1" data-audio-group="music"></audio>

      {(chr(10) + "      ").join(sfx_tags)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
(P / "index.html").write_text(index)
print("film", END, "| cold chips", len(cold_chips), "| main chips", len(main_chips), "suppressed", sorted(suppressed))
for k, c in allc:
    print(f'{c["start"]:6.2f}-{c["end"]:6.2f} {c["spk"]} {" ".join(w[0] for w in c["words"])}')
