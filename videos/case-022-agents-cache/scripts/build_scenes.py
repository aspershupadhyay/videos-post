"""Case 022: writes compositions/s*.html, compositions/captions.html and index.html from assets/vo/timing.json.
Every cut and cue derives from the voice's word times, so a re-voiced line only needs a rerun.

    python3 scripts/build_scenes.py [--demo] [--captions]

--demo      only s1-s5 (the style demo, rule 15)
--captions  small 2-3 word captions, the reference's style (Varun Mayya's Short): an opt-in layer, off by default
            because rule 16 says no subtitles. The creator decides on the demo.

Look (fresh for this story, rule 15): frame 0 is the paper cover (STRATEGY.md §5), then the cover lifts off a black
world (#0A0A0A). The mechanism is drawn as a cell grid with mono labels (the reference's best idea, done our way);
the proof is OpenAI's own report, shot from the page as white printed cards. Red #DD483F is one thing only: the
secret / the leak (a red dot that travels, a red cell, the pen).
"""
import json
import re
import sys
from pathlib import Path

P = Path(__file__).resolve().parent.parent
T = json.loads((P / "assets/vo/timing.json").read_text())
L = {l["id"]: l for l in T["lines"]}
DEMO = "--demo" in sys.argv
CAPTIONS = "--captions" in sys.argv


def w(vid, word, n=1):
    """Start time of the n-th occurrence of a word in a line (case-insensitive, punctuation ignored)."""
    hits = [s for ww, s, e in L[vid]["words"] if re.sub(r"[^\w]", "", ww).lower() == word.lower()]
    return hits[n - 1]


BASE = """
    @font-face { font-family: "Inter"; font-weight: 100 900; font-display: block; src: url("assets/fonts/Inter.ttf") format("truetype"); }
    @font-face { font-family: "Instrument Serif"; font-style: italic; font-weight: 400; font-display: block; src: url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2"); }
    @font-face { font-family: "Courier Prime"; font-weight: 700; font-display: block; src: url("assets/fonts/CourierPrime-Bold.ttf") format("truetype"); }
    #root { position: absolute; inset: 0; overflow: hidden; background: #0a0a0a; color: #f4f2ee; font-family: "Inter", sans-serif; }
    .h { position: absolute; left: 76px; width: 930px; font-weight: 800; font-size: 118px; letter-spacing: -0.055em; line-height: 0.93; }
    .it { position: relative; display: inline-block; font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; color: #dd483f; letter-spacing: -0.01em; font-size: 1.12em; line-height: 0.8; padding-right: 0.06em; }
    .ul { position: absolute; left: -2%; bottom: -0.16em; width: 104%; height: 0.3em; overflow: visible; }
    .ul path { fill: none; stroke: #dd483f; stroke-width: 7; stroke-linecap: round; stroke-dasharray: 1; stroke-dashoffset: 1; }
    .mono { position: absolute; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 28px; letter-spacing: 0.14em; text-transform: uppercase; color: #8c8c88; white-space: nowrap; }
    .row { position: absolute; left: 0; width: 1080px; text-align: center; }
    .card { position: absolute; overflow: hidden; background: #fff; border-radius: 22px; box-shadow: 0 40px 90px rgba(0, 0, 0, 0.55); }
    .card img { position: absolute; left: 0; top: 0; display: block; }
    .pen { position: absolute; overflow: visible; }
    .pen path { fill: none; stroke: #dd483f; stroke-width: 8; stroke-linecap: round; stroke-linejoin: round; stroke-dasharray: 1; stroke-dashoffset: 1; }
    .box { position: absolute; border-radius: 34px; background: #121211; border: 3px solid #2e2e2c; }
    .grid { position: absolute; display: grid; }
    .cell { border-radius: 10px; background: #1e1e1d; }
    .cell.on { background: #f4f2ee; }
    .dot { position: absolute; border-radius: 50%; background: #dd483f; }
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
      const rise = (sel, t, d = 0.45) => tl.fromTo(sel, {{ opacity: 0, y: 60, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: d, ease: "expo.out", immediateRender: false }}, at(t));
      const pen = (sel, t, d = 0.36) => tl.to(sel, {{ strokeDashoffset: 0, duration: d, ease: "power2.inOut" }}, at(t));
      const type = (sel, t, cps = 34) => tl.to(sel + " .ch", {{ opacity: 1, duration: 0.001, stagger: 1 / cps, immediateRender: false }}, at(t));
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
    """The one red serif-italic word, with the pen underline inside it (pathLength 1, drawn by pen())."""
    return (f'<span class="it" id="{id_}">{text}<svg class="ul" viewBox="0 0 100 20" preserveAspectRatio="none" aria-hidden="true">'
            f'<path pathLength="1" vector-effect="non-scaling-stroke" d="M2 12 C 30 7, 66 11, 98 5" /></svg></span>')


def typed(text):
    return "".join(c if c == " " else f'<span class="ch" style="opacity:0">{c}</span>' for c in text)


def grid(id_, cols, rows, cell, gap, on, extra=""):
    """A cache grid: cells are spans with stable ids (id-N); `on` lists the lit ones."""
    cells = "".join(f'<span id="{id_}-{i}" class="cell{" on" if i in on else ""}"></span>' for i in range(cols * rows))
    return (f'<div id="{id_}" class="grid" style="grid-template-columns:repeat({cols},{cell}px);grid-auto-rows:{cell}px;'
            f'gap:{gap}px;{extra}">{cells}</div>')


def ring_img(id_, left, top, width, height, start_deg=340):
    """The logo's own hand-drawn pen circle, stretched round a target and drawn on with a conic mask."""
    m = f"conic-gradient(from {start_deg}deg at 50% 50%, #000 calc(var(--p) * 1deg), transparent calc(var(--p) * 1deg))"
    return (f'<div id="{id_}" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;height:{height}px;--p:0;'
            f'-webkit-mask-image:{m};mask-image:{m}">'
            f'<img src="assets/logo/circle-crop.png" alt="" style="position:absolute;left:0;top:0;width:100%;height:100%" /></div>')


WORDMARK = ('<div id="{id}" style="position:absolute;left:0;top:{top}px;width:1080px;text-align:center;font-family:\'Courier Prime\',monospace;'
            'font-weight:700;font-size:46px;letter-spacing:0.3em;color:#3f3f3d">CATCH · THE · <span style="position:relative;display:inline-block;'
            'color:#dd483f">E<img src="assets/logo/circle-crop.png" alt="" style="position:absolute;left:-0.44em;top:-0.36em;width:1.75em;'
            'height:1.6em" /></span>RROR</div>')

S = []
cut = lambda vid: round(L[vid]["start"] - 0.2, 2)
FILM = T["film"]
b = [0.0] + [cut(f"vo-{i:02d}") for i in range(2, 11)] + [FILM]
if DEMO:
    FILM = round(L["vo-05"]["end"] + 0.45, 2)
    b[5] = FILM

# two agent boxes (s1, carried into s3): each a sealed VM with its own lit cells -----------------------------------
A_ON, B_ON = {0, 3, 5, 6, 9, 15}, {1, 2, 7, 8, 12, 14}


def agents(pfx):
    return f"""
    <div id="{pfx}-a" class="box" style="left:110px;top:700px;width:360px;height:360px">
      {grid(f"{pfx}-ga", 4, 4, 62, 14, A_ON, "left:35px;top:35px")}
    </div>
    <div id="{pfx}-b" class="box" style="left:610px;top:700px;width:360px;height:360px">
      {grid(f"{pfx}-gb", 4, 4, 62, 14, B_ON, "left:35px;top:35px")}
    </div>
    <div id="{pfx}-la" class="mono" style="left:110px;top:1086px;width:360px;text-align:center">Agent A · VM 1</div>
    <div id="{pfx}-lb" class="mono" style="left:610px;top:1086px;width:360px;text-align:center">Agent B · VM 2</div>"""


# S1 hook. Frame 0 = the cover (paper). It lifts off; two sealed boxes; a red dot (the secret) crosses the wall. -----
s, e = b[0], b[1]
t_go = 0.32
t_sealed, t_secret = w("vo-01", "sealed"), w("vo-01", "secret")
S.append(scene("s1", s, e, f"""
    #s1-cover {{ position: absolute; inset: 0; background: #e7e7e5 url("assets/logo/paper-1080x1920.png") 0 0 / 1080px 1920px; color: #141414; z-index: 5; }}
    #s1-k {{ position: absolute; left: 76px; top: 262px; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 30px; letter-spacing: 0.12em; text-transform: uppercase; color: #5f5f5c; }}
    #s1-g {{ position: absolute; left: 76px; top: 318px; font-weight: 600; font-size: 46px; letter-spacing: -0.025em; color: #7b7b77; }}
    #s1-h {{ top: 392px; font-size: 150px; width: 960px; }}
    #s1-sub {{ position: absolute; left: 76px; top: 852px; font-weight: 700; font-size: 52px; letter-spacing: -0.025em; color: #3a3a38; }}
    #s1-cov {{ left: 150px; top: 1010px; width: 780px; height: 408px; border: 6px solid #1b1b1b; border-radius: 26px; box-shadow: 14px 16px 0 rgba(20, 20, 18, 0.10), 0 34px 70px rgba(20, 20, 18, 0.12); }}
    #s1-cov img {{ width: 768px; height: 401px; }}
    #s1-wall {{ position: absolute; left: 524px; top: 680px; width: 32px; height: 400px; border-radius: 6px;
      background: repeating-linear-gradient(-45deg, #3a3a38 0 6px, #161615 6px 14px); }}
    #s1-seal {{ top: 1170px; color: #c9c9c5; opacity: 0; }}
    #s1-dot {{ left: 272px; top: 862px; width: 36px; height: 36px; opacity: 0; }}""", f"""
    <div id="s1-world" style="position:absolute;inset:0">
    {agents("s1")}
    <div id="s1-wall"></div>
    <div id="s1-seal" class="mono row">No network · No shared file</div>
    <div id="s1-dot" class="dot"></div>
    </div>
    <div id="s1-cover">
      <div id="s1-k">Case 022 / A.I. agents</div>
      <div id="s1-g">Fact check · OpenAI's agent report</div>
      <div id="s1-h" class="h" style="color:#141414">A.I. agents broke {it("s1-it", "out?")}</div>
      <div id="s1-sub">Sealed off. Still talking. Really?</div>
      <div id="s1-cov" class="card" style="transform: rotate(-2.5deg)"><img src="assets/shots/cover-still.png" alt="OfficeChai headline: OpenAI says its AI agents found a way to talk through the processor's cache" /></div>
      {WORDMARK.format(id="s1-wm", top=1530)}
    </div>""", f"""
      tl.set("#s1-it path", {{ strokeDashoffset: 0 }}, 0);
      // the cover lifts off the black world underneath
      tl.to("#s1-cover", {{ y: -1920, duration: 0.5, ease: "power3.inOut" }}, at({t_go}));
      tl.fromTo(["#s1-a", "#s1-b"], {{ scale: 0.86, y: 80 }}, {{ scale: 1, y: 0, duration: 0.7, ease: "expo.out", stagger: 0.08 }}, at({t_go + 0.15}));
      // two sealed machines: the borders lock white, the seal line lands
      tl.to(["#s1-a", "#s1-b"], {{ borderColor: "#f4f2ee", duration: 0.12, stagger: 0.1 }}, at({t_sealed}));
      tl.fromTo(["#s1-a", "#s1-b"], {{ scale: 1.04 }}, {{ scale: 1, duration: 0.35, ease: "back.out(2)", stagger: 0.1, immediateRender: false }}, at({t_sealed}));
      rise("#s1-seal", {t_sealed + 0.25});
      // the wall slams down between them, and the camera keeps leaning in
      tl.fromTo("#s1-wall", {{ y: -1500 }}, {{ y: 0, duration: 0.35, ease: "power4.in" }}, at({t_sealed + 0.35}));
      tl.fromTo("#s1-world", {{ scale: 1 }}, {{ scale: 1.14, duration: {e - t_sealed:.2f}, ease: "sine.inOut", transformOrigin: "540px 880px", immediateRender: false }}, at({t_sealed}));
      // ...and they still passed a secret: the red dot hops the wall
      tl.fromTo("#s1-dot", {{ opacity: 0, scale: 0 }}, {{ opacity: 1, scale: 1, duration: 0.2, ease: "back.out(3)", immediateRender: false }}, at({w('vo-01', 'still')}));
      tl.to("#s1-dot", {{ keyframes: [{{ x: 250, y: -260, duration: 0.3, ease: "power2.out" }}, {{ x: 500, y: 0, duration: 0.3, ease: "power2.in" }}] }}, at({t_secret - 0.35}));
      tl.to("#s1-gb-5", {{ backgroundColor: "#dd483f", duration: 0.08 }}, at({t_secret + 0.25}));
      tl.to("#s1-dot", {{ opacity: 0, duration: 0.08 }}, at({t_secret + 0.25}));
      tl.fromTo("#s1-b", {{ x: 0 }}, {{ keyframes: [{{ x: 10, duration: 0.05 }}, {{ x: -8, duration: 0.05 }}, {{ x: 0, duration: 0.08 }}], immediateRender: false }}, at({t_secret + 0.25}));"""))

# S2 the loop: real headlines stack up; then OpenAI's own report, its title redacted (paid off in s6) --------------
s, e = b[1], b[2]
t_read, t_scary = w("vo-02", "read"), w("vo-02", "scary")
HEADS = [("officechai", 1274, 442, 880, 76, 300, -2.2), ("vgtimes", 2020, 372, 960, 60, 680, 1.6), ("hakky", 684, 314, 620, 230, 930, -1.2)]
cards, js = [], []
for n, (name, iw, ih, cw, x, y, rot) in enumerate(HEADS):
    ch = round(ih * cw / iw)
    cards.append(f'<div id="s2-h{n}" class="card" style="left:{x}px;top:{y}px;width:{cw}px;height:{ch}px;opacity:0">'
                 f'<img src="assets/shots/head-{name}.png" alt="" style="width:{cw}px;height:{ch}px" /></div>')
    t = s + 0.05 + n * 0.55
    js.append(f'tl.fromTo("#s2-h{n}", {{ opacity: 1, y: 140, rotation: {rot * 3}, scale: 1.12 }}, {{ opacity: 1, y: 0, rotation: {rot}, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false }}, at({t:.2f}));')
    js.append(f'tl.to("#s2-h{n}", {{ x: {-1300 if n % 2 == 0 else 1300}, rotation: {rot * 6}, duration: 0.4, ease: "power3.in" }}, at({t_read - 0.25 + n * 0.04:.2f}));')
RW, RH = 960, round(460 * 960 / 1498)
S.append(scene("s2", s, e, f"""
    #s2-rep {{ left: 60px; top: 660px; width: {RW}px; height: {RH}px; opacity: 0; }}
    #s2-rep img {{ width: {RW}px; height: {RH}px; }}
    #s2-bar {{ position: absolute; left: 0; top: 0; width: {RW}px; height: 130px; background: #0a0a0a; transform-origin: 0 50%; }}
    #s2-q {{ top: 1110px; color: #dd483f; opacity: 0; }}""", f"""
    {"".join(cards)}
    <div id="s2-cam" style="position:absolute;inset:0">
      <div id="s2-rep" class="card"><img src="assets/shots/report-head.png" alt="OpenAI's misalignment report, title hidden" /><div id="s2-bar"></div></div>
    </div>
    <div id="s2-q" class="mono row">[ title hidden for now ]</div>""", f"""
      {chr(10).join("      " + j for j in js)}
      tl.fromTo("#s2-rep", {{ opacity: 1, y: 700, rotation: 4 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "expo.out", immediateRender: false }}, at({t_read}));
      tl.fromTo("#s2-bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.inOut", immediateRender: false }}, at({t_scary - 0.1}));
      tl.fromTo("#s2-q", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({w('vo-02', 'somewhere')}));
      tl.fromTo("#s2-cam", {{ scale: 1 }}, {{ scale: 1.1, duration: {e - t_read:.2f}, ease: "none", transformOrigin: "540px 760px", immediateRender: false }}, at({t_read}));"""))

# S3 the trick: pull back; both boxes wire down into one chip with one shared cache ------------------------------------
s, e = b[2], b[3]
t_both, t_share, t_proc = w("vo-03", "both"), w("vo-03", "share"), w("vo-03", "processor")
CHIP_ON = {3, 10, 12, 21, 27, 30, 36, 44, 45, 51, 58, 61}
S.append(scene("s3", s, e, f"""
    #s3-chip {{ left: 220px; top: 820px; width: 640px; height: 640px; background: #121211; border-color: #f4f2ee;
      outline: 14px dashed #2e2e2c; outline-offset: 10px; opacity: 0; }}
    #s3-lc {{ top: 300px; opacity: 0; color: #c9c9c5; }}
    #s3-wire {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    #s3-wire path {{ stroke-width: 6; stroke: #f4f2ee; }}""", f"""
    {agents("s3")}
    <svg id="s3-wire" class="pen" viewBox="0 0 1080 1920" aria-hidden="true">
      <path pathLength="1" d="M290 570 C 290 700, 470 680, 470 806" />
      <path pathLength="1" d="M790 570 C 790 700, 610 680, 610 806" />
    </svg>
    <div id="s3-chip" class="box">{grid("s3-g", 8, 8, 56, 14, CHIP_ON, "left:44px;top:44px")}</div>
    <div id="s3-lc" class="mono row">One processor · one shared cache</div>""", f"""
      // carry from s1: the boxes shrink up and make room for the chip
      tl.fromTo("#s3-a", {{ x: 0, y: 0, scale: 1 }}, {{ x: 50, y: -310, scale: 0.62, duration: 0.6, ease: "power3.inOut" }}, 0);
      tl.fromTo("#s3-b", {{ x: 0, y: 0, scale: 1 }}, {{ x: -50, y: -310, scale: 0.62, duration: 0.6, ease: "power3.inOut" }}, 0);
      tl.to(["#s3-la", "#s3-lb"], {{ opacity: 0, duration: 0.2 }}, 0);
      tl.set(["#s3-a", "#s3-b"], {{ borderColor: "#f4f2ee" }}, 0);
      tl.set("#s3-gb-5", {{ backgroundColor: "#dd483f" }}, 0);
      tl.fromTo("#s3-chip", {{ opacity: 1, y: 500, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "expo.out", immediateRender: false }}, at({t_both - 0.1}));
      pen("#s3-wire path", {t_share - 0.05}, 0.4);
      tl.fromTo("#s3-lc", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, immediateRender: false }}, at({t_proc}));
      tl.fromTo("#s3-g .cell", {{ scale: 0.6 }}, {{ scale: 1, duration: 0.3, ease: "back.out(2)", stagger: {{ each: 0.008, from: "center", grid: [8, 8] }}, immediateRender: false }}, at({t_proc}));
      tl.to("#s3-chip", {{ scale: 1.06, duration: {e - t_proc:.2f}, ease: "none" }}, at({t_proc + 0.3}));"""))

# S4 how it talks: zoom into the cache; A evicts cells; B times its reads; fast / slow / fast; bits = a message ------
s, e = b[3], b[4]
COLS, CELL, GAP, GX, GY = 6, 130, 22, 95, 520
ROW = 2
BITS = [0, 1, 0, 1, 1, 0]
G_ON = {0, 2, 5, 7, 9, 19, 20, 22} | {ROW * COLS + i for i in range(COLS)}
t_kick, t_times = w("vo-04", "kicks"), w("vo-04", "times")
t_f1, t_sl, t_f2, t_msg = w("vo-04", "fast"), w("vo-04", "slow"), w("vo-04", "fast", 2), w("vo-04", "message")
probe_t = [t_f1, t_sl, t_f2, t_f2 + 0.35, t_f2 + 0.6, t_f2 + 0.85]
cx = lambda i: GX + i * (CELL + GAP)
ry = GY + ROW * (CELL + GAP)
labels = "".join(f'<div id="s4-l{i}" class="mono" style="left:{cx(i) - 20}px;top:{ry + CELL + 26}px;width:{CELL + 40}px;text-align:center;'
                 f'color:{"#dd483f" if BITS[i] else "#f4f2ee"};opacity:0">{"slow" if BITS[i] else "fast"}</div>' for i in range(3))
bars = "".join(f'<div id="s4-t{i}" style="position:absolute;left:{cx(i) + 14}px;top:{ry + CELL - 24}px;width:{(CELL - 28) * (0.92 if BITS[i] else 0.28):.0f}px;'
               f'height:12px;border-radius:6px;background:{"#dd483f" if BITS[i] else "#0a0a0a"};transform-origin:0 50%;transform:scaleX(0)"></div>' for i in range(COLS))
bits = "".join(f'<span id="s4-b{i}" style="display:inline-block;width:{CELL + GAP}px;opacity:0;color:{"#dd483f" if BITS[i] else "#f4f2ee"}">{BITS[i]}</span>' for i in range(COLS))
evict = [f"#s4-g-{ROW * COLS + i}" for i in range(COLS) if BITS[i]]
js4 = [f'tl.to("#s4-probe", {{ x: {cx(i) - cx(0)}, duration: 0.12, ease: "power2.out" }}, at({t:.2f}));'
       f'tl.to("#s4-t{i}", {{ scaleX: 1, duration: {0.35 if BITS[i] else 0.1}, ease: "power1.out" }}, at({t:.2f}));' for i, t in enumerate(probe_t)]
js4 += [f'tl.fromTo("#s4-l{i}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: 0.2, ease: "power3.out", immediateRender: false }}, at({probe_t[i]:.2f}));' for i in range(3)]
js4 += [f'tl.fromTo("#s4-b{i}", {{ opacity: 0, y: -60 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "back.out(2)", immediateRender: false }}, at({t_msg - 0.3 + i * 0.05:.2f}));' for i in range(COLS)]
S.append(scene("s4", s, e, f"""
    #s4-cam {{ position: absolute; inset: 0; }}
    #s4-g .cell {{ border-radius: 16px; }}
    #s4-row {{ position: absolute; left: {GX - 26}px; top: {ry - 26}px; width: {COLS * CELL + (COLS - 1) * GAP + 52}px; height: {CELL + 52}px; border-radius: 30px; border: 3px solid #3a3a38; }}
    #s4-probe {{ position: absolute; left: {GX - 10}px; top: {ry - 10}px; width: {CELL + 20}px; height: {CELL + 20}px; border-radius: 22px; border: 5px solid #f4f2ee; opacity: 0; }}
    #s4-A, #s4-B {{ top: 390px; display: flex; align-items: center; gap: 18px; }}
    #s4-A {{ left: 95px; }} #s4-B {{ right: 95px; }}
    #s4-A i, #s4-B i {{ display: inline-block; width: 30px; height: 30px; border-radius: 50%; background: #f4f2ee; }}
    #s4-bits {{ position: absolute; left: {GX}px; top: 1150px; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 110px; text-align: center; }}
    #s4-bits span {{ text-align: center; margin-left: {-GAP // 2}px; }}""", f"""
    <div id="s4-cam">
      <div id="s4-A" class="mono"><i></i>Agent A</div>
      <div id="s4-B" class="mono">Agent B<i id="s4-Bdot"></i></div>
      {grid("s4-g", COLS, 4, CELL, GAP, G_ON, f"left:{GX}px;top:{GY}px")}
      <div id="s4-row"></div>
      {bars}
      <div id="s4-probe"></div>
      {labels}
      <div id="s4-bits">{bits}</div>
    </div>""", f"""
      // zoom in from the chip: the grid arrives big
      tl.fromTo("#s4-cam", {{ scale: 0.55, y: 140 }}, {{ scale: 1, y: 0, duration: 0.6, ease: "expo.out" }}, 0);
      // the other rows step back so the one being used reads
      tl.to("{', '.join(f'#s4-g-{i}' for i in range(24) if i // COLS != ROW)}", {{ opacity: 0.3, duration: 0.3 }}, at({t_kick - 0.2}));
      // A kicks data out: the '1' cells go dark
      tl.to("#s4-A", {{ color: "#f4f2ee", scale: 1.15, duration: 0.15 }}, at({t_kick}));
      tl.to({json.dumps(evict)}, {{ backgroundColor: "#1e1e1d", scale: 0.8, duration: 0.18, stagger: 0.12, ease: "power3.in" }}, at({t_kick + 0.1}));
      tl.to("#s4-A", {{ color: "#8c8c88", scale: 1, duration: 0.2 }}, at({t_times - 0.3}));
      // B times its reads: a probe walks the row; fast reads get a short bar, slow (evicted) ones a long red bar
      tl.to("#s4-B", {{ color: "#f4f2ee", scale: 1.15, duration: 0.15, transformOrigin: "100% 50%" }}, at({t_times}));
      tl.fromTo("#s4-probe", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.2, immediateRender: false }}, at({t_times + 0.1}));
      {chr(10).join("      " + j for j in js4)}
      // that's a message
      tl.to("#s4-probe", {{ opacity: 0, duration: 0.2 }}, at({t_msg - 0.35}));
      tl.to("#s4-Bdot", {{ backgroundColor: "#dd483f", scale: 1.5, duration: 0.2, ease: "back.out(3)" }}, at({t_msg}));
      tl.to("#s4-cam", {{ scale: 1.06, duration: {e - t_kick:.2f}, ease: "none", transformOrigin: "540px 900px" }}, at({t_kick}));"""))

# S5 the twist: they were asked to. The coverage's own line, pen under "asked to"; "It was a test." -----------------
s, e = b[4], b[5]
t_told, t_test = w("vo-05", "told"), w("vo-05", "test")
# asked.png 1893x273, line 2 = y 62..132; crop A = "The agents were then asked to exchange" (x 1180..1893), crop B = line 3 start
AW, AK = 940, 940 / 713
S.append(scene("s5", s, e, f"""
    #s5-h {{ top: 330px; }}
    #s5-card {{ left: 50px; top: 760px; width: 980px; height: 300px; }}
    #s5-l1, #s5-l2 {{ position: absolute; left: 20px; width: {AW}px; overflow: hidden; }}
    #s5-l1 {{ top: 40px; height: {70 * AK:.0f}px; }} #s5-l2 {{ top: {50 + 70 * AK:.0f}px; height: {70 * AK:.0f}px; width: {545 * AK:.0f}px; }}
    #s5-l1 img {{ left: {-1180 * AK:.0f}px; top: {-62 * AK:.0f}px; width: {1893 * AK:.0f}px; height: {273 * AK:.0f}px; }}
    #s5-l2 img {{ left: 0; top: {-128 * AK:.0f}px; width: {1893 * AK:.0f}px; height: {273 * AK:.0f}px; }}
    #s5-ul {{ left: {20 + 350 * AK:.0f}px; top: {40 + 66 * AK:.0f}px; width: {335 * AK:.0f}px; height: 24px; }}""", f"""
    <div id="s5-h" class="h">It was a {it("s5-it", "test.")}</div>
    <div id="s5-card" class="card">
      <div id="s5-l1"><img src="assets/shots/asked.png" alt="The agents were then asked to exchange" /></div>
      <div id="s5-l2"><img src="assets/shots/asked.png" alt="synthetic secrets with each other" /></div>
      <svg id="s5-ul" class="pen" viewBox="0 0 {335 * AK:.0f} 24" aria-hidden="true"><path pathLength="1" d="M24 14 C {120 * AK:.0f} 9, {220 * AK:.0f} 13, {331 * AK:.0f} 7" /></svg>
    </div>""", f"""
      tl.fromTo("#s5-card", {{ y: 260, rotation: 3, scale: 0.9 }}, {{ y: 0, rotation: -1, scale: 1, duration: 0.5, ease: "expo.out" }}, 0);
      tl.fromTo("#s5-h", {{ opacity: 0.85, y: -20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, 0);
      pen("#s5-ul path", {t_told}, 0.4);
      tl.to("#s5-card", {{ scale: 1.05, duration: {e - t_told:.2f}, ease: "power1.inOut", transformOrigin: "50% 50%" }}, at({t_told}));
      pen("#s5-it path", {t_test + 0.1}, 0.3);"""))

# captions (opt-in): the reference's style, 2-3 words, small, mid-frame, on a dark chip -------------------------------
if CAPTIONS:
    groups = []
    for l in T["lines"]:
        if l["start"] >= FILM:
            break
        cues = json.loads((P / f"assets/vo/raw/subs/{l['take']}.subs.json").read_text())["cues"]
        groups += [(l["start"] + c["s"], min(l["start"] + c["e"], FILM), c["text"]) for c in cues]
    body = "".join(f'<div id="c{i}" class="cap" style="opacity:0"><span>{txt}</span></div>' for i, (st, en, txt) in enumerate(groups))
    js = "".join(f'tl.set("#c{i}", {{ opacity: 1, visibility: "visible" }}, {max(st, 0.15):.3f}); tl.set("#c{i}", {{ opacity: 0, visibility: "hidden" }}, {en:.3f});\n      '
                 for i, (st, en, txt) in enumerate(groups))
    (P / "compositions/captions.html").write_text(f"""<template>
  <style>
    @font-face {{ font-family: "Inter"; font-weight: 100 900; font-display: block; src: url("assets/fonts/Inter.ttf") format("truetype"); }}
    #root {{ position: absolute; inset: 0; overflow: visible; background: transparent; }}
    .cap {{ position: absolute; left: 0; top: 1300px; width: 1080px; text-align: center; }}
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
if not DEMO:
    sting_at = b[9] + 0.05
    hosts += (f'\n      <div id="sting" data-composition-id="logo-sting" data-composition-src="compositions/logo-sting.html" data-start="{sting_at:.2f}" '
              f'data-duration="{FILM - sting_at:.2f}" data-track-index="2" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: 50"></div>')
if CAPTIONS:
    hosts += (f'\n      <div id="caps" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" '
              f'data-duration="{FILM}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index: 60"></div>')
vo = "\n".join(
    f'      <audio id="{l["id"]}" class="clip" src="assets/vo/{l["id"]}.wav" data-start="{l["start"]}" data-duration="{l["duration"]}" '
    f'data-track-index="10" data-volume="1" data-audio-group="voiceover"></audio>' for l in T["lines"] if l["start"] < FILM)
old = (P / "index.html").read_text()
sfx = re.search(r"(      <!-- SFX:BEGIN.*?<!-- SFX:END -->)", old, re.S)
sfx = sfx.group(1) if sfx else "      <!-- SFX:BEGIN (generated by scripts/build_sfx.py from scripts/sfx_cues.json) -->\n      <!-- SFX:END -->"
(P / "index.html").write_text(f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>CatchTheError — Case 022: the A.I. agents' "secret channel" was a test</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0a0a0a; }}
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
