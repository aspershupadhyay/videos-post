"""Case 026: writes compositions/s*.html, compositions/captions.html and index.html from assets/vo/timing.json.
Every cut and cue derives from the voice's word times, so a re-voiced line only needs a rerun.

    python3 scripts/build_scenes.py [--no-captions]

Look (fresh for this story, rule 15), learned from Apple's own touchscreen MacBook Pro film (brand/MOTION.md):
full-bleed 9:16 crops of the 4K film, cut on the word; labels that live in the scene, both ways Apple does it:
  - pinned: "Spin." sits on the display glass and rides it as the camera pulls back (tools/track_plane.py + pin());
  - fixed: the label holds still in one slot while the world moves past it ("Trackpad ✓", "In the panel.").
Ours on top: Inter 800, the red pen #DD483F as the one accent (the 2010 underline, the strike through "doesn't", the
pen along the hinge, the asterisk on "3 pounds", the underline under the fine print), the paper cover for frame 0 (its
printed photo grows into the film) and the paper end card with the logo sting. Captions on (rule 16).
"""
import json
import re
import sys
from pathlib import Path

import numpy as np

P = Path(__file__).resolve().parent.parent
T = json.loads((P / "assets/vo/timing.json").read_text())
L = {l["id"]: l for l in T["lines"]}
SHOTS = json.loads((P / "assets/clips/shots.json").read_text())
CAPTIONS = "--no-captions" not in sys.argv
RED = "#dd483f"
K = 1080 / 607.5          # source px (1920-wide) -> frame px; the 9:16 window is 607.5 source px wide


def w(vid, word, n=1):
    """Start time of the n-th occurrence of a word in a line (case-insensitive, punctuation ignored)."""
    alts = word.lower().split("|")
    hits = [s for ww, s, e in L[vid]["words"] if re.sub(r"[^\w]", "", ww).lower() in alts]
    return hits[n - 1]


def src2out(shot, x, y):
    return ((x - (SHOTS[shot]["cx"] - 303.75)) * K, y * K)


def track(shot):
    """The tracked surface of a shot as per-frame CSS matrix3d strings in frame px (H in source px -> A H A^-1)."""
    tr = json.loads((P / f"assets/track/{shot}.json").read_text())
    ox = SHOTS[shot]["cx"] - 303.75
    A = np.array([[K, 0, -K * ox], [0, K, 0], [0, 0, 1]])
    Ai = np.linalg.inv(A)
    mats = []
    for h in tr["H"]:
        M = A @ np.array(h).reshape(3, 3) @ Ai
        M = M / M[2, 2]
        mats.append([M[0, 0], M[1, 0], 0, M[2, 0], M[0, 1], M[1, 1], 0, M[2, 1], 0, 0, 1, 0, M[0, 2], M[1, 2], 0, M[2, 2]])
    return mats, tr["fps"] * abs(SHOTS[shot]["speed"])     # frames per second of film time


BASE = """
    @font-face { font-family: "Inter"; font-weight: 100 900; font-display: block; src: url("assets/fonts/Inter.ttf") format("truetype"); }
    @font-face { font-family: "Instrument Serif"; font-style: italic; font-weight: 400; font-display: block; src: url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2"); }
    @font-face { font-family: "Courier Prime"; font-weight: 700; font-display: block; src: url("assets/fonts/CourierPrime-Bold.ttf") format("truetype"); }
    #root { position: absolute; inset: 0; overflow: hidden; background: #0a0a0a; color: #f5f5f7; font-family: "Inter", sans-serif; }
    .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }
    .full video { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; display: block; }
    .h { position: absolute; left: 76px; width: 930px; font-weight: 800; font-size: 118px; letter-spacing: -0.055em; line-height: 0.95; text-shadow: 0 4px 40px rgba(0, 0, 0, 0.45); }
    .it { position: relative; display: inline-block; font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; color: #dd483f; letter-spacing: -0.01em; font-size: 1.12em; line-height: 0.8; padding-right: 0.06em; }
    .ul { position: absolute; left: -2%; bottom: -0.16em; width: 104%; height: 0.3em; overflow: visible; }
    .ul path { fill: none; stroke: #dd483f; stroke-width: 7; stroke-linecap: round; stroke-dasharray: 1400; stroke-dashoffset: 1400; }
    .lab { position: absolute; left: 0; width: 1080px; text-align: center; font-weight: 600; font-size: 78px; letter-spacing: -0.03em; line-height: 1.08; color: #f5f5f7; text-shadow: 0 0 18px rgba(0, 0, 0, 0.75), 0 2px 44px rgba(0, 0, 0, 0.7); }
    .pen { position: absolute; overflow: visible; }
    .pen path { fill: none; stroke: #dd483f; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1400; stroke-dashoffset: 1400; }
    .scrim { position: absolute; left: 0; top: 0; width: 1080px; height: 760px; background: linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0)); }
    .pin { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; transform-origin: 0 0; }
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
      const pop = (sel, t, d = 0.32) => tl.fromTo(sel, {{ opacity: 0, scale: 0.86 }}, {{ opacity: 1, scale: 1, duration: d, ease: "back.out(2)", immediateRender: false }}, at(t));
      const pen = (sel, t, d = 0.36) => tl.to(sel, {{ strokeDashoffset: 0, duration: d, ease: "power2.inOut" }}, at(t));
      const ring = (sel, t, d = 0.5) => tl.to(sel, {{ "--p": 360, duration: d, ease: "power2.inOut" }}, at(t));
      // a pinned layer follows a tracked surface: one matrix3d per source frame, stepped by the timeline (seek-safe)
      const pin = (sel, mats, fps, t0) => {{
        const el = document.querySelector(sel), p = {{ f: 0 }}, n = mats.length - 1;
        const set = () => {{ el.style.transform = "matrix3d(" + mats[Math.min(n, Math.max(0, Math.floor(p.f)))].join(",") + ")"; }};
        set();
        tl.to(p, {{ f: n + 0.999, duration: (n + 1) / fps, ease: "none", onUpdate: set }}, t0);
      }};
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
    """The one red serif-italic word, with the pen underline inside it (drawn by pen())."""
    return (f'<span class="it" id="{id_}">{text}<svg class="ul" viewBox="0 0 100 20" preserveAspectRatio="none" aria-hidden="true">'
            f'<path vector-effect="non-scaling-stroke" d="M2 12 C 30 7, 66 11, 98 5" /></svg></span>')


def ring_img(id_, left, top, width, height, start_deg=340):
    """The logo's own hand-drawn pen circle, stretched round a target and drawn on with a conic mask."""
    m = f"conic-gradient(from {start_deg}deg at 50% 50%, #000 calc(var(--p) * 1deg), transparent calc(var(--p) * 1deg))"
    return (f'<div id="{id_}" style="position:absolute;left:{left:.0f}px;top:{top:.0f}px;width:{width}px;height:{height}px;--p:0;'
            f'-webkit-mask-image:{m};mask-image:{m}">'
            f'<img src="assets/logo/circle-crop.png" alt="" style="position:absolute;left:0;top:0;width:100%;height:100%" /></div>')


def vid(id_, src, start, dur, media_start=0.0, cls="clip"):
    ms = f' data-media-start="{media_start:.3f}"' if media_start else ""
    return f'<video id="{id_}" class="{cls}" src="assets/clips/{src}.mp4" data-start="{start:.3f}" data-duration="{dur:.3f}"{ms} muted playsinline></video>'


def full(id_, src, start, dur, media_start=0.0, z=1):
    return f'    <div id="{id_}-w" class="full" style="z-index:{z}">{vid(id_, src, start, dur, media_start)}</div>'


def mats_js(name, shot):
    m, fps = track(shot)
    return f"const {name} = {json.dumps([[round(v, 6) for v in r] for r in m])}; const {name}_fps = {fps:.4f};"


S = []
cut = lambda vid_: round(L[vid_]["start"] - 0.2, 3)
FILM = T["film"]
b = [0.0] + [cut(f"vo-{i:02d}") for i in range(2, 14)] + [FILM]

# S1 hook. Frame 0 = the cover; its printed photo grows into the film: a hand on the screen. ---------------------------
s, e = b[0], b[1]
t_go = 0.36
PH = "inset(840px 90px 603px 90px round 26px)"        # the cover's printed photo (scripts/cover.html #ph)
S.append(scene("s1", s, e, f"""
    #s1-cov {{ position: absolute; inset: 0; background: url("assets/shots/cover.png") 0 0 / 1080px 1920px; z-index: 5; }}
    #s1-world {{ clip-path: {PH}; z-index: 6; }}
    #s1-q {{ top: 300px; z-index: 8; opacity: 0; }}
    #s1-scrim {{ z-index: 7; opacity: 0; }}""", f"""
    <div id="s1-cov"></div>
    <div id="s1-world" class="full">{vid("s1-v", "tap", t_go - 0.06, e - s - t_go + 0.06)}</div>
    <div id="s1-scrim" class="scrim"></div>
    <div id="s1-q" class="h">&ldquo;It doesn&rsquo;t<br />work.&rdquo;</div>""", f"""
      // the photo becomes the world (Terra's zoom-through, Apple's full bleed): clip opens from the photo to the frame
      tl.to("#s1-world", {{ clipPath: "inset(0px 0px 0px 0px round 0px)", duration: 0.55, ease: "expo.inOut" }}, {t_go});
      tl.fromTo("#s1-world", {{ rotation: -2.5 }}, {{ rotation: 0, duration: 0.55, ease: "expo.inOut", immediateRender: false }}, {t_go});
      tl.to("#s1-cov", {{ opacity: 0, duration: 0.3 }}, {t_go + 0.3});
      tl.to("#s1-scrim", {{ opacity: 1, duration: 0.3 }}, {t_go + 0.4});
      rise("#s1-q", {t_go + 0.5:.2f});"""))

# S2 "That was twenty ten. He said your arm would fall off." The arm reaches out; on "fall", the shot falls off. ------
s, e = b[1], b[2]
t_fall = w("vo-02", "fall")
S.append(scene("s2", s, e, f"""
    #s2-fall {{ z-index: 3; transform-origin: 1080px 0px; }}
    #s2-y {{ top: 300px; font-size: 300px; z-index: 4; opacity: 0; }}
    #s2-y .it {{ font-size: 1em; }}""", f"""
    <div id="s2-fall" class="full">{vid("s2-v", "arm", 0, e - s)}
      <div class="scrim"></div>
      <div id="s2-y" class="h">{it("s2-it", "2010")}</div>
    </div>
    {full("s2-under", "logo", t_fall - 0.05 - s, e - (t_fall - 0.05))}""", f"""
      pop("#s2-y", {w("vo-02", "twenty") - 0.1:.2f}, 0.4);
      pen("#s2-it .ul path", {w("vo-02", "ten"):.2f}, 0.4);
      // "fall off": the whole shot drops away from its top-right corner and the next shot is under it
      tl.to("#s2-fall", {{ rotation: 24, y: 1500, duration: 0.62, ease: "power2.in" }}, at({t_fall:.2f}));"""))
LOGO_IN = t_fall - 0.05                                   # the logo clip started under s2

# S3 "This week, Apple shipped one anyway." The lid's logo lights up; the pen strikes "doesn't". -----------------------
s, e = b[2], b[3]
S.append(scene("s3", s, e, f"""
    #s3-q {{ top: 300px; z-index: 4; }}
    #s3-x {{ left: 286px; top: 312px; width: 520px; height: 90px; z-index: 5; }}""", f"""
{full("s3", "logo", 0, e - s, s - LOGO_IN)}
    <div class="scrim" style="z-index:3"></div>
    <div id="s3-q" class="h">&ldquo;It <span id="s3-dn">doesn&rsquo;t</span><br />work.&rdquo;</div>
    <svg id="s3-x" class="pen" viewBox="0 0 520 90" preserveAspectRatio="none"><path d="M4 58 C 140 40, 330 52, 516 30" /></svg>""", f"""
      tl.fromTo("#s3-q", {{ opacity: 0.85 }}, {{ opacity: 1, duration: 0.2 }}, 0);
      pen("#s3-x path", {w("vo-03", "anyway") - 0.05:.2f}, 0.32);
      tl.to("#s3-dn", {{ opacity: 0.38, duration: 0.25 }}, at({w("vo-03", "anyway") + 0.2:.2f}));"""))

# S4 "The touch is built right into the screen." A finger in Finder, a pinch on a 3D car; a fixed label. -------------
s, e = b[3], b[4]
f_len = 1.34
S.append(scene("s4", s, e, """
    #s4-l { top: 700px; z-index: 5; opacity: 0; }
    #s4-l small { display: block; font-size: 46px; font-weight: 500; color: #d2d2d7; letter-spacing: -0.02em; margin-top: 10px; }""", f"""
{full("s4a", "finder", 0, f_len)}
{full("s4b", "car", f_len, e - s - f_len, 0.55, 2)}
    <div id="s4-l" class="lab">In the panel.<small>Not layered on top.</small></div>""", f"""
      rise("#s4-l", {w("vo-04", "built") - 0.1:.2f}, 0.5);"""))

# S5 "Spin a 3D model with one finger." The label is pinned to the display glass and rides it as the camera pulls back.
s, e = b[4], b[5]
lx, ly = src2out("spin", 560, 205)
S.append(scene("s5", s, e, f"""
    #s5-pin {{ z-index: 4; }}
    #s5-l {{ position: absolute; left: {lx:.0f}px; top: {ly:.0f}px; font-weight: 800; font-size: 150px; letter-spacing: -0.05em; color: #fff; opacity: 0; text-shadow: 0 0 30px rgba(0,0,0,0.35); }}""", f"""
{full("s5", "spin", 0, e - s)}
    <div id="s5-pin" class="pin"><div id="s5-l">Spin.</div></div>""", f"""
      {mats_js("M5", "spin")}
      pin("#s5-pin", M5, M5_fps, 0);
      tl.fromTo("#s5-l", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.35, ease: "expo.out", immediateRender: false }}, at({w("vo-05", "spin") - 0.05:.2f}));"""))

# S6 "Play piano on the display." ---------------------------------------------------------------------------------
s, e = b[5], b[6]
S.append(scene("s6", s, e, "", f"""
{full("s6", "piano", 0, e - s, 1.2)}""", f"""
      tl.fromTo("#s6-w", {{ scale: 1 }}, {{ scale: 1.08, duration: {e - s:.2f}, ease: "sine.inOut" }}, 0);"""))

# S7 "And that screen is OLED. Two thousand nits." Macro on the pixels, then the Photoshop art; the one number. --------
s, e = b[6], b[7]
m_len = 1.26
S.append(scene("s7", s, e, """
    #s7-n { position: absolute; left: 0; top: 560px; width: 1080px; text-align: center; z-index: 5; opacity: 0; }
    #s7-n b { display: block; font-weight: 800; font-size: 270px; letter-spacing: -0.06em; line-height: 0.9; color: #fff; text-shadow: 0 6px 60px rgba(0,0,0,0.6); }
    #s7-n span { display: block; margin-top: 26px; font-weight: 600; font-size: 64px; letter-spacing: -0.03em; color: #f5f5f7; text-shadow: 0 2px 30px rgba(0,0,0,0.7); }
""", f"""
{full("s7a", "macro", 0, m_len)}
{full("s7b", "red", m_len, e - s - m_len, 0, 2)}
    <div id="s7-n"><b>2,000</b><span>nits · tandem OLED</span></div>""", f"""
      tl.fromTo("#s7-n", {{ opacity: 0, scale: 0.9 }}, {{ opacity: 1, scale: 1, duration: 0.5, ease: "expo.out", immediateRender: false }}, at({w("vo-07", "two") - 0.05:.2f}));
      tl.fromTo("#s7b-w", {{ scale: 1.0 }}, {{ scale: 1.12, duration: {e - s - m_len:.2f}, ease: "sine.inOut", immediateRender: false }}, {m_len});"""))

# S8 re-hook "So, what about the arm?" The arm shot again (the music drops out). ---------------------------------------
s, e = b[7], b[8]
S.append(scene("s8", s, e, """
    #s8-q { top: 300px; z-index: 4; opacity: 0; font-size: 150px; }""", f"""
{full("s8", "arm", 0, e - s)}
    <div class="scrim" style="z-index:3"></div>
    <div id="s8-q" class="h">The {it("s8-it", "arm?")}</div>""", f"""
      rise("#s8-q", {w("vo-08", "what") - 0.1:.2f}, 0.4);
      pen("#s8-it .ul path", {w("vo-08", "arm") + 0.05:.2f}, 0.36);"""))

# S9 "Apple's answer: you never have to lift it. The trackpad stays. The keyboard stays." -----------------------------
# the arm goes on, then plays backwards (it never has to lift), then hands on the keyboard with fixed labels
s, e = b[8], b[9]
arm_left = SHOTS["arm"]["out"] - SHOTS["arm"]["in"] - (s - b[7])
t_rev = w("vo-09", "you") - 0.08
rev_len = 1.42
S.append(scene("s9", s, e, """
    #s9-l1, #s9-l2 { z-index: 5; opacity: 0; }
    #s9-l1 { top: 600px; }
    #s9-l2 { top: 720px; }
    .tick { position: relative; display: inline-block; width: 64px; height: 56px; margin-left: 14px; vertical-align: -4px; }
    .tick path { fill: none; stroke: #dd483f; stroke-width: 11; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 200; stroke-dashoffset: 200; }""", f"""
{full("s9a", "arm", 0, min(arm_left, t_rev - s), s - b[7])}
{full("s9b", "armrev", t_rev - s, rev_len, 0, 2)}
{full("s9c", "open", t_rev - s + rev_len - 0.02, e - (t_rev + rev_len - 0.02), 0, 3)}
    <div id="s9-l1" class="lab">Trackpad<svg class="tick" viewBox="0 0 64 56"><path d="M6 30 L 24 48 L 58 8" /></svg></div>
    <div id="s9-l2" class="lab">Keyboard<svg class="tick" viewBox="0 0 64 56"><path d="M6 30 L 24 48 L 58 8" /></svg></div>""", f"""
      rise("#s9-l1", {w("vo-09", "trackpad") - 0.05:.2f}, 0.4);
      tl.to("#s9-l1 .tick path", {{ strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }}, at({w("vo-09", "stays") + 0.0:.2f}));
      rise("#s9-l2", {w("vo-09", "keyboard") - 0.05:.2f}, 0.4);
      tl.to("#s9-l2 .tick path", {{ strokeDashoffset: 0, duration: 0.3, ease: "power2.out" }}, at({w("vo-09", "stays", 2):.2f}));"""))

# S10 "And a new hinge holds the screen steady when you tap." A finger on the screen; a fixed label (the hinge itself
# sits at y~1580 in this crop, under the Reels caption area, so the label carries it). --------------------------------
s, e = b[9], b[10]
S.append(scene("s10", s, e, """
    #s10-l { top: 600px; z-index: 5; opacity: 0; }
    #s10-l small { display: block; font-size: 46px; font-weight: 500; color: #e8e8ed; letter-spacing: -0.02em; margin-top: 10px; }""", f"""
{full("s10", "tap2", 0, e - s)}
    <div id="s10-l" class="lab">New hinge.<small>Steadier when you tap.</small></div>""", f"""
      rise("#s10-l", {w("vo-10", "hinge") - 0.1:.2f}, 0.5);
      tl.fromTo("#s10-w", {{ scale: 1 }}, {{ scale: 1.06, duration: {e - s:.2f}, ease: "sine.inOut", transformOrigin: "540px 600px" }}, 0);"""))

# S11 "We read the whole ad for a catch. The only fine print? Weight varies." -----------------------------------------
# the ad races past (4 cuts), Apple's own "3 pounds light" gets the asterisk, then the ad's last frame and its one line
s, e = b[10], b[11]
t_only, t_wt = w("vo-11", "only") - 0.1, w("vo-11", "weight") - 0.12
mont = [("drone1", 0.0), ("magsafe", 0.0), ("hdmi", 0.0), ("car", 1.2)]
seg = (t_only - s) / len(mont)
EK = 920 / 1026                                          # endframe.png (1026x860) shown 920 wide
CT, CL = 560, 80
body11 = "\n".join(full(f"s11m{i}", name, i * seg, seg + 0.02, ms, i + 1) for i, (name, ms) in enumerate(mont))
S.append(scene("s11", s, e, f"""
    #s11-star {{ position: absolute; left: 990px; top: 790px; font-family: "Instrument Serif", serif; font-style: italic; font-size: 120px; line-height: 1; color: {RED}; z-index: 8; opacity: 0; }}
    #s11-card {{ position: absolute; inset: 0; background: #0a0a0a; z-index: 9; opacity: 0; }}
    #s11-ph {{ left: {CL}px; top: {CT}px; width: {920 + 12}px; height: {round(860 * EK) + 12}px; }}
    #s11-ph img {{ width: 920px; height: {round(860 * EK)}px; }}
    #s11-ul {{ left: {CL + 6 + 70 * EK:.0f}px; top: {CT + 6 + 834 * EK:.0f}px; width: {240 * EK:.0f}px; height: 24px; z-index: 10; }}""", f"""
{body11}
{full("s11c", "carry", t_only - s, t_wt - t_only + 0.05, 0, 6)}
    <div id="s11-star">*</div>
    <div id="s11-card"><div id="s11-ph" class="photo"><img src="assets/shots/endframe.png" alt="" /></div>
      <svg id="s11-ul" class="pen" viewBox="0 0 100 20" preserveAspectRatio="none"><path vector-effect="non-scaling-stroke" d="M1 11 C 30 7, 64 13, 99 7" /></svg>
    </div>""", f"""
      pop("#s11-star", {w("vo-11", "print") - 0.05:.2f}, 0.3);
      tl.to("#s11-star", {{ opacity: 0, duration: 0.05 }}, at({t_wt - 0.05:.2f}));
      tl.fromTo("#s11-card", {{ opacity: 0.9 }}, {{ opacity: 1, duration: 0.1, immediateRender: false }}, at({t_wt:.2f}));
      tl.fromTo("#s11-ph", {{ y: 120, rotation: 3 }}, {{ y: 0, rotation: 0, duration: 0.45, ease: "expo.out", immediateRender: false }}, at({t_wt:.2f}));
      pen("#s11-ul path", {w("vo-11", "varies") + 0.05:.2f}, 0.34);
      tl.fromTo("#s11-card", {{ scale: 1 }}, {{ scale: 1.22, duration: {e - t_wt - 0.45:.2f}, ease: "sine.inOut", transformOrigin: "545px 1293px", immediateRender: false }}, at({t_wt + 0.45:.2f}));"""))

# S12 "Jobs was right. That's why touch is optional." The lid closes and its logo lights: the ad's own ending. ----------
s, e = b[11], b[12]
S.append(scene("s12", s, e, """
    #s12-q { top: 300px; z-index: 4; opacity: 0; font-size: 140px; }""", f"""
{full("s12", "close", 0, e - s)}
    <div class="scrim" style="z-index:3"></div>
    <div id="s12-q" class="h">Touch is<br />{it("s12-it", "optional.")}</div>""", f"""
      rise("#s12-q", {w("vo-12", "touch") - 0.1:.2f}, 0.45);
      pen("#s12-it .ul path", {w("vo-12", "optional") + 0.15:.2f}, 0.42);"""))

# S13 end card on the logo's paper: the spoken ask; the logo sting plays over it -----------------------------------------
s, e = b[12], b[13]
S.append(scene("s13", s, e, """
    #root { background: #e7e7e5 url("assets/logo/paper-1080x1920.png") 0 0 / 1080px 1920px; color: #141414; }
    #s13-a, #s13-c { position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 66px; letter-spacing: -0.03em; }
    #s13-c { opacity: 0; }""", """
    <div id="s13-a">Would you touch it?</div>
    <div id="s13-c">Tell us below.</div>""", f"""
      tl.fromTo("#s13-a", {{ opacity: 0.85, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, 0);
      tl.to("#s13-a", {{ opacity: 0, duration: 0.12 }}, at({w('vo-13', 'tell') - 0.12:.2f}));
      tl.fromTo("#s13-c", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({w('vo-13', 'tell'):.2f}));"""))

# captions: the reference's style, 2-3 words, mid-frame, on a dark chip; groups break at punctuation --------------------
if CAPTIONS:
    groups = []
    for l in T["lines"][:-1]:                        # not over the end card (its ask is on screen)
        cur = []
        for i, (ww, st, en) in enumerate(l["words"]):
            cur.append((ww, st, en))
            nxt = l["words"][i + 1] if i + 1 < len(l["words"]) else None
            if len(cur) == 3 or re.search(r"[.,?!:]$", ww) or nxt is None:
                groups.append((cur[0][1], cur[-1][2], " ".join(x[0] for x in cur).rstrip(",")))
                cur = []
    groups = [(st, (groups[i + 1][0] if i + 1 < len(groups) and groups[i + 1][0] - en < 0.35 else en + 0.1), txt) for i, (st, en, txt) in enumerate(groups)]
    groups = [(max(st, 0.95), en, txt) for st, en, txt in groups if en > 1.2]   # nothing over the cover
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
      {js}tl.set({{}}, {{}}, {b[12]});
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
sting_at = b[12] + 0.05
hosts += (f'\n      <div id="sting" data-composition-id="logo-sting" data-composition-src="compositions/logo-sting.html" data-start="{sting_at:.2f}" '
          f'data-duration="{FILM - sting_at:.2f}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 50"></div>')
if CAPTIONS:
    hosts += (f'\n      <div id="caps" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" '
              f'data-duration="{b[12]}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 60"></div>')
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
    <title>CatchTheError — Case 026: the touchscreen Mac Steve Jobs said doesn't work</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0a0a0a; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FILM}" data-width="1080" data-height="1920">
      <!-- Scenes, cut to the narration (SPEC.md); the logo sting plays over the end card. Footage: Apple's MacBook Pro with PROLED XDR film. -->
{hosts}

      <!-- Voiceover: VoiceBox, trained voice "sparsh" (myvoice); levelled to -14 LUFS (scripts/prep_audio.py). -->
{vo}

      <!-- Music bed: "Pamgaea", Kevin MacLeod (incompetech.com), CC BY 4.0; envelope baked in. -->
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
