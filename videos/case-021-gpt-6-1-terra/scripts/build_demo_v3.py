"""Case 021 v3 look demo: the first ~19 s (vo-01..vo-04) rebuilt for the creator's "it feels empty" note (2026-10-27).

v3 moves (vs v2): footage fills the whole frame every shot (safe zones limit text, not footage); a visual change every
1.5-2 s; big kinetic keyword labels on most beats (paper strips, 1-3 words, never the full sentence); the red pen is the
constant anchor (rings, underlines, strikes, a redaction, a cursor); a hero "printed photo" sits over its own blurred plate.
Writes v3-demo/index.html (assets is a symlink to ../assets).
"""
import json
import re
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
T = json.loads((P / "assets/vo/timing.json").read_text())
L = {l["id"]: l for l in T["lines"]}
END = 19.0


def w(vid, word, n=1):
    hits = [s for ww, s, e in L[vid]["words"] if re.sub(r"[^\w.]", "", ww).lower().strip(".") == word.lower()]
    return hits[n - 1]


def bleed(src, cx, cy, k):
    """Style for a 1920x1080 video/img filling 1080x1920, scale k, source point (cx, cy) at frame centre."""
    vw, vh = 1920 * k, 1080 * k
    left = min(0, max(1080 - vw, 540 - cx * k))
    top = min(0, max(1920 - vh, 960 - cy * k))
    return f"left:{left:.1f}px;top:{top:.1f}px;width:{vw:.1f}px;height:{vh:.1f}px"


def it(id_, text):
    return (f'<span class="it" id="{id_}">{text}<svg class="ul" viewBox="0 0 100 20" preserveAspectRatio="none" aria-hidden="true">'
            f'<path pathLength="1" vector-effect="non-scaling-stroke" d="M2 12 C 30 7, 66 11, 98 5" /></svg></span>')


def ring(id_, left, top, width, height, start_deg=340):
    m = f"conic-gradient(from {start_deg}deg at 50% 50%, #000 calc(var(--p) * 1deg), transparent calc(var(--p) * 1deg))"
    return (f'<div id="{id_}" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{height}px;--p:0;'
            f'-webkit-mask-image:{m};mask-image:{m}">'
            f'<img src="assets/logo/circle-crop.png" alt="" style="position:absolute;left:0;top:0;width:100%;height:100%" /></div>')


SHOTS = []   # (id, start, end, inner html)


def shot(id_, start, end, inner):
    SHOTS.append((id_, round(start, 3), round(end, 3), inner))


def vid(id_, src, start, dur, style, media_start=0.0, extra=""):
    return (f'<video id="{id_}" class="clip" src="{src}" data-start="{start:.3f}" data-duration="{dur:.3f}" '
            f'data-media-start="{media_start:.2f}" muted playsinline style="position:absolute;{style}{extra}"></video>')


# beat times from the voice --------------------------------------------------------------------------------------
t_photo, t_sent, t_ai, t_toy = 0.0, w("vo-01", "one", 2) - 0.08, w("vo-01", "and") - 0.06, w("vo-01", "this") - 0.12
t_but, t_line, t_demo, t_keep = L["vo-02"]["start"] - 0.2, w("vo-02", "line"), w("vo-02", "demo"), w("vo-02", "keep") - 0.1
t_this, t_gpt, t_not, t_use = L["vo-03"]["start"] - 0.2, w("vo-03", "gpt"), w("vo-03", "its") - 0.1, w("vo-03", "its", 2) - 0.1
t_here, t_build, t_p1, t_p2, t_p3 = L["vo-04"]["start"] - 0.2, w("vo-04", "builds") - 0.1, w("vo-04", "piece"), w("vo-04", "by"), w("vo-04", "piece", 2)

PHOTO_BOX = (409, 134, 1511, 938)            # photo + prompt card inside the 1920x1080 frame
BUILD_WIN = (174, 100, 1738, 962)            # the 3D app window incl. the footnote line
FOOT = (738, 944, 1182, 962)                 # "Shown at actual speed. Some sections omitted."

# A  "One photo."  the printed photo, big, over its own blurred plate; the pen rings the tram ------------------------
HW = 1000
k = HW / (PHOTO_BOX[2] - PHOTO_BOX[0])
HH = round((PHOTO_BOX[3] - PHOTO_BOX[1]) * k)
hero_media = f"left:{-PHOTO_BOX[0] * k:.1f}px;top:{-PHOTO_BOX[1] * k:.1f}px;width:{1920 * k:.1f}px;height:{1080 * k:.1f}px"
HT = 640
shot("A", t_photo, t_sent, f"""
  <div class="plate"><img src="assets/shots/photo-end.png" style="position:absolute;{bleed(0, 960, 520, 2.4)}" alt="" /></div>
  <div id="A-hero" class="photo" style="left:40px;top:{HT}px;width:{HW}px;height:{HH}px">
    <img src="assets/shots/photo-end.png" style="position:absolute;{hero_media}" alt="The Lisbon photo OpenAI's demo starts from" />
  </div>
  {ring("A-ring", 40 + round((870 - PHOTO_BOX[0]) * k), HT + round((470 - PHOTO_BOX[1]) * k), 300, 230)}
  <div id="A-l" class="lab" style="top:330px">One {it("A-it", "photo.")}</div>""")

# B  "One sentence."  push in on the prompt bar while it types; the pen underlines it --------------------------------
shot("B", t_sent, t_ai, f"""
  <div class="plate"><img src="assets/shots/photo-end.png" style="position:absolute;{bleed(0, 960, 520, 2.4)}" alt="" /></div>
  <div id="B-cam" style="position:absolute;inset:0">
    <div class="photo" style="left:40px;top:{HT}px;width:{HW}px;height:{HH}px">
      <img src="assets/shots/photo-end.png" style="position:absolute;{hero_media}" alt="" />
      {vid("B-v", "assets/footage/photo.mp4", t_sent, t_ai - t_sent, hero_media, 0.6)}
    </div>
    <svg id="B-ul" class="pen" style="left:70px;top:{HT + HH - 8}px;width:900px;height:40px" viewBox="0 0 900 40" aria-hidden="true"><path pathLength="1" d="M6 24 C 260 14, 600 22, 894 10" /></svg>
  </div>
  <div id="B-l" class="lab" style="top:330px">One {it("B-it", "sentence.")}</div>""")

# C  "and an A.I. designed"  hard cut: the 3D viewport, full-bleed, already building ------------------------------
shot("C", t_ai, t_toy, f"""
  <div class="bleed">{vid("C-v", "assets/footage/build.mp4", t_ai, t_toy - t_ai, bleed(0, 940, 520, 2.5), 2.4)}</div>
  <div id="C-l" class="lab" style="top:330px">A.I. {it("C-it", "designed")}</div>""")

# D  "this toy."  the hand sets the real toy down, full-bleed; the pen rings it -------------------------------------
shot("D", t_toy, t_but, f"""
  <div class="bleed" style="background:#fff">
    <img src="assets/shots/toytall-end.png" style="position:absolute;left:0;top:0;width:1080px;height:1920px" alt="" />
    {vid("D-v", "assets/footage/toytall.mp4", t_toy, min(1.63, t_but - t_toy), "left:0;top:0;width:1080px;height:1920px")}
  </div>
  {ring("D-ring", 200, 660, 720, 540)}
  <div id="D-l" class="lab" style="top:330px">this {it("D-it", "toy.")}</div>""")

# E/F/G  the demo, hero over its own plate; "one tiny line"; the pen rings it, then REDACTS it (the open loop) ---------
k2 = HW / (BUILD_WIN[2] - BUILD_WIN[0])
H2 = round((BUILD_WIN[3] - BUILD_WIN[1]) * k2)
build_media = f"left:{-BUILD_WIN[0] * k2:.1f}px;top:{-BUILD_WIN[1] * k2:.1f}px;width:{1920 * k2:.1f}px;height:{1080 * k2:.1f}px"
T2 = 720
fx, fy = 40 + (FOOT[0] - BUILD_WIN[0]) * k2, T2 + (FOOT[1] - BUILD_WIN[1]) * k2
fw, fh = (FOOT[2] - FOOT[0]) * k2, (FOOT[3] - FOOT[1]) * k2
shot("E", t_but, t_this, f"""
  <div class="plate">{vid("E-pv", "assets/footage/build.mp4", t_but, t_this - t_but, bleed(0, 960, 520, 2.3), 0.2)}</div>
  <div id="E-cam" style="position:absolute;inset:0">
    <div id="E-hero" class="photo" style="left:40px;top:{T2}px;width:{HW}px;height:{H2}px">
      {vid("E-v", "assets/footage/build.mp4", t_but, t_this - t_but, build_media, 0.2)}
    </div>
    {ring("E-ring", round(fx - 40), round(fy - 34), round(fw + 80), round(fh + 64))}
    <div id="E-red" style="position:absolute;left:{fx - 6:.0f}px;top:{fy - 3:.0f}px;width:{fw + 12:.0f}px;height:{fh + 8:.0f}px;background:#dd483f;clip-path:inset(0 100% 0 0);border-radius:3px"></div>
  </div>
  <div id="E-l" class="lab" style="top:330px">One tiny {it("E-it", "line.")}</div>
  <div id="E-l2" class="lab" style="top:330px;opacity:0">Keep your {it("E-it2", "eye")} on it.</div>""")

# H  "This is GPT-6.1 Terra."  OpenAI's earth dive (globe -> cloud -> Lisbon), full-bleed; the name slams in ----------------------------------
shot("H", t_this, t_not, f"""
  <div class="bleed" style="background:#000">{vid("H-v", "assets/footage/source.mp4", t_this, t_not - t_this, bleed(0, 960, 560, 1.85), 1.35)}</div>
  <div id="H-l" class="lab" style="top:330px">GPT-6.1 {it("H-it", "Terra")}</div>""")

# I  "It's not built to chat."  aerial Lisbon from the film, full-bleed; the pen strikes "chat" ----------------------
shot("I", t_not, t_use, f"""
  <div class="bleed">{vid("I-v", "assets/footage/source.mp4", t_not, t_use - t_not, bleed(0, 1100, 540, 1.85), 4.6)}</div>
  <div id="I-l" class="lab" style="top:330px">Built to <span id="I-chat" style="position:relative;display:inline-block">chat.<svg class="pen" style="left:-4%;top:0;width:108%;height:100%" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path id="I-strike" pathLength="1" vector-effect="non-scaling-stroke" d="M2 58 C 30 50, 70 54, 98 46" style="stroke-width:13" /></svg></span></div>""")

# J  "It's built to use your computer."  the ChatGPT app, full-bleed; a red cursor clicks -----------------------------
shot("J", t_use, t_here, f"""
  <div class="bleed" style="background:#fff">{vid("J-v", "assets/footage/app.mp4", t_use, t_here - t_use, bleed(0, 900, 560, 1.9), 0.4)}</div>
  <svg id="J-cur" style="position:absolute;left:0;top:0;width:70px;height:90px;overflow:visible" viewBox="0 0 70 90" aria-hidden="true"><path d="M4 4 L 4 70 L 22 54 L 36 84 L 48 78 L 34 50 L 58 50 Z" fill="#dd483f" stroke="#fff" stroke-width="5" stroke-linejoin="round" /></svg>
  <div id="J-rip" style="position:absolute;width:120px;height:120px;border:7px solid #dd483f;border-radius:50%;opacity:0"></div>
  <div id="J-l" class="lab" style="top:330px">Uses your {it("J-it", "computer.")}</div>""")

# K  "Here, it opens a 3D app"  the whole app window, full-bleed (real UI) ----------------------------------------
shot("K", t_here, t_build, f"""
  <div class="bleed" style="background:#e9e9e9">{vid("K-v", "assets/footage/build.mp4", t_here, t_build - t_here, bleed(0, 700, 500, 2.1), 0.0)}</div>
  <div id="K-l" class="lab" style="top:330px">Opens a {it("K-it", "3D app.")}</div>""")

# L  "and builds the tram"  push into the viewport ----------------------------------------------------------------
shot("L", t_build, t_p1, f"""
  <div class="bleed" style="background:#9a9a9a"><div id="L-z" style="position:absolute;inset:0">{vid("L-v", "assets/footage/build.mp4", t_build, t_p1 - t_build, bleed(0, 950, 520, 2.6), 1.6)}</div></div>
  <div id="L-l" class="lab" style="top:330px">builds the {it("L-it", "tram.")}</div>""")

# M  "piece by piece."  three stutter cuts through the build stages, one word per cut ------------------------------
stages = [(t_p1, t_p2, 0.6), (t_p2, t_p3, 2.6), (t_p3, END, 4.2)]
for i, (a, b_, ms) in enumerate(stages):
    words = ["piece", "piece by", "piece by piece."][i]
    shot(f"M{i}", a, b_, f"""
  <div class="bleed" style="background:#9a9a9a">{vid(f"M{i}-v", "assets/footage/build.mp4", a, b_ - a, bleed(0, 950, 540, 2.9 - 0.2 * i), ms)}</div>
  <div id="M{i}-l" class="lab" style="top:330px">{words.replace("piece.", it(f"M{i}-it", "piece.")) if i == 2 else words}</div>""")

# timeline --------------------------------------------------------------------------------------------------------
js = []
J = js.append
slap = lambda sel, t: J(f'tl.fromTo("{sel}", {{ scale: 1.35, rotation: -6, opacity: 0 }}, {{ scale: 1, rotation: -2, opacity: 1, duration: 0.22, ease: "back.out(2.4)", immediateRender: false }}, {t:.3f});')
pen = lambda sel, t, d=0.32: J(f'tl.fromTo("{sel}", {{ strokeDashoffset: 1 }}, {{ strokeDashoffset: 0, duration: {d}, ease: "power2.inOut", immediateRender: false }}, {t:.3f});')
draw_ring = lambda sel, t, d=0.45: J(f'tl.fromTo("{sel}", {{ "--p": 0 }}, {{ "--p": 360, duration: {d}, ease: "power2.inOut", immediateRender: false }}, {t:.3f});')
push = lambda sel, t0, t1, s0=1.0, s1=1.08, o="50% 50%": J(f'tl.fromTo("{sel}", {{ scale: {s0} }}, {{ scale: {s1}, duration: {t1 - t0:.3f}, ease: "none", transformOrigin: "{o}", immediateRender: false }}, {t0:.3f});')

# hard cuts: the wrappers are untimed (timed <video>s can't sit in a timed wrapper), so the timeline shows each one
for sid, a, b_, _ in SHOTS:
    J(f'tl.set("#{sid}", {{ visibility: "visible" }}, {a:.3f}); tl.set("#{sid}", {{ visibility: "hidden" }}, {b_:.3f});')
# every shot breathes (no frozen frame) and lands with a small punch-in
for sid, a, b_, _ in SHOTS:
    J(f'tl.fromTo("#{sid} .bleed, #{sid} .plate", {{ scale: 1.12 }}, {{ scale: 1.0, duration: {b_ - a:.3f}, ease: "power1.out", immediateRender: false }}, {a:.3f});')

slap("#A-l", 0.05); pen("#A-it path", w("vo-01", "photo") + 0.1); draw_ring("#A-ring", 0.55)
J(f'tl.fromTo("#A-hero", {{ y: 260, rotation: 4, scale: 0.9 }}, {{ y: 0, rotation: -1.5, scale: 1, duration: 0.5, ease: "expo.out", immediateRender: false }}, 0);')
slap("#B-l", t_sent); pen("#B-it path", w("vo-01", "sentence") + 0.2); pen("#B-ul path", t_sent + 0.25, 0.5)
J(f'tl.fromTo("#B-cam", {{ scale: 1 }}, {{ scale: 1.35, duration: {t_ai - t_sent:.3f}, ease: "power2.inOut", transformOrigin: "540px {HT + HH}px", immediateRender: false }}, {t_sent:.3f});')
slap("#C-l", t_ai + 0.35); pen("#C-it path", w("vo-01", "designed") + 0.15)
slap("#D-l", t_toy + 0.05); draw_ring("#D-ring", w("vo-01", "toy") - 0.05); pen("#D-it path", w("vo-01", "toy") + 0.1)
J(f'tl.fromTo("#E-hero", {{ y: 300, rotation: -4, scale: 0.9 }}, {{ y: 0, rotation: 0, scale: 1, duration: 0.5, ease: "expo.out", immediateRender: false }}, {t_but:.3f});')
slap("#E-l", w("vo-02", "one")); pen("#E-it path", t_line + 0.1); draw_ring("#E-ring", t_line, 0.5)
J(f'tl.fromTo("#E-cam", {{ scale: 1 }}, {{ scale: 1.6, duration: 0.7, ease: "power2.inOut", transformOrigin: "{fx + fw / 2:.0f}px {fy:.0f}px", immediateRender: false }}, {t_demo - 0.35:.3f});')
J(f'tl.to("#E-red", {{ clipPath: "inset(0 0% 0 0)", duration: 0.3, ease: "power2.inOut" }}, {t_demo + 0.15:.3f});')
J(f'tl.to("#E-l", {{ opacity: 0, duration: 0.08 }}, {t_keep:.3f});')
slap("#E-l2", t_keep); pen("#E-it2 path", w("vo-02", "eye") + 0.05)
J(f'tl.to("#E-cam", {{ scale: 3.4, duration: {t_this - t_keep:.3f}, ease: "power1.in", transformOrigin: "{fx + fw / 2:.0f}px {fy:.0f}px" }}, {t_keep:.3f});')
slap("#H-l", t_gpt - 0.05); pen("#H-it path", w("vo-03", "tera") + 0.05)
slap("#I-l", w("vo-03", "built") - 0.05); pen("#I-strike", w("vo-03", "chat") + 0.12, 0.22)
slap("#J-l", w("vo-03", "use")); pen("#J-it path", w("vo-03", "computer") + 0.15)
J(f'tl.fromTo("#J-cur", {{ x: 900, y: 1500 }}, {{ x: 610, y: 1080, duration: 0.6, ease: "power3.out", immediateRender: false }}, {t_use:.3f});')
J(f'tl.to("#J-cur", {{ scale: 0.85, duration: 0.06, yoyo: true, repeat: 1, transformOrigin: "0 0" }}, {t_use + 0.62:.3f});')
J(f'tl.fromTo("#J-rip", {{ x: 550, y: 1020, scale: 0.2, opacity: 1 }}, {{ scale: 1.4, opacity: 0, duration: 0.45, ease: "power2.out", immediateRender: false }}, {t_use + 0.64:.3f});')
J(f'tl.to("#J-cur", {{ x: 360, y: 1250, duration: 0.6, ease: "power2.inOut" }}, {t_use + 0.95:.3f});')
slap("#K-l", w("vo-04", "opens")); pen("#K-it path", w("vo-04", "app") + 0.05)
slap("#L-l", t_build + 0.05); pen("#L-it path", w("vo-04", "tram") + 0.05)
J(f'tl.fromTo("#L-z", {{ scale: 1 }}, {{ scale: 1.25, duration: {t_p1 - t_build:.3f}, ease: "power2.in", immediateRender: false }}, {t_build:.3f});')
for i, (a, _, _) in enumerate(stages):
    J(f'tl.fromTo("#M{i}-l", {{ scale: 1.15, rotation: -2 }}, {{ scale: 1, rotation: -2, duration: 0.18, ease: "power3.out", immediateRender: false }}, {a:.3f});')
pen("#M2-it path", t_p3 + 0.2)

# sound: voice, the case's music bed, one hit per cut -------------------------------------------------------------
def dur(f):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(P / f)]).decode())


cues = [(t_sent, "whoosh-short", 0.14), (t_sent + 0.2, "typing", 0.1), (t_ai, "whoosh", 0.16), (t_toy, "thud-wood", 0.3),
        (w("vo-01", "toy") - 0.05, "scratch-c", 0.4), (t_but, "tick-a", 0.25), (t_line, "scratch-a", 0.4),
        (t_demo + 0.15, "scratch-b", 0.45), (t_keep, "whoosh-cinematic", 0.12), (t_gpt - 0.05, "stamp-a", 0.25),
        (t_not, "whoosh-short", 0.14), (w("vo-03", "chat") + 0.12, "scratch-a", 0.4), (t_use, "whoosh-short", 0.14),
        (t_use + 0.62, "click-soft", 0.35), (t_here, "tick-b", 0.25), (t_build, "whoosh", 0.14),
        (t_p1, "thud-wood", 0.3), (t_p2, "plate", 0.3), (t_p3, "drop", 0.35)]
# labels slap in with a stamp under them
for t in [0.05, t_sent, t_ai + 0.35, t_toy + 0.05, w("vo-02", "one"), t_keep, w("vo-03", "built") - 0.05, w("vo-03", "use"), w("vo-04", "opens"), t_build + 0.05]:
    cues.append((t, "stamp-b", 0.12))
sfx = "\n".join(
    f'    <audio id="sfx-{i:02d}" class="clip" src="assets/sfx/{f}.mp3" data-start="{t:.3f}" data-duration="{min(dur(f"assets/sfx/{f}.mp3"), END - t):.3f}" '
    f'data-track-index="{12 + i % 2}" data-volume="{v}" data-audio-group="sfx"></audio>' for i, (t, f, v) in enumerate(sorted(cues)))
vo = "\n".join(
    f'    <audio id="{l["id"]}" class="clip" src="assets/vo/{l["id"]}.wav" data-start="{l["start"]}" data-duration="{l["duration"]}" '
    f'data-track-index="10" data-volume="1" data-audio-group="voiceover"></audio>' for l in T["lines"][:4])

shots_html = "\n".join(
    f'  <div id="{sid}" class="shot">{inner}\n  </div>'
    for sid, a, b_, inner in SHOTS)

(P / "v3-demo/index.html").write_text(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=1080, height=1920" />
  <title>CatchTheError — Case 021 v3 look demo</title>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
  <style>
    @font-face {{ font-family: "Inter"; font-weight: 100 900; font-display: block; src: url("assets/fonts/Inter.ttf") format("truetype"); }}
    @font-face {{ font-family: "Instrument Serif"; font-style: italic; font-weight: 400; font-display: block; src: url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2"); }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #e7e7e5; }}
    #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #e7e7e5; font-family: "Inter", sans-serif; color: #141414; }}
    .shot {{ position: absolute; inset: 0; overflow: hidden; visibility: hidden; }}
    .bleed, .plate {{ position: absolute; inset: 0; overflow: hidden; }}
    .plate {{ filter: blur(26px) brightness(0.72) saturate(1.1); transform: scale(1.12); }}
    .photo {{ position: absolute; overflow: hidden; background: #fff; border: 6px solid #1b1b1b; border-radius: 26px; box-shadow: 14px 16px 0 rgba(0, 0, 0, 0.28), 0 40px 90px rgba(0, 0, 0, 0.35); }}
    /* the keyword label: a strip of the logo's paper, slapped on the footage */
    .lab {{ position: absolute; left: 56px; max-width: 880px; padding: 16px 34px 26px; background: #e7e7e5 url("assets/logo/paper-1080x1920.png") 0 0 / 1080px 1920px;
           font-weight: 800; font-size: 124px; letter-spacing: -0.055em; line-height: 0.95; color: #141414; transform: rotate(-2deg); transform-origin: 0 50%;
           box-shadow: 10px 12px 0 rgba(0, 0, 0, 0.32); }}
    .it {{ position: relative; display: inline-block; font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; color: #dd483f; letter-spacing: -0.01em; font-size: 1.14em; line-height: 0.8; padding-right: 0.06em; }}
    .ul {{ position: absolute; left: -2%; bottom: -0.14em; width: 104%; height: 0.3em; overflow: visible; }}
    .ul path, .pen path {{ fill: none; stroke: #dd483f; stroke-width: 8; stroke-linecap: round; stroke-dasharray: 1; stroke-dashoffset: 1; }}
    .pen {{ position: absolute; overflow: visible; }}
    #grain {{ position: absolute; inset: 0; background: url("assets/logo/paper-1080x1920.png") 0 0 / 1080px 1920px; mix-blend-mode: multiply; opacity: 0.22; pointer-events: none; z-index: 40; }}
  </style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
{shots_html}
  <div id="grain"></div>
{vo}
    <audio id="music" class="clip" src="assets/music/bed.wav" data-start="0" data-duration="{END}" data-track-index="11" data-volume="1" data-audio-group="music"></audio>
{sfx}
</div>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
  {chr(10).join("  " + l for l in js)}
  tl.set({{}}, {{}}, {END});
  window.__timelines["main"] = tl;
</script>
</body>
</html>
""")
print("shots", [(s, a, b_) for s, a, b_, _ in SHOTS])
