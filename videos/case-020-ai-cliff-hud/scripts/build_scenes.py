"""One-time scaffold for Case 020: writes compositions/*.html and index.html from assets/vo/timing.json.
Edit the HTML directly after the first build (Studio edits live there); rerun only to rebuild from new voice timings.
Reusable pattern for the next case: shared type system, panel + credit layout, red-pen helper, research-card scene."""
import json
from pathlib import Path
P = Path(__file__).resolve().parent.parent
T = json.loads((P / "assets/vo/timing.json").read_text())
FILM = T["film"]
L = {l["id"]: l for l in T["lines"]}

def icon(name, size=34, color="#f4f2ee"):
    s = (P / f"assets/icons/{name}.svg").read_text()
    s = s[s.index("<svg"):]
    s = s.replace('width="24"', f'width="{size}"').replace('height="24"', f'height="{size}"').replace("currentColor", color)
    return s.replace('class="lucide', 'aria-hidden="true" class="ic lucide')

BASE = """
    @font-face { font-family: "Geist"; font-weight: 100 900; font-display: block; src: url("assets/fonts/Geist.woff2") format("woff2"); }
    @font-face { font-family: "Geist Mono"; font-weight: 100 900; font-display: block; src: url("assets/fonts/GeistMono.woff2") format("woff2"); }
    @font-face { font-family: "Instrument Serif"; font-style: italic; font-weight: 400; font-display: block; src: url("assets/fonts/InstrumentSerif-Italic.woff2") format("woff2"); }
    #root { position: absolute; inset: 0; overflow: hidden; background: #0a0a0a; color: #f4f2ee; font-family: "Geist", sans-serif; }
    .disp { font-weight: 800; letter-spacing: -0.045em; line-height: 0.96; }
    .it { font-family: "Instrument Serif", serif; font-style: italic; font-weight: 400; letter-spacing: -0.01em; }
    .mono { font-family: "Geist Mono", monospace; font-weight: 500; font-size: 28px; letter-spacing: 0.05em; text-transform: uppercase; color: #8c8a86; }
    .panel { position: absolute; left: 0; top: 1480px; width: 1080px; height: 440px; background: #0a0a0a; }
    .head { position: absolute; left: 64px; top: 1528px; width: 952px; font-size: 84px; }
    .credit { position: absolute; left: 64px; top: 1836px; width: 952px; }
    .full { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; }
    .full video, .full img { position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }
    .pen path { fill: none; stroke: #e0502b; stroke-width: 8; stroke-linecap: round; stroke-linejoin: round; }
    .card { position: absolute; border-radius: 18px; overflow: hidden; background: #fff; }
    .card img { display: block; width: 100%; height: auto; }
    .ic { vertical-align: -6px; margin-right: 14px; }
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
      const blurIn = (sel, t, d = 0.18) => tl.fromTo(sel, {{ opacity: 0, filter: "blur(10px)", y: 14 }}, {{ opacity: 1, filter: "blur(0px)", y: 0, duration: d, ease: "power4.out", immediateRender: false }}, at(t));
      const out = (sel, t) => tl.to(sel, {{ opacity: 0, filter: "blur(8px)", duration: 0.14, ease: "power2.in" }}, at(t));
      const pen = (sel, t, d = 0.38) => tl.to(sel, {{ strokeDashoffset: 0, duration: d, ease: "power2.inOut" }}, at(t));
{js}
      tl.set({{}}, {{}}, {dur});
      window.__timelines["{sid}"] = tl;
    }})();
  </script>
</template>
"""
    (P / f"compositions/{sid}.html").write_text(html)
    return (sid, start, dur)

S = []
b = [0.0, 7.4, 10.6, 13.75, 16.7, 22.1, 27.0, 32.55, 37.6, 39.95, 43.45, FILM]

# S1 hook ---------------------------------------------------------------
s, e = b[0], b[1]
S.append(scene("s1", s, e, """
    #s1-t1 { top: 1500px; }
    #s1-t2, #s1-t3, #s1-c2 { opacity: 0; }
    #s1-n { font-variant-numeric: tabular-nums; }""", f"""
    <div id="s1-wrap" class="full"><video id="s1-v" class="clip" src="assets/footage/hook.mp4" data-start="0" data-duration="{e-s:.3f}" muted playsinline></video></div>
    <div class="panel"></div>
    <div id="s1-t1" class="head disp">AI picks every <span class="it">safe</span> step down a cliff.</div>
    <div id="s1-c1" class="credit mono">The viral clip · as posted on X</div>
    <div id="s1-t2" class="head disp"><span id="s1-n">568,000</span> views.</div>
    <div id="s1-c2" class="credit mono">X post by @CodeByPoonam · 5.2K likes · 637 reposts</div>
    <div id="s1-t3" class="head disp">Nobody checked the <span class="it">readout.</span></div>""", f"""
      tl.fromTo("#s1-wrap", {{ scale: 1 }}, {{ scale: 1.07, duration: {e-s:.2f}, ease: "none", transformOrigin: "540px 700px" }}, 0);
      out(["#s1-t1", "#s1-c1"], {L['vo-02']['start']-0.12});
      blurIn(["#s1-t2", "#s1-c2"], {L['vo-02']['start']});
      const n = {{ v: 0 }};
      tl.fromTo(n, {{ v: 0 }}, {{ v: 568000, duration: 1.1, ease: "power3.out", immediateRender: false, onUpdate: () => {{ document.querySelector("#s1-n").textContent = Math.round(n.v).toLocaleString("en-US"); }} }}, at({L['vo-02']['start']}));
      out(["#s1-t2", "#s1-c2"], {L['vo-03']['start']-0.12});
      blurIn("#s1-t3", {L['vo-03']['start']});"""))

# S2 the drop readout ----------------------------------------------------
s, e = b[1], b[2]
p = L["vo-04"]["phrases"]
S.append(scene("s2", s, e, """
    #s2-pen path { stroke-dasharray: 1100; stroke-dashoffset: 1100; }
    #s2-t2 { opacity: 0; }""", f"""
    <div id="s2-wrap" class="full">
      <video id="s2-v" class="clip" src="assets/footage/drop.mp4" data-start="0" data-duration="{e-s:.3f}" muted playsinline></video>
      <svg id="s2-pen" class="pen full" viewBox="0 0 1080 1920" aria-hidden="true"><path d="M850 832 C 975 828, 1030 880, 1022 960 C 1014 1062, 930 1094, 840 1092 C 730 1090, 668 1046, 672 962 C 676 880, 742 836, 880 834" /></svg>
    </div>
    <div class="panel"></div>
    <div id="s2-t1" class="head disp">Look at the readout.</div>
    <div id="s2-t2" class="head disp">Drop: <span class="it">over 300 meters.</span></div>
    <div class="credit mono">Overlay text in the clip: “DROP SIM &gt;300 METER”</div>""", f"""
      out("#s2-t1", {p[1]-0.1});
      blurIn("#s2-t2", {p[1]});
      tl.to("#s2-wrap", {{ scale: 1.32, duration: 0.7, ease: "expo.inOut", transformOrigin: "846px 960px" }}, at({p[2]-0.2}));
      pen("#s2-pen path", {p[2]+0.45});"""))

# S3 the scale -----------------------------------------------------------
s, e = b[2], b[3]
st = L["vo-05"]["start"]
S.append(scene("s3", s, e, """
    #s3-card { left: 40px; top: 190px; width: 1000px; }
    #s3-src { position: absolute; left: 40px; top: 300px; }
    #s3-ground { position: absolute; left: 120px; top: 1700px; width: 840px; height: 2px; background: #2a2a2a; }
    #s3-bar { position: absolute; left: 300px; top: 560px; width: 6px; height: 1140px; background: #f4f2ee; transform-origin: 50% 100%; }
    #s3-tick { position: absolute; left: 282px; top: 1681px; width: 42px; height: 19px; background: #f4f2ee; }
    #s3-top { position: absolute; left: 350px; top: 540px; }
    #s3-bot { position: absolute; left: 350px; top: 1600px; }
    .s3-big { font-size: 120px; }
    .s3-lab { margin-top: 10px; }
    #s3-pen { position: absolute; left: 40px; top: 190px; width: 1000px; height: 84px; overflow: visible; }
    #s3-pen path { stroke-dasharray: 400; stroke-dashoffset: 400; }
    #s3-top, #s3-bot, #s3-tick { opacity: 0; }""", f"""
    <div id="s3-card" class="card"><img src="assets/shots/apple-lidar.png" alt="Apple: The LiDAR Scanner measures the distance to surrounding objects up to 5 meters away" /></div>
    <svg id="s3-pen" class="pen" viewBox="0 0 1000 84" aria-hidden="true"><path d="M316 80 C 390 76, 480 79, 574 75" /></svg>
    <div id="s3-src" class="mono">Apple Newsroom · iPad Pro LiDAR Scanner · Mar 2020</div>
    <div id="s3-ground"></div>
    <div id="s3-bar"></div>
    <div id="s3-tick"></div>
    <div id="s3-top"><div class="disp s3-big">300 m</div><div class="mono s3-lab">The drop the overlay “measured”</div></div>
    <div id="s3-bot"><div class="disp s3-big"><span class="it">5 m</span></div><div class="mono s3-lab">What Apple's LiDAR reaches · to scale</div></div>""", f"""
      tl.fromTo("#s3-bar", {{ scaleY: 0.02 }}, {{ scaleY: 1, duration: 0.8, ease: "expo.out" }}, at({st}));
      blurIn("#s3-top", {st+0.35});
      tl.to("#s3-bar", {{ opacity: 0.35, duration: 0.3 }}, at({st+1.6}));
      tl.to("#s3-top", {{ opacity: 0.45, duration: 0.3 }}, at({st+1.6}));
      tl.fromTo("#s3-tick", {{ opacity: 0, scaleX: 0 }}, {{ opacity: 1, scaleX: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }}, at({st+1.7}));
      blurIn("#s3-bot", {st+1.75});
      pen("#s3-pen path", {st+1.9}, 0.32);"""))

# S4 wonderful -----------------------------------------------------------
s, e = b[3], b[4]
p = L["vo-06"]["phrases"]
S.append(scene("s4", s, e, """
    #s4-pen path { stroke-dasharray: 900; stroke-dashoffset: 900; }
    #s4-t2 { opacity: 0; }""", f"""
    <div id="s4-wrap" class="full">
      <img src="assets/shots/wonderful.png" alt="Frame from the viral clip: WONDERFUL, DROP SIM >300 METER" />
      <svg id="s4-pen" class="pen full" viewBox="0 0 1080 1920" aria-hidden="true"><path d="M168 522 C 360 512, 640 518, 918 508" /></svg>
    </div>
    <div class="panel"></div>
    <div id="s4-t1" class="head disp">No sensor on Earth writes…</div>
    <div id="s4-t2" class="head disp"><span class="it">“Wonderful.”</span></div>
    <div class="credit mono">Frame from the viral clip</div>""", f"""
      tl.fromTo("#s4-wrap", {{ scale: 1 }}, {{ scale: 1.1, duration: {e-s:.2f}, ease: "none", transformOrigin: "540px 440px" }}, 0);
      out("#s4-t1", {p[1]-0.1});
      blurIn("#s4-t2", {p[1]});
      pen("#s4-pen path", {p[1]+0.1});"""))

# S5 the post names nothing ---------------------------------------------
s, e = b[4], b[5]
p = L["vo-07"]["phrases"]
rows = [("company", "Company", "not named", p[0]+0.95), ("paper", "Paper", "none cited", p[1]), ("device", "Device", "none shown", p[2]), ("search", "Our search", "nothing", p[3])]
rows_html = "\n".join(f'    <div id="s5-r-{k}" class="s5-row" style="top:{1170+i*120}px"><span class="mono s5-k">{lab}</span><span class="disp s5-v">{val}</span></div>' for i, (k, lab, val, t) in enumerate(rows))
S.append(scene("s5", s, e, f"""
    #s5-post {{ position: absolute; left: 150px; top: 150px; width: 780px; border-radius: 22px; overflow: hidden; border: 1px solid #2a2a2a; }}
    #s5-post img {{ display: block; width: 780px; }}
    .s5-row {{ position: absolute; left: 150px; width: 780px; height: 100px; border-top: 1px solid #2a2a2a; display: flex; align-items: center; justify-content: space-between; opacity: 0; }}
    .s5-k {{ font-size: 28px; }}
    .s5-v {{ font-size: 58px; }}
    #s5-pen {{ position: absolute; left: 600px; top: 1505px; width: 360px; height: 120px; overflow: visible; }}
    #s5-pen path {{ stroke-dasharray: 900; stroke-dashoffset: 900; }}""", f"""
    <div id="s5-post"><img src="assets/shots/x-post.png" alt="X post by Poonam Soni: AI uses Cameras and Lidars to spot dangerous rock slopes. 568K views" /></div>
{rows_html}
    <svg id="s5-pen" class="pen" viewBox="0 0 360 120" aria-hidden="true"><path d="M190 14 C 300 8, 352 40, 344 66 C 334 104, 200 112, 110 104 C 40 98, 14 72, 30 44 C 50 16, 140 10, 230 16" /></svg>""",
    "\n".join(f'      blurIn("#s5-r-{k}", {t:.3f});' for k, _, _, t in rows) + f"""
      tl.fromTo("#s5-post", {{ scale: 1 }}, {{ scale: 1.04, duration: {e-s:.2f}, ease: "none", transformOrigin: "540px 600px" }}, 0);
      pen("#s5-pen path", {p[4]});"""))

# S6 the twist (white) ----------------------------------------------------
s, e = b[5], b[6]
p = L["vo-08"]["phrases"]
S.append(scene("s6", s, e, """
    #root { background: #fafafa; color: #0a0a0a; }
    #s6-a { position: absolute; left: 80px; top: 560px; font-size: 52px; font-weight: 600; letter-spacing: -0.02em; color: #6b6965; }
    #s6-b { position: absolute; left: 80px; top: 680px; width: 920px; font-size: 132px; }
    #s6-c { position: absolute; left: 80px; top: 1010px; width: 920px; font-size: 132px; }
    #s6-b, #s6-c { opacity: 0; }""", f"""
    <div id="s6-a">Here's the twist.</div>
    <div id="s6-b" class="disp">The real AI exists.</div>
    <div id="s6-c" class="disp">It just doesn't <span class="it">walk with you.</span></div>""", f"""
      tl.fromTo("#s6-a", {{ opacity: 0.35 }}, {{ opacity: 1, duration: 0.25, immediateRender: false }}, at({p[0]}));
      blurIn("#s6-b", {p[1]});
      blurIn("#s6-c", {p[2]});"""))

# S7 + S8 the real research ------------------------------------------------
def research(sid, s, e, ic, where, head, fig_a, alt_a, credit_a, t_fig, fig_b=None, alt_b="", credit_b="", t_b=None, push_origin="540px 900px"):
    cssb = f"#{sid}-fb, #{sid}-cb {{ opacity: 0; }}" if fig_b else ""
    body = f"""
    <div id="{sid}-where" class="mono" style="position:absolute;left:60px;top:120px;color:#f4f2ee">{icon(ic)}{where}</div>
    <div id="{sid}-head" class="card" style="left:60px;top:190px;width:960px"><img src="assets/shots/{head}" alt="Paper header" /></div>
    <div id="{sid}-figs" style="position:absolute;left:40px;top:{"560" if sid=="s7" else "600"}px;width:1000px">
      <div id="{sid}-fa" class="card" style="position:absolute;left:0;top:0;width:1000px"><img src="assets/shots/{fig_a}" alt="{alt_a}" /></div>
      {f'<div id="{sid}-fb" class="card" style="position:absolute;left:0;top:0;width:1000px"><img src="assets/shots/{fig_b}" alt="{alt_b}" /></div>' if fig_b else ''}
    </div>
    <div id="{sid}-ca" class="credit mono">{credit_a}</div>
    {f'<div id="{sid}-cb" class="credit mono">{credit_b}</div>' if fig_b else ''}"""
    js = f"""
      tl.fromTo("#{sid}-head", {{ scale: 1 }}, {{ scale: 1.03, duration: {e-s:.2f}, ease: "none" }}, 0);
      tl.fromTo("#{sid}-fa", {{ opacity: 0, y: 80, filter: "blur(10px)" }}, {{ opacity: 1, y: 0, filter: "blur(0px)", duration: 0.5, ease: "expo.out", immediateRender: false }}, at({t_fig}));
      tl.fromTo("#{sid}-figs", {{ scale: 1 }}, {{ scale: 1.08, duration: {e-t_fig:.2f}, ease: "none", transformOrigin: "{push_origin}" }}, at({t_fig}));"""
    if fig_b:
        js += f"""
      tl.fromTo("#{sid}-fb", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, immediateRender: false }}, at({t_b}));
      tl.to("#{sid}-ca", {{ opacity: 0, duration: 0.15 }}, at({t_b}));
      tl.fromTo("#{sid}-cb", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, immediateRender: false }}, at({t_b}));"""
    return scene(sid, s, e, cssb, body, js)

S.append(research("s7", b[6], b[7], "cctv", "Chongqing, China · Scientific Reports · Jul 2026", "ptz-head.png",
                  "p9.png", "Fig. 9: PTZ camera frames tracking falling rocks on a slope",
                  "Fig. 9 · Huang et al., Sci. Rep. 16, 19993 (2026) · CC BY-NC-ND 4.0", b[6] + 0.9, push_origin="280px 300px"))
S.append(research("s8", b[7], b[8], "drone", "Hong Kong · Nature Communications · Aug 2025", "drone-head.png",
                  "drone-fig2.png", "Fig. 2: the LiDAR quadrotor and its mapping system",
                  "Fig. 2 · Liu et al., Nat. Commun. 16, 7411 (2025) · CC BY-NC-ND 4.0", b[7] + 0.35,
                  "drone-fig1.png", "Fig. 1: landslide, debris-resisting barriers, dense vegetation",
                  "Fig. 1 · Liu et al., Nat. Commun. 16, 7411 (2025) · CC BY-NC-ND 4.0", L["vo-10"]["end"] - 1.45, push_origin="300px 300px"))

# S9 edit vs research ---------------------------------------------------
s, e = b[8], b[9]
p = L["vo-11"]["phrases"]
S.append(scene("s9", s, e, """
    .s9-box { position: absolute; left: 40px; width: 1000px; height: 700px; border-radius: 20px; overflow: hidden; background: #fff; }
    #s9-b1 { top: 110px; background: #000; }
    #s9-b1 video { position: absolute; left: 0; top: -350px; width: 1000px; height: 1778px; }
    #s9-b2 { top: 980px; }
    #s9-b2 img { position: absolute; left: 75px; top: 0; height: 700px; width: auto; }
    .s9-l { position: absolute; left: 40px; font-size: 64px; }
    #s9-l1 { top: 830px; } #s9-l2 { top: 1700px; }
    #s9-l2 { opacity: 0; } #s9-b2 { opacity: 0.25; }""", f"""
    <div id="s9-b1" class="s9-box"><video id="s9-v" class="clip" src="assets/footage/walk.mp4" data-start="0" data-duration="{e-s:.3f}" muted playsinline></video></div>
    <div id="s9-l1" class="s9-l disp">Less cinematic</div>
    <div id="s9-b2" class="s9-box"><img src="assets/shots/p9.png" alt="Fig. 9 from Huang et al. 2026" /></div>
    <div id="s9-l2" class="s9-l disp"><span class="it">Actually real.</span></div>""", f"""
      tl.to("#s9-b1", {{ opacity: 0.35, duration: 0.3 }}, at({p[1]-0.05}));
      tl.to("#s9-b2", {{ opacity: 1, duration: 0.3 }}, at({p[1]-0.05}));
      blurIn("#s9-l2", {p[1]});"""))

# S10 the line (white) -----------------------------------------------------
s, e = b[9], b[10]
p = L["vo-12"]["phrases"]
S.append(scene("s10", s, e, """
    #root { background: #fafafa; color: #0a0a0a; }
    #s10-a { position: absolute; left: 80px; top: 620px; width: 920px; font-size: 120px; }
    #s10-b { position: absolute; left: 80px; top: 1010px; width: 920px; font-size: 120px; opacity: 0; }
    #s10-pen { position: absolute; left: 76px; top: 1196px; width: 260px; height: 60px; overflow: visible; }
    #s10-pen path { stroke-dasharray: 500; stroke-dashoffset: 500; }""", f"""
    <div id="s10-a" class="disp">If the AI looks like a movie,</div>
    <div id="s10-b" class="disp">it's probably an<br /><span class="it">edit.</span></div>
    <svg id="s10-pen" class="pen" viewBox="0 0 400 60" aria-hidden="true"><path d="M6 30 C 80 24, 170 27, 252 20" /></svg>""", f"""
      tl.fromTo("#s10-a", {{ opacity: 0.4 }}, {{ opacity: 1, duration: 0.25, immediateRender: false }}, at({p[0]}));
      blurIn("#s10-b", {p[1]});
      pen("#s10-pen path", {p[1]+0.55}, 0.3);"""))

# S11 end card ------------------------------------------------------------
s, e = b[10], b[11]
p = L["vo-13"]["phrases"]
end = (P.parent / "case-018-kimi-k3-1-pro/compositions/s9-end.html").read_text()
mark = end[end.index("<svg"):end.index("</svg>") + 6].replace("s9-", "s11-")
S.append(scene("s11", s, e, """
    #s11-mark { position: absolute; left: 315px; top: 470px; width: 450px; height: 450px; overflow: visible; }
    #s11-line { position: absolute; left: 0; top: 960px; width: 1080px; text-align: center; font-size: 52px; font-weight: 600; letter-spacing: -0.02em; color: #8c8a86; }
    #s11-word { position: absolute; left: 0; top: 1040px; width: 1080px; text-align: center; font-size: 124px; }
    #s11-handle { position: absolute; left: 0; top: 1200px; width: 1080px; text-align: center; font-size: 32px; color: #f4f2ee; }
    #s11-ring { stroke-dasharray: 942.48; stroke-dashoffset: 942.48; }
    #s11-glint, #s11-bug, #s11-handle-g, #s11-word, #s11-handle { opacity: 0; }""", f"""
    {mark}
    <div id="s11-line">We read the fine print.</div>
    <div id="s11-word" class="disp">Catch the Error</div>
    <div id="s11-handle" class="mono">@catchtheerror</div>""", f"""
      tl.to("#s11-ring", {{ strokeDashoffset: 0, duration: 0.5, ease: "power2.inOut" }}, at({s+0.05}));
      tl.fromTo("#s11-bug", {{ opacity: 1, y: -380 }}, {{ opacity: 1, y: 0, duration: 0.28, ease: "power4.in", immediateRender: false }}, at({s+0.3}));
      tl.fromTo("#s11-handle-g", {{ opacity: 1, rotation: -150, svgOrigin: "214 214" }}, {{ opacity: 1, rotation: 0, svgOrigin: "214 214", duration: 0.5, ease: "expo.out", immediateRender: false }}, at({s+0.5}));
      tl.fromTo("#s11-glint", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.12, immediateRender: false }}, at({s+0.8}));
      blurIn("#s11-word", {p[1]}, 0.22);
      blurIn("#s11-handle", {p[1]+0.9});
      tl.fromTo("#s11-mark", {{ scale: 1 }}, {{ scale: 1.04, duration: {e-s:.2f}, ease: "none" }}, 0);"""))

# index -------------------------------------------------------------------
hosts = "\n".join(f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" data-duration="{d}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920" style="z-index: {i+1}"></div>' for i, (sid, st, d) in enumerate(S))
vo = "\n".join(f'      <audio id="{l["id"]}" class="clip" src="assets/vo/{l["id"]}.wav" data-start="{l["start"]}" data-duration="{l["duration"]}" data-track-index="10" data-volume="1" data-audio-group="voiceover"></audio>' for l in T["lines"])
idx = f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>CatchTheError — Case 020: the AI that picks your steps</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #0a0a0a; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FILM}" data-width="1080" data-height="1920">
      <!-- Scenes, cut to the narration (SPEC.md). -->
{hosts}

      <!-- Voiceover: VoiceBox, trained voice "sparsh" (myvoice), no subtitles/polish; levelled to -14 LUFS (scripts/prep_audio.py). -->
{vo}

      <!-- Music bed: "Ethernight Club", Kevin MacLeod (incompetech.com), CC BY 4.0; envelope baked in. -->
      <audio id="music" class="clip" src="assets/music/bed.wav" data-start="0" data-duration="{FILM}" data-track-index="11" data-volume="1" data-audio-group="music"></audio>

      <!-- SFX:BEGIN (generated by scripts/build_sfx.py from scripts/sfx_cues.json) -->
      <!-- SFX:END -->
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
"""
(P / "index.html").write_text(idx)
print(S)
