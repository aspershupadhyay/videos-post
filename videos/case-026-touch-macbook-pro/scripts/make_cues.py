"""Write scripts/sfx_cues.json from the voice timings (so a re-voiced line moves its SFX too), then run build_sfx.py.
Each cue: [film time the picture lands, sfx file, volume, label]. Takes rotate (scratch-a/b/c, tick-a/b, whoosh kinds).
Only visible actions get a sound (PLAYBOOK.md §4)."""
import json
import re
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
T = json.loads((P / "assets/vo/timing.json").read_text())
L = {l["id"]: l for l in T["lines"]}
SH = json.loads((P / "assets/clips/shots.json").read_text())
cut = lambda vid: round(L[vid]["start"] - 0.2, 3)


def w(vid, word, n=1):
    alts = word.split("|")
    return [s for ww, s, e in L[vid]["words"] if re.sub(r"[^\w]", "", ww).lower() in alts][n - 1]


t_rev = w("vo-09", "you") - 0.08
c11 = cut("vo-11")
seg = (w("vo-11", "only") - 0.1 - c11) / 4
lid = cut("vo-12") + (109.1 - SH["close"]["in"]) / SH["close"]["speed"]     # the lid shuts (measured in Apple's film)
sting = cut("vo-13") + 0.05
cues = [
    # s1 the cover's photo grows into the film; the quote
    [0.36, "whoosh-cinematic", 0.16, "the photo becomes the world"],
    [0.86, "click-soft", 0.2, "the quote"],
    # s2 2010, the pen, the shot falls off
    [w("vo-02", "twenty") - 0.1, "punch", 0.22, "2010 lands"],
    [w("vo-02", "ten") + 0.05, "scratch-a", 0.38, "pen under 2010"],
    [w("vo-02", "fall"), "whoosh", 0.18, "the shot falls off"],
    [w("vo-02", "fall") + 0.55, "impact-bass-1", 0.18, "the lid's logo underneath"],
    # s3 the strike
    [w("vo-03", "anyway") + 0.05, "scratch-c", 0.42, "pen strikes doesn't"],
    # s4-s6 the touch montage
    [cut("vo-04"), "whoosh-short", 0.14, "finder"],
    [w("vo-04", "built"), "select", 0.2, "label: in the panel"],
    [cut("vo-04") + 1.34, "tick-a", 0.2, "cut to the car"],
    [cut("vo-05"), "whoosh-short", 0.14, "spin shot"],
    [w("vo-05", "spin"), "pop", 0.25, "Spin. on the glass"],
    [cut("vo-06"), "tick-b", 0.22, "piano"],
    # s7 OLED
    [cut("vo-07"), "whoosh-short", 0.14, "macro"],
    [cut("vo-07") + 1.26, "tick-a", 0.2, "the art"],
    [w("vo-07", "two"), "impact-bass-2", 0.2, "2,000"],
    # s8 re-hook
    [w("vo-08", "what") - 0.05, "punch", 0.2, "The arm?"],
    [w("vo-08", "arm") + 0.1, "scratch-b", 0.38, "pen under arm"],
    # s9 the answer
    [t_rev, "whoosh", 0.16, "the arm goes back down"],
    [t_rev + 1.4, "whoosh-short", 0.14, "hands on the keyboard"],
    [w("vo-09", "trackpad"), "select", 0.2, "Trackpad"],
    [w("vo-09", "stays") + 0.1, "key-press", 0.3, "tick"],
    [w("vo-09", "keyboard"), "select", 0.2, "Keyboard"],
    [w("vo-09", "stays", 2) + 0.1, "key-press", 0.3, "tick"],
    # s10 the hinge
    [cut("vo-10"), "whoosh-short", 0.14, "hinge shot"],
    [w("vo-10", "hinge"), "select", 0.2, "label: new hinge"],
    [w("vo-10", "tap"), "click-soft", 0.3, "tap"],
    # s11 the whole ad races past, the asterisk, the last frame
    *[[c11 + i * seg, ["tick-a", "tick-b"][i % 2], 0.22, f"ad cut {i + 1}"] for i in range(4)],
    [w("vo-11", "only") - 0.1, "whoosh-short", 0.14, "3 pounds light"],
    [w("vo-11", "print") + 0.05, "pop", 0.25, "the red asterisk"],
    [w("vo-11", "weight") - 0.1, "plate", 0.2, "the ad's last frame"],
    [w("vo-11", "varies") + 0.1, "scratch-a", 0.42, "pen under Weight varies"],
    # s12 the lid closes
    [cut("vo-12"), "whoosh", 0.14, "the closing shot"],
    [lid, "thud-wood", 0.24, "the lid shuts"],
    [w("vo-12", "optional") + 0.2, "scratch-b", 0.4, "pen under optional"],
    # s13 sting (beats from brand/motion/logo-sting.html)
    [sting + 0.32, "drop", 0.3, "the dot lands on the rule"],
    [sting + 0.85, "thud-wood", 0.22, "c lands"],
    [sting + 0.97, "plate", 0.18, "t lands"],
    [sting + 0.8, "pop", 0.25, "the dot becomes the e"],
    [sting + 1.1, "scratch-c", 0.45, "the pen circles the e"],
    [sting + 1.75, "typing", 0.14, "CATCH · THE · ERROR"],
]
cues.sort(key=lambda c: c[0])
(P / "scripts/sfx_cues.json").write_text(json.dumps({"cues": [[round(c[0], 3), *c[1:]] for c in cues]}, indent=1))
subprocess.run(["python3", str(P / "scripts/build_sfx.py")], check=True)
