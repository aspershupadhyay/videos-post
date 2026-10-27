"""Case 021 v2: writes compositions/s*.html and index.html from assets/vo/timing.json.
Every cut and cue derives from the voice's word times, so a re-voiced line only needs a rerun.

Look v5 (creator's cover reference, 2026-10-27): logo paper ground; real footage big, in "printed photo" frames
(dark border, offset shadow); NO subtitles and no on-screen credits; at most one short expressive line per beat in
Inter 800 with one red Instrument Serif italic word underlined by the pen. Visual metaphors over read-outs.
Moves from OpenAI's Terra film are in brand/MOTION.md.
"""
import json
import re
import shutil
from pathlib import Path

P = Path(__file__).resolve().parent.parent
T = json.loads((P / "assets/vo/timing.json").read_text())
FILM = T["film"]
L = {l["id"]: l for l in T["lines"]}


def w(vid, word, n=1):
    """Start time of the n-th occurrence of a word in a line (case-insensitive, punctuation ignored)."""
    hits = [s for ww, s, e in L[vid]["words"] if re.sub(r"[^\w.]", "", ww).lower().strip(".") == word.lower()]
    return hits[n - 1]


BASE = """
    @font-face { font-family: "Inter"; font-weight: 100 900; font-display: block; src: url("assets/fonts/Inter.ttf") format("truetype"); }
    @font-face { font-family: "Instrument Serif"; font-style: italic; font-weight: 400; font-display: block; src: url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2"); }
    @font-face { font-family: "Courier Prime"; font-weight: 700; font-display: block; src: url("assets/fonts/CourierPrime-Bold.ttf") format("truetype"); }
    #root { position: absolute; inset: 0; overflow: hidden; background: #e7e7e5 url("assets/logo/paper-1080x1920.png") 0 0 / 1080px 1920px; color: #141414; font-family: "Inter", sans-serif; }
    .h { position: absolute; left: 76px; width: 930px; font-weight: 800; font-size: 118px; letter-spacing: -0.055em; line-height: 0.93; }
    .it { position: relative; display: inline-block; font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; color: #dd483f; letter-spacing: -0.01em; font-size: 1.12em; line-height: 0.8; padding-right: 0.06em; }
    .ul { position: absolute; left: -2%; bottom: -0.16em; width: 104%; height: 0.3em; overflow: visible; }
    .ul path { fill: none; stroke: #dd483f; stroke-width: 7; stroke-linecap: round; stroke-dasharray: 1; stroke-dashoffset: 1; }
    .kick { position: absolute; left: 76px; font-weight: 600; font-size: 46px; letter-spacing: -0.025em; color: #7b7b77; }
    .mono { position: absolute; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.12em; text-transform: uppercase; color: #5f5f5c; }
    .photo { position: absolute; overflow: hidden; background: #fff; border: 6px solid #1b1b1b; border-radius: 26px; box-shadow: 14px 16px 0 rgba(20, 20, 18, 0.10), 0 34px 70px rgba(20, 20, 18, 0.12); }
    .photo video, .photo img.fill { position: absolute; }
    .pen { position: absolute; overflow: visible; }
    .pen path { fill: none; stroke: #dd483f; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; }
    .pill { position: relative; display: inline-block; background: #fff; border-radius: 80px; padding: 24px 48px; font-weight: 700; font-size: 58px; letter-spacing: -0.03em; white-space: nowrap; box-shadow: 0 18px 50px rgba(0, 0, 0, 0.2); }
    .row { position: absolute; left: 0; width: 1080px; text-align: center; }
    .ch { opacity: 0; }
    .wm { position: absolute; left: 0; width: 1080px; text-align: center; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 46px; letter-spacing: 0.3em; color: #3f3f3d; }
    .wm-e { position: relative; display: inline-block; color: #dd483f; }
    .wm-e img { position: absolute; left: -0.44em; top: -0.36em; width: 1.75em; height: 1.6em; }
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
      const blurIn = (sel, t, d = 0.2) => tl.fromTo(sel, {{ opacity: 0, filter: "blur(12px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: d, ease: "power4.out", immediateRender: false }}, at(t));
      const rise = (sel, t) => tl.fromTo(sel, {{ opacity: 0, y: 60, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out", immediateRender: false }}, at(t));
      const out = (sel, t, d = 0.16) => tl.to(sel, {{ opacity: 0, filter: "blur(10px)", duration: d, ease: "power2.in" }}, at(t));
      const pen = (sel, t, d = 0.36) => tl.to(sel, {{ strokeDashoffset: 0, duration: d, ease: "power2.inOut" }}, at(t));
      const type = (sel, t, cps = 34) => tl.to(sel + " .ch", {{ opacity: 1, duration: 0.001, stagger: 1 / cps, immediateRender: false }}, at(t));
      const ring = (sel, t, d = 0.5) => tl.to(sel, {{ "--p": 360, duration: d, ease: "power2.inOut" }}, at(t));
{js}
      tl.set({{}}, {{}}, {dur});
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    (P / f"compositions/{sid}.html").write_text(html)
    return (sid, start, dur)


def typed(text):
    return "".join(c if c == " " else f'<span class="ch">{c}</span>' for c in text)


def it(id_, text):
    """The one red serif-italic word, with the pen underline inside it (pathLength 1, drawn by pen())."""
    return (f'<span class="it" id="{id_}">{text}<svg class="ul" viewBox="0 0 100 20" preserveAspectRatio="none" aria-hidden="true">'
            f'<path pathLength="1" vector-effect="non-scaling-stroke" d="M2 12 C 30 7, 66 11, 98 5" /></svg></span>')


def ring_img(id_, left, top, width, height, start_deg=340):
    """The logo's own hand-drawn pen circle, stretched round a target and drawn on with a conic mask."""
    m = f"conic-gradient(from {start_deg}deg at 50% 50%, #000 calc(var(--p) * 1deg), transparent calc(var(--p) * 1deg))"
    return (f'<div id="{id_}" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{height}px;--p:0;'
            f'-webkit-mask-image:{m};mask-image:{m}">'
            f'<img src="assets/logo/circle-crop.png" alt="" style="position:absolute;left:0;top:0;width:100%;height:100%" /></div>')


WORDMARK = '<div id="{id}" class="wm" style="top:{top}px">CATCH · THE · <span class="wm-e">E<img src="assets/logo/circle-crop.png" alt="" /></span>RROR</div>'


def card_media(crop, cw):
    """Source frames are 1920x1080. A card shows crop (x0, y0, x1, y1) scaled to the card width."""
    x0, y0, x1, y1 = crop
    k = cw / (x1 - x0)
    return k, round((y1 - y0) * k), f"left:{-x0 * k:.1f}px;top:{-y0 * k:.1f}px;width:{1920 * k:.1f}px;height:{1080 * k:.1f}px"


S = []
cut = lambda vid: round(L[vid]["start"] - 0.2, 2)
b = [0.0, cut("vo-02"), cut("vo-03"), cut("vo-04"), cut("vo-05"), cut("vo-06"), cut("vo-07"), cut("vo-08"),
     cut("vo-09"), cut("vo-10"), FILM]
BORDER = 6

# S1 hook. Frame 0 = the cover. Then the photo + prompt (real clip), a zoom-through, the toy full-bleed, the pen ring. ---
s, e = b[0], b[1]
_, _, st_cov = card_media((760, 130, 1360, 718), 528)   # square window on the toy (safe zone: card ends at y 1480)        # 4:5 window on the toy for the cover card
k_sq, h_sq, st_sq = card_media((420, 0, 1500, 1080), 1000)    # square window on the photo + prompt
t_go, t_photo, t_toy = 0.3, 0.56, w("vo-01", "designed") - 0.32
TX, TY = (1030 - 700) * 1080 / 608, 490 * 1920 / 1080          # toy centre on the 9:16 toy clip
S.append(scene("s1", s, e, f"""
    #s1-k {{ left: 76px; top: 262px; }}
    #s1-g {{ top: 318px; }}
    #s1-h {{ top: 392px; font-size: 150px; width: 960px; }}
    #s1-sub {{ top: 852px; font-weight: 700; font-size: 52px; color: #3a3a38; }}
    #s1-cov {{ left: 270px; top: 948px; width: 540px; height: 532px; }}
    #s1-cov img {{ {st_cov} }}
    #s1-sq {{ left: 40px; top: 430px; width: 1000px; height: 1000px; opacity: 0; }}
    #s1-sq video, #s1-sq img {{ {st_sq} }}
    #s1-full {{ position: absolute; inset: 0; opacity: 0; background: #fff; }}
    #s1-full video, #s1-full img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}""", f"""
    <div id="s1-full">
      <img src="assets/shots/toytall-end.png" alt="" />
      <video id="s1-toy" class="clip" src="assets/footage/toytall.mp4" data-start="{t_toy:.3f}" data-duration="{min(1.63, e - t_toy):.3f}" muted playsinline></video>
      {ring_img("s1-ring", 210, 670, 700, 520)}
    </div>
    <div id="s1-sq" class="photo">
      <img class="fill" src="assets/shots/photo-end.png" alt="" />
      <video id="s1-photo" class="clip" src="assets/footage/photo.mp4" data-start="{t_photo:.3f}" data-duration="2.0" muted playsinline></video>
    </div>
    <div id="s1-cover">
      <div id="s1-k" class="mono">Case 021 / GPT-6.1 Terra</div>
      <div id="s1-g" class="kick">Fact check · OpenAI's demo</div>
      <div id="s1-h" class="h">AI built this toy from one {it("s1-it", "photo?")}</div>
      <div id="s1-sub" class="kick">Half the price. 3× faster. Really?</div>
      <div id="s1-cov" class="photo"><img class="fill" src="assets/shots/toy-start.png" alt="A hand sets down a die-cast Lisbon tram" /></div>
      {WORDMARK.format(id="s1-wm", top=1530)}
    </div>""", f"""
      tl.set("#s1-it path", {{ strokeDashoffset: 0 }}, 0);
      tl.set("#s1-cov", {{ rotation: -2.5 }}, 0);
      // the cover clears: type lifts away, the card swells and hands over to the photo clip
      tl.to(["#s1-k", "#s1-g", "#s1-h", "#s1-sub", "#s1-wm"], {{ y: -70, opacity: 0, filter: "blur(10px)", duration: 0.28, ease: "power3.in", stagger: 0.02 }}, at({t_go}));
      tl.to("#s1-cov", {{ scale: 1.5, rotation: 0, y: -200, opacity: 0, duration: 0.42, ease: "power3.inOut" }}, at({t_go}));
      tl.fromTo("#s1-sq", {{ opacity: 0, scale: 0.7, rotation: -2.5 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.5, ease: "expo.out", immediateRender: false }}, at({t_photo}));
      // zoom through the photo into the toy, full-bleed
      tl.to("#s1-sq", {{ scale: 2.8, filter: "blur(14px)", opacity: 0, duration: 0.34, ease: "power3.in", transformOrigin: "50% 40%" }}, at({t_toy - 0.3}));
      tl.fromTo("#s1-full", {{ opacity: 1, scale: 1.3, filter: "blur(14px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out", immediateRender: false }}, at({t_toy}));
      ring("#s1-ring", {w('vo-01', 'toy') - 0.05}, 0.45);"""))

# S2 the loop: the demo, one tiny line under it, ringed ---------------------------------------------------
BUILD = (200, 90, 1720, 990)
k, chh, st = card_media(BUILD, 1000)
fx, fy = (738 - 200) * k, (944 - 90) * k
fw, fh = (1182 - 738) * k, (962 - 944) * k
s, e = b[1], b[2]
CT = 700                                                          # card top
ring_box = (round(40 + fx - 62), round(CT + fy - 40), round(fw + 80), round(fh + 68))
S.append(scene("s2", s, e, f"""
    #s2-h {{ top: 330px; }}
    #s2-cam {{ position: absolute; inset: 0; }}
    #s2-card {{ left: 40px; top: {CT}px; width: 1000px; height: {chh + 2 * BORDER}px; }}
    #s2-card video, #s2-card img.fill {{ {st} }}""", f"""
    <div id="s2-h" class="h">One tiny {it("s2-it", "line.")}</div>
    <div id="s2-cam">
      <div id="s2-card" class="photo">
        <img class="fill" src="assets/shots/build-end.png" alt="" />
        <video id="s2-v" class="clip" src="assets/footage/build.mp4" data-start="0" data-duration="{min(4.95, e - s):.3f}" muted playsinline></video>
      </div>
      {ring_img("s2-ring", *ring_box)}
    </div>""", f"""
      tl.fromTo("#s2-card", {{ y: 220, rotation: 3, scale: 0.92 }}, {{ y: 0, rotation: 0, scale: 1, duration: 0.55, ease: "expo.out" }}, 0);
      tl.fromTo("#s2-h", {{ opacity: 0.85, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, 0);
      ring("#s2-ring", {w('vo-02', 'tiny')}, 0.55);
      pen("#s2-it path", {w('vo-02', 'line')}, 0.35);
      // keep your eye on it: the camera leans in on the line
      tl.to("#s2-cam", {{ scale: 1.45, duration: 0.9, ease: "power2.inOut", transformOrigin: "540px {CT + fy:.0f}px" }}, at({w('vo-02', 'keep')}));
      tl.to("#s2-h", {{ opacity: 0, y: -40, filter: "blur(8px)", duration: 0.3, ease: "power2.in" }}, at({w('vo-02', 'keep')}));"""))

# S3 what it is: OpenAI's earth -> Lisbon zoom, full-bleed; prompt pills; the world shrinks into a card -----------
s, e = b[2], b[3]
t_gpt, t_chat, t_use = w("vo-03", "gpt") - 0.1, w("vo-03", "not"), w("vo-03", "built", 2)
t_shrink = w("vo-03", "computer") - 0.15
S.append(scene("s3", s, e, f"""
    #s3-world {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }}
    #s3-world video, #s3-world img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    #s3-r1 {{ top: 700px; }} #s3-r1 .pill {{ font-size: 76px; }}
    #s3-r2, #s3-r3 {{ top: 880px; opacity: 0; }}
    #s3-strike {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; }}
    #s3-strike path {{ stroke-dasharray: 1; stroke-dashoffset: 1; }}""", f"""
    <div id="s3-world">
      <img src="assets/shots/earth-end.png" alt="" />
      <video id="s3-v" class="clip" src="assets/footage/earth.mp4" data-start="0" data-duration="{min(5.12, e - s):.3f}" muted playsinline></video>
    </div>
    <div id="s3-r1" class="row"><div class="pill">{typed("GPT-6.1 Terra")}</div></div>
    <div id="s3-r2" class="row"><div class="pill">built to chat<svg id="s3-strike" class="pen" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M4 56 C 30 50, 70 52, 96 46" vector-effect="non-scaling-stroke" /></svg></div></div>
    <div id="s3-r3" class="row"><div class="pill">{typed("built to use your computer")}</div></div>""", f"""
      type("#s3-r1", {t_gpt}, 26);
      tl.fromTo("#s3-r1", {{ scale: 0.9 }}, {{ scale: 1, duration: 0.35, ease: "back.out(1.6)", immediateRender: false }}, at({t_gpt}));
      tl.fromTo("#s3-r2", {{ opacity: 0, scaleX: 0.4, filter: "blur(12px)" }}, {{ opacity: 1, scaleX: 1, filter: "blur(0px)", duration: 0.22, ease: "power3.out", immediateRender: false }}, at({t_chat}));
      pen("#s3-strike path", {w('vo-03', 'chat')}, 0.3);
      out("#s3-r2", {t_use - 0.1}, 0.1);
      tl.fromTo("#s3-r3", {{ opacity: 1 }}, {{ opacity: 1, duration: 0.01, immediateRender: false }}, at({t_use}));
      type("#s3-r3", {t_use}, 40);
      // the world shrinks into a printed card (OpenAI's own move)
      tl.to("#s3-world", {{ scale: 0.6, borderRadius: 40, rotation: -2, y: -60, duration: 0.6, ease: "power2.inOut", transformOrigin: "540px 960px" }}, at({t_shrink}));
      tl.to(["#s3-r1", "#s3-r3"], {{ y: -60, scale: 0.8, duration: 0.6, ease: "power2.inOut" }}, at({t_shrink}));"""))

# S4 how: the 3D app builds the tram, big; then the result in ChatGPT with a push to the model ------------------------
s, e = b[3], b[4]
VIEW = (470, 110, 1450, 960)
k2, ch2, st2 = card_media(VIEW, 1000)
APP = (150, 40, 1770, 1040)
k3, ch3, st3 = card_media(APP, 1000)
t_app = w("vo-04", "tram") - 0.15
A_TOP = (1920 - ch2) // 2 - 80
S.append(scene("s4", s, e, f"""
    #s4-a {{ left: 40px; top: {A_TOP}px; width: 1000px; height: {ch2 + 2 * BORDER}px; }}
    #s4-a video, #s4-a img.fill {{ {st2} }}
    #s4-b {{ left: 40px; top: {A_TOP + (ch2 - ch3) // 2}px; width: 1000px; height: {ch3 + 2 * BORDER}px; opacity: 0; }}
    #s4-bz {{ position: absolute; inset: 0; }}
    #s4-b video, #s4-b img.fill {{ {st3} }}""", f"""
    <div id="s4-a" class="photo">
      <img class="fill" src="assets/shots/build-end.png" alt="" />
      <video id="s4-va" class="clip" src="assets/footage/build.mp4" data-start="0" data-media-start="1.8" data-duration="{min(3.1, e - s):.3f}" muted playsinline></video>
    </div>
    <div id="s4-b" class="photo"><div id="s4-bz">
      <img class="fill" src="assets/shots/app-end.png" alt="" />
      <video id="s4-vb" class="clip" src="assets/footage/app.mp4" data-start="{t_app - s:.3f}" data-duration="{min(3.45, e - t_app):.3f}" muted playsinline></video>
    </div></div>""", f"""
      // the small card from the last scene lands as this one (carry across)
      tl.fromTo("#s4-a", {{ scale: 0.62, rotation: -2, y: -60 }}, {{ scale: 1, rotation: 0, y: 0, duration: 0.6, ease: "expo.out" }}, 0);
      tl.fromTo("#s4-a", {{ scale: 1 }}, {{ scale: 1.06, duration: {t_app - s - 0.6:.2f}, ease: "none", immediateRender: false }}, 0.6);
      tl.to("#s4-a", {{ opacity: 0, x: -200, rotation: -6, duration: 0.3, ease: "power3.in" }}, at({t_app}));
      tl.fromTo("#s4-b", {{ opacity: 1, x: 1100, rotation: 6 }}, {{ opacity: 1, x: 0, rotation: 0, duration: 0.45, ease: "expo.out", immediateRender: false }}, at({t_app}));
      tl.fromTo("#s4-bz", {{ scale: 1 }}, {{ scale: 1.6, duration: {e - t_app - 0.3:.2f}, ease: "power2.inOut", transformOrigin: "50% 62%" }}, at({t_app + 0.25}));"""))

# S5 the numbers as objects: the pen slices the tram in half (half the price); whole again, it bolts (3x faster) ------
s, e = b[4], b[5]
t_price, t_says, t_three, t_fast = w("vo-05", "price"), w("vo-05", "openai"), w("vo-05", "three"), w("vo-05", "faster")
TRAM = 'style="position:absolute;left:0;top:0;width:760px;height:760px"'
S.append(scene("s5", s, e, f"""
    #s5-h1 {{ top: 300px; }}
    #s5-h2 {{ top: 300px; opacity: 0; }}
    #s5-tram {{ position: absolute; left: 160px; top: 640px; width: 760px; height: 760px; }}
    #s5-l, #s5-r {{ position: absolute; inset: 0; }}
    #s5-l {{ clip-path: polygon(0 0, 53% 0, 47% 100%, 0 100%); }}
    #s5-r {{ clip-path: polygon(53% 0, 100% 0, 100% 100%, 47% 100%); }}
    #s5-slash {{ position: absolute; left: 0; top: 0; width: 760px; height: 760px; }}
    #s5-slash path {{ stroke-dasharray: 1; stroke-dashoffset: 1; stroke-width: 11; }}""", f"""
    <div id="s5-h1" class="h">Half the {it("s5-it1", "price.")}</div>
    <div id="s5-h2" class="h">3× {it("s5-it2", "faster.")}</div>
    <div id="s5-tram">
      <div id="s5-l"><img src="assets/shots/tram-alpha.png" alt="The die-cast tram from OpenAI's film" {TRAM} /></div>
      <div id="s5-r"><img src="assets/shots/tram-alpha.png" alt="" {TRAM} /></div>
      <svg id="s5-slash" class="pen" viewBox="0 0 760 760" aria-hidden="true"><path pathLength="1" d="M418 40 C 404 260, 382 480, 352 720" /></svg>
    </div>""", f"""
      tl.fromTo("#s5-tram", {{ x: -1100 }}, {{ x: 0, duration: 0.7, ease: "expo.out" }}, 0);
      tl.fromTo("#s5-h1", {{ opacity: 0, filter: "blur(12px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power4.out", immediateRender: false }}, at({w('vo-05', 'half') - 0.05}));
      // half the price: the pen slices it, one half falls away
      pen("#s5-slash path", {t_price - 0.05}, 0.2);
      pen("#s5-it1 path", {t_price + 0.1}, 0.3);
      tl.to("#s5-r", {{ x: 70, y: 46, rotation: 7, opacity: 0.28, duration: 0.5, ease: "power3.out", transformOrigin: "50% 100%" }}, at({t_price + 0.18}));
      // OpenAI says: whole again
      tl.to("#s5-slash", {{ opacity: 0, duration: 0.2 }}, at({t_says - 0.1}));
      tl.to("#s5-r", {{ x: 0, y: 0, rotation: 0, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, at({t_says}));
      out("#s5-h1", {t_three - 0.18}, 0.14);
      tl.fromTo("#s5-h2", {{ opacity: 0, scale: 1.25, filter: "blur(14px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: "expo.out", immediateRender: false, transformOrigin: "0% 50%" }}, at({t_three}));
      pen("#s5-it2 path", {t_fast + 0.05}, 0.3);
      // ...and it bolts off, then comes round again
      tl.to("#s5-tram", {{ x: 1200, filter: "blur(6px)", duration: 0.42, ease: "power3.in" }}, at({t_fast}));
      tl.fromTo("#s5-tram", {{ x: -1200, filter: "blur(6px)" }}, {{ x: 0, filter: "blur(0px)", duration: 0.7, ease: "expo.out", immediateRender: false }}, at({t_fast + 0.75}));"""))

# S6 the payoff: back to the demo; zoom into the real footnote, through it; it becomes the headline ---------------
s, e = b[5], b[6]
fcx, fcy = 40 + fx + fw / 2, CT + fy + fh / 2
t_zoom, t_shown, t_some = w("vo-06", "that") - 0.1, w("vo-06", "shown") - 0.12, w("vo-06", "some")
_, mh, st_m = card_media(BUILD, 760)
S.append(scene("s6", s, e, f"""
    #s6-cam {{ position: absolute; inset: 0; }}
    #s6-card {{ left: 40px; top: {CT}px; width: 1000px; height: {chh + 2 * BORDER}px; }}
    #s6-card video, #s6-card img.fill {{ {st} }}
    #s6-q1 {{ top: 330px; font-weight: 600; font-size: 56px; letter-spacing: -0.03em; color: #6f6f6b; opacity: 0; }}
    #s6-q2 {{ top: 410px; opacity: 0; }}
    #s6-mini {{ left: 160px; top: 830px; width: 760px; height: {mh + 2 * BORDER}px; opacity: 0; }}
    #s6-mini video, #s6-mini img.fill {{ {st_m} }}""", f"""
    <div id="s6-cam">
      <div id="s6-card" class="photo">
        <img class="fill" src="assets/shots/build-end.png" alt="" />
        <video id="s6-v" class="clip" src="assets/footage/build.mp4" data-start="0" data-media-start="0.6" data-duration="{min(4.3, e - s):.3f}" muted playsinline></video>
      </div>
      {ring_img("s6-ring", *ring_box)}
    </div>
    <div id="s6-q1" class="kick">“Shown at actual speed.</div>
    <div id="s6-q2" class="h">Some sections {it("s6-it", "omitted.”")}</div>
    <div id="s6-mini" class="photo">
      <img class="fill" src="assets/shots/build-end.png" alt="" />
      <video id="s6-v2" class="clip" src="assets/footage/build.mp4" data-start="{t_shown + 0.2 - s:.3f}" data-media-start="1.2" data-duration="{min(3.7, e - t_shown - 0.2):.3f}" muted playsinline></video>
    </div>""", f"""
      tl.set("#s6-ring", {{ "--p": 360 }}, 0);
      tl.fromTo("#s6-card", {{ y: 160, scale: 0.94 }}, {{ y: 0, scale: 1, duration: 0.45, ease: "expo.out" }}, 0);
      tl.to("#s6-cam", {{ scale: 2.6, duration: {t_shown - t_zoom - 0.05:.2f}, ease: "power2.inOut", transformOrigin: "{fcx:.0f}px {fcy:.0f}px" }}, at({t_zoom}));
      tl.to("#s6-cam", {{ scale: 14, opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power3.in", transformOrigin: "{fcx:.0f}px {fcy:.0f}px" }}, at({t_shown - 0.05}));
      blurIn("#s6-q1", {t_shown + 0.12});
      tl.fromTo("#s6-q2", {{ opacity: 0, scale: 1.2, filter: "blur(14px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: "expo.out", immediateRender: false, transformOrigin: "0% 50%" }}, at({t_some - 0.05}));
      pen("#s6-it path", {w('vo-06', 'omitted') + 0.2}, 0.4);
      rise("#s6-mini", {t_shown + 0.3});"""))

# S7 "with the slow parts cut out": the pen cuts the demo itself, the halves part ------------------------------
s, e = b[6], b[7]
t_slow, t_cut = w("vo-07", "slow"), w("vo-07", "cut")
_, h7, st7 = card_media(BUILD, 1000)
C7 = 760
POLY_A, POLY_B = "polygon(0 0, 100% 0, 100% 34%, 0 66%)", "polygon(0 66%, 100% 34%, 100% 100%, 0 100%)"
half = lambda id_, poly: (f'<div id="{id_}" style="position:absolute;left:0;top:0;width:1000px;height:{h7 + 2 * BORDER}px;clip-path:{poly}">'
                          f'<div class="photo" style="left:0;top:0;width:1000px;height:{h7 + 2 * BORDER}px">'
                          f'<img class="fill" src="assets/shots/build-end.png" alt="" style="{st7}" />'
                          f'<video id="{id_}-v" class="clip" src="assets/footage/build.mp4" data-start="0" data-media-start="0.2" data-duration="{min(4.7, e - s):.3f}" muted playsinline style="{st7}"></video>'
                          f'</div></div>')
S.append(scene("s7", s, e, f"""
    #s7-h {{ top: 330px; }}
    #s7-card {{ position: absolute; left: 40px; top: {C7}px; width: 1000px; height: {h7 + 2 * BORDER}px; }}
    #s7-slash {{ position: absolute; left: -40px; top: -20px; width: 1080px; height: {h7 + 40}px; }}
    #s7-slash path {{ stroke-dasharray: 1; stroke-dashoffset: 1; stroke-width: 10; }}""", f"""
    <div id="s7-h" class="h">Actual {it("s7-it", "speed.")}</div>
    <div id="s7-card">
      {half("s7-a", POLY_A)}
      {half("s7-b", POLY_B)}
      <svg id="s7-slash" class="pen" viewBox="0 0 1080 {h7 + 40}" preserveAspectRatio="none" aria-hidden="true"><path pathLength="1" d="M20 {0.66 * h7 + 26:.0f} L 1060 {0.34 * h7 + 26:.0f}" /></svg>
    </div>""", f"""
      tl.fromTo("#s7-h", {{ opacity: 0.85, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, 0);
      tl.fromTo("#s7-card", {{ opacity: 0.85, scale: 0.94 }}, {{ opacity: 1, scale: 1, duration: 0.4, ease: "expo.out" }}, 0);
      pen("#s7-it path", {w('vo-07', 'speed')}, 0.3);
      pen("#s7-slash path", {t_slow}, 0.28);
      tl.to("#s7-slash", {{ opacity: 0, duration: 0.15 }}, at({t_cut - 0.05}));
      tl.to("#s7-a", {{ x: -46, y: -64, rotation: -4, duration: 0.5, ease: "expo.out" }}, at({t_cut}));
      tl.to("#s7-b", {{ x: 46, y: 64, rotation: 3, duration: 0.5, ease: "expo.out" }}, at({t_cut}));"""))

# S8 the catch: 3x, footnoted like OpenAI footnotes its demo -------------------------------------------------------
s, e = b[7], b[8]
t_test, t_none, t_conf = w("vo-08", "thats"), w("vo-08", "no"), w("vo-08", "confirmed")
S.append(scene("s8", s, e, f"""
    #s8-big {{ position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; font-weight: 800; font-size: 560px; letter-spacing: -0.07em; line-height: 0.9; }}
    #s8-ast {{ color: #dd483f; font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; font-size: 0.6em; vertical-align: 0.42em; margin-left: -0.04em; opacity: 0; display: inline-block; }}
    #s8-f {{ position: absolute; left: 0; top: 880px; width: 1080px; text-align: center; font-family: "Instrument Serif", serif; font-style: italic; font-size: 120px; color: #dd483f; letter-spacing: -0.01em; }}
    #s8-n1, #s8-n2 {{ position: absolute; left: 0; width: 1080px; text-align: center; font-size: 46px; font-weight: 500; letter-spacing: -0.02em; color: #2a2a28; opacity: 0; }}
    #s8-n1 {{ top: 1110px; }} #s8-n2 {{ top: 1176px; color: #6f6f6b; }}""", f"""
    <div id="s8-big">3×<span id="s8-ast">*</span></div>
    <div id="s8-f">faster?</div>
    <div id="s8-n1">*Measured by OpenAI.</div>
    <div id="s8-n2">Not yet checked by anyone else.</div>
    {ring_img("s8-ring", 175, 1148, 730, 112)}""", f"""
      tl.fromTo("#s8-big", {{ scale: 1.35, opacity: 0.85, filter: "blur(10px)" }}, {{ scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.5, ease: "expo.out" }}, 0);
      tl.fromTo("#s8-f", {{ opacity: 0.85, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }}, 0.1);
      // the asterisk lands, then the footnote under it, the way OpenAI footnoted its demo
      tl.fromTo("#s8-ast", {{ opacity: 1, scale: 3, rotation: -40 }}, {{ opacity: 1, scale: 1, rotation: 0, duration: 0.45, ease: "back.out(2)", immediateRender: false }}, at({t_test}));
      tl.to(["#s8-big", "#s8-f"], {{ y: -60, duration: 0.5, ease: "power3.inOut" }}, at({t_test}));
      rise("#s8-n1", {w('vo-08', 'own')});
      rise("#s8-n2", {t_none});
      ring("#s8-ring", {t_conf}, 0.5);
      // unchecked, the claim fades to a ghost
      tl.to("#s8-big", {{ color: "#c9c9c5", scale: 0.94, duration: 0.6, ease: "power2.inOut" }}, at({t_conf - 0.2}));"""))

# S9 the take: the demo gets an AD stamp; the pen draws the line under it ---------------------------------------
s, e = b[8], b[9]
C9 = 720
S.append(scene("s9", s, e, f"""
    #s9-h {{ top: 330px; }}
    #s9-card {{ left: 40px; top: {C9}px; width: 1000px; height: {chh + 2 * BORDER}px; }}
    #s9-card video, #s9-card img.fill {{ {st} }}
    #s9-ad {{ position: absolute; left: 70px; top: {C9 - 60}px; padding: 4px 30px 8px; border: 10px solid #dd483f; border-radius: 22px; color: #dd483f; font-weight: 900; font-size: 140px; letter-spacing: -0.02em; opacity: 0; background: rgba(231, 231, 229, 0.55); }}
    #s9-ul {{ position: absolute; left: {40 + fx - 20:.0f}px; top: {C9 + fy + fh + 4:.0f}px; width: {fw + 40:.0f}px; height: 30px; }}
    #s9-ul path {{ stroke-dasharray: 1; stroke-dashoffset: 1; stroke-width: 7; }}""", f"""
    <div id="s9-h" class="h">A demo is an {it("s9-it", "ad.")}</div>
    <div id="s9-cam" style="position:absolute;inset:0">
    <div id="s9-card" class="photo">
      <img class="fill" src="assets/shots/build-end.png" alt="" />
      <video id="s9-v" class="clip" src="assets/footage/build.mp4" data-start="0" data-media-start="1.6" data-duration="{min(3.3, e - s):.3f}" muted playsinline></video>
    </div>
    <div id="s9-ad">AD</div>
    <svg id="s9-ul" class="pen" viewBox="0 0 {fw + 40:.0f} 30" aria-hidden="true"><path pathLength="1" d="M4 18 C {fw * 0.3:.0f} 12, {fw * 0.66:.0f} 16, {fw + 36:.0f} 10" /></svg>
    </div>""", f"""
      tl.fromTo("#s9-card", {{ y: 180, rotation: -3, scale: 0.94 }}, {{ y: 0, rotation: 0, scale: 1, duration: 0.5, ease: "expo.out" }}, 0);
      tl.fromTo("#s9-h", {{ opacity: 0.85 }}, {{ opacity: 1, duration: 0.2 }}, 0);
      tl.fromTo("#s9-ad", {{ opacity: 1, scale: 2.4, rotation: -2 }}, {{ opacity: 1, scale: 1, rotation: -9, duration: 0.28, ease: "power4.in", immediateRender: false }}, at({w('vo-09', 'ad') - 0.12}));
      pen("#s9-it path", {w('vo-09', 'ad') + 0.1}, 0.3);
      // read the line under it: the camera leans to the footnote, the pen underlines it
      tl.to("#s9-cam", {{ scale: 1.35, duration: 0.7, ease: "power2.inOut", transformOrigin: "540px {C9 + fy:.0f}px" }}, at({w('vo-09', 'read')}));
      pen("#s9-ul path", {w('vo-09', 'under')}, 0.4);"""))

# S10 end card (the creator liked it as is): the spoken ask; the logo sting plays over it -------------------------
s, e = b[9], b[10]
S.append(scene("s10", s, e, f"""
    #s10-a, #s10-c {{ position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 72px; letter-spacing: -0.03em; }}
    #s10-c {{ opacity: 0; }}
    #s10-b {{ left: 0; top: 1290px; width: 1080px; text-align: center; opacity: 0; font-size: 28px; letter-spacing: 0.08em; }}""", f"""
    <div id="s10-a">Seen a demo like this?</div>
    <div id="s10-c">We'll check it.</div>
    <div id="s10-b" class="mono">Send it to @catchtheerror · we'll check it</div>
    <svg id="s10-pen" class="pen" style="left:340px;top:1326px;width:420px;height:30px" viewBox="0 0 420 30" aria-hidden="true"><path d="M6 16 C 140 10, 280 14, 414 8" style="stroke-dasharray:500;stroke-dashoffset:500;stroke-width:6" /></svg>""", f"""
      tl.fromTo("#s10-a", {{ opacity: 0.85 }}, {{ opacity: 1, duration: 0.2 }}, 0);
      blurIn("#s10-b", {w('vo-10', 'send')});
      pen("#s10-pen path", {w('vo-10', 'check')}, 0.4);
      out("#s10-a", {w('vo-10', 'well') - 0.1}, 0.12);
      blurIn("#s10-c", {w('vo-10', 'well')});"""))

shutil.copy(P.parent.parent / "brand/motion/logo-sting.html", P / "compositions/logo-sting.html")

# index.html ---------------------------------------------------------------------------------------------
hosts = "\n".join(
    f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" '
    f'data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {i + 1}"></div>'
    for i, (sid, st, d) in enumerate(S))
sting_at = b[9] + 0.05
hosts += (f'\n      <div id="sting" data-composition-id="logo-sting" data-composition-src="compositions/logo-sting.html" data-start="{sting_at:.2f}" '
          f'data-duration="{FILM - sting_at:.2f}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 50"></div>')
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
    <title>CatchTheError — Case 021: GPT-6.1 Terra, read the line under the demo</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #e7e7e5; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FILM}" data-width="1080" data-height="1920">
      <!-- Scenes, cut to the narration (SPEC.md); the logo sting plays over the end card. -->
{hosts}

      <!-- Voiceover: VoiceBox, trained voice "sparsh" (myvoice); levelled to -14 LUFS (scripts/prep_audio.py). -->
{vo}

      <!-- Music bed: "Ethernight Club", Kevin MacLeod (incompetech.com), CC BY 4.0; envelope baked in. -->
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
