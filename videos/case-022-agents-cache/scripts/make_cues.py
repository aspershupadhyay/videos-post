"""Write scripts/sfx_cues.json from the voice timings (so a re-voiced line moves its SFX too), then run build_sfx.py.
Each cue: [film time the picture lands, sfx file, volume, label]. Takes rotate (scratch-a/b/c, tick-a/b, stamp-a/b/c).
Cues past the film's end (the --demo cut) are dropped."""
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
    return [s for ww, s, e in L[vid]["words"] if re.sub(r"[^\w]", "", ww).lower() == word][n - 1]


sting = cut("vo-10") + 0.05
N, BITS = 8, [1, 0, 1, 1, 0, 1, 0, 0]
t_bit, t_msg = w("vo-04c", "bit"), w("vo-04c", "message")
step = (t_msg - t_bit - 0.1) / (N - 2)
cues = [
    # s1 hook
    [0.32, "whoosh", 0.16, "the cover lifts off"],
    [w("vo-01", "sealed"), "click-soft", 0.3, "box A locks"],
    [w("vo-01", "sealed") + 0.1, "select", 0.2, "box B locks"],
    [w("vo-01", "sealed") + 0.7, "impact-bass-2", 0.25, "the wall slams down"],
    [w("vo-01", "still"), "pop", 0.2, "the red dot appears"],
    [w("vo-01", "secret") - 0.35, "whoosh-short", 0.14, "the dot hops the wall"],
    [w("vo-01", "secret") + 0.25, "drop", 0.3, "the dot lands in B"],
    # s2 headlines -> report
    [cut("vo-02") + 0.05, "plate", 0.18, "headline 1"],
    [w("vo-02", "breakout") - 0.05, "thud-wood", 0.18, "headline 2"],
    [w("vo-02", "read") - 0.2, "whoosh", 0.14, "headlines fly off"],
    [w("vo-02", "read") + 0.15, "thud-wood", 0.2, "the report lands"],
    [w("vo-02", "scary"), "scratch-b", 0.35, "the title is redacted"],
    # s3 chip
    [cut("vo-03"), "whoosh-short", 0.12, "the boxes shrink up"],
    [w("vo-03", "both") + 0.1, "impact-bass-1", 0.2, "the chip rises"],
    [w("vo-03", "share"), "scratch-a", 0.3, "wires draw"],
    # s4 explainer
    [cut("vo-03b"), "whoosh", 0.14, "into the CPU"],
    [w("vo-03b", "cache") - 0.1, "typing", 0.12, "the shelf fills"],
    [w("vo-03b", "shelf"), "scratch-c", 0.25, "the plank draws"],
    [w("vo-03b", "memory"), "thud-wood", 0.15, "memory slides in"],
    [w("vo-03c", "reads"), "key-press", 0.35, "fast read"],
    [w("vo-03c", "off") + 0.3, "drop", 0.25, "block drops to memory"],
    [w("vo-03c", "reads", 2), "riser", 0.12, "slow read climbs"],
    [w("vo-04", "kicks") + 0.4, "drop", 0.28, "A kicks a block off"],
    [w("vo-04", "1"), "pop", 0.25, "bit 1"],
    [w("vo-04", "leaves"), "whoosh-short", 0.1, "A moves on"],
    [w("vo-04", "0"), "tick-a", 0.3, "bit 0"],
    [w("vo-04b", "times") + 0.05, "riser", 0.12, "B: slow read"],
    [w("vo-04b", "slow") + 0.3, "stamp-a", 0.2, "slow = 1"],
    [w("vo-04b", "fast") + 0.15, "key-press", 0.35, "fast = 0"],
] + [[t_bit + (i - 2) * step + step * 0.5, ("tick-a" if i % 2 else "tick-b"), 0.25, f"bit {i}"] for i in range(2, N)] + [
    [t_msg, "pop", 0.25, "message received"],
    # s5 twist (the music drops out)
    [cut("vo-05"), "thud-wood", 0.2, "the coverage card lands"],
    [w("vo-05", "told"), "scratch-c", 0.4, "pen under 'asked to exchange'"],
    [w("vo-05", "test") + 0.1, "scratch-a", 0.35, "pen under 'test.'"],
    # s6 the real breakout
    [cut("vo-06"), "impact-bass-1", 0.22, "the report returns"],
    [w("vo-06", "nobody"), "whoosh-short", 0.2, "the redaction tears off"],
    [w("vo-06", "september"), "scratch-b", 0.35, "pen under Sep 20"],
    [w("vo-06", "blocked") - 0.15, "whoosh-short", 0.14, "the proxy block slides in"],
    [w("vo-06", "live"), "scratch-c", 0.4, "ring CACHE_MISS"],
    [w("vo-06", "questions") - 0.5, "thud-wood", 0.2, "the model's reasoning lands"],
    [w("vo-06", "dns") - 0.2, "scratch-a", 0.45, "pen under its reasoning"],
    # s7 France
    [cut("vo-07"), "whoosh-short", 0.14, "the DNS query card"],
    [w("vo-07", "whats"), "typing", 0.12, "underline the query"],
    [w("vo-07", "capital"), "whoosh-short", 0.14, "the answer comes back"],
    [w("vo-07", "france") + 0.1, "scratch-b", 0.4, "ring Paris"],
    # s8 the clock
    [cut("vo-08"), "thud-wood", 0.2, "timeline lands"],
    [w("vo-08", "alarm"), "scratch-c", 0.35, "ring the alert"],
    [w("vo-08", "12"), "punch", 0.25, "12 min"],
    [w("vo-08", "auto") - 0.2, "whoosh-short", 0.12, "not-stopped line"],
    [w("vo-08", "two") - 0.1, "impact-bass-2", 0.25, "2.5 hours"],
    [w("vo-08", "two") + 0.5, "scratch-a", 0.35, "pen under hours"],
    # s9 the take
    [cut("vo-09"), "click-soft", 0.25, "the switch"],
    [w("vo-09", "kill"), "plate", 0.25, "flip... stuck"],
    [w("vo-09", "kill") + 0.5, "stamp-b", 0.2, "it won't go off"],
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
