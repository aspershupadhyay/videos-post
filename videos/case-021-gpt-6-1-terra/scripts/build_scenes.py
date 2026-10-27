"""Scaffold for Case 021: writes compositions/s*.html and index.html from assets/vo/timing.json.
Every cut and cue derives from the voice's word times, so a re-voiced line only needs a rerun.

Look v4 "paper" (from logo v3): paper ground, ink type in Courier Prime Bold, OpenAI's own footage in rounded
cards, one red (#DD483F) element per scene: the pen. Moves borrowed from OpenAI's Terra film (brand/MOTION.md):
zoom-through, full-bleed shrinking into a card, typed prompt pills, an object placed inline in a sentence.
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


RED = "#dd483f"
BASE = """
    @font-face { font-family: "Courier Prime"; font-weight: 700; font-display: block; src: url("assets/fonts/CourierPrime-Bold.ttf") format("truetype"); }
    @font-face { font-family: "Courier Prime"; font-weight: 400; font-display: block; src: url("assets/fonts/CourierPrime-Regular.ttf") format("truetype"); }
    #root { position: absolute; inset: 0; overflow: hidden; background: #e7e7e5 url("assets/logo/paper-1080x1920.png") 0 0 / 1080px 1920px; color: #161616; font-family: "Courier Prime", monospace; font-weight: 700; }
    .head { position: absolute; left: 60px; top: 1150px; width: 960px; font-size: 84px; line-height: 1.0; letter-spacing: -0.03em; }
    .big { font-size: 108px; line-height: 0.98; letter-spacing: -0.04em; }
    .mono { position: absolute; font-size: 28px; letter-spacing: 0.08em; text-transform: uppercase; color: #6b6b68; font-weight: 700; }
    .credit { left: 60px; top: 192px; width: 960px; }
    .red { color: #dd483f; }
    .card { position: absolute; border-radius: 30px; overflow: hidden; background: #fff; box-shadow: 0 24px 60px rgba(20, 20, 18, 0.13); }
    .card video, .card img.fill { position: absolute; }
    .pen { position: absolute; overflow: visible; }
    .pen path { fill: none; stroke: #dd483f; stroke-width: 9; stroke-linecap: round; stroke-linejoin: round; }
    .ch { opacity: 0; }
    .pill { position: absolute; background: #fff; border-radius: 80px; padding: 26px 46px; font-size: 60px; letter-spacing: -0.02em; white-space: nowrap; box-shadow: 0 18px 50px rgba(0, 0, 0, 0.18); }
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
      const blurIn = (sel, t, d = 0.18) => tl.fromTo(sel, {{ opacity: 0, filter: "blur(10px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: d, ease: "power4.out", immediateRender: false }}, at(t));
      const out = (sel, t, d = 0.14) => tl.to(sel, {{ opacity: 0, filter: "blur(8px)", duration: d, ease: "power2.in" }}, at(t));
      const pen = (sel, t, d = 0.36) => tl.to(sel, {{ strokeDashoffset: 0, duration: d, ease: "power2.inOut" }}, at(t));
      const type = (sel, t, cps = 34) => {{ const n = document.querySelectorAll(sel + " .ch").length; tl.to(sel + " .ch", {{ opacity: 1, duration: 0.001, stagger: 1 / cps, immediateRender: false }}, at(t)); return n / cps; }};
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
    """Letters that type on one by one (each a .ch span); spaces stay normal so lines wrap at words."""
    return "".join(c if c == " " else f'<span class="ch">{c}</span>' for c in text)


def ring_img(id_, left, top, width, height, start_deg=340):
    """The logo's own hand-drawn pen circle, stretched round a target and drawn on with a conic mask."""
    m = f"conic-gradient(from {start_deg}deg at 50% 50%, #000 calc(var(--p) * 1deg), transparent calc(var(--p) * 1deg))"
    return (f'<div id="{id_}" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{height}px;--p:0;'
            f'-webkit-mask-image:{m};mask-image:{m}">'
            f'<img src="assets/logo/circle-crop.png" alt="" style="position:absolute;left:0;top:0;width:100%;height:100%" /></div>')


# Source frames are 1920x1080. A card shows a crop of it: (x0, y0, x1, y1) in source px, scaled to the card width.
def card_media(crop, cw):
    x0, y0, x1, y1 = crop
    k = cw / (x1 - x0)
    return k, round((y1 - y0) * k), f"left:{-x0 * k:.1f}px;top:{-y0 * k:.1f}px;width:{1920 * k:.1f}px;height:{1080 * k:.1f}px"


S = []
cut = lambda vid: round(L[vid]["start"] - 0.2, 2)
b = [0.0, cut("vo-02"), cut("vo-03"), cut("vo-04"), cut("vo-05"), cut("vo-06"), cut("vo-07"), cut("vo-08"),
     cut("vo-09"), cut("vo-10"), FILM]

# S1 hook: frame 0 = the toy + "This toy.*" (the cover). One photo -> one sentence -> zoom through -> the toy. ---
s, e = b[0], b[1]
k, ch, st = card_media((436, 90, 1484, 990), 1000)   # a 1000x859 window on the centre of the frame
t_photo, t_sent, t_toy = w("vo-01", "photo") - 0.06, w("vo-01", "sentence") - 0.42, w("vo-01", "designed") - 0.32
S.append(scene("s1", s, e, f"""
    #s1-card {{ left: 40px; top: 250px; width: 1000px; height: 860px; }}
    #s1-card video, #s1-card img.fill {{ {st} }}
    #s1-h1, #s1-h2, #s1-h3, #s1-photo-w, #s1-toy-w {{ opacity: 0; }}
    #s1-photo-w, #s1-toy-w, #s1-still-w {{ position: absolute; inset: 0; }}""", f"""
    <div class="mono credit">Case 021 · GPT-6.1 Terra · OpenAI's launch film</div>
    <div id="s1-card" class="card">
      <div id="s1-still-w"><img class="fill" src="assets/shots/toy-start.png" alt="A hand sets down a die-cast Lisbon tram" /></div>
      <div id="s1-photo-w">
        <img class="fill" src="assets/shots/photo-end.png" alt="" />
        <video id="s1-photo" class="clip" src="assets/footage/photo.mp4" data-start="{t_photo:.3f}" data-duration="2.0" muted playsinline></video>
      </div>
      <div id="s1-toy-w">
        <img class="fill" src="assets/shots/toy-end.png" alt="" />
        <video id="s1-toy" class="clip" src="assets/footage/toy.mp4" data-start="{t_toy:.3f}" data-duration="{min(1.63, e - t_toy):.3f}" muted playsinline></video>
      </div>
    </div>
    <div id="s1-h0" class="head big">This toy.<span class="red">*</span></div>
    <div id="s1-h1" class="head big">One photo.</div>
    <div id="s1-h2" class="head big">One sentence.</div>
    <div id="s1-h3" class="head big">This toy.<span id="s1-ast" class="red" style="display:inline-block">*</span></div>""", f"""
      // photo: blur swap on one stage
      out("#s1-still-w", {t_photo - 0.02}, 0.12);
      out("#s1-h0", {t_photo - 0.12}, 0.1);
      tl.fromTo("#s1-photo-w", {{ opacity: 0, scale: 1.04 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "power3.out", immediateRender: false }}, at({t_photo}));
      blurIn("#s1-h1", {t_photo});
      out("#s1-h1", {t_sent - 0.1}, 0.1);
      blurIn("#s1-h2", {t_sent});
      // zoom through the photo into the toy (OpenAI's push-through, faster)
      tl.to("#s1-photo-w", {{ scale: 2.6, filter: "blur(14px)", duration: 0.32, ease: "power3.in", transformOrigin: "50% 42%" }}, at({t_toy - 0.3}));
      tl.fromTo("#s1-toy-w", {{ opacity: 1, scale: 1.25, filter: "blur(12px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out", immediateRender: false }}, at({t_toy}));
      out("#s1-h2", {t_toy - 0.1}, 0.1);
      blurIn("#s1-h3", {t_toy + 0.25});
      tl.fromTo("#s1-ast", {{ scale: 2.4, rotation: -30 }}, {{ scale: 1, rotation: 0, duration: 0.4, ease: "back.out(2)", immediateRender: false }}, at({w('vo-01', 'toy')}));"""))

# S2 the demo + one tiny line, circled with the logo's pen ring --------------------------------------
BUILD = (200, 90, 1720, 990)
k, chh, st = card_media(BUILD, 1000)
fx, fy = (738 - 200) * k, (944 - 90) * k          # footnote box in card px
fw, fh = (1182 - 738) * k, (962 - 944) * k
s, e = b[1], b[2]
CARD_TOP = 330
S.append(scene("s2", s, e, f"""
    #s2-cam {{ position: absolute; inset: 0; }}
    #s2-card {{ left: 40px; top: {CARD_TOP}px; width: 1000px; height: {chh}px; }}
    #s2-card video, #s2-card img.fill {{ {st} }}
    #s2-h2 {{ opacity: 0; }}""", f"""
    <div class="mono credit">OpenAI's demo: GPT-6.1 Terra driving a 3D app</div>
    <div id="s2-cam">
      <div id="s2-card" class="card">
        <img class="fill" src="assets/shots/build-end.png" alt="" />
        <video id="s2-v" class="clip" src="assets/footage/build.mp4" data-start="0" data-duration="{min(4.95, e - s):.3f}" muted playsinline></video>
      </div>
      {ring_img("s2-ring", round(40 + fx - 62), round(CARD_TOP + fy - 40), round(fw + 80), round(fh + 68))}
    </div>
    <div id="s2-h1" class="head">One tiny line under this demo.</div>
    <div id="s2-h2" class="head">Keep your eye on it.</div>""", f"""
      tl.fromTo("#s2-card", {{ scale: 1.06, filter: "blur(8px)" }}, {{ scale: 1, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }}, 0);
      tl.fromTo("#s2-cam", {{ scale: 1 }}, {{ scale: 1.07, duration: {e - s:.2f}, ease: "none", transformOrigin: "540px {CARD_TOP + fy:.0f}px" }}, 0);
      ring("#s2-ring", {w('vo-02', 'tiny')}, 0.55);
      out("#s2-h1", {w('vo-02', 'keep') - 0.1}, 0.1);
      blurIn("#s2-h2", {w('vo-02', 'keep')});"""))

# S3 what it is: OpenAI's earth -> Lisbon zoom, full-bleed; typed prompt pills; then the world shrinks into a card ---
s, e = b[2], b[3]
t_gpt, t_chat, t_use = w("vo-03", "gpt") - 0.1, w("vo-03", "not"), w("vo-03", "built", 2)
t_shrink = w("vo-03", "computer") - 0.15
S.append(scene("s3", s, e, f"""
    #s3-world {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }}
    #s3-world video, #s3-world img {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    .row {{ position: absolute; left: 0; width: 1080px; text-align: center; }}
    .row .pill {{ position: relative; display: inline-block; }}
    #s3-r1 {{ top: 700px; }} #s3-r1 .pill {{ font-size: 76px; }}
    #s3-r2, #s3-r3 {{ top: 880px; }}
    #s3-r2, #s3-r3 {{ opacity: 0; }}
    #s3-strike {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; }}
    #s3-strike path {{ stroke-dasharray: 700; stroke-dashoffset: 700; }}
    #s3-cr {{ left: 60px; top: 1290px; color: #f4f2ee; opacity: 0.85; }}""", f"""
    <div id="s3-world">
      <img src="assets/shots/earth-end.png" alt="" />
      <video id="s3-v" class="clip" src="assets/footage/earth.mp4" data-start="0" data-duration="{min(5.12, e - s):.3f}" muted playsinline></video>
      <div id="s3-cr" class="mono">OpenAI · GPT-6.1 Terra launch film</div>
    </div>
    <div id="s3-r1" class="row"><div id="s3-p1" class="pill">{typed("GPT-6.1 Terra")}</div></div>
    <div id="s3-r2" class="row"><div id="s3-p2" class="pill">built to chat<svg id="s3-strike" class="pen" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><path d="M4 56 C 30 50, 70 52, 96 46" vector-effect="non-scaling-stroke" /></svg></div></div>
    <div id="s3-r3" class="row"><div id="s3-p3" class="pill">{typed("built to use your computer")}</div></div>""", f"""
      type("#s3-p1", {t_gpt}, 26);
      tl.fromTo("#s3-p1", {{ scale: 0.9 }}, {{ scale: 1, duration: 0.35, ease: "back.out(1.6)", immediateRender: false }}, at({t_gpt}));
      tl.fromTo("#s3-r2", {{ opacity: 0, scaleX: 0.4, filter: "blur(12px)" }}, {{ opacity: 1, scaleX: 1, filter: "blur(0px)", duration: 0.22, ease: "power3.out", immediateRender: false }}, at({t_chat}));
      pen("#s3-strike path", {w('vo-03', 'chat')}, 0.3);
      out("#s3-r2", {t_use - 0.1}, 0.1);
      tl.fromTo("#s3-r3", {{ opacity: 1 }}, {{ opacity: 1, duration: 0.01, immediateRender: false }}, at({t_use}));
      type("#s3-p3", {t_use}, 40);
      // the world shrinks into a card (OpenAI's own move)
      tl.to("#s3-world", {{ scale: 0.62, borderRadius: 48, y: -140, duration: 0.6, ease: "power2.inOut", transformOrigin: "540px 960px" }}, at({t_shrink}));
      tl.to(["#s3-r1", "#s3-r3"], {{ y: -150, scale: 0.8, duration: 0.6, ease: "power2.inOut" }}, at({t_shrink}));"""))

# S4 how: the 3D app builds the tram, then the result in ChatGPT with a push to the model -------------------
s, e = b[3], b[4]
VIEW = (470, 110, 1450, 960)
k2, ch2, st2 = card_media(VIEW, 1000)
APP = (150, 40, 1770, 1040)
k3, ch3, st3 = card_media(APP, 1000)
t_app = w("vo-04", "tram") - 0.15
S.append(scene("s4", s, e, f"""
    #s4-a {{ left: 40px; top: 250px; width: 1000px; height: {ch2}px; }}
    #s4-a video, #s4-a img.fill {{ {st2} }}
    #s4-b {{ left: 40px; top: {250 + (ch2 - ch3) // 2}px; width: 1000px; height: {ch3}px; opacity: 0; }}
    #s4-bz {{ position: absolute; inset: 0; }}
    #s4-b video, #s4-b img.fill {{ {st3} }}
    #s4-h2 {{ opacity: 0; }}""", f"""
    <div class="mono credit">OpenAI's demo · GPT-6.1 Terra at work</div>
    <div id="s4-a" class="card">
      <img class="fill" src="assets/shots/build-end.png" alt="" />
      <video id="s4-va" class="clip" src="assets/footage/build.mp4" data-start="0" data-media-start="1.8" data-duration="{min(3.1, e - s):.3f}" muted playsinline></video>
    </div>
    <div id="s4-b" class="card"><div id="s4-bz">
      <img class="fill" src="assets/shots/app-end.png" alt="" />
      <video id="s4-vb" class="clip" src="assets/footage/app.mp4" data-start="{t_app - s:.3f}" data-duration="{min(3.45, e - t_app):.3f}" muted playsinline></video>
    </div></div>
    <div id="s4-h1" class="head">It opens a 3D app.</div>
    <div id="s4-h2" class="head">Builds the tram, piece by piece.</div>""", f"""
      tl.fromTo("#s4-a", {{ scale: 0.86, borderRadius: 48 }}, {{ scale: 1, borderRadius: 30, duration: 0.45, ease: "expo.out" }}, 0);
      tl.fromTo("#s4-a", {{ filter: "blur(10px)" }}, {{ filter: "blur(0px)", duration: 0.3, ease: "power2.out" }}, 0);
      // carry across: the app card takes over, then the camera pushes to the model (OpenAI 21-22 s)
      tl.to("#s4-a", {{ opacity: 0, scale: 0.94, filter: "blur(8px)", duration: 0.22, ease: "power2.in" }}, at({t_app}));
      tl.fromTo("#s4-b", {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "expo.out", immediateRender: false }}, at({t_app}));
      tl.fromTo("#s4-bz", {{ scale: 1 }}, {{ scale: 1.55, duration: {e - t_app - 0.2:.2f}, ease: "power2.inOut", transformOrigin: "50% 62%" }}, at({t_app + 0.25}));
      out("#s4-h1", {w('vo-04', 'builds') - 0.1}, 0.1);
      blurIn("#s4-h2", {w('vo-04', 'builds')});"""))

# S5 the numbers: "Half the price. [tram] 3x faster*" (OpenAI's "Sees it. [tram] Does it." layout) -------------
s, e = b[4], b[5]
t_half, t_three = w("vo-05", "half") - 0.05, w("vo-05", "three") - 0.05
S.append(scene("s5", s, e, f"""
    #s5-a {{ position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; font-size: 112px; letter-spacing: -0.04em; }}
    #s5-am {{ left: 0; top: 470px; width: 1080px; text-align: center; }}
    #s5-tram {{ position: absolute; left: 330px; top: 540px; width: 420px; height: 420px; mix-blend-mode: multiply; -webkit-mask-image: radial-gradient(ellipse 50% 50% at 50% 52%, #000 72%, transparent 100%); mask-image: radial-gradient(ellipse 50% 50% at 50% 52%, #000 72%, transparent 100%); }}
    #s5-b {{ position: absolute; left: 0; top: 990px; width: 1080px; text-align: center; font-size: 172px; letter-spacing: -0.05em; opacity: 0; }}
    #s5-bm {{ left: 0; top: 1195px; width: 1080px; text-align: center; opacity: 0; }}
    #s5-tram {{ opacity: 0; }}""", f"""
    <div id="s5-a">{typed("Half the price.")}</div>
    <div id="s5-am" class="mono">API price vs the last Terra (GPT-5.6)</div>
    <img id="s5-tram" src="assets/shots/tram-cutout.png" alt="The die-cast tram from OpenAI's film" />
    <div id="s5-says" class="mono" style="left:0;top:950px;width:1080px;text-align:center">{typed("OpenAI says")}</div>
    <div id="s5-b">3× faster<span class="red">*</span></div>
    <div id="s5-bm" class="mono"><span class="red">*</span>OpenAI's number · vs its GPT-6 Astra and GPT-6.1 Sol</div>""", f"""
      tl.fromTo("#s5-a .ch", {{ opacity: 0.25 }}, {{ opacity: 0.25, duration: 0.01 }}, 0);
      type("#s5-a", {t_half}, 30);
      // the tram is set down like the toy in OpenAI's film
      tl.fromTo("#s5-tram", {{ opacity: 1, x: -900 }}, {{ opacity: 1, x: 0, duration: 1.5, ease: "power3.out", immediateRender: false }}, at({w('vo-05', 'terra') - 0.3}));
      type("#s5-says", {w('vo-05', 'openai')}, 24);
      // the tram drives off to the right, into the next scene
      tl.to("#s5-tram", {{ x: 1000, duration: 0.45, ease: "power3.in" }}, at({w('vo-05', 'faster')}));
      tl.fromTo("#s5-b", {{ opacity: 0, scale: 0.86, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.3, ease: "expo.out", immediateRender: false }}, at({t_three}));
      blurIn("#s5-bm", {w('vo-05', 'bigger')});"""))

# S6 the payoff: back to the demo, zoom into the real footnote, then it fills the frame in our type -------------
s, e = b[5], b[6]
fcx, fcy = 40 + fx + fw / 2, CARD_TOP + fy + fh / 2
t_zoom, t_shown, t_some = w("vo-06", "that") - 0.1, w("vo-06", "shown") - 0.12, w("vo-06", "some")
S.append(scene("s6", s, e, f"""
    #s6-cam {{ position: absolute; inset: 0; }}
    #s6-card {{ left: 40px; top: {CARD_TOP}px; width: 1000px; height: {chh}px; }}
    #s6-card video, #s6-card img.fill {{ {st} }}
    #s6-type {{ position: absolute; left: 70px; top: 600px; width: 960px; font-size: 70px; line-height: 1.02; letter-spacing: -0.04em; }}
    #s6-l2 {{ margin-top: 40px; }}
    #s6-type {{ opacity: 0; }}
    #s6-pen {{ position: absolute; left: 64px; top: 800px; width: 940px; height: 60px; }}
    #s6-pen path {{ stroke-dasharray: 1000; stroke-dashoffset: 1000; stroke-width: 11; }}
    #s6-src {{ left: 70px; top: 900px; opacity: 0; }}""", f"""
    <div class="mono credit">The line, as printed under OpenAI's demo</div>
    <div id="s6-cam">
      <div id="s6-card" class="card">
        <img class="fill" src="assets/shots/build-end.png" alt="" />
        <video id="s6-v" class="clip" src="assets/footage/build.mp4" data-start="0" data-media-start="0.6" data-duration="{min(4.3, e - s):.3f}" muted playsinline></video>
      </div>
      {ring_img("s6-ring", round(40 + fx - 62), round(CARD_TOP + fy - 40), round(fw + 80), round(fh + 68))}
    </div>
    <div id="s6-type">
      <div id="s6-l1">{typed("Shown at actual speed.")}</div>
      <div id="s6-l2">{typed("Some sections omitted.")}</div>
    </div>
    <svg id="s6-pen" class="pen" viewBox="0 0 900 60" aria-hidden="true"><path d="M6 34 C 200 24, 520 30, 880 18" /></svg>
    <div id="s6-src" class="mono">OpenAI · GPT-6.1 Terra launch film, 0:12–0:17</div>
    <div id="s6-mini" class="card" style="left:190px;top:990px;width:700px;height:{round(chh * 0.7)}px;opacity:0">
      <video id="s6-v2" class="clip" src="assets/footage/build.mp4" data-start="{t_shown + 0.2 - s:.3f}" data-media-start="1.2" data-duration="{min(3.7, e - t_shown - 0.2):.3f}" muted playsinline style="{card_media(BUILD, 700)[2]}"></video>
    </div>""", f"""
      tl.set("#s6-ring", {{ "--p": 360 }}, 0);
      // zoom into the real footnote
      tl.to("#s6-cam", {{ scale: 2.6, duration: {t_shown - t_zoom - 0.05:.2f}, ease: "power2.inOut", transformOrigin: "{fcx:.0f}px {fcy:.0f}px" }}, at({t_zoom}));
      // zoom through it: the line becomes the frame
      tl.to("#s6-cam", {{ scale: 14, opacity: 0, filter: "blur(10px)", duration: 0.3, ease: "power3.in", transformOrigin: "{fcx:.0f}px {fcy:.0f}px" }}, at({t_shown - 0.05}));
      tl.fromTo("#s6-type", {{ opacity: 1 }}, {{ opacity: 1, duration: 0.01, immediateRender: false }}, at({t_shown + 0.1}));
      type("#s6-l1", {t_shown + 0.1}, 30);
      type("#s6-l2", {t_some - 0.05}, 28);
      pen("#s6-pen path", {w('vo-06', 'omitted') + 0.15}, 0.45);
      blurIn("#s6-src", {w('vo-06', 'omitted') + 0.3});
      tl.fromTo("#s6-mini", {{ opacity: 0, y: 80, filter: "blur(8px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.45, ease: "expo.out", immediateRender: false }}, at({t_shown + 0.25}));"""))

# S7 the read: "Actual speed. Slow parts: cut." and the word "cut" is cut -----------------------------------
s, e = b[6], b[7]
t_slow, t_cut = w("vo-07", "with") - 0.05, w("vo-07", "cut")
S.append(scene("s7", s, e, f"""
    #s7-a {{ position: absolute; left: 60px; top: 600px; width: 960px; font-size: 96px; letter-spacing: -0.04em; }}
    #s7-b {{ position: absolute; left: 60px; top: 760px; width: 960px; font-size: 96px; white-space: nowrap; letter-spacing: -0.04em; opacity: 0; }}
    #s7-cut {{ position: relative; display: inline-block; }}
    #s7-c1, #s7-c2 {{ display: inline-block; }}
    #s7-c2 {{ position: absolute; left: 0; top: 0; }}
    #s7-c1 {{ clip-path: polygon(0 0, 100% 0, 100% 38%, 0 70%); }}
    #s7-c2 {{ clip-path: polygon(0 70%, 100% 38%, 100% 100%, 0 100%); }}
    #s7-slash {{ position: absolute; left: -16px; top: -6px; width: 240px; height: 120px; }}
    #s7-slash path {{ stroke-dasharray: 400; stroke-dashoffset: 400; }}""", f"""
    <div id="s7-a">Actual speed.</div>
    <div id="s7-b">Slow parts: <span id="s7-cut"><span id="s7-c1">cut.</span><span id="s7-c2">cut.</span><svg id="s7-slash" class="pen" viewBox="0 0 240 120" aria-hidden="true"><path d="M6 92 L 234 40" /></svg></span></div>""", f"""
      tl.fromTo("#s7-a", {{ opacity: 0.85, scale: 0.97 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "power3.out" }}, 0);
      blurIn("#s7-b", {t_slow});
      pen("#s7-slash path", {t_cut - 0.05}, 0.12);
      tl.to("#s7-c1", {{ x: -12, y: -10, rotation: -3, duration: 0.3, ease: "expo.out" }}, at({t_cut + 0.07}));
      tl.to("#s7-c2", {{ x: 14, y: 12, rotation: 2, duration: 0.3, ease: "expo.out" }}, at({t_cut + 0.07}));"""))

# S8 the catch: the screenshot sits in a window; the camera zooms to each sentence as it is said -----------
s, e = b[7], b[8]
t_q, t_test, t_none = w("vo-08", "three") - 0.05, w("vo-08", "thats") - 0.05, w("vo-08", "no") - 0.05
SHOT_W, WIN_H, Z = 1000, 520, 1.9
shot_h = round(500 * SHOT_W / 1750)
oy = (WIN_H - shot_h) // 2                     # shot's top inside the window


def aim(cx, cy):
    """x/y that put shot point (cx, cy) at the window centre at zoom Z (transform origin 0 0)."""
    return round(SHOT_W / 2 - cx * Z), round(WIN_H / 2 - (oy + cy) * Z)


x2, y2 = aim(764, 240)   # "tasks more than three times faster than"
x1, y1 = aim(330, 72)    # "these are OpenAI's claims, not independent results."
S.append(scene("s8", s, e, f"""
    #s8-q {{ position: absolute; left: 0; top: 300px; width: 1080px; text-align: center; font-size: 150px; letter-spacing: -0.05em; }}
    #s8-win {{ left: 40px; top: 520px; width: {SHOT_W}px; height: {WIN_H}px; }}
    #s8-zoom {{ position: absolute; left: 0; top: 0; width: {SHOT_W}px; height: {WIN_H}px; }}
    #s8-shot {{ position: absolute; left: 0; top: {oy}px; width: {SHOT_W}px; }}
    #s8-p1, #s8-p2 {{ position: absolute; left: 0; top: {oy}px; width: {SHOT_W}px; height: {shot_h}px; }}
    #s8-p1 path, #s8-p2 path {{ stroke-dasharray: 1200; stroke-dashoffset: 1200; stroke-width: 5; }}
    #s8-src {{ left: 40px; top: {520 + WIN_H + 22}px; }}
    #s8-n {{ position: absolute; left: 60px; top: 1150px; width: 960px; font-size: 76px; letter-spacing: -0.03em; opacity: 0; }}""", f"""
    <div id="s8-q">3× faster?</div>
    <div id="s8-win" class="card"><div id="s8-zoom">
      <img id="s8-shot" src="assets/shots/devto-claims.png" alt="dev.to: these are OpenAI's claims, not independent results ... Terra finishes tasks more than three times faster than Astra or Sol." />
      <svg id="s8-p1" class="pen" viewBox="0 0 {SHOT_W} {shot_h}" aria-hidden="true"><path d="M98 74 C 260 71, 440 73, 602 70" /></svg>
      <svg id="s8-p2" class="pen" viewBox="0 0 {SHOT_W} {shot_h}" aria-hidden="true"><path d="M574 248 C 700 246, 830 248, 954 245" /></svg>
    </div></div>
    <div id="s8-src" class="mono">dev.to · "OpenAI's GPT-6.1 Terra" · Oct 27 2026</div>
    <div id="s8-n">Checked outside OpenAI? <span class="red">Not yet.</span></div>
    {ring_img("s8-ring", 372, 1212, 410, 136)}""", f"""
      tl.fromTo("#s8-win", {{ opacity: 0.85, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }}, 0);
      tl.fromTo("#s8-q", {{ opacity: 0.85, scale: 1.06 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "expo.out" }}, 0);
      // zoom to the 3x sentence, then pan to "OpenAI's claims", then back out
      tl.fromTo("#s8-zoom", {{ scale: 1, x: 0, y: 0, transformOrigin: "0 0" }}, {{ scale: {Z}, x: {x2}, y: {y2}, duration: 0.6, ease: "power2.inOut", transformOrigin: "0 0", immediateRender: false }}, at({t_q}));
      pen("#s8-p2 path", {t_q + 0.55}, 0.4);
      tl.to("#s8-zoom", {{ x: {x1}, y: {y1}, duration: 0.55, ease: "power2.inOut" }}, at({t_test - 0.1}));
      pen("#s8-p1 path", {w('vo-08', 'own')}, 0.45);
      tl.to("#s8-zoom", {{ scale: 1, x: 0, y: 0, duration: 0.6, ease: "power2.inOut" }}, at({t_none - 0.2}));
      blurIn("#s8-n", {t_none});
      ring("#s8-ring", {w('vo-08', 'confirmed')}, 0.5);
      tl.to("#s8-win", {{ opacity: 0.3, scale: 0.96, duration: 0.4, ease: "power2.inOut" }}, at({w('vo-08', 'confirmed') - 0.1}));"""))

# S9 the repeatable line, with the pen under the line --------------------------------------------------------
s, e = b[8], b[9]
S.append(scene("s9", s, e, f"""
    #s9-a {{ position: absolute; left: 60px; top: 620px; width: 960px; font-size: 96px; white-space: nowrap; letter-spacing: -0.04em; }}
    #s9-b {{ position: absolute; left: 60px; top: 780px; width: 960px; font-size: 66px; white-space: nowrap; letter-spacing: -0.03em; opacity: 0; }}
    #s9-pen {{ position: absolute; left: 56px; top: 858px; width: 920px; height: 60px; }}
    #s9-pen path {{ stroke-dasharray: 1000; stroke-dashoffset: 1000; stroke-width: 11; }}""", f"""
    <div id="s9-a">A demo is an ad.</div>
    <div id="s9-b">Read the line under it.</div>
    <svg id="s9-pen" class="pen" viewBox="0 0 920 60" aria-hidden="true"><path d="M8 30 C 240 22, 600 30, 900 20" /></svg>""", f"""
      tl.fromTo("#s9-a", {{ opacity: 0.85, filter: "blur(4px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power3.out" }}, 0);
      blurIn("#s9-b", {w('vo-09', 'read')});
      pen("#s9-pen path", {w('vo-09', 'under')}, 0.4);"""))

# S10 end card: the spoken ask; the logo sting plays over it (brand/motion/logo-sting.html) ----------------------
s, e = b[9], b[10]
S.append(scene("s10", s, e, f"""
    #s10-a {{ position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; font-size: 72px; letter-spacing: -0.03em; }}
    #s10-b {{ position: absolute; left: 0; top: 1290px; width: 1080px; text-align: center; opacity: 0; }}""", f"""
    <div id="s10-a">Seen a demo like this?</div>
    <div id="s10-c" style="position:absolute;left:0;top:330px;width:1080px;text-align:center;font-size:72px;letter-spacing:-0.03em;opacity:0">We'll check it.</div>
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
