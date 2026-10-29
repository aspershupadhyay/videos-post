"""Case 023: writes compositions/s*.html, compositions/captions.html and index.html from assets/vo/timing.json.
Every cut and cue derives from the voice's word times, so a re-voiced line only needs a rerun.

    python3 scripts/build_scenes.py [--no-captions]

Look (fresh for this story, rule 15): the language of the story's own source, Apple's M6 film ("Everyday tasks. No sweat."):
real footage inside angled shards on black that morph from cut to cut, a world that breaks into pieces, and type that sits
beside the shard. Ours on top: black #0A0A0A, Inter 800, the red pen #DD483F as the one accent (the asterisk, the ring
round the fine print, the dot that turns 13 into 1.3), the paper cover for frame 0 (it breaks into two shards) and the
paper end card with the logo sting. Captions on (rule 16: 2-3 words, Inter 700 44 px, dark chip, y 1400).
"""
import json
import re
import sys
from pathlib import Path

P = Path(__file__).resolve().parent.parent
T = json.loads((P / "assets/vo/timing.json").read_text())
L = {l["id"]: l for l in T["lines"]}
CAPTIONS = "--no-captions" not in sys.argv
INK, RED = "#f4f2ee", "#dd483f"


def w(vid, word, n=1):
    """Start time of the n-th occurrence of a word in a line (case-insensitive, punctuation ignored)."""
    alts = word.lower().split("|")
    hits = [s for ww, s, e in L[vid]["words"] if re.sub(r"[^\w]", "", ww).lower() in alts]
    return hits[n - 1]


BASE = """
    @font-face { font-family: "Inter"; font-weight: 100 900; font-display: block; src: url("assets/fonts/Inter.ttf") format("truetype"); }
    @font-face { font-family: "Instrument Serif"; font-style: italic; font-weight: 400; font-display: block; src: url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2"); }
    @font-face { font-family: "Courier Prime"; font-weight: 700; font-display: block; src: url("assets/fonts/CourierPrime-Bold.ttf") format("truetype"); }
    #root { position: absolute; inset: 0; overflow: hidden; background: #0a0a0a; color: #f4f2ee; font-family: "Inter", sans-serif; }
    .h { position: absolute; left: 76px; width: 930px; font-weight: 800; font-size: 118px; letter-spacing: -0.055em; line-height: 0.93; }
    .it { position: relative; display: inline-block; font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; color: #dd483f; letter-spacing: -0.01em; font-size: 1.12em; line-height: 0.8; padding-right: 0.06em; }
    .ul { position: absolute; left: -2%; bottom: -0.16em; width: 104%; height: 0.3em; overflow: visible; }
    .ul path { fill: none; stroke: #dd483f; stroke-width: 7; stroke-linecap: round; stroke-dasharray: 1400; stroke-dashoffset: 1400; }
    .mono { position: absolute; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.14em; text-transform: uppercase; color: #9a9a96; white-space: nowrap; }
    .row { position: absolute; left: 0; width: 1080px; text-align: center; }
    .pen { position: absolute; overflow: visible; }
    .pen path { fill: none; stroke: #dd483f; stroke-width: 8; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1400; stroke-dashoffset: 1400; }
    .shard { position: absolute; inset: 0; overflow: hidden; }
    .shard video, .shard img.fill { position: absolute; display: block; }
    .chip { position: absolute; padding: 10px 20px 12px; border-radius: 12px; background: rgba(10, 10, 10, 0.78); font-weight: 800; font-size: 44px; letter-spacing: -0.03em; white-space: nowrap; }
    .photo { position: absolute; overflow: hidden; border: 6px solid #f4f2ee; border-radius: 22px; background: #000; box-shadow: 0 40px 90px rgba(0, 0, 0, 0.6); }
    .photo img { position: absolute; left: 0; top: 0; display: block; }
"""


def scene(sid, start, end, css, body, js):
    dur = round(end - start, 3)
    html = f"""<template>
  <style>{BASE}{css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1080" data-height="1920">
{body}
  </div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      const at = (abs) => Math.max(0, abs - {start});
      const rise = (sel, t, d = 0.45) => tl.fromTo(sel, {{ opacity: 0, y: 50 }}, {{ opacity: 1, y: 0, duration: d, ease: "expo.out", immediateRender: false }}, at(t));
      const pen = (sel, t, d = 0.36) => tl.to(sel, {{ strokeDashoffset: 0, duration: d, ease: "power2.inOut" }}, at(t));
      const ring = (sel, t, d = 0.5) => tl.to(sel, {{ "--p": 360, duration: d, ease: "power2.inOut" }}, at(t));
      const shape = (sel, poly, t, d = 0.3) => tl.to(sel, {{ clipPath: poly, duration: d, ease: "power3.inOut" }}, at(t));
{js}
      tl.set({{}}, {{}}, {dur});
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    (P / f"compositions/{sid}.html").write_text(html)
    return (sid, start, dur)


def it(id_, text):
    """The one red serif-italic word, with the pen underline inside it (dash 1400 screen px, drawn by pen()).
    pathLength + non-scaling-stroke draws dashed in Chrome, so the dash is in screen px instead."""
    return (f'<span class="it" id="{id_}">{text}<svg class="ul" viewBox="0 0 100 20" preserveAspectRatio="none" aria-hidden="true">'
            f'<path vector-effect="non-scaling-stroke" d="M2 12 C 30 7, 66 11, 98 5" /></svg></span>')


def underline(id_, x, y, wdt, sw=8):
    return (f'<svg id="{id_}" class="pen" style="left:{x}px;top:{y}px;width:{wdt}px;height:24px" viewBox="0 0 100 20" preserveAspectRatio="none">'
            f'<path vector-effect="non-scaling-stroke" style="stroke-width:{sw}" d="M1 11 C 30 7, 64 13, 99 7" /></svg>')


def ring_img(id_, left, top, width, height, start_deg=340):
    """The logo's own hand-drawn pen circle, stretched round a target and drawn on with a conic mask."""
    m = f"conic-gradient(from {start_deg}deg at 50% 50%, #000 calc(var(--p) * 1deg), transparent calc(var(--p) * 1deg))"
    return (f'<div id="{id_}" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{height}px;--p:0;'
            f'-webkit-mask-image:{m};mask-image:{m}">'
            f'<img src="assets/logo/circle-crop.png" alt="" style="position:absolute;left:0;top:0;width:100%;height:100%" /></div>')


def poly(*pts):
    """Polygon in frame px (1080x1920) -> clip-path string. All shards use 4 points so GSAP can morph between them."""
    return "polygon(" + ", ".join(f"{x}px {y}px" for x, y in pts) + ")"


def vid(id_, src, start, dur, box, media_start=0.0):
    """A muted clip at local time `start` inside a shard; box = (left, top, width, height)."""
    l, t, wd, ht = box
    ms = f' data-media-start="{media_start}"' if media_start else ""
    return (f'<video id="{id_}" class="clip" src="assets/clips/{src}" data-start="{start:.3f}" data-duration="{dur:.3f}"{ms} '
            f'muted playsinline style="left:{l}px;top:{t}px;width:{wd}px;height:{ht}px;object-fit:cover"></video>')


WORDMARK = ('<div id="{id}" style="position:absolute;left:0;top:{top}px;width:1080px;text-align:center;font-family:\'Courier Prime\',monospace;'
            'font-weight:700;font-size:46px;letter-spacing:0.3em;color:#3f3f3d">CATCH · THE · <span style="position:relative;display:inline-block;'
            'color:#dd483f">E<img src="assets/logo/circle-crop.png" alt="" style="position:absolute;left:-0.44em;top:-0.36em;width:1.75em;'
            'height:1.6em" /></span>RROR</div>')

S = []
cut = lambda vid_: round(L[vid_]["start"] - 0.2, 2)
FILM = T["film"]
b = [0.0] + [cut(f"vo-{i:02d}") for i in range(2, 11)] + [FILM]

# the ad's last frame (1920x1080) shown 1080 wide; its fine print sits at source y 964-1026, x 233-1684
AD_K = 988 / 1920                     # shown as a printed frame: 1000 px card, 6 px white border
AD_TOP = 560
FP = (233 * AD_K, AD_TOP + 964 * AD_K, 1684 * AD_K, AD_TOP + 1026 * AD_K)   # fine print box in frame px
FP_CX, FP_CY = (FP[0] + FP[2]) / 2, (FP[1] + FP[3]) / 2

# S1 hook. Frame 0 = the cover; it breaks into two shards and falls away from Apple's own "13X" shot. ----------------
s, e = b[0], b[1]
t_go = 0.36
VK = 1135 / 1920                       # the ad's frame at 1135 px wide: "UP TO 13X FASTER AI PERFORMANCE" fits the width
VL, VT = round((1080 - 1135) / 2), 560
COVER_A = poly((0, 0), (1080, 0), (1080, 700), (0, 1060))
COVER_B = poly((0, 1060), (1080, 700), (1080, 1920), (0, 1920))
S.append(scene("s1", s, e, f"""
    #s1-cov-a, #s1-cov-b {{ background: url("assets/shots/cover.png") 0 0 / 1080px 1920px; z-index: 5; }}
    #s1-cov-a {{ clip-path: {COVER_A}; }}
    #s1-cov-b {{ clip-path: {COVER_B}; }}
    #s1-star {{ position: absolute; left: {VL + round(722 * VK)}px; top: {VT + round(640 * VK)}px; font-family: "Instrument Serif", serif; font-style: italic; font-size: 150px; line-height: 1; color: {RED}; opacity: 0; }}""", f"""
    <div id="s1-world" class="shard">
      {vid("s1-v", "x13.mp4", 0, min(4.1, e - s), (VL, VT, 1135, 639))}
      <div id="s1-star">*</div>
    </div>
    <div id="s1-cov-a" class="shard"></div>
    <div id="s1-cov-b" class="shard"></div>""", f"""
      // the cover cracks along a diagonal and the two halves fall out of frame (the M6 film's shard break)
      tl.to("#s1-cov-a", {{ x: -180, y: -1300, rotation: -9, duration: 0.62, ease: "power3.in" }}, {t_go});
      tl.to("#s1-cov-b", {{ x: 220, y: 1500, rotation: 7, duration: 0.62, ease: "power3.in" }}, {t_go + 0.04});
      tl.fromTo("#s1-world", {{ scale: 1.18 }}, {{ scale: 1, duration: 0.9, ease: "expo.out" }}, {t_go + 0.1});
      tl.fromTo("#s1-world", {{ scale: 1 }}, {{ scale: 1.1, duration: {e - s - t_go - 1.0:.2f}, ease: "sine.inOut", transformOrigin: "300px 1080px", immediateRender: false }}, {t_go + 1.0});
      // "...at A.I." -> the red asterisk: there's fine print
      tl.fromTo("#s1-star", {{ opacity: 0, scale: 2.2, rotation: -40 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2.5)", immediateRender: false }}, at({w('vo-01', 'ai')}));"""))

# S2 loop: the ad flashes past in morphing shards, then lands on its last frame; the pen rings the grey line. ------
s, e = b[1], b[2]
t_tiny, t_grey, t_last = w("vo-02", "tiny"), w("vo-02", "gray|grey"), w("vo-02", "last")
VB = (-314, 480, 1707, 960)            # a 16:9 clip filling the shard's band
SH = [poly((60, 520), (1020, 610), (980, 1330), (110, 1240)),
      poly((0, 640), (1080, 470), (1080, 1180), (0, 1380)),
      poly((200, 480), (1080, 760), (880, 1380), (0, 1100))]
t0, t1 = 0.0, (t_tiny - s) / 2
S.append(scene("s2", s, e, f"""
    #s2-sh {{ clip-path: {SH[0]}; }}
    #s2-end {{ position: absolute; left: 40px; top: {AD_TOP}px; width: 1000px; height: 568px; opacity: 0; border: 6px solid #f4f2ee; border-radius: 22px; box-shadow: 0 40px 90px rgba(0, 0, 0, 0.6); }}
    #s2-end img {{ position: absolute; left: 0; top: 0; width: 988px; height: 556px; border-radius: 16px; }}
    #s2-lab {{ top: 420px; opacity: 0; }}""", f"""
    <div id="s2-sh" class="shard">
      {vid("s2-va", "title.mp4", t0, t1, VB, 0.3)}
      {vid("s2-vb", "carry.mp4", t1, t_tiny - s - t1 + 0.05, VB)}
    </div>
    <div id="s2-end">
      <img src="assets/shots/ad-45.png" alt="The last frame of Apple's M6 ad: the Apple logo and two lines of grey fine print" />
      {ring_img("s2-ring", round(FP[0]) - 46, round(FP[1] - AD_TOP) - 40, round(FP[2] - FP[0]) + 92, round(FP[3] - FP[1]) + 80)}
    </div>
    <div id="s2-lab" class="mono row">The ad's last frame</div>""", f"""
      tl.fromTo("#s2-sh", {{ scale: 0.92, rotation: -3 }}, {{ scale: 1, rotation: 0, duration: 0.5, ease: "expo.out" }}, 0);
      shape("#s2-sh", "{SH[1]}", {t1 - 0.12:.2f}, 0.24);
      shape("#s2-sh", "{SH[2]}", {t_tiny - s - 0.3:.2f}, 0.22);
      // "tiny grey text": hard cut to the last frame, the shard snaps shut
      tl.to("#s2-sh", {{ opacity: 0, duration: 0.06 }}, at({t_tiny - 0.06}));
      tl.fromTo("#s2-end", {{ opacity: 0, scale: 1.06 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "expo.out", immediateRender: false }}, at({t_tiny - 0.04}));
      ring("#s2-ring", {t_grey + 0.05:.2f}, 0.5);
      rise("#s2-lab", {t_last - 0.1:.2f}, 0.35);
      // zoom through the fine print into the next shot
      tl.to("#s2-end", {{ scale: 5, duration: 0.42, ease: "power3.in", transformOrigin: "{FP_CX:.0f}px {FP_CY - AD_TOP:.0f}px" }}, {e - s - 0.42:.2f});
      tl.to("#s2-lab", {{ opacity: 0, duration: 0.2 }}, {e - s - 0.42:.2f});"""))

# S3 the fine print, read out: the ad's own grey pixels, lifted to white as the voice reads them; the pen under "M1". ----
s, e = b[2], b[3]
FK = 1.9                              # crops were enlarged 1.9x from the 1920 frame (scripts note in SPEC.md)
fa_y, fb_y = 650, 760
t_mac, t_with, t_m1 = w("vo-03", "macbook"), w("vo-03", "with"), w("vo-03", "m1")
m1x0, m1x1 = round((1025 - 718) * FK), round((1131 - 718) * FK)       # "with M1." inside the second crop
S.append(scene("s3", s, e, f"""
    #s3-all {{ position: absolute; inset: 0; }}
    .fp {{ position: absolute; left: 70px; }}
    .fp img {{ position: absolute; left: 0; top: 0; display: block; }}
    .fp .hi {{ clip-path: inset(0 100% 0 0); }}
    #s3-lab {{ top: 540px; }}""", f"""
    <div id="s3-all">
      <div id="s3-lab" class="mono row">Apple's fine print</div>
      <div class="fp" style="top:{fa_y}px;width:939px;height:76px"><img src="assets/shots/fp-a.png" alt="" style="width:939px;height:76px" />
        <img id="s3-ha" class="hi" src="assets/shots/fp-a-hi.png" data-text-px="30" alt="Performance testing against specific" style="width:939px;height:76px" /></div>
      <div class="fp" style="top:{fb_y}px;width:802px;height:76px"><img src="assets/shots/fp-b.png" alt="" style="width:802px;height:76px" />
        <img id="s3-hb" class="hi" src="assets/shots/fp-b-hi.png" data-text-px="30" alt="MacBook Pro systems with M1." style="width:802px;height:76px" /></div>
      {underline("s3-ul", 70 + m1x0 - 4, fb_y + 70, m1x1 - m1x0 + 8)}
    </div>""", f"""
      tl.fromTo("#s3-all", {{ scale: 1.45, opacity: 0.85 }}, {{ scale: 1, opacity: 1, duration: 0.55, ease: "expo.out", transformOrigin: "540px 740px" }}, 0);
      tl.fromTo("#s3-all", {{ scale: 1 }}, {{ scale: 1.1, duration: {e - s - 0.55:.2f}, ease: "none", transformOrigin: "{70 + m1x0}px 800px", immediateRender: false }}, 0.55);
      tl.to("#s3-ha", {{ clipPath: "inset(0 0% 0 0)", duration: {t_mac - L['vo-03']['start']:.2f}, ease: "none" }}, at({L['vo-03']['start']}));
      tl.to("#s3-hb", {{ clipPath: "inset(0 0% 0 0)", duration: {t_m1 + 0.3 - t_mac:.2f}, ease: "none" }}, at({t_mac}));
      pen("#s3-ul path", {t_m1 + 0.05:.2f}, 0.35);"""))

# S4 "M1. That's a laptop from 2020." The M1 MacBook Pro in Apple's own 2020 photo, as a printed photo. -------------------
s, e = b[3], b[4]
t_lap, t_2020 = w("vo-04", "laptop"), w("vo-04", "2020")
S.append(scene("s4", s, e, f"""
    #s4-m1 {{ position: absolute; left: 76px; top: 300px; font-weight: 800; font-size: 330px; letter-spacing: -0.06em; line-height: 0.9; }}
    #s4-yr {{ position: absolute; left: 600px; top: 388px; font-family: "Instrument Serif", serif; font-style: italic; font-size: 230px; line-height: 0.9; color: {RED}; opacity: 0; }}
    #s4-ph {{ left: 90px; top: 780px; width: 900px; height: 518px; }}
    #s4-ph img {{ width: 888px; height: 506px; }}""", f"""
    <div id="s4-m1">M1</div>
    <div id="s4-yr">2020{underline("s4-yu", 0, 205, 380)}</div>
    <div id="s4-ph" class="photo"><img src="assets/shots/m1-2020.jpg" alt="Apple's November 2020 press photo of the 13-inch MacBook Pro with M1" /></div>""", f"""
      tl.fromTo("#s4-m1", {{ scale: 1.6, opacity: 0.85 }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "expo.out", transformOrigin: "200px 450px" }}, 0);
      tl.fromTo("#s4-m1", {{ x: 0 }}, {{ x: 20, duration: {e - s - 0.5:.2f}, ease: "none", immediateRender: false }}, 0.5);
      tl.fromTo("#s4-ph", {{ opacity: 1, y: 1200, rotation: -11 }}, {{ opacity: 1, y: 0, rotation: -3, duration: 0.6, ease: "expo.out", immediateRender: false }}, at({t_lap - 0.35:.2f}));
      tl.set("#s4-ph", {{ y: 1200 }}, 0);
      tl.fromTo("#s4-ph img", {{ scale: 1.12 }}, {{ scale: 1, duration: 1.6, ease: "sine.out", immediateRender: false }}, at({t_lap - 0.35:.2f}));
      tl.fromTo("#s4-yr", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "expo.out", immediateRender: false }}, at({t_2020 - 0.05:.2f}));
      pen("#s4-yu path", {t_2020 + 0.3:.2f}, 0.35);"""))

# S5 "Against last year's M5? ... 1.3 times." Apple's own newsroom line; a red dot drops into 13 and makes it 1.3. -------
s, e = b[4], b[5]
t_m5, t_one, t_pt = w("vo-05", "m5"), w("vo-05", "1"), w("vo-05", "3")
BJ = json.loads((P / "assets/shots/nr-bullet.json").read_text())
CW, PAD = 880, 34
BK = (CW - 2 * PAD) / 1038                    # bullet.png is 1038 px wide (400 css x3 + 8 px pad)
CT = 790


def hl(id_, phrase, card_top=CT, extra=""):
    """A full-brightness copy of the card's image, clipped to a phrase's line boxes (the rest of the card is dimmed)."""
    rects = BJ["boxes"][phrase]
    parts = []
    for x, y, wd, ht in rects:
        x0, y0 = (x + 8) * 3 * BK - 6, (y + 8) * 3 * BK - 4
        x1, y1 = (x + wd + 8) * 3 * BK + 6, (y + ht + 8) * 3 * BK + 6
        parts.append((x0, y0, x1, y1))
    clip = " ".join(f"M{x0:.0f} {y0:.0f}H{x1:.0f}V{y1:.0f}H{x0:.0f}Z" for x0, y0, x1, y1 in parts)
    return (f'<img id="{id_}" src="assets/shots/nr-bullet.png" alt="" style="position:absolute;left:{PAD}px;top:{PAD}px;width:{CW - 2 * PAD}px;'
            f'height:{round(423 * BK)}px;clip-path:path(\'{clip}\');opacity:0{extra}" />'), parts


hl_m5, m5_parts = hl("s5-h1", "14-inch MacBook Pro with M5")
hl_13, x13_parts = hl("s5-h2", "up to 1.3x faster")
u0, uy, u1 = x13_parts[0][0], x13_parts[0][3], x13_parts[0][2]
S.append(scene("s5", s, e, f"""
    #s5-n {{ top: 300px; font-weight: 800; font-size: 330px; letter-spacing: -0.06em; line-height: 0.9; }}
    #s5-n span {{ display: inline-block; }}
    #s5-dot {{ position: absolute; left: 0; top: 0; width: 64px; height: 64px; border-radius: 50%; background: {RED}; opacity: 0; }}
    #s5-card {{ position: absolute; left: 76px; top: {CT}px; width: {CW}px; height: {round(423 * BK) + 2 * PAD}px; border-radius: 26px; background: #000; border: 2px solid #262624; overflow: visible; }}
    #s5-base {{ position: absolute; left: {PAD}px; top: {PAD}px; width: {CW - 2 * PAD}px; height: {round(423 * BK)}px; }}""", f"""
    <div id="s5-n" class="row"><span id="s5-1">1</span><span id="s5-3">3×</span></div>
    <div id="s5-dot"></div>
    <div id="s5-card">
      <img id="s5-base" src="assets/shots/nr-bullet.png" data-text-px="37" alt="Apple Newsroom: Up to 13x faster time to first token performance for LLM prompt processing compared to the 13-inch MacBook Pro with M1, and up to 1.3x faster than the 14-inch MacBook Pro with M5." />
      {hl_m5}
      {hl_13}
      {underline("s5-ul", PAD + u0, PAD + uy + 2, u1 - u0)}
    </div>""", f"""
      tl.fromTo("#s5-n", {{ scale: 0.9, opacity: 0.85 }}, {{ scale: 1, opacity: 1, duration: 0.5, ease: "expo.out" }}, 0);
      tl.fromTo("#s5-card", {{ y: 700 }}, {{ y: 0, duration: 0.55, ease: "expo.out" }}, 0.05);
      // "last year's M5": the card dims to the M5 line
      tl.to("#s5-base", {{ opacity: 0.22, duration: 0.3 }}, at({t_m5 - 0.1:.2f}));
      tl.to("#s5-h1", {{ opacity: 1, duration: 0.2 }}, at({t_m5 - 0.1:.2f}));
      // "1 . 3": the digits part, a red dot falls into the gap (the logo's falling dot), 13x becomes 1.3x
      tl.to("#s5-1", {{ x: -46, duration: 0.25, ease: "power3.out" }}, at({t_one:.2f}));
      tl.to("#s5-3", {{ x: 58, duration: 0.25, ease: "power3.out" }}, at({t_one:.2f}));
      tl.fromTo("#s5-dot", {{ opacity: 1, x: DOT_X, y: -120 }}, {{ opacity: 1, x: DOT_X, y: DOT_Y, duration: 0.42, ease: "bounce.out", immediateRender: false }}, at({t_one + 0.06:.2f}));
      tl.to("#s5-h2", {{ opacity: 1, duration: 0.2 }}, at({t_pt:.2f}));
      pen("#s5-ul path", {t_pt + 0.2:.2f}, 0.35);
      tl.fromTo("#s5-n", {{ scale: 1 }}, {{ scale: 1.06, duration: {e - t_pt:.2f}, ease: "sine.out", transformOrigin: "540px 0px", immediateRender: false }}, at({t_pt:.2f}));""".replace("DOT_X", "DOT_X_PX").replace("DOT_Y", "DOT_Y_PX")))

# S6 "What got 13x faster? The wait before the A.I. starts answering." Apple's own words + Apple's own A.I. UI. ----------
s, e = b[5], b[6]
t_wait, t_ans = w("vo-06", "wait"), w("vo-06", "answering")
LK = 1000 / 1038
ttft0, ttft1 = (125.56 + 8) * 3 * LK, (125.56 + 134.42 + 8) * 3 * LK
SH6 = [poly((40, 540), (1040, 600), (1040, 1150), (40, 1110)), poly((40, 600), (1040, 540), (1040, 1110), (40, 1150))]
ai_start = t_ans + 0.2 - 1.51 - s              # Apple's suggestion text (source 13.63 s, slowed 2.6x) lands just after "answering"
S.append(scene("s6", s, e, f"""
    #s6-line {{ position: absolute; left: 40px; top: 300px; width: 1000px; height: {round(96 * LK)}px; }}
    #s6-line img {{ position: absolute; left: 0; top: 0; width: 1000px; height: {round(96 * LK)}px; }}
    #s6-sh {{ clip-path: {SH6[0]}; }}
    #s6-lab {{ left: 60px; top: 1194px; }}
    #s6-bar {{ position: absolute; left: 60px; top: 1260px; width: 960px; height: 14px; border-radius: 7px; background: #262624; }}
    #s6-fill {{ position: absolute; left: 0; top: 0; width: 960px; height: 14px; border-radius: 7px; background: {RED}; transform-origin: 0 50%; transform: scaleX(0); }}""", f"""
    <div id="s6-line"><img src="assets/shots/nr-line1.png" data-text-px="37" alt="Apple Newsroom: Up to 13x faster time to first token" />
      {underline("s6-ul", round(ttft0), 66, round(ttft1 - ttft0))}</div>
    <div id="s6-sh" class="shard">
      {vid("s6-va", "x13.mp4", 0, ai_start + 0.04, (-180, 540, 1440, 810), 1.2)}
      {vid("s6-vb", "ai.mp4", ai_start, e - s - ai_start, (-560, 270, 1600, 900))}
    </div>
    <div id="s6-lab" class="mono">Time to first token</div>
    <div id="s6-bar"><div id="s6-fill"></div></div>""", f"""
      tl.fromTo("#s6-line", {{ y: -40, opacity: 0.85 }}, {{ y: 0, opacity: 1, duration: 0.45, ease: "expo.out" }}, 0);
      tl.fromTo("#s6-sh", {{ x: 1080 }}, {{ x: 0, duration: 0.5, ease: "expo.out" }}, 0);
      pen("#s6-ul path", {w('vo-06', 'faster') - 0.1:.2f}, 0.4);
      shape("#s6-sh", "{SH6[1]}", {ai_start - 0.12:.2f}, 0.28);
      // the wait: the bar runs from "wait" until Apple's A.I. starts answering
      tl.to("#s6-fill", {{ scaleX: 0.42, duration: {t_ans - t_wait:.2f}, ease: "none" }}, at({t_wait:.2f}));
      tl.fromTo("#s6-bar", {{ scaleY: 1 }}, {{ keyframes: [{{ scaleY: 2, duration: 0.08 }}, {{ scaleY: 1, duration: 0.2 }}], immediateRender: false }}, at({t_ans:.2f}));"""))

# S7 "Not the whole answer. Just how fast it starts." An answer streams in; only its first token was timed. --------------
s, e = b[6], b[7]
t_whole, t_just, t_starts = w("vo-07", "whole"), w("vo-07", "just"), w("vo-07", "starts")
ROWS = [[100, 178, 82, 212, 136], [162, 102, 221, 119, 128], [196, 83, 153, 178, 102], [128, 221, 94, 162], [178, 110]]
pills, i = [], 0
for r, row in enumerate(ROWS):
    x = 0
    for wd in row:
        pills.append(f'<span id="s7-p{i}" class="pill" style="left:{x}px;top:{r * 74}px;width:{wd}px"></span>')
        x += wd + 18
        i += 1
NP = i
S.append(scene("s7", s, e, f"""
    #s7-card {{ position: absolute; left: 70px; top: 560px; width: 940px; height: 500px; border-radius: 30px; background: #141413; border: 2px solid #262624; }}
    #s7-tok {{ position: absolute; left: 48px; top: 60px; }}
    .pill {{ position: absolute; height: 40px; border-radius: 20px; background: #5a5a57; opacity: 0; }}
    #s7-a {{ top: 470px; }}
    #s7-b {{ top: 1110px; color: {RED}; opacity: 0; }}""", f"""
    <div id="s7-a" class="mono row">The whole answer: not timed</div>
    <div id="s7-card"><div id="s7-tok">{"".join(pills)}</div>
      {ring_img("s7-ring", 14, 28, 170, 104)}</div>
    <div id="s7-b" class="mono row">First token: the 13× part</div>""", f"""
      tl.fromTo("#s7-card", {{ y: 80, scale: 0.94, opacity: 0.85 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.5, ease: "expo.out" }}, 0);
      // the answer streams in, token by token
      tl.to(".pill", {{ opacity: 1, duration: 0.05, stagger: {(t_just - 0.25 - s - 0.1) / NP:.3f} }}, 0.1);
      tl.fromTo("#s7-a", {{ opacity: 0.85 }}, {{ opacity: 1, duration: 0.2 }}, 0);
      // "just how fast it starts": the first token goes red, the rest of the answer fades
      tl.to("#s7-p0", {{ backgroundColor: "{RED}", duration: 0.12 }}, at({t_just:.2f}));
      tl.to(".pill:not(#s7-p0)", {{ opacity: 0.55, duration: 0.3 }}, at({t_just:.2f}));
      ring("#s7-ring", {t_just + 0.25:.2f}, 0.45);
      rise("#s7-b", {t_just + 0.3:.2f}, 0.35);
      tl.fromTo("#s7-card", {{ scale: 1 }}, {{ scale: 1.08, duration: {e - t_just:.2f}, ease: "sine.inOut", transformOrigin: "100px 100px", immediateRender: false }}, at({t_just:.2f}));"""))

# S8 the take: two shards, the M1 owner and the M5 owner. ---------------------------------------------------------------
s, e = b[7], b[8]
t_real, t_bought, t_keep = w("vo-08", "real"), w("vo-08", "bought"), w("vo-08", "keep")
TOP_SH = poly((0, 250), (1080, 250), (1080, 610), (0, 700))
BOT_SH = poly((0, 930), (1080, 870), (1080, 1180), (0, 1180))
S.append(scene("s8", s, e, f"""
    #s8-a {{ clip-path: {TOP_SH}; }}
    #s8-b {{ clip-path: {BOT_SH}; }}
    #s8-l1 {{ left: 60px; top: 276px; }}
    #s8-l2 {{ left: 60px; top: 960px; }}
    #s8-t1 {{ top: 735px; font-size: 96px; opacity: 0; }}
    #s8-t2 {{ top: 1212px; font-size: 96px; opacity: 0; }}""", f"""
    <div id="s8-a" class="shard"><img class="fill" src="assets/shots/m1-2020.jpg" alt="Apple's 2020 photo of the 13-inch MacBook Pro with M1" style="left:-40px;top:200px;width:1160px;height:652px" /></div>
    <div id="s8-b" class="shard">{vid("s8-v", "funnel.mp4", t_bought - s - 0.3, e - (t_bought - 0.3), (-280, 700, 1640, 922))}</div>
    <div id="s8-l1" class="chip">M1 → M6</div>
    <div id="s8-l2" class="chip" style="opacity:0">M5 → M6</div>
    <div id="s8-t1" class="h">Real upgrade.</div>
    <div id="s8-t2" class="h">Keep your {it("s8-it", "money.")}</div>""", f"""
      tl.fromTo("#s8-a", {{ x: -1080 }}, {{ x: 0, duration: 0.5, ease: "expo.out" }}, 0);
      tl.fromTo("#s8-l1", {{ x: -500 }}, {{ x: 0, duration: 0.5, ease: "expo.out" }}, 0.08);
      tl.fromTo("#s8-a img", {{ scale: 1.15 }}, {{ scale: 1, duration: {e - s:.2f}, ease: "sine.out" }}, 0);
      rise("#s8-t1", {t_real - 0.1:.2f}, 0.4);
      tl.fromTo("#s8-b", {{ x: 1080 }}, {{ x: 0, duration: 0.5, ease: "expo.out", immediateRender: false }}, at({t_bought - 0.3:.2f}));
      tl.set("#s8-b", {{ x: 1080 }}, 0);
      tl.fromTo("#s8-l2", {{ opacity: 1, x: 500 }}, {{ opacity: 1, x: 0, duration: 0.5, ease: "expo.out", immediateRender: false }}, at({t_bought - 0.22:.2f}));
      tl.to("#s8-a", {{ opacity: 0.45, duration: 0.3 }}, at({t_bought - 0.3:.2f}));
      tl.to(["#s8-t1", "#s8-l1"], {{ opacity: 0.45, duration: 0.3 }}, at({t_bought - 0.3:.2f}));
      rise("#s8-t2", {t_keep - 0.1:.2f}, 0.4);
      pen("#s8-it path", {w('vo-08', 'money') + 0.25:.2f}, 0.35);"""))

# S9 the line: the ad races past in shards, then the last frame again, and the pen rings the grey line. ----------------
s, e = b[8], b[9]
t_ans9, t_last9 = w("vo-09", "the", 1), w("vo-09", "last")
seg = (t_ans9 - s - 0.05) / 4
SH9 = [poly((120, 560), (1000, 500), (1040, 1180), (60, 1260)), poly((0, 700), (1080, 520), (900, 1300), (160, 1180)),
       poly((60, 480), (900, 640), (1080, 1240), (0, 1100)), poly((200, 520), (1080, 600), (880, 1280), (0, 1220))]
clips9 = [("x13.mp4", 1.6), ("title.mp4", 0.5), ("carry.mp4", 0.0), ("spin.mp4", 0.2)]
S.append(scene("s9", s, e, f"""
    #s9-sh {{ clip-path: {SH9[0]}; }}
    #s9-end {{ position: absolute; left: 40px; top: {AD_TOP}px; width: 1000px; height: 568px; opacity: 0; border: 6px solid #f4f2ee; border-radius: 22px; box-shadow: 0 40px 90px rgba(0, 0, 0, 0.6); }}
    #s9-end img {{ position: absolute; left: 0; top: 0; width: 988px; height: 556px; border-radius: 16px; }}""", f"""
    <div id="s9-sh" class="shard">
      {"".join(vid(f"s9-v{k}", src, k * seg, seg + 0.04, VB, ms) for k, (src, ms) in enumerate(clips9))}
    </div>
    <div id="s9-end">
      <img src="assets/shots/ad-45.png" alt="The last frame of Apple's M6 ad" />
      {ring_img("s9-ring", round(FP[0]) - 46, round(FP[1] - AD_TOP) - 40, round(FP[2] - FP[0]) + 92, round(FP[3] - FP[1]) + 80)}
    </div>""", f"""
      tl.fromTo("#s9-sh", {{ scale: 1.1 }}, {{ scale: 1, duration: 0.4, ease: "expo.out" }}, 0);
      {"".join(f'shape("#s9-sh", "{SH9[k]}", {k * seg - 0.1:.2f}, 0.2);' for k in range(1, 4))}
      tl.to("#s9-sh", {{ opacity: 0, duration: 0.06 }}, at({t_ans9 - 0.06:.2f}));
      tl.fromTo("#s9-end", {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "expo.out", immediateRender: false }}, at({t_ans9 - 0.04:.2f}));
      tl.fromTo("#s9-end", {{ scale: 1 }}, {{ scale: 1.22, duration: {e - t_ans9 - 0.4:.2f}, ease: "sine.inOut", transformOrigin: "{FP_CX:.0f}px {FP_CY - AD_TOP:.0f}px", immediateRender: false }}, at({t_ans9 + 0.36:.2f}));
      ring("#s9-ring", {t_last9:.2f}, 0.5);"""))

# S10 end card on the logo's paper: the spoken ask; the logo sting plays over it -----------------------------------------
s, e = b[9], b[10]
S.append(scene("s10", s, e, f"""
    #root {{ background: #e7e7e5 url("assets/logo/paper-1080x1920.png") 0 0 / 1080px 1920px; color: #141414; }}
    #s10-a, #s10-c {{ position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 72px; letter-spacing: -0.03em; }}
    #s10-c {{ opacity: 0; }}
    #s10-b {{ left: 0; top: 1290px; width: 1080px; text-align: center; opacity: 0; font-size: 28px; letter-spacing: 0.08em; color: #5f5f5c; }}""", f"""
    <div id="s10-a">Seen an ad like this?</div>
    <div id="s10-c">We'll check it.</div>
    <div id="s10-b" class="mono">Send it to @catchtheerror</div>""", f"""
      tl.fromTo("#s10-a", {{ opacity: 0.85, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, 0);
      tl.fromTo("#s10-b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({w('vo-10', 'send'):.2f}));
      tl.to("#s10-a", {{ opacity: 0, duration: 0.12 }}, at({w('vo-10', 'well') - 0.1:.2f}));
      tl.fromTo("#s10-c", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({w('vo-10', 'well'):.2f}));"""))

# the s5 dot's landing spot (between the parted 1 and 3x), measured from a snapshot of s5 (see SPEC.md)
DOT = json.loads((P / "scripts/dot.json").read_text()) if (P / "scripts/dot.json").exists() else {"x": 470, "y": 520}
s5 = (P / "compositions/s5.html").read_text().replace("DOT_X_PX", str(DOT["x"])).replace("DOT_Y_PX", str(DOT["y"]))
(P / "compositions/s5.html").write_text(s5)

# captions: the reference's style, 2-3 words, small, mid-frame, on a dark chip -------------------------------------------
FIX = {"gray": "grey"}
if CAPTIONS:
    groups = []
    for l in T["lines"]:
        cues = json.loads((P / f"assets/vo/raw/subs/{l['take']}.subs.json").read_text())["cues"]
        for c in cues:
            txt = " ".join(FIX.get(t, t) for t in c["text"].split()).strip()
            if txt:
                groups.append((l["start"] + c["s"], min(l["start"] + c["e"], FILM), txt))
    # a caption holds until the next one starts (no flicker in short gaps)
    groups = [(st, (groups[i + 1][0] if i + 1 < len(groups) and groups[i + 1][0] - en < 0.25 else en), txt) for i, (st, en, txt) in enumerate(groups)]
    # nothing over the cover (it leaves at ~0.4-1.0 s): the first groups start at 0.95 s or are dropped
    groups = [(max(st, 0.95), en, txt) for st, en, txt in groups if en > 1.2]
    body = "".join(f'<div id="c{i}" class="cap" style="opacity:0"><span>{txt}</span></div>' for i, (st, en, txt) in enumerate(groups))
    js = "".join(f'tl.set("#c{i}", {{ opacity: 1, visibility: "visible" }}, {st:.3f}); tl.set("#c{i}", {{ opacity: 0, visibility: "hidden" }}, {en:.3f});\n      '
                 for i, (st, en, txt) in enumerate(groups))
    (P / "compositions/captions.html").write_text(f"""<template>
  <style>
    @font-face {{ font-family: "Inter"; font-weight: 100 900; font-display: block; src: url("assets/fonts/Inter.ttf") format("truetype"); }}
    #root {{ position: absolute; inset: 0; overflow: visible; background: transparent; }}
    .cap {{ position: absolute; left: 0; top: 1400px; width: 1080px; text-align: center; }}
    .cap span {{ display: inline-block; padding: 8px 18px 10px; border-radius: 12px; background: rgba(10, 10, 10, 0.72); color: #fff;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 44px; letter-spacing: -0.035em; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{body}</div>
  <script>
    (() => {{
      const tl = gsap.timeline({{ paused: true }});
      {js}tl.set({{}}, {{}}, {FILM});
      window.__timelines["captions"] = tl;
    }})();
  </script>
</template>
""")

# index.html ---------------------------------------------------------------------------------------------------
hosts = "\n".join(
    f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" '
    f'data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {i + 1}"></div>'
    for i, (sid, st, d) in enumerate(S))
sting_at = b[9] + 0.05
hosts += (f'\n      <div id="sting" data-composition-id="logo-sting" data-composition-src="compositions/logo-sting.html" data-start="{sting_at:.2f}" '
          f'data-duration="{FILM - sting_at:.2f}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 50"></div>')
if CAPTIONS:
    hosts += (f'\n      <div id="caps" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" '
              f'data-duration="{b[9]}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 60"></div>')
vo = "\n".join(
    f'      <audio id="{l["id"]}" class="clip" src="assets/vo/{l["id"]}.wav" data-start="{l["start"]}" data-duration="{l["duration"]}" '
    f'data-track-index="10" data-volume="1" data-audio-group="voiceover"></audio>' for l in T["lines"])
old = (P / "index.html").read_text()
sfx = re.search(r"(      <!-- SFX:BEGIN.*?<!-- SFX:END -->)", old, re.S)
sfx = sfx.group(1) if sfx else "      <!-- SFX:BEGIN (generated by scripts/build_sfx.py from scripts/sfx_cues.json) -->\n      <!-- SFX:END -->"
(P / "index.html").write_text(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>CatchTheError — Case 023: Apple's "13x faster" M6, against a 2020 laptop</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0a0a0a; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FILM}" data-width="1080" data-height="1920">
      <!-- Scenes, cut to the narration (SPEC.md); the logo sting plays over the end card. Footage: Apple's M6 MacBook Pro film. -->
{hosts}

      <!-- Voiceover: VoiceBox, trained voice "sparsh" (myvoice); levelled to -14 LUFS (scripts/prep_audio.py). -->
{vo}

      <!-- Music bed: "Voxel Revolution", Kevin MacLeod (incompetech.com), CC BY 4.0; envelope baked in. -->
      <audio id="music" class="clip" src="assets/music/bed.wav" data-start="0" data-duration="{FILM}" data-track-index="11" data-volume="1" data-audio-group="music"></audio>

{sfx}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print("film", FILM, "cuts", b)
