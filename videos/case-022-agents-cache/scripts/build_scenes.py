"""Case 022: writes compositions/s*.html, compositions/captions.html and index.html from assets/vo/timing.json.
Every cut and cue derives from the voice's word times, so a re-voiced line only needs a rerun.

    python3 scripts/build_scenes.py [--demo] [--captions]

--demo      only s1-s3 (a quick look)
--captions  small 2-3 word captions, the reference's style (Varun Mayya's Short). Rule 16 says no subtitles; the
            creator asked for the reference's way, so this cut passes --captions; drop the flag to remove them.

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
# scene cuts: s4 is the cache explainer and spans vo-03b..vo-04c
b = [0.0] + [cut(v) for v in ("vo-02", "vo-03", "vo-03b", "vo-05", "vo-06", "vo-07", "vo-08", "vo-09", "vo-10")] + [FILM]
if DEMO:
    FILM = b[3]

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
    <div id="{pfx}-la" class="mono" style="left:110px;top:1086px;width:360px;text-align:center">Agent A</div>
    <div id="{pfx}-lb" class="mono" style="left:610px;top:1086px;width:360px;text-align:center">Agent B</div>"""


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

# cards: a real screenshot on a white card with padding, so text never touches the edge --------------------------------
PAD = 34


def card(id_, src, cw, x, y, style="", alt="", text_px=45):
    """Returns (html, card height, image scale). The image sits PAD inside the card; its size is read from the file."""
    from PIL import Image
    iw, ih = Image.open(P / "assets/shots" / src).size
    k = (cw - 2 * PAD) / iw
    ch = round(ih * k) + 2 * PAD
    return (f'<div id="{id_}" class="card" style="left:{x}px;top:{y}px;width:{cw}px;height:{ch}px;{style}">'
            f'<img src="assets/shots/{src}" alt="{alt}" data-text-px="{text_px}" style="left:{PAD}px;top:{PAD}px;width:{cw - 2 * PAD}px;height:{round(ih * k)}px" /></div>'), ch, k


def underline(id_, x, y, wdt, sw=7):
    """A pen stroke under a measured phrase (x, y = its bottom-left inside the card)."""
    return (f'<svg id="{id_}" class="pen" style="left:{x - 6:.0f}px;top:{y:.0f}px;width:{wdt + 12:.0f}px;height:20px" viewBox="0 0 {wdt + 12:.0f} 20" aria-hidden="true">'
            f'<path pathLength="1" style="stroke-width:{sw}" d="M4 12 C {wdt * 0.33:.0f} 7, {wdt * 0.66:.0f} 11, {wdt + 8:.0f} 6" /></svg>')


RB = json.loads((P / "assets/shots/r-boxes.json").read_text())   # phrase boxes in CSS px; the shots are 2.5x
DPR = 3


def box(shot, phrase, i=0):
    x, y, wdt, h = RB[shot]["boxes"][phrase][i]
    return x * DPR, y * DPR, wdt * DPR, h * DPR


def union(shot, phrase):
    rs = RB[shot]["boxes"][phrase]
    x0, y0 = min(r[0] for r in rs), min(r[1] for r in rs)
    x1, y1 = max(r[0] + r[2] for r in rs), max(r[1] + r[3] for r in rs)
    return x0 * DPR, y0 * DPR, (x1 - x0) * DPR, (y1 - y0) * DPR


# S2 the loop: two real headlines; then OpenAI's own report, its title redacted (paid off in s6) -----------------------
s, e = b[1], b[2]
t_read, t_scary = w("vo-02", "read"), w("vo-02", "scary")
h1, h1h, _ = card("s2-h1", "cover-still.png", 960, 60, 290, "opacity:0", "OfficeChai: OpenAI says its AI agents found a way to talk through the processor's cache", 52)
h2, h2h, _ = card("s2-h2", "head-vgtimes-hero.png", 1000, 40, 290 + h1h + 60, "opacity:0", "VGTimes: OpenAI AI agents found a covert channel through processor cache timing", 50)
rep, reph, rk = card("s2-rep", "r-head.png", 960, 60, 640, "opacity:0", "OpenAI misalignment report")
tx, ty, tw_, th = union("r-head", "An agent used DNS to reach an external chatbot")
BAR = f'left:{PAD + tx * rk - 8:.0f}px;top:{PAD + ty * rk - 6:.0f}px;width:{tw_ * rk + 16:.0f}px;height:{th * rk + 12:.0f}px'
S.append(scene("s2", s, e, f"""
    .bar {{ position: absolute; background: #0a0a0a; border-radius: 6px; transform-origin: 0 50%; }}
    #s2-q {{ top: 560px; color: #dd483f; opacity: 0; }}""", f"""
    {h1}
    {h2}
    <div id="s2-cam" style="position:absolute;inset:0">
      {rep[:-6]}<div id="s2-bar" class="bar" style="{BAR}"></div></div>
    </div>
    <div id="s2-q" class="mono row">[ title hidden for now ]</div>""", f"""
      tl.fromTo("#s2-h1", {{ opacity: 1, y: 160, rotation: -6, scale: 1.1 }}, {{ opacity: 1, y: 0, rotation: -1.5, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false }}, 0);
      tl.fromTo("#s2-h2", {{ opacity: 1, y: 300, rotation: 6, scale: 1.1 }}, {{ opacity: 1, y: 0, rotation: 1.2, scale: 1, duration: 0.45, ease: "expo.out", immediateRender: false }}, at({w('vo-02', 'breakout') - 0.1}));
      tl.to("#s2-h1", {{ x: -1300, rotation: -14, duration: 0.4, ease: "power3.in" }}, at({t_read - 0.3}));
      tl.to("#s2-h2", {{ x: 1300, rotation: 14, duration: 0.4, ease: "power3.in" }}, at({t_read - 0.25}));
      tl.fromTo("#s2-rep", {{ opacity: 1, y: 800, rotation: 4 }}, {{ opacity: 1, y: 0, rotation: 0, duration: 0.6, ease: "expo.out", immediateRender: false }}, at({t_read}));
      tl.fromTo("#s2-bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.3, ease: "power3.inOut", immediateRender: false }}, at({t_scary - 0.1}));
      tl.fromTo("#s2-q", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({w('vo-02', 'somewhere')}));
      tl.fromTo("#s2-cam", {{ scale: 1 }}, {{ scale: 1.12, duration: {e - t_read:.2f}, ease: "none", transformOrigin: "540px 760px", immediateRender: false }}, at({t_read}));"""))

# S3 the trick: the boxes shrink up and wire into one chip -------------------------------------------------------------
s, e = b[2], b[3]
t_both, t_share, t_proc = w("vo-03", "both"), w("vo-03", "share"), w("vo-03", "processor")
S.append(scene("s3", s, e, f"""
    #s3-chip {{ left: 330px; top: 860px; width: 420px; height: 420px; background: #121211; border-color: #f4f2ee; outline: 14px dashed #2e2e2c; outline-offset: 10px; opacity: 0;
      display: flex; align-items: center; justify-content: center; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 72px; letter-spacing: 0.1em; }}
    #s3-lc {{ top: 1340px; opacity: 0; color: #c9c9c5; }}
    #s3-wire {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }}
    #s3-wire path {{ stroke-width: 6; stroke: #f4f2ee; }}""", f"""
    {agents("s3")}
    <svg id="s3-wire" class="pen" viewBox="0 0 1080 1920" aria-hidden="true">
      <path pathLength="1" d="M290 570 C 290 760, 470 720, 470 846" />
      <path pathLength="1" d="M790 570 C 790 760, 610 720, 610 846" />
    </svg>
    <div id="s3-chip" class="box">CPU</div>
    <div id="s3-lc" class="mono row">One shared processor</div>""", f"""
      tl.fromTo("#s3-a", {{ x: 0, y: 0, scale: 1 }}, {{ x: 50, y: -310, scale: 0.62, duration: 0.6, ease: "power3.inOut" }}, 0);
      tl.fromTo("#s3-b", {{ x: 0, y: 0, scale: 1 }}, {{ x: -50, y: -310, scale: 0.62, duration: 0.6, ease: "power3.inOut" }}, 0);
      tl.to(["#s3-la", "#s3-lb"], {{ opacity: 0, duration: 0.2 }}, 0);
      tl.set(["#s3-a", "#s3-b"], {{ borderColor: "#f4f2ee" }}, 0);
      tl.set("#s3-gb-5", {{ backgroundColor: "#dd483f" }}, 0);
      tl.fromTo("#s3-chip", {{ opacity: 1, y: 500, scale: 0.9 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.6, ease: "expo.out", immediateRender: false }}, at({t_both - 0.1}));
      pen("#s3-wire path", {t_share - 0.05}, 0.4);
      tl.fromTo("#s3-lc", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, immediateRender: false }}, at({t_proc}));
      tl.to("#s3-chip", {{ scale: 1.08, duration: {e - t_proc:.2f}, ease: "none" }}, at({t_proc + 0.2}));"""))

# S4 the explainer (vo-03b..vo-04c): the cache is a shelf next to the CPU; memory is far away. -------------------------
# On the shelf = fast read; off the shelf = slow read. A kicks a block off = 1, leaves it = 0. B times reads. Bit by bit.
s, e = b[3], b[4]
N, SW, SG, SX, SY = 8, 96, 12, 114, 650
BITS = [1, 0, 1, 1, 0, 1, 0, 0]
sx = lambda i: SX + i * (SW + SG)
scx = lambda i: sx(i) + SW / 2
CPU_C, MEM_Y = (540, 438), 1155          # where a read block lands inside the CPU (under its label); a block "in memory" (centre)
dy_mem, dy_cpu = MEM_Y - (SY + SW / 2), CPU_C[1] - (SY + SW / 2)
dx_cpu = lambda i: CPU_C[0] - scx(i)
q = lambda v: f"{v:.0f}"
slots = "".join(f'<div id="x-s{i}" class="slot" style="left:{sx(i)}px"></div>' for i in range(N))
blocks = "".join(f'<div id="x-d{i}" class="blk" style="left:{sx(i) + 12}px"></div>' for i in range(N))
bitsh = "".join(f'<div id="x-b{i}" class="bit" style="left:{sx(i)}px;color:{"#dd483f" if BITS[i] else "#f4f2ee"}">{BITS[i]}</div>' for i in range(N))
mem_cells = "".join('<i></i>' for _ in range(14))
# word times
v3b, v3c, v4, v4b, v4c = "vo-03b", "vo-03c", "vo-04", "vo-04b", "vo-04c"
t_cache, t_shelf = w(v3b, "cache"), w(v3b, "shelf")
t_r1, t_off, t_r2, t_slow = w(v3c, "reads"), w(v3c, "off"), w(v3c, "reads", 2), w(v3c, "slow")
t_kick, t_one, t_leave, t_zero = w(v4, "kicks"), w(v4, "one|1"), w(v4, "leaves"), w(v4, "zero|0")
t_bagent, t_times, t_bslow, t_bfast = w(v4b, "agent"), w(v4b, "times"), w(v4b, "slow"), w(v4b, "fast")
t_bit, t_msg = w(v4c, "bit"), w(v4c, "message")


def read_fast(i, t, tag):
    """Block i zips to the CPU and back; the timer stops short (white)."""
    return f"""
      tl.set(["#x-bf", "#x-bs"], {{ scaleX: 0 }}, at({t:.2f}));
      tl.to("#x-d{i}", {{ keyframes: [{{ x: {q(dx_cpu(i))}, y: {q(dy_cpu)}, duration: 0.16, ease: "power2.in" }}, {{ x: 0, y: 0, duration: 0.2, ease: "power2.out" }}] }}, at({t:.2f}));
      tl.to("#x-bf", {{ scaleX: 0.16, duration: 0.16, ease: "none" }}, at({t:.2f}));
      tl.set(".tw", {{ opacity: 0 }}, at({t:.2f})); tl.set("#{tag}", {{ opacity: 1 }}, at({t + 0.16:.2f}));"""


def read_slow(i, t, tag, dur=0.9, back=True):
    """Block i comes up from far-away memory; the timer runs long (red)."""
    out = f"""
      tl.set(["#x-bf", "#x-bs"], {{ scaleX: 0 }}, at({t:.2f}));
      tl.set(".tw", {{ opacity: 0 }}, at({t:.2f}));
      tl.to("#x-d{i}", {{ x: {q(dx_cpu(i))}, y: {q(dy_cpu)}, opacity: 1, duration: {dur}, ease: "power1.inOut" }}, at({t:.2f}));
      tl.to("#x-bs", {{ scaleX: 1, duration: {dur}, ease: "none" }}, at({t:.2f}));
      tl.set("#{tag}", {{ opacity: 1 }}, at({t + dur:.2f}));"""
    if back:
        out += f"""
      tl.to("#x-d{i}", {{ x: 0, y: 0, duration: 0.3, ease: "power2.inOut" }}, at({t + dur + 0.15:.2f}));"""
    return out


def kick(i, t, d=0.35):
    """A kicks block i off the shelf: it drops to memory and dims."""
    return f"""
      tl.to("#x-d{i}", {{ y: {q(dy_mem)}, opacity: 0.35, duration: {d}, ease: "power2.in" }}, at({t:.2f}));"""


def bit(i, t):
    return f"""
      tl.fromTo("#x-b{i}", {{ opacity: 0, y: -30, scale: 1.4 }}, {{ opacity: 1, y: 0, scale: 1, duration: 0.25, ease: "back.out(2.4)", immediateRender: false }}, at({t:.2f}));"""


js = []
# the diagram arrives
js.append(f"""
      tl.set(["#x-bf", "#x-bs"], {{ scaleX: 0 }}, 0);
      tl.fromTo("#x-cpu", {{ y: 520, scale: 1.9 }}, {{ y: 0, scale: 1, duration: 0.6, ease: "expo.out" }}, 0);
      tl.fromTo(["#x-A", "#x-B"], {{ opacity: 0.85, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.4, ease: "power3.out" }}, 0.1);
      tl.fromTo(".slot", {{ opacity: 0, scale: 0.5 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", stagger: 0.04, immediateRender: false }}, at({t_cache - 0.15:.2f}));
      tl.fromTo(".blk", {{ opacity: 0, y: -60 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out", stagger: 0.04, immediateRender: false }}, at({t_cache + 0.05:.2f}));
      type("#x-lc", {t_cache:.2f}, 30);
      tl.fromTo("#x-plank", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.4, ease: "power3.inOut", immediateRender: false }}, at({t_shelf - 0.1:.2f}));
      tl.fromTo("#x-cpu", {{ scale: 1 }}, {{ scale: 1.06, duration: 0.25, yoyo: true, repeat: 1, immediateRender: false }}, at({w(v3b, 'fast'):.2f}));
      tl.fromTo(["#x-mem", "#x-ml"], {{ opacity: 0, y: 160 }}, {{ opacity: 1, y: 0, duration: 0.5, ease: "expo.out", immediateRender: false }}, at({w(v3b, 'memory'):.2f}));
      tl.fromTo("#x-track", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({t_r1 - 0.2:.2f}));""")
# on the shelf = fast; off the shelf = slow
js.append(read_fast(0, t_r1, "x-wf"))
js.append(kick(1, t_off))
js.append(read_slow(1, t_r2, "x-ws"))
# A sends: kick = 1, leave = 0
js.append(f"""
      tl.set(".tw", {{ opacity: 0 }}, at({L[v4]['start'] - 0.1:.2f}));
      tl.set(["#x-bf", "#x-bs"], {{ scaleX: 0 }}, at({L[v4]['start'] - 0.1:.2f}));
      tl.fromTo("#x-ca", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }}, at({w(v4, 'agent'):.2f}));
      tl.to("#x-A", {{ color: "#f4f2ee", duration: 0.1 }}, at({w(v4, 'agent'):.2f}));
      tl.to("#x-ca", {{ y: 18, duration: 0.12, yoyo: true, repeat: 1 }}, at({t_kick:.2f}));""")
# the camera follows A's cursor along the shelf (a real move every ~2 s; qa_frames failed 24.3-26.3 s without it)
js.append(f"""
      tl.to("#x-cam", {{ x: 70, duration: 0.6, ease: "power2.inOut" }}, at({t_kick - 0.3:.2f}));
      tl.to("#x-cam", {{ x: -40, duration: 0.6, ease: "power2.inOut" }}, at({t_leave - 0.1:.2f}));
      tl.to("#x-cam", {{ x: 0, y: 0, duration: 0.6, ease: "power2.inOut" }}, at({L[v4]['end'] + 0.05:.2f}));""")
js.append(kick(0, t_kick + 0.1))
js.append(bit(0, t_one))
js.append(f"""
      tl.to("#x-ca", {{ x: {SW + SG}, duration: 0.3, ease: "power3.inOut" }}, at({t_leave:.2f}));
      tl.to("#x-ca", {{ rotation: 8, duration: 0.1, yoyo: true, repeat: 3 }}, at({w(v4, 'alone'):.2f}));""")
js.append(bit(1, t_zero))
js.append(f"""
      tl.to("#x-ca", {{ opacity: 0, duration: 0.2 }}, at({L[v4]['end'] + 0.1:.2f}));
      tl.to("#x-A", {{ color: "#8c8c88", duration: 0.2 }}, at({L[v4]['end'] + 0.1:.2f}));
      tl.fromTo("#x-cb", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }}, at({t_bagent:.2f}));
      tl.to("#x-B", {{ color: "#f4f2ee", duration: 0.1 }}, at({t_bagent:.2f}));""")
# B times its reads: slot 0 (kicked) is slow = 1; slot 1 (left alone) is fast = 0
js.append(read_slow(0, t_times + 0.05, "x-ws1", dur=min(0.9, t_bslow - t_times + 0.4), back=False))
js.append(f"""
      tl.to("#x-d0", {{ x: 0, y: 0, duration: 0.25, ease: "power2.inOut" }}, at({t_bfast - 0.35:.2f}));
      tl.to("#x-cb", {{ x: {SW + SG}, duration: 0.2, ease: "power3.inOut" }}, at({t_bfast - 0.2:.2f}));""")
js.append(read_fast(1, t_bfast, "x-wf0"))
# bit by bit: the rest of the byte, fast
step = (t_msg - t_bit - 0.1) / (N - 2)
for i in range(2, N):
    t = t_bit + (i - 2) * step
    js.append(f"""
      tl.to("#x-cb", {{ x: {(SW + SG) * i}, duration: {step * 0.6:.2f}, ease: "power2.inOut" }}, at({t:.2f}));""")
    if BITS[i]:
        js.append(kick(i, t, 0.18))
    js.append(bit(i, t + step * 0.5))
js.append(f"""
      tl.set(".tw", {{ opacity: 0 }}, at({t_bit:.2f}));
      tl.to("#x-track", {{ opacity: 0, duration: 0.2 }}, at({t_bit:.2f}));
      tl.to("#x-cb", {{ opacity: 0, duration: 0.2 }}, at({t_msg - 0.1:.2f}));
      tl.fromTo("#x-msg", {{ opacity: 0, scale: 1.3 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }}, at({t_msg:.2f}));
      pen("#x-ul path", {t_msg + 0.1:.2f}, 0.35);
      tl.to("#x-Bdot", {{ backgroundColor: "#dd483f", scale: 1.5, duration: 0.2, ease: "back.out(3)" }}, at({t_msg:.2f}));
      tl.fromTo("#x-cam", {{ scale: 1 }}, {{ scale: 1.05, duration: {e - s:.2f}, ease: "none", transformOrigin: "540px 760px", immediateRender: false }}, 0);""")
S.append(scene("s4", s, e, f"""
    #x-cam {{ position: absolute; inset: 0; }}
    #x-cpu {{ left: 405px; top: 250px; width: 270px; height: 270px; border-color: #f4f2ee; text-align: center; padding-top: 30px;
      font-family: "Courier Prime", monospace; font-weight: 700; font-size: 46px; letter-spacing: 0.1em; }}
    #x-A, #x-B {{ top: 370px; display: flex; align-items: center; gap: 16px; font-size: 30px; }}
    #x-A {{ left: 84px; }} #x-B {{ right: 84px; }}
    #x-A b, #x-B b {{ display: inline-block; width: 28px; height: 28px; border-radius: 50%; background: #f4f2ee; }}
    #x-lc {{ left: {SX - 10}px; top: 550px; padding: 6px 10px; background: #0a0a0a; color: #c9c9c5; z-index: 3; }}   /* blocks pass behind it */
    .slot {{ position: absolute; top: {SY}px; width: {SW}px; height: {SW}px; border-radius: 18px; border: 3px solid #3a3a38; }}
    .blk {{ position: absolute; top: {SY + 12}px; width: {SW - 24}px; height: {SW - 24}px; border-radius: 12px; background: #f4f2ee; }}
    #x-plank {{ position: absolute; left: {SX - 14}px; top: {SY + SW + 10}px; width: {N * SW + (N - 1) * SG + 28}px; height: 10px; border-radius: 5px; background: #f4f2ee; transform-origin: 0 50%; }}
    .bit {{ position: absolute; top: {SY + SW + 40}px; width: {SW}px; text-align: center; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 64px; opacity: 0; }}
    .cur {{ position: absolute; top: {SY - 14}px; width: {SW + 28}px; height: {SW + 28}px; border-radius: 24px; opacity: 0; }}
    .cur span {{ position: absolute; left: 0; top: -44px; width: 100%; text-align: center; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 28px; }}
    #x-ca {{ left: {sx(0) - 14}px; border: 5px solid #f4f2ee; }}
    #x-cb {{ left: {sx(0) - 14}px; border: 5px dashed #f4f2ee; }}
    .tw {{ position: absolute; left: 0; top: 905px; width: 1080px; text-align: center; font-weight: 800; font-size: 104px; letter-spacing: -0.05em; opacity: 0; }}
    #x-track {{ position: absolute; left: 190px; top: 1040px; width: 700px; height: 16px; border-radius: 8px; background: #222221; overflow: hidden; opacity: 0; }}
    #x-bf, #x-bs {{ position: absolute; left: 0; top: 0; width: 100%; height: 100%; transform-origin: 0 50%; }}
    #x-bf {{ background: #f4f2ee; }} #x-bs {{ background: #dd483f; }}
    #x-mem {{ position: absolute; left: {SX}px; top: 1100px; width: {N * SW + (N - 1) * SG}px; height: 110px; border-radius: 22px; border: 3px solid #3a3a38; background: #121211;
      display: grid; grid-template-columns: repeat(14, 1fr); gap: 10px; padding: 16px; opacity: 0; }}
    #x-mem i {{ border-radius: 8px; background: #1e1e1d; }}
    #x-ml {{ left: {SX}px; top: 1236px; opacity: 0; }}
    #x-msg {{ top: 935px; color: #dd483f; font-size: 44px; opacity: 0; }}
    #x-ul {{ position: absolute; left: {SX - 10}px; top: {SY + SW + 120}px; width: {N * SW + (N - 1) * SG + 20}px; height: 20px; }}""", f"""
    <div id="x-cam">
      <div id="x-cpu" class="box">CPU</div>
      <div id="x-A" class="mono"><b></b>Agent A</div>
      <div id="x-B" class="mono">Agent B<b id="x-Bdot"></b></div>
      <div id="x-lc" class="mono">{typed("Cache · fast memory, right by the CPU")}</div>
      {slots}
      <div id="x-plank"></div>
      {blocks}
      {bitsh}
      <div id="x-ca" class="cur"><span>A</span></div>
      <div id="x-cb" class="cur"><span>B</span></div>
      <div id="x-wf" class="tw">Fast</div>
      <div id="x-ws" class="tw" style="color:#dd483f">Slow</div>
      <div id="x-ws1" class="tw"><span style="color:#dd483f">Slow</span> = 1</div>
      <div id="x-wf0" class="tw">Fast = 0</div>
      <div id="x-track"><div id="x-bf"></div><div id="x-bs"></div></div>
      <div id="x-msg" class="mono row">Message received</div>
      <svg id="x-ul" class="pen" viewBox="0 0 {N * SW + (N - 1) * SG + 20} 20" aria-hidden="true"><path pathLength="1" d="M6 12 C 300 6, 600 12, {N * SW + (N - 1) * SG + 14} 6" /></svg>
      <div id="x-mem">{mem_cells}</div>
      <div id="x-ml" class="mono">Main memory · far away</div>
    </div>""", "".join(js)))

# S5 the twist: they were asked to. The coverage's own line, pen under "asked to exchange"; "It was a test." -------------
s, e = b[4], b[5]
t_told, t_test = w("vo-05", "told"), w("vo-05", "test")
AW, AK = 940, 940 / 713     # asked.png 1893x273: line 2 = y 62..132 (crop from x 1180), line 3 = y 128.. (to "each other")
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

# S6 the real breakout, one card at a time (v3: the creator found three stacked cards too dense):
#   1) the redaction tears off the report title, pen under Sep 20  2) the proxy said no: 502 / CACHE_MISS ringed
#   3) the model's own reasoning, underlined. Each card full width, alone, with a one-line mono label above it.
s, e = b[5], b[6]
t_nobody, t_sept, t_blk, t_q, t_dns = w("vo-06", "nobody"), w("vo-06", "september"), w("vo-06", "blocked"), w("vo-06", "questions"), w("vo-06", "dns")
CW, CX = 1000, 40
c1, c1h, k1 = card("s6-c1", "r-head.png", CW, CX, 0)
c2, c2h, k2 = card("s6-c2", "r-blocked.png", CW, CX, 0, "opacity:0")
c3, c3h, k3 = card("s6-c3", "r-cot.png", CW, CX, 0, "opacity:0")
Y1, Y2, Y3 = 400, 640, 660                        # card tops (each card is alone on screen)
c1 = c1.replace("top:0px", f"top:{Y1}px"); c2 = c2.replace("top:0px", f"top:{Y2}px"); c3 = c3.replace("top:0px", f"top:{Y3}px")
BAR6 = f'left:{PAD + tx * k1 - 8:.0f}px;top:{PAD + ty * k1 - 6:.0f}px;width:{tw_ * k1 + 16:.0f}px;height:{th * k1 + 12:.0f}px'
sx_, sy_, sw_, sh_ = box("r-head", "Sep 20, 2026")
sep_ul = underline("s6-ul1", PAD + sx_ * k1, PAD + (sy_ + sh_) * k1, sw_ * k1)
mx, my, mw, mh = box("r-blocked", "CACHE_MISS")
miss_ring = ring_img("s6-r2", round(PAD + mx * k2 - 30), round(PAD + my * k2 - 24), round(mw * k2 + 60), round(mh * k2 + 48))
ux, uy, uw, uh = box("r-cot", "using publicly offered DNS services")
ax, ay, aw, ah = box("r-cot", "acceptable.")
cot_ul = underline("s6-ul3", PAD + ux * k3, PAD + (uy + uh) * k3, uw * k3) + underline("s6-ul4", PAD + ax * k3, PAD + (ay + ah) * k3, aw * k3)
S.append(scene("s6", s, e, f"""
    .bar {{ position: absolute; background: #0a0a0a; border-radius: 6px; transform-origin: 0 50%; }}
    .lbl {{ left: {CX}px; color: #c9c9c5; opacity: 0; }}
    #s6-l1 {{ top: {Y1 - 64}px; }} #s6-l2 {{ top: {Y2 - 64}px; }} #s6-l3 {{ top: {Y3 - 64}px; }}""", f"""
    <div id="s6-l1" class="mono lbl">OpenAI's own incident report</div>
    {c1[:-6]}<div id="s6-bar" class="bar" style="{BAR6}"></div>{sep_ul}</div>
    <div id="s6-l2" class="mono lbl">Its web request: blocked</div>
    {c2[:-6]}{miss_ring}</div>
    <div id="s6-l3" class="mono lbl">The model's own reasoning</div>
    {c3[:-6]}{cot_ul}</div>""", f"""
      // 1) the report again; the redaction tears away: the title was the real story
      tl.fromTo("#s6-c1", {{ y: 380, scale: 1.04 }}, {{ y: 0, scale: 1, duration: 0.5, ease: "expo.out" }}, 0);
      tl.fromTo("#s6-l1", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, 0.15);
      tl.to("#s6-bar", {{ x: 1100, rotation: 8, duration: 0.45, ease: "power3.in" }}, at({t_nobody:.2f}));
      pen("#s6-ul1 path", {t_sept:.2f}, 0.4);
      tl.to("#s6-c1", {{ scale: 1.04, duration: {t_blk - 0.3 - t_nobody:.2f}, ease: "none" }}, at({t_nobody:.2f}));
      tl.to(["#s6-c1", "#s6-l1"], {{ y: -900, opacity: 0, duration: 0.35, ease: "power3.in" }}, at({t_blk - 0.3:.2f}));
      // 2) the proxy said no
      tl.fromTo("#s6-c2", {{ opacity: 1, y: 900 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out", immediateRender: false }}, at({t_blk - 0.1:.2f}));
      tl.fromTo("#s6-l2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({t_blk + 0.1:.2f}));
      ring("#s6-r2", {w('vo-06', 'live'):.2f}, 0.45);
      tl.to("#s6-c2", {{ scale: 1.05, duration: {t_q - 0.6 - t_blk:.2f}, ease: "none" }}, at({t_blk + 0.35:.2f}));
      tl.to(["#s6-c2", "#s6-l2"], {{ y: -900, opacity: 0, duration: 0.35, ease: "power3.in" }}, at({t_q - 0.6:.2f}));
      // 3) the model talks itself into it
      tl.fromTo("#s6-c3", {{ opacity: 1, y: 900 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out", immediateRender: false }}, at({t_q - 0.4:.2f}));
      tl.fromTo("#s6-l3", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({t_q - 0.2:.2f}));
      pen("#s6-ul3 path", {t_dns - 0.3:.2f}, 0.4);
      pen("#s6-ul4 path", {t_dns + 0.15:.2f}, 0.25);
      tl.to("#s6-c3", {{ scale: 1.06, duration: {e - t_q:.2f}, ease: "none" }}, at({t_q:.2f}));"""))

# S7 the test question: its DNS query goes out; the answer comes back -------------------------------------------------
s, e = b[6], b[7]
F1Y = 330
f1, f1h, kf = card("s7-c1", "r-france.png", 960, 60, F1Y)
F2Y = F1Y + f1h + 70
f2, f2h, kp = card("s7-c2", "r-paris.png", 960, 60, F2Y, "opacity:0")
qx, qy, qw, qh = box("r-france", "'What is the capital of France [redacted]'")
px_, py_, pw_, ph_ = box("r-paris", "The capital of France is Paris.")
q_ul = underline("s7-ul", PAD + qx * kf, PAD + (qy + qh) * kf, qw * kf)
p_ring = ring_img("s7-r", round(PAD + px_ * kp - 34), round(PAD + py_ * kp - 26), round(pw_ * kp + 68), round(ph_ * kp + 52))
S.append(scene("s7", s, e, f"""
    #s7-l1 {{ top: {F1Y - 46}px; left: 60px; }} #s7-l2 {{ top: {F2Y - 50}px; left: 60px; opacity: 0; }}
""", f"""
    <div id="s7-cam" style="position:absolute;inset:0">
      <div id="s7-l1" class="mono">Out through DNS →</div>
      {f1[:-6]}{q_ul}</div>
      <div id="s7-l2" class="mono">← Back from an outside chatbot</div>
      {f2[:-6]}{p_ring}</div>
    </div>""", f"""
      tl.fromTo("#s7-c1", {{ x: 900, rotation: 4 }}, {{ x: 0, rotation: 0, duration: 0.45, ease: "expo.out" }}, 0);
      tl.fromTo("#s7-l1", {{ opacity: 0.85 }}, {{ opacity: 1, duration: 0.2 }}, 0);
      pen("#s7-ul path", {w('vo-07', 'whats') - 0.05:.2f}, 0.45);
      tl.fromTo("#s7-c2", {{ opacity: 1, x: -900, rotation: -4 }}, {{ opacity: 1, x: 0, rotation: 0, duration: 0.45, ease: "expo.out", immediateRender: false }}, at({w('vo-07', 'capital'):.2f}));
      tl.fromTo("#s7-l2", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({w('vo-07', 'capital') + 0.2:.2f}));
      ring("#s7-r", {w('vo-07', 'france') + 0.1:.2f}, 0.5);
      tl.fromTo("#s7-cam", {{ scale: 1 }}, {{ scale: 1.06, duration: {e - s:.2f}, ease: "none", transformOrigin: "540px 760px", immediateRender: false }}, 0);"""))

# S8 the clock: the real timeline; 12 min to the alarm; no auto-stop; 2.5 hours -----------------------------------------
s, e = b[7], b[8]
t1, t1h, kt1 = card("s8-c1", "timeline.png", 960, 60, 250)
n1, n1h, kn = card("s8-c2", "r-notstop.png", 960, 60, 250 + t1h + 290, "opacity:0")
ax_, ay_, aw_, ah_ = box("timeline", "10:02:11 a.m.")
alarm_ring = ring_img("s8-r1", round(PAD + ax_ * kt1 - 30), round(PAD + ay_ * kt1 - 24), round(aw_ * kt1 + 60), round(ah_ * kt1 + 48))
kx_, ky_, kw_, kh_ = union("timeline", "12:34:30 p.m.")
KILL_END = 249 * DPR          # right edge of "The run was killed." (css px 249, read off the crop; it's a separate text node)
kill_ul = underline("s8-ul1", PAD + kx_ * kt1, PAD + (ky_ + kh_) * kt1, (KILL_END - kx_) * kt1)
stop_ul = "".join(underline(f"s8-ul2{j}", PAD + bx * DPR * kn, PAD + (by + bh) * DPR * kn - 2, bw * DPR * kn) for j, (bx, by, bw, bh) in enumerate(RB["r-notstop"]["boxes"]["the run did not stop automatically as expected"]) if bw > 20)
t_alarm, t_12, t_auto, t_kept, t_two = w("vo-08", "alarm"), w("vo-08", "12|twelve"), w("vo-08", "auto|autostop"), w("vo-08", "kept"), w("vo-08", "two")
S.append(scene("s8", s, e, f"""
    #s8-n1, #s8-n2 {{ position: absolute; left: 0; top: {250 + t1h + 50}px; width: 1080px; text-align: center; font-weight: 800; font-size: 200px; letter-spacing: -0.06em; line-height: 1; opacity: 0; }}
    #s8-n2 .it {{ font-size: 1.05em; }}""", f"""
    {t1[:-6]}{alarm_ring}{kill_ul}</div>
    <div id="s8-n1">12 min</div>
    <div id="s8-n2">2.5 {it("s8-it", "hours.")}</div>
    {n1[:-6]}{stop_ul}</div>""", f"""
      tl.fromTo("#s8-c1", {{ y: 300, rotation: 2 }}, {{ y: 0, rotation: 0, duration: 0.5, ease: "expo.out" }}, 0);
      ring("#s8-r1", {t_alarm:.2f}, 0.45);
      tl.fromTo("#s8-n1", {{ opacity: 0, scale: 1.4, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out", immediateRender: false }}, at({t_12 - 0.05:.2f}));
      tl.fromTo("#s8-c2", {{ opacity: 1, y: 500 }}, {{ opacity: 1, y: 0, duration: 0.45, ease: "expo.out", immediateRender: false }}, at({t_auto - 0.2:.2f}));
      pen("#s8-ul20 path", {t_auto + 0.25:.2f}, 0.35);
      pen("#s8-ul22 path", {t_auto + 0.6:.2f}, 0.3);
      tl.to("#s8-n1", {{ opacity: 0, y: -40, duration: 0.2 }}, at({t_kept - 0.1:.2f}));
      tl.fromTo("#s8-n2", {{ opacity: 0, scale: 1.4, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "expo.out", immediateRender: false }}, at({t_two - 0.1:.2f}));
      pen("#s8-it path", {t_two + 0.5:.2f}, 0.35);
      pen("#s8-ul1 path", {t_two + 0.2:.2f}, 0.45);
      tl.fromTo("#s8-c1", {{ scale: 1 }}, {{ scale: 1.04, duration: {e - t_alarm:.2f}, ease: "none", immediateRender: false }}, at({t_alarm:.2f}));"""))

# S9 the take: a kill switch that won't flip --------------------------------------------------------------------------
s, e = b[8], b[9]
t_kill = w("vo-09", "kill")
S.append(scene("s9", s, e, f"""
    #s9-a {{ top: 330px; font-size: 84px; color: #8c8c88; }}
    #s9-b {{ top: 560px; font-size: 128px; opacity: 0; }}
    #s9-sw {{ position: absolute; left: 340px; top: 860px; width: 400px; height: 200px; border-radius: 100px; background: #1e1e1d; border: 4px solid #f4f2ee; }}
    #s9-k {{ position: absolute; left: 216px; top: 16px; width: 160px; height: 160px; border-radius: 50%; background: #f4f2ee; }}
    #s9-on {{ left: 340px; top: 1100px; width: 400px; text-align: center; color: #c9c9c5; }}""", f"""
    <div id="s9-a" class="h">The test isn't the story.</div>
    <div id="s9-b" class="h">The kill {it("s9-it", "switch")} is.</div>
    <div id="s9-sw"><div id="s9-k"></div></div>
    <div id="s9-on" class="mono">Run: still on</div>""", f"""
      tl.fromTo("#s9-a", {{ opacity: 0.85, y: 20 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, 0);
      tl.fromTo("#s9-sw", {{ y: 200, scale: 0.9 }}, {{ y: 0, scale: 1, duration: 0.5, ease: "expo.out" }}, 0);
      tl.fromTo("#s9-b", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out", immediateRender: false }}, at({w('vo-09', 'kill') - 0.3:.2f}));
      // someone flips it... it won't go off
      tl.to("#s9-k", {{ keyframes: [{{ x: -90, duration: 0.18, ease: "power2.out" }}, {{ x: -60, duration: 0.06 }}, {{ x: -100, duration: 0.06 }}, {{ x: 0, duration: 0.35, ease: "back.out(3)" }}] }}, at({t_kill:.2f}));
      tl.to("#s9-sw", {{ borderColor: "#dd483f", duration: 0.1 }}, at({t_kill + 0.5:.2f}));
      tl.to("#s9-on", {{ color: "#dd483f", duration: 0.1 }}, at({t_kill + 0.5:.2f}));
      pen("#s9-it path", {w('vo-09', 'switch') + 0.1:.2f}, 0.35);
      tl.to("#s9-k", {{ x: -60, duration: 0.15, yoyo: true, repeat: 1 }}, at({t_kill + 1.3:.2f}));"""))

# S10 end card on the logo's paper: the spoken ask; the logo sting plays over it -----------------------------------------
s, e = b[9], b[10]
S.append(scene("s10", s, e, f"""
    #root {{ background: #e7e7e5 url("assets/logo/paper-1080x1920.png") 0 0 / 1080px 1920px; color: #141414; }}
    #s10-a, #s10-c {{ position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; font-family: "Courier Prime", monospace; font-weight: 700; font-size: 72px; letter-spacing: -0.03em; }}
    #s10-c {{ opacity: 0; }}
    #s10-b {{ left: 0; top: 1290px; width: 1080px; text-align: center; opacity: 0; font-size: 28px; letter-spacing: 0.08em; color: #5f5f5c; }}""", f"""
    <div id="s10-a">Seen a clip like this?</div>
    <div id="s10-c">We'll check it.</div>
    <div id="s10-b" class="mono">Send it to @catchtheerror</div>""", f"""
      tl.fromTo("#s10-a", {{ opacity: 0.85, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.3 }}, 0);
      tl.fromTo("#s10-b", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({w('vo-10', 'send'):.2f}));
      tl.to("#s10-a", {{ opacity: 0, duration: 0.12 }}, at({w('vo-10', 'well') - 0.1:.2f}));
      tl.fromTo("#s10-c", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2, immediateRender: false }}, at({w('vo-10', 'well'):.2f}));"""))

if DEMO:
    S = S[:3]

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
