"""Write scripts/sfx_cues.json from the voice timings (so a re-voiced line moves its SFX too), then run build_sfx.py.
Each cue: [film time the picture lands, sfx file, volume, label]. Takes rotate (scratch-a/b/c, tick-a/b, stamp-a/b/c).
Only visible actions get a sound (PLAYBOOK.md §4)."""
import json
import re
import subprocess
from pathlib import Path

P = Path(__file__).resolve().parent.parent
FILM = float(re.search(r'data-composition-id="main" data-start="0" data-duration="([\d.]+)"', (P / "index.html").read_text()).group(1))
T = json.loads((P / "assets/vo/timing.json").read_text())
L = {l["id"]: l for l in T["lines"]}
cut = lambda vid: round(L[vid]["start"] - 0.2, 2)


def w(vid, word, n=1):
    alts = word.split("|")
    return [s for ww, s, e in L[vid]["words"] if re.sub(r"[^\w]", "", ww).lower() in alts][n - 1]


sting = cut("vo-10") + 0.05
c09 = cut("vo-09")
seg9 = (w("vo-09", "the") - c09 - 0.05) / 4
cues = [
    # s1 hook: the cover cracks and falls away; the asterisk
    [0.36, "impact-bass-2", 0.22, "the cover cracks"],
    [0.4, "whoosh-cinematic", 0.16, "the halves fall away"],
    [w("vo-01", "ai") + 0.05, "pop", 0.25, "the red asterisk"],
    # s2 loop: shards flash, the last frame, the ring
    [cut("vo-02"), "whoosh-short", 0.14, "shard in"],
    [cut("vo-02") + (w("vo-02", "tiny") - cut("vo-02")) / 2 - 0.1, "click-soft", 0.22, "shard morphs"],
    [w("vo-02", "tiny") - 0.04, "plate", 0.18, "cut to the last frame"],
    [w("vo-02", "gray") + 0.1, "scratch-b", 0.4, "ring the fine print"],
    [cut("vo-03") - 0.42, "riser", 0.12, "zoom into the fine print"],
    # s3 the fine print (music drops out)
    [cut("vo-03") + 0.05, "impact-bass-1", 0.18, "arrive in the fine print"],
    [w("vo-03", "m1") + 0.05, "scratch-a", 0.4, "pen under 'with M1.'"],
    # s4 M1 2020
    [cut("vo-04") + 0.02, "punch", 0.22, "M1 lands"],
    [w("vo-04", "laptop") - 0.35, "whoosh-short", 0.14, "the 2020 photo flies in"],
    [w("vo-04", "laptop") + 0.1, "thud-wood", 0.22, "the photo lands"],
    [w("vo-04", "2020"), "stamp-a", 0.2, "2020"],
    [w("vo-04", "2020") + 0.3, "scratch-c", 0.35, "pen under 2020"],
    # s5 1.3x
    [cut("vo-05") + 0.05, "whoosh", 0.14, "the newsroom card slides up"],
    [w("vo-05", "m5") - 0.1, "click-soft", 0.25, "dim to the M5 line"],
    [w("vo-05", "1"), "select", 0.22, "the digits part"],
    [w("vo-05", "1") + 0.4, "drop", 0.32, "the red dot lands: 1.3"],
    [w("vo-05", "3") + 0.2, "scratch-b", 0.35, "pen under 1.3x"],
    # s6 time to first token
    [cut("vo-06"), "whoosh", 0.14, "the shard slides in"],
    [w("vo-06", "faster") - 0.1, "scratch-a", 0.35, "pen under 'time to first token'"],
    [w("vo-06", "wait"), "tick-a", 0.2, "the wait starts"],
    [w("vo-06", "answering"), "key-press", 0.35, "the A.I. answers"],
    # s7 the whole answer vs the first token
    [cut("vo-07") + 0.1, "typing", 0.12, "tokens stream in"],
    [w("vo-07", "just"), "pop", 0.25, "the first token goes red"],
    [w("vo-07", "just") + 0.25, "scratch-c", 0.4, "ring the first token"],
    # s8 the take
    [cut("vo-08"), "whoosh-short", 0.14, "M1 shard slides in"],
    [w("vo-08", "real") - 0.1, "thud-wood", 0.2, "Real upgrade."],
    [w("vo-08", "bought") - 0.3, "whoosh-short", 0.14, "M5 shard slides in"],
    [w("vo-08", "keep") - 0.1, "thud-wood", 0.2, "Keep your money."],
    [w("vo-08", "money") + 0.25, "scratch-b", 0.35, "pen under money"],
    # s9 the line: the montage, the last frame, the ring
    [c09, "whoosh-short", 0.14, "montage in"],
] + [[c09 + k * seg9, ("tick-a" if k % 2 else "tick-b"), 0.22, f"shard cut {k}"] for k in range(1, 4)] + [
    [w("vo-09", "the") - 0.04, "impact-bass-1", 0.2, "the last frame again"],
    [w("vo-09", "last"), "scratch-c", 0.4, "ring the fine print"],
    # s10 sting
    [sting + 0.32, "drop", 0.3, "the dot lands on the rule"],
    [sting + 0.52, "thud-wood", 0.22, "c lands"],
    [sting + 0.64, "plate", 0.18, "t lands"],
    [sting + 0.85, "pop", 0.25, "the dot becomes the e"],
    [sting + 1.3, "scratch-c", 0.45, "the pen circles the e"],
    [sting + 1.75, "typing", 0.14, "CATCH · THE · ERROR"],
]
cues = sorted([c for c in cues if c[0] < FILM - 0.1], key=lambda c: c[0])
(P / "scripts/sfx_cues.json").write_text(json.dumps({"cues": [[round(c[0], 3)] + c[1:] for c in cues]}, indent=1, ensure_ascii=False))
subprocess.run(["python3", str(P / "scripts/build_sfx.py")], check=True)
